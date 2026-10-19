"""구형 v0.1 보존 진단용. 현재 DB 통과/분석/승인에 사용하지 않음. 원문은 backup에 보존."""
from pathlib import Path
import argparse, json, hashlib, math
from jsonschema import Draft202012Validator, FormatChecker

BASE=Path(__file__).resolve().parents[1]
def read(rel): return json.loads((BASE/rel).read_text(encoding='utf-8'))
def schema_errors(instance, filename):
    schema=read('04_기록규격/'+('구형최소기록_스키마_v0.1.json' if filename=='최소기록_스키마.json' else filename))
    Draft202012Validator.check_schema(schema)
    return [('/'.join(map(str,e.path))+': '+('수치 추정 규격: ' if 'measurement' in e.path or (e.validator=='required' and 'measurement' in e.message) else '')+e.message) for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(instance)]
def catalogs():
    t=read('01_공통용어/공통용어사전.json')
    s=read('05_출처와검토/출처목록.json')
    p=read('02_원칙과레이아웃/모션과정보전달원칙.json')
    q=read('02_원칙과레이아웃/화면설계원칙.json')
    l=read('02_원칙과레이아웃/레이아웃지식.json')
    d=read('03_한맥디자인/한맥디자인정본.json')
    return t,s,p,q,l,d
def unique(items, label, errors):
    ids=[x['id'] for x in items]
    if len(set(ids))!=len(ids):errors.append(label+' ID 중복')
def finite(value, errors):
    if isinstance(value,float) and not math.isfinite(value):errors.append('NaN/Infinity는 기록 값이 아님')
    elif isinstance(value,dict):
        for v in value.values():finite(v,errors)
    elif isinstance(value,list):
        for v in value:finite(v,errors)
def validate_catalogs():
    t,s,p,q,l,d=catalogs();errors=[]
    for x,sch in [(t,'공통용어_스키마.json'),(s,'출처목록_스키마.json'),(p,'원칙지식_스키마.json'),(q,'원칙지식_스키마.json'),(l,'레이아웃지식_스키마.json')]:
        errors.extend(schema_errors(x,sch));finite(x,errors)
    if errors:return errors
    sources={x['id'] for x in s['sources']};axes={x['id'] for x in t['axes']};terms={x['id']:x for x in t['terms']}
    knowledge=p['principles']+q['principles']+l['layouts'];known={x['id'] for x in knowledge}
    for rows,label in [(t['terms'],'용어'),(s['sources'],'출처'),(knowledge,'지식')]:unique(rows,label,errors)
    for term in t['terms']:
        if term['axis'] not in axes:errors.append('없는 분류축: '+term['id'])
        for key in ['parent_id','replaced_by']:
            if term.get(key) and term[key] not in terms:errors.append('없는 용어 연결: '+term['id'])
        if term['parent_id'] and terms[term['parent_id']]['axis']!=term['axis']:errors.append('서로 다른 축의 상위 용어: '+term['id'])
        if term['status']=='deprecated' and not term['replaced_by']:errors.append('폐기 용어의 대체 없음: '+term['id'])
    for item in list(terms.values())+knowledge:
        for key in ['source_refs','interpretation_source_refs','application_reference_refs']:
            for ref in item.get(key,[]):
                if ref not in sources:errors.append('없는 출처: '+ref)
        for ref in item.get('related_ids',[]):
            if ref not in known and ref not in terms:errors.append('없는 관련 항목: '+ref)
    for item in l['layouts']:
        if item['term_id'] not in terms or terms[item['term_id']]['axis']!='layout':errors.append('레이아웃의 용어 연결 불일치')
    current_colors=[x for x in d['color_tokens'] if x['scope']=='global_color_library']
    if len(current_colors)!=30:errors.append('기존 한맥 전역 컬러 30개 불일치')
    tokenids={x['id'] for x in d['color_tokens']}
    for role in d['semantic_roles']:
        if role['token_id'] not in tokenids:errors.append('한맥 역할의 토큰 없음')
    if d['source_selection']['ui_mandatory'] is not False:errors.append('UI가 필수로 승격됨')
    return errors
def validate_record(r):
    errors=schema_errors(r,'최소기록_스키마.json');finite(r,errors)
    if errors:return errors
    t,s,p,q,l,d=catalogs();terms={x['id']:x for x in t['terms']};sources={x['id'] for x in s['sources']}
    scenarios={x['id'] for x in r['scenario_segments']};evidence={x['id']:x for x in r['evidence']}
    frames={x['id']:x for seg in r['segments'] for x in seg['frames']}
    ids=[r['asset']['id']]+[x['id'] for x in r['scenario_segments']]+[x['id'] for x in r['evidence']]+[x['id'] for x in r['claims']]+[x['id'] for x in r['segments']]+[x['id'] for seg in r['segments'] for x in seg['frames']]+[x['id'] for seg in r['segments'] for x in seg['beats']]
    if len(ids)!=len(set(ids)):errors.append('기록 내부 ID 중복')
    synthetic=r['asset']['source_type']=='synthetic_example'
    if r['taxonomy_ref']!=t['taxonomy_id']+'@'+t['version']:errors.append('분류 사전 버전 불일치')
    if r['design']['profile_ref']!=d['profile_id']+'@'+d['version']:errors.append('한맥 프로필 버전 불일치')
    tokens={x['id']:x for x in d['color_tokens']};styles={x['id'] for x in d['references']}|{x['id'] for x in d['gradients']}
    for role,token in r['design']['palette_role_bindings'].items():
        if token not in tokens:errors.append('없는 한맥 토큰: '+token)
        elif tokens[token]['scope']!='global_color_library':errors.append('선택 알파를 전역 단색처럼 연결: '+token)
    for ref in r['design']['optional_style_refs']:
        if ref not in styles:errors.append('없는 선택 스타일: '+ref)
    for override in r['design']['project_overrides']:
        if synthetic and override['review_state']=='approved':errors.append('설명용 예의 override 승인 금지')
    def time_check(period,label):
        start,end=period['start_s'],period['end_s']
        if start is not None and end is not None and end<start:errors.append(label+' 종료가 시작보다 빠름')
        if (start is None)!=(end is None):errors.append(label+' 시간 범위 반쪽만 입력')
        if start is not None and period['time_basis']=='unknown':errors.append(label+' 수치 시간의 기준 미기록')
        duration=r['asset']['duration_s']
        if end is not None and duration is not None and end>duration:errors.append(label+' 원본 길이 초과')
    def refs_check(refs):
        for ref in refs:
            if ref not in evidence:errors.append('없는 근거: '+ref)
    def measurement_check(item,label):
        v=item.get('measurement')
        if not isinstance(v,dict) or not all(k in v for k in ['method','quantity','unit','value','uncertainty','source_frame_refs','limitations','assumptions']):errors.append(label+' 수치 추정의 방법·단위·불확실성·근거 부족');return
        if not v['source_frame_refs'] or any(ref not in frames or frames[ref]['kind']!='extracted' for ref in v['source_frame_refs']):errors.append(label+' 수치 추정의 추출 프레임 근거 없음')
        if v['quantity']=='opacity_estimate' and not v['assumptions']:errors.append(label+' opacity 합성 조건 미기록')
    def supported(item,label):
        mode=item['support_mode'];refs_check(item['evidence_refs'])
        if mode in ['rendered_observation','numerical_estimate','scenario_supported','intent_confirmed'] and not item['evidence_refs']:errors.append(label+' 확인 주장에 근거 없음')
        if mode=='rendered_observation':
            if synthetic:errors.append('설명용 예는 원본 관측이 아님')
            valid=[]
            for ref in item['evidence_refs']:
                e=evidence.get(ref,{})
                if e.get('kind')=='frame':
                    f=frames.get(e.get('target_id'))
                    valid.append(bool(f and f['kind']=='extracted' and f['path'] and f['source_pts'] is not None and f['time_base']))
                elif e.get('kind')=='clip':
                    valid.append(bool(e.get('target_id') in {seg['id'] for seg in r['segments']} and e.get('sha256') and e.get('period',{}).get('start_s') is not None))
            if not any(valid):errors.append(label+' 렌더 관측에 실제 추출 프레임/클립 대상 연결 없음')
        if mode=='intent_confirmed' and not any(evidence.get(ref,{}).get('kind') in ['creator_confirmation','project_document'] for ref in item['evidence_refs']):errors.append(label+' 의도 확인의 제작자/기획 근거 없음')
        if mode=='scenario_supported':
            if not any(evidence.get(ref,{}).get('kind')=='script' and evidence.get(ref,{}).get('target_id') in scenarios and next(x for x in r['scenario_segments'] if x['id']==evidence[ref]['target_id'])['kind'] in ['original_scenario','transcript'] for ref in item['evidence_refs']):
                errors.append(label+' 시나리오 지원의 원문/전사 대상 근거 없음')
        if mode=='numerical_estimate':measurement_check(item,label)
    if not synthetic and (not r['asset']['path'] or not r['asset']['sha256']):errors.append('실제 자산 경로·해시 미기록')
    for x in r['scenario_segments']:
        time_check(x['period'],'시나리오')
        if x['source_ref'] not in sources:errors.append('시나리오 출처 없음')
    for e in evidence.values():
        if e['source_ref'] not in sources:errors.append('근거 출처 없음')
        if not synthetic and e['kind']=='example_description':errors.append('실제 사례에 설명용 근거 사용')
        if e['kind']=='frame' and (e.get('target_id') not in frames or frames.get(e.get('target_id'),{}).get('kind')!='extracted'):errors.append('프레임 근거의 원본 추출 대상 없음')
        if e['kind']=='clip' and e.get('target_id') not in {seg['id'] for seg in r['segments']}:errors.append('클립 근거의 구간 대상 없음')
        if e['kind']=='script' and e.get('target_id') not in scenarios:errors.append('시나리오 근거의 대상 없음')
    for seg in r['segments']:
        time_check(seg['period'],'구간')
        for ref in seg['scenario_refs']:
            if ref not in scenarios:errors.append('구간 시나리오 연결 없음')
        for axis,refs in seg['classification'].items():
            if axis not in {a['id'] for a in t['axes']}:errors.append('없는 분류축: '+axis)
            for ref in refs:
                if ref not in terms or terms[ref]['axis']!=axis:errors.append('분류 용어·축 불일치: '+ref)
                elif terms[ref]['status']=='deprecated':errors.append('폐기 용어 신규 사용: '+ref)
        if not any(seg['classification'].values()) and not seg['unclassified_reason']:errors.append('미분류 이유 없음')
        for frame in seg['frames']:
            if frame['kind']=='extracted' and (frame['source_pts'] is None or frame['time_base'] is None or not frame['path']):errors.append('추출 프레임의 원본 시간·파일 미기록')
            if frame['kind']=='extracted' and frame['actual_s'] is None:errors.append('추출 프레임의 실제 표시 시각 미기록')
        for beat in seg['beats']:
            time_check(beat['period'],'모션');supported(beat,'모션')
            start,end=beat['period']['start_s'],beat['period']['end_s'];ps,pe=seg['period']['start_s'],seg['period']['end_s']
            if all(x is not None for x in [start,end,ps,pe]) and (start<ps or end>pe):errors.append('모션이 상위 구간 시간 밖')
            for key,axis in [('property_ids','motion_property'),('function_ids','motion_function'),('timing_ids','timing')]:
                for ref in beat[key]:
                    if ref not in terms or terms[ref]['axis']!=axis:errors.append('모션 용어·축 불일치: '+ref)
    for c in r['claims']:supported(c,'주장')
    review=r['review']
    if review['state']=='approved':
        if synthetic:errors.append('설명용 예의 회사 승인 금지')
        if review['approval_kind']=='company_rule':errors.append('이 최소 사례 계약은 회사 문법 승인을 담지 않는다. 01-B 별도 패턴 검수 필요')
        if not review['reviewer'] or not review['reviewed_at'] or not review['approved_scope']:errors.append('승인 검수자·시각·범위 없음')
        decisions=read('05_출처와검토/검수결정.json')['decisions']
        decision=next((x for x in decisions if x['id']==review['decision_ref']),None)
        if not decision or any(decision.get(k)!=v for k,v in {'object_id':r['record_id'],'object_version':r['version'],'approval_kind':review['approval_kind'],'reviewer':review['reviewer'],'approved_scope':review['approved_scope']}.items()):errors.append('대상·종류·범위가 일치하는 별도 사람 검수 결정 없음')
        if decision and (decision.get('state')!='approved' or decision.get('reviewed_at')!=review['reviewed_at'] or not FormatChecker().conforms(decision.get('reviewed_at'),'date-time')):errors.append('승인 결정의 상태·검수 시각 불일치')
        if review['object_version']!=r['version']:errors.append('승인 대상 버전 불일치')
        for ref in evidence:
            if review['evidence_versions'].get(ref)!=evidence[ref]['version']:errors.append('승인 근거 버전 미고정')
    return errors
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    errors=validate_catalogs()
    if args.record:errors+=validate_record(json.loads(args.record.read_text(encoding='utf-8')))
    else:errors+=validate_record(read('04_기록규격/설명용_단계구성_예시.json'))
    result={'valid':not errors,'errors':errors,'scope':'Phase 00 데이터·기록 계약. 실영상 정확도/효과 검증 아님.'}
    if args.output:
        output=args.output.resolve()
        if not output.is_relative_to(BASE):raise ValueError('검사 결과는 Phase 00 안에 저장')
        output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
