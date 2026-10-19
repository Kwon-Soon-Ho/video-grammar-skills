"""R4-2 계약 검사. 사실판정/미디어읽기/인간승인/자동영상분석을 하지 않는다."""
from pathlib import Path
from fractions import Fraction
import json, hashlib, math, importlib.util
from jsonschema import Draft202012Validator,FormatChecker
BASE=Path(__file__).resolve().parents[1]
def q(v): return None if v is None else Fraction(v['num'],v['den'])
def context_hash(data,claim):
    # 미검토 변경을 놓치지 않도록 패키지 자료/대상/근거/시간 전체를 고정한다.
    payload={k:data[k] for k in ['contract_version','record_purpose','time_contract','materials','targets','evidence']}
    payload['claim']={k:v for k,v in claim.items() if k!='review_ref'}
    payload['validator_dependencies']={p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in ['04_기록규격/근거주장_스키마.json','07_실행도구/근거주장_규격검사.py','07_실행도구/시간프레임_규격검사.py']}
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()
def validate(data,schema=None):
    if schema is None:schema=json.loads((BASE/'04_기록규격/근거주장_스키마.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errors=[];unresolved=[];queue=[];states=[]
    def diagnostic(text):return str(text).encode('utf-8',errors='backslashreplace').decode('utf-8')
    def err(label,message):errors.append(diagnostic(label)+': '+diagnostic(message))
    def pending(label,message):unresolved.append(label+': '+message)
    def walk(v,path='record'):
        if isinstance(v,str):
            try:v.encode('utf-8')
            except UnicodeEncodeError:err(path,'UTF-8로 표현 불가능한 surrogate 문자열 금지')
        elif isinstance(v,float) and not math.isfinite(v):err(path,'NaN/Infinity 금지')
        elif isinstance(v,dict):
            for k,x in v.items():
                if not isinstance(k,str):err(path,'JSON 객체 key는 문자열');continue
                try:k.encode('utf-8')
                except UnicodeEncodeError:err(path,'UTF-8로 표현 불가능한 surrogate key 금지')
                if k in ['start','end','num','den','stream_index','frame_count','source_frame_ordinal'] and isinstance(x,(int,float)) and type(x) is not int:err(path+'.'+k,'정수 타입 필요')
                walk(x,path+'.'+diagnostic(k))
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,path+f'[{i}]')
    walk(data)
    for e in ([] if errors else Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data)):
        msg=e.message if len(e.message)<400 else e.message[:180]+' … '+e.message[-180:]
        err(str(list(e.path)),msg)
    def output():return {'valid':not errors,'errors':errors,'unresolved':list(dict.fromkeys(unresolved)),'human_review_queue':queue,'claim_states':states,'fact_verified':False,'human_identity_verified':False,'company_approved':False,'operational_release':False}
    if errors:return output()
    spec=importlib.util.spec_from_file_location('r4_time_dependency',BASE/'07_실행도구/시간프레임_규격검사.py');tm=importlib.util.module_from_spec(spec);spec.loader.exec_module(tm)
    tr=data['time_contract']; time_result=tm.validate(tr,schema['properties']['time_contract'])
    errors.extend('time: '+e for e in time_result['errors']);unresolved.extend('time: '+e for e in time_result['unresolved'])
    if errors:return output()
    mats={x['id']:x for x in data['materials']};targets={x['id']:x for x in data['targets']};evs={x['id']:x for x in data['evidence']};reviews={x['id']:x for x in data['review_records']}
    periods={x['id']:x for x in tr['periods']};frames={x['id']:x for x in tr['frames']};tls={x['id']:x for x in tr['timelines']}
    allids=[x['id'] for k in ['materials','targets','evidence','claims','review_records'] for x in data[k]]
    if len(allids)!=len(set(allids)):err('record','자료/대상/근거/주장/검수 ID 중복')
    def resolve(ref,table,label,hashed=False):
        item=table.get(ref['id'])
        if item is None:err(label,'없는 참조 '+ref['id']);return None
        if item['version']!=ref['version'] or (hashed and item['sha256']!=ref['sha256']):err(label,'참조 버전/hash 불일치 '+ref['id']);return None
        return item
    root=mats.get(tr['asset']['id'])
    if root is None or root['kind']!='video' or any(root[k]!=tr['asset'][k] for k in ['id','version','sha256']):err('record','R4-1 원본 영상 identity 불일치')
    if root is not None and root['source_type']!=tr['source_type']:err('record','시간계약/영상 source_type 불일치')
    if data['record_purpose']=='spec_test':
        if tr['source_type']!='synthetic_example' or any(m['source_type']!='synthetic_example' for m in mats.values()):err('record','spec_test는 모든 자료를 synthetic_example로 격리')
    elif tr['source_type']=='synthetic_example' or any(m['source_type']=='synthetic_example' for m in mats.values()):err('record','실제 draft에 합성 자료 승격 금지')
    derivation_pending=set()
    for m in mats.values():
        if m['availability']!='present':pending(m['id'],'자료 접근/내용 확인 필요')
        if m['parent_ref'] is not None:resolve(m['parent_ref'],mats,m['id'],True)
        if m['kind'] in ['frame','clip','transcript','ocr','reconstruction'] and m['parent_ref'] is None:err(m['id'],'파생 자료의 원본 참조 필요')
        if m['kind'] in ['scenario','transcript','ocr','project_document','creator_confirmation'] and m['text'] is None:pending(m['id'],'텍스트 표현 미확보')
        if m['kind']=='frame':
            if m['frame_ref'] not in frames:err(m['id'],'frame 자료의 source frame_ref 필요')
            if m['period_ref'] is not None:err(m['id'],'frame 자료 period_ref는 null')
        elif m['frame_ref'] is not None:err(m['id'],'frame 이외 자료에 frame_ref 금지')
        if m['kind']=='clip' and (m['period_ref'] not in periods or periods[m['period_ref']]['kind']!='range'):err(m['id'],'clip 자료의 원본 range 참조 필요')
        if m['period_ref'] is not None and m['period_ref'] not in periods:err(m['id'],'자료 period 참조 없음')
        seen={m['id']};node=m
        while node['parent_ref'] is not None:
            node=mats.get(node['parent_ref']['id'])
            if node is None:break
            if node['id'] in seen:err(m['id'],'자료 파생 순환');break
            seen.add(node['id'])
        if m['authority'] is not None:
            for ref in m['authority']['target_refs']:resolve(ref,targets,m['id'])
    def ancestor(a,b):
        # a가 b의 자기 자신/상위 대상인가? 참조 버전은 별도로 확인한다.
        seen=set();n=targets.get(b)
        while n is not None and n['id'] not in seen:
            if n['id']==a:return True
            seen.add(n['id']);n=targets.get(n['parent_ref']['id']) if n['parent_ref'] else None
        return False
    def period(ref,label):
        if ref is None:return None
        if ref not in periods:err(label,'없는 시간 구간 '+ref);return None
        return periods[ref]
    def contains(outer,inner):
        if outer is None or inner is None or outer['kind']=='unknown' or inner['kind']=='unknown':return None
        if outer['timeline_ref']!=inner['timeline_ref']:return False
        a,b=q(outer['start']),q(outer['end']);c,d=q(inner['start']),q(inner['end'])
        if outer['kind']=='instant':return inner['kind']=='instant' and a==c
        return a<=c<b and (d is None or d<=b)
    for t in targets.values():
        resolve(t['asset_ref'],mats,t['id'],True)
        if root is not None and t['asset_ref']['id']!=root['id']:err(t['id'],'분석 대상은 현재 원본 영상에 연결')
        if t['parent_ref']:
            parent=resolve(t['parent_ref'],targets,t['id'])
            if parent and contains(period(parent['period_ref'],parent['id']),period(t['period_ref'],t['id'])) is False:err(t['id'],'대상 시간이 부모 범위 밖')
            if t['unit']=='asset':err(t['id'],'asset 대상은 부모 없는 영상 전체')
            if parent and t['unit']=='segment' and parent['unit']!='asset':err(t['id'],'segment 부모는 asset')
            if parent and t['unit']=='screen_state' and parent['unit']!='segment':err(t['id'],'screen_state 부모는 segment')
            if parent and t['unit']=='beat' and parent['unit'] not in ['segment','screen_state']:err(t['id'],'beat 부모는 segment/screen_state')
        elif t['unit']!='asset':err(t['id'],'비영상 대상의 부모 참조 필요')
        period(t['period_ref'],t['id'])
        seen={t['id']};n=t
        while n['parent_ref']:
            n=targets.get(n['parent_ref']['id'])
            if n is None:break
            if n['id'] in seen:err(t['id'],'대상 부모 순환');break
            seen.add(n['id'])
    def has_video_origin(m):
        seen=set()
        while m and m['id'] not in seen:
            if root and m['id']==root['id']:return True
            if m['kind'] not in ['frame','clip']:return False
            seen.add(m['id']);m=mats.get(m['parent_ref']['id']) if m['parent_ref'] else None
        return False
    for m in mats.values():
        parent=mats.get(m['parent_ref']['id']) if m['parent_ref'] else None
        if not parent:continue
        if m['kind']=='frame':
            if parent['kind'] not in ['video','clip','frame']:err(m['id'],'원본 frame 파생 부모 종류 불일치')
            if parent['kind']=='frame' and m['frame_ref']!=parent['frame_ref']:
                f,g=frames.get(m['frame_ref']),frames.get(parent['frame_ref'])
                if f and g:
                    if f['actual'] is not None and g['actual'] is not None and (f['timeline_ref']!=g['timeline_ref'] or q(f['actual'])!=q(g['actual'])):err(m['id'],'frame 사본은 같은 원본 frame identity 유지')
                    elif all(v['mapping_state']=='mapped' and v['pts_kind']=='original_pts' and v['source_frame_ordinal'] is not None and v['source_pts'] is not None and v['time_base'] is not None for v in [f,g]):
                        if (f['timeline_ref'],f['source_frame_ordinal'],f['source_pts'],q(f['time_base']))!=(g['timeline_ref'],g['source_frame_ordinal'],g['source_pts'],q(g['time_base'])):err(m['id'],'frame 사본은 같은 원본 frame identity 유지')
                    else:derivation_pending.add(m['id']);pending(m['id'],'파생 프레임 별칭 identity 미확인')
            if parent['kind']=='clip':
                f=frames.get(m['frame_ref'])
                if f and f['actual'] is not None and contains(periods.get(parent['period_ref']),{'kind':'instant','start':f['actual'],'end':None,'timeline_ref':f['timeline_ref']}) is False:err(m['id'],'파생 frame이 부모 clip 시간 밖')
        if m['kind']=='clip':
            if parent['kind'] not in ['video','clip']:err(m['id'],'원본 clip 파생 부모 종류 불일치')
            if parent['kind']=='clip' and contains(periods.get(parent['period_ref']),periods.get(m['period_ref'])) is False:err(m['id'],'파생 clip이 부모 clip 범위 밖')
    for e in evs.values():
        m=resolve(e['material_ref'],mats,e['id'],True);target=resolve(e['target_ref'],targets,e['id']);s=e['selector']
        if s['kind']=='frame':
            if not m or m['kind']!='frame' or not has_video_origin(m):err(e['id'],'frame 근거의 원본 파생 연결 필요')
            f=frames.get(s['frame_ref'])
            if f is None:err(e['id'],'없는 원본 frame_ref')
            if m and m['frame_ref']!=s['frame_ref']:err(e['id'],'자료와 selector frame_ref 불일치')
            if s['period_ref'] is not None or any(s[k] is not None for k in ['exact','start','end']):err(e['id'],'frame selector에 다른 선택값 혼용 금지')
            if f and target:
                p=period(target['period_ref'],target['id'])
                instant={'kind':'instant','start':f['actual'],'end':None,'timeline_ref':f['timeline_ref']}
                if f['actual'] is None:pending(e['id'],'프레임 시각 미확인')
                elif contains(p,instant) is False:err(e['id'],'프레임이 대상 시간 밖')
        elif s['kind']=='clip':
            if not m or m['kind'] not in ['video','clip'] or not has_video_origin(m):err(e['id'],'clip 원본 파생 연결 필요')
            p=period(s['period_ref'],e['id'])
            if p is None or p['kind']!='range':err(e['id'],'clip selector에는 range 필요')
            if p and m and m['kind']=='clip' and contains(periods.get(m['period_ref']),p) is False:err(e['id'],'선택 clip이 파생 자료 범위 밖')
            if any(s[k] is not None for k in ['frame_ref','exact','start','end']):err(e['id'],'clip selector 혼용 금지')
            if p and target and contains(period(target['period_ref'],target['id']),p) is False:err(e['id'],'clip이 대상 시간 밖')
        elif s['kind']=='text':
            if not m or m['kind'] not in ['scenario','transcript','ocr','project_document','creator_confirmation','design_profile','example_description']:err(e['id'],'text selector 자료종류 불일치')
            if s['exact'] is None or s['start'] is None or s['end'] is None or s['start']>=s['end']:err(e['id'],'텍스트 정확 인용/시작<끝 필요')
            elif m and m['text'] is not None:
                if s['end']>len(m['text']) or m['text'][s['start']:s['end']]!=s['exact']:err(e['id'],'텍스트 위치/인용 불일치')
            else:pending(e['id'],'원문 없음 — 인용 검사 미해결')
            if s['frame_ref'] is not None:err(e['id'],'text selector frame_ref 혼용 금지')
            tp=period(s['period_ref'],e['id']);mp=period(m['period_ref'],m['id']) if m else None
            if tp and mp and contains(mp,tp) is False:err(e['id'],'text 선택 시간이 자료 범위 밖')
            if tp and target and contains(period(target['period_ref'],target['id']),tp) is False:err(e['id'],'text 선택 시간이 대상 범위 밖')
        else:
            if any(s[k] is not None for k in ['frame_ref','period_ref','exact','start','end']):err(e['id'],'document/none selector 혼용 금지')
            pending(e['id'],'문서 전체/미선택 근거의 해당 부분 지정 필요')
    for t in tls.values():
        for ref in t['duration_evidence_refs']+t['origin']['evidence_refs']:
            if ref not in evs:err(t['id'],'시간 메타 근거 ID 없음 '+ref)
            else:
                e=evs[ref];m=mats.get(e['material_ref']['id']);target=targets.get(e['target_ref']['id'])
                if not target or target['unit']!='asset' or not root or target['asset_ref']['id']!=root['id'] or not m or m['kind'] not in ['project_document','creator_confirmation'] or e['selector']['kind']!='text':err(t['id'],'시간 메타 근거는 해당 영상의 확인 문서 부분이어야 함')
    for c in data['claims']:
        label=c['id'];claim_errors=len(errors);risks=[]
        if errors:risks.append('공통 자료/참조 구조 오류 — 사람 검수 전에 수정 필요')
        if time_result['unresolved']:risks.append('시간 검사 미해결 — 사람이 시간 근거 확인 필요')
        target=resolve(c['scope']['target_ref'],targets,label);cp=period(c['scope']['period_ref'],label);extent=c['scope']['extent'];mode=c['support_mode'];aspect=c['aspect']
        if target and contains(period(target['period_ref'],target['id']),cp) is False:err(label,'주장 시간이 대상 범위 밖')
        if extent=='instant' and (cp is None or cp['kind']!='instant'):err(label,'instant 주장 범위 필요')
        if extent in ['sampled','continuous','whole_asset'] and (cp is None or cp['kind']!='range'):err(label,'시간 확장 주장에 range 필요')
        if extent=='whole_asset' and cp and target:
            dur=q(tls[cp['timeline_ref']]['duration'])
            if target['unit']!='asset' or q(cp['start'])!=0 or q(cp['end'])!=dur:err(label,'whole_asset은 영상 전체 시간/대상 필요')
        if mode in ['rendered_observation','numerical_estimate'] and (cp is None or cp['kind']=='unknown'):risks.append('관측 시간 미확인')
        if mode in ['rendered_observation','numerical_estimate']:
            for t in tls.values():
                for er in t['duration_evidence_refs']+t['origin']['evidence_refs']:
                    em=evs.get(er);material=mats.get(em['material_ref']['id']) if em else None
                    if material is None or material['availability']!='present' or material['text'] is None:risks.append('시간 메타 근거 내용/접근 미확인')
        if target and target['period_ref'] is None:risks.append('대상 시간 미확인')
        if mode=='rendered_observation' and aspect=='temporal_change' and extent not in ['sampled','continuous','whole_asset']:err(label,'시간 변화 주장은 range 범위가 필요')
        allowed={'visual_presence':['rendered_observation'],'temporal_change':['rendered_observation'],'acceleration':['numerical_estimate'],'numeric_value':['numerical_estimate'],'scenario_content':['scenario_supported'],'intent':['intent_confirmed'],'implementation':['hypothesis'],'generalization':['hypothesis'],'negative_absence':['rendered_observation']}
        if mode not in ['hypothesis','not_observed_example'] and mode not in allowed[aspect]:err(label,'주장 aspect/support_mode 불일치')
        if mode=='not_observed_example' and data['record_purpose']!='spec_test':err(label,'미관측 설명 예시는 실제 draft에 혼합 금지')
        if aspect in ['implementation','generalization']:risks.append('구현/회사 일반화는 해당 원본과 후속단계 검수 필요')
        linked=[]
        linkids=[x['ref']['id'] for x in c['evidence_links']]
        if len(linkids)!=len(set(linkids)):err(label,'동일 근거를 중복 role로 등록 금지')
        for link in c['evidence_links']:
            e=resolve(link['ref'],evs,label)
            if e is None:continue
            linked.append((link['role'],e))
            if link['role']!='context' and target and not ancestor(e['target_ref']['id'],target['id']):err(label,'근거와 주장 대상 불일치')
            if link['role']=='oppose' and e['selector']['kind']=='frame':
                f=frames.get(e['selector']['frame_ref'])
                if f and f['actual'] is not None and contains(cp,{'kind':'instant','start':f['actual'],'end':None,'timeline_ref':f['timeline_ref']}) is False:err(label,'반대 프레임이 주장 시간 밖 — 문맥으로 기록')
            if link['role']!='context':
                ep=period(e['selector']['period_ref'],label) if e['selector']['period_ref'] else None
                material=mats.get(e['material_ref']['id'])
                mp=period(material['period_ref'],label) if material and material['period_ref'] else None
                for timed in [ep,mp]:
                    if timed and cp and contains(timed,cp) is False and contains(cp,timed) is False:
                        if timed['kind']=='unknown' or cp['kind']=='unknown':risks.append('근거 시간 범위 미확인')
                        elif timed['timeline_ref']!=cp['timeline_ref']:err(label,'지지/반대 근거 시간축 불일치')
                        elif timed['kind']=='instant':err(label,'지지/반대 순간 근거가 주장 시간 밖')
                        elif cp['kind']=='instant' or q(timed['end'])<=q(cp['start']) or q(cp['end'])<=q(timed['start']):err(label,'지지/반대 timed 근거가 주장 시간과 겹치지 않음')
        support=[e for role,e in linked if role=='support'];oppose=[e for role,e in linked if role=='oppose']
        if mode not in ['hypothesis','not_observed_example'] and not support:err(label,'확인 성격 주장에 support 근거 필요')
        frame_times=[];clips=[]
        for e in support:
            m=mats.get(e['material_ref']['id']);s=e['selector']
            if m and m['availability']!='present':risks.append('근거 자료 접근 미확인')
            if m and s['kind']=='text' and m['text'] is None:risks.append('지지 원문 내용 미확인')
            seen=set();source=m
            while source and source['id'] not in seen:
                seen.add(source['id'])
                if source['availability']!='present':risks.append('지지 근거의 원본/파생 자료 접근 미확인')
                if source['id'] in derivation_pending:risks.append('파생 프레임 별칭 identity 미확인')
                source=mats.get(source['parent_ref']['id']) if source['parent_ref'] else None
            if s['kind']=='frame':
                f=frames.get(s['frame_ref'])
                if f:
                    if f['mapping_state']!='mapped' or f['pts_kind']!='original_pts' or f['actual'] is None or f['role']!='within_period':risks.append('원본 프레임의 시간/내부소속 확인 필요')
                    else:
                        instant={'kind':'instant','start':f['actual'],'end':None,'timeline_ref':f['timeline_ref']}
                        if contains(cp,instant) is False:err(label,'support 프레임이 주장 시간 밖')
                        frame_times.append((f['timeline_ref'],q(f['actual'])))
            elif s['kind']=='clip':
                p=period(s['period_ref'],label)
                if p:clips.append(p)
                if p and cp and p['kind']=='range' and cp['kind'] in ['range','instant'] and contains(p,cp) is False:
                    if p['timeline_ref']!=cp['timeline_ref'] or q(p['end'])<=q(cp['start']) or (cp['end'] is not None and q(cp['end'])<=q(p['start'])):err(label,'support clip이 주장 시간과 겹치지 않음')
            if mode=='scenario_supported' and (not m or m['kind'] not in ['scenario','transcript'] or s['kind']!='text'):err(label,'시나리오 주장은 원문/전사 text 근거 필요')
            if mode=='intent_confirmed':
                authority=m['authority'] if m else None
                if not m or m['kind'] not in ['creator_confirmation','project_document'] or s['kind']!='text' or authority is None or authority['role'] not in ['creator','planner']:err(label,'의도는 제작자/기획 책임자 확인 부분 필요')
                elif target and not any(r['id']==target['id'] and r['version']==target['version'] for r in authority['target_refs']):err(label,'의도 확인 대상 범위 불일치')
                risks.append('실제 확인 주체/문장의 의도 내용 검수')
            if mode in ['rendered_observation','numerical_estimate'] and s['kind'] not in ['frame','clip']:err(label,'렌더/실측 주장은 원본 frame/clip 근거 필요')
        covering=any(contains(p,cp) is True for p in clips)
        if mode=='rendered_observation':
            if aspect=='temporal_change' and not covering and len(set(frame_times))<2:err(label,'변화 주장에는 서로 다른 시각2개 또는 범위 clip 필요')
            if extent in ['continuous','whole_asset'] and not covering:err(label,'연속/전체 주장에는 전체 범위 clip 필요')
            if aspect=='negative_absence' and extent!='instant' and not covering:err(label,'구간 내 부재는 단일 프레임으로 확인 불가')
            risks.append('화면 내용/동일 대상/가림/표본 충분성 사람 검수')
        measurement=c['measurement']
        if mode=='numerical_estimate':
            if measurement is None:err(label,'수치 추정에 measurement 필요')
            else:
                times=[]
                if measurement['quantity']=='other':risks.append('사용자 정의 측정량/단위 계약 미확인 — 사람 검수 및 계약 확장 필요')
                if measurement['uncertainty_kind']=='unknown':
                    if measurement['uncertainty'] is not None:err(label,'미상 불확실성은 null')
                    risks.append('측정 불확실성 미확인')
                elif measurement['uncertainty'] is None:err(label,'알려진 불확실성 종류에는 값 필요')
                units={'position_x':['px','normalized'],'position_y':['px','normalized'],'width':['px','normalized'],'height':['px','normalized'],'average_speed':['px/s','normalized/s'],'average_acceleration':['px/s^2','normalized/s^2'],'duration':['s'],'count':['count'],'opacity_estimate':['ratio','percent']}
                if measurement['quantity'] in units and measurement['unit'] not in units[measurement['quantity']]:err(label,'측정량/결과 단위 차원 불일치')
                if measurement['quantity'] in ['width','height','average_speed','duration','count'] and measurement['value']<0:err(label,'이 측정량은 음수 결과 불가')
                if measurement['quantity']=='count' and (type(measurement['value']) is not int):err(label,'정적 개수는 정수 타입 필요')
                if measurement['quantity'] in ['average_speed','average_acceleration'] and measurement['sample_unit'] not in ['px','normalized']:err(label,'공간 속도 표본 단위는 위치 단위')
                if measurement['quantity']=='opacity_estimate':
                    maximum=1 if measurement['unit']=='ratio' else 100
                    if not 0<=measurement['value']<=maximum:err(label,'opacity 추정 값/단위 범위 밖')
                for sample in measurement['samples']:
                    e=resolve(sample['evidence_ref'],evs,label);f=frames.get(sample['frame_ref']);resolve(sample['target_ref'],targets,label)
                    if e is None or f is None:err(label,'측정 표본 근거/프레임 없음');continue
                    if sample['evidence_ref']['id'] not in [v['id'] for v in support] or e['selector']['kind']!='frame' or e['selector']['frame_ref']!=sample['frame_ref']:err(label,'표본은 해당 support frame 근거에 연결')
                    if target and sample['target_ref']!=c['scope']['target_ref']:err(label,'측정 표본 대상 불일치')
                    if f['mapping_state']!='mapped' or f['pts_kind']!='original_pts' or f['actual'] is None:risks.append('측정 표본 원본 시간 미확인')
                    else:times.append((f['timeline_ref'],q(f['actual'])))
                    if measurement['quantity'] in ['position_x','position_y','average_speed','average_acceleration','width','height'] and sample['coordinate_space_ref'] is None:risks.append('공간 측정 좌표 계약 R4-3 확인 필요')
                    elif sample['coordinate_space_ref'] is not None:risks.append('좌표 참조 실재/변환 검증 R4-3 필요')
                minimum=3 if aspect=='acceleration' or measurement['quantity']=='average_acceleration' else 2 if measurement['quantity'] in ['average_speed','duration'] else 1
                if minimum>1 and (cp is None or cp['kind']!='range' or extent not in ['sampled','continuous','whole_asset']):err(label,'시간 측정은 range 주장 범위 필요')
                if len(set(times))<minimum:err(label,'측정에 서로 다른 원본 시각 '+str(minimum)+'개 필요')
                if times and len({t for t,_ in times})!=1:err(label,'측정 표본 시간축 혼용 금지')
                if aspect=='acceleration' and measurement['quantity']!='average_acceleration':err(label,'가속도 주장 측정량 불일치')
                if measurement['quantity']=='opacity_estimate' and not measurement['assumptions']:err(label,'opacity 합성 조건 가정 필요')
                risks.append('측정량/단위/계산법/오차/표본 충분성 사람 검수')
        elif measurement is not None:err(label,'measurement는 numerical_estimate에만 기록')
        if oppose:risks.append('반대 근거의 충돌 판정 필요')
        if mode=='scenario_supported':risks.append('시나리오 원문 의미 검수 — 실제 화면 발생과 구분')
        if extent=='unspecified':risks.append('주장 범위 미지정')
        state='not_reviewed';review=reviews.get(c['review_ref'])
        if c['review_ref'] is not None and review is None:err(label,'없는 사람 검수 기록')
        elif review:
            if data['record_purpose']=='spec_test' and review['kind']!='specimen':err(label,'합성 시험에 실제 사람 검수 선언 금지')
            if data['record_purpose']=='draft_record' and review['kind']!='human':err(label,'실제 기록에 specimen 검수 금지')
            if review['claim_ref']!={'id':c['id'],'version':c['version']}:err(label,'검수 주장 버전 불일치')
            if review['context_sha256']!=context_hash(data,c):state='stale';risks.append('검수 뒤 근거/대상/시간/주장 변경 — 재검수 필요')
            elif data['record_purpose']=='spec_test':
                state='example_only'
            else:
                state='declared_'+review['outcome']
                if review['outcome']=='supported' and risks and any(any(word in r for word in ['미확인','미해결','R4-3','범위 미지정','재검수','구조 오류']) for r in risks):err(label,'미해결 근거/좌표/범위를 supported로 통과 금지')
                if review['outcome']=='supported' and oppose and not review['conflict_resolution']:err(label,'반대 근거 해결 기록 없이는 supported 금지')
                if review['outcome']=='supported' and mode in ['hypothesis','not_observed_example']:err(label,'가설/미관측 예시는 확인된 주장으로 승격 금지')
        needs_review=state in ['not_reviewed','stale','declared_inconclusive','example_only'] or len(errors)>claim_errors
        if needs_review:
            queue.append({'claim_id':c['id'],'claim_version':c['version'],'priority':'high' if mode in ['numerical_estimate','intent_confirmed'] or oppose or aspect in ['implementation','generalization','negative_absence','temporal_change'] else 'normal','reasons':list(dict.fromkeys(risks or ['주장 내용 사람 검수 필요'])),'status':'specimen_only' if data['record_purpose']=='spec_test' else 'awaiting_human','routing':'실제 자료 확보 후 사용자 또는 지정 제작자/디자이너 검수. 이 검사기는 대신 승인하지 않음.'})
        states.append({'claim_id':c['id'],'content_review_state':state,'structure_status':'invalid' if len(errors)>claim_errors else 'draft_structure_pass','human_review_required':needs_review,'verified_fact':False})
    used={c['review_ref'] for c in data['claims'] if c['review_ref']}
    if any(r['id'] not in used for r in data['review_records']):err('record','대상 주장에 연결되지 않은 검수 기록')
    return output()
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);a=p.parse_args()
    result=validate(json.loads(a.record.read_text(encoding='utf-8')))
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['valid'] else 1)
