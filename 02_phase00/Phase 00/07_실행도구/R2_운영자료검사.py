"""R2 운영자료/설명용 기록의 참조·범위 검사. 영상 분류기나 R4 기록 검증기가 아니다."""
from pathlib import Path
import json,hashlib
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S={'type':'string','minLength':1,'pattern':r'\S'}
def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def arr(item):return {'type':'array','items':item}
def many(item):return {**arr(item),'minItems':1,'uniqueItems':True}
V={'type':'string','pattern':r'^\d+\.\d+\.\d+$'}
KINDS={'enum':['asset','segment','state','beat']}
ru=obj({k:S for k in ['id','name_ko','meaning','boundary','example','counterexample','existing_field']})
RULE_SCHEMA=obj({'version':V,'status':{'const':'project_draft'},'decision':S,'taxonomy_ref':S,'taxonomy_sha256':S,'units':many(ru),'axis_units':{'type':'object','additionalProperties':many(KINDS),'minProperties':1},'cross_unit_policy':S,'states':many(S),'reason_codes':many(S),'unclassified_policy':S,'mapping_boundary':S,'company_approval':{'const':False},'claim_status_policy':S,'evidence_rules':{'type':'object','minProperties':1,'additionalProperties':obj({'requires':many(S),'limit':S})}})
guide=obj({**{k:S for k in ['term_id','axis','name_ko','minimum_evidence','positive_example','negative_example','abstain_when','claim_scope_note']},'record_version':V,'status':{'const':'project_draft'},'units':many(KINDS),'source_refs':many(S),'example_origin':{'const':'synthetic_example'},'company_approved':{'const':False}})
GUIDE_SCHEMA=obj({'version':V,'taxonomy_ref':S,'taxonomy_sha256':S,'interpretation':S,'guides':many(guide)})
pair=obj({**{k:S for k in ['id','title','contrast','avoid']},'term_ids':{**many(S),'minItems':2},'status':{'const':'project_draft'}})
PAIR_SCHEMA=obj({'version':V,'origin':{'const':'synthetic_example'},'pairs':many(pair)})
unit=obj({'id':S,'kind':{'enum':['asset','segment','state','beat']},'parent_id':{'type':['string','null']},'scope_note':S})
annotation=obj({'unit_id':S,'target_scope':S,'claim_scope':S,'axis':S,'term_ids':arr(S),'status':{'enum':['classified','unknown','not_applicable','other_candidate','not_assessed']},'reason':S,'reason_code':{'type':['string','null']},'basis':{'const':'synthetic_description'},'candidate_text':{'type':['string','null']},'limitations':arr(S)})
case=obj({'id':S,'title':S,'origin':{'const':'synthetic_example'},'units':arr(unit),'annotations':arr(annotation),'interpretation':S,'company_approved':{'const':False}})
SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema',**obj({'version':S,'taxonomy_ref':S,'origin':{'const':'synthetic_example'},'cases':{**arr(case),'minItems':1},'limit':S})}
case['properties']['units']['minItems']=1
case['properties']['annotations']['minItems']=1
def _validate(rules,guides,pairs,cases,sources,taxonomy):
    errors=[]
    for data,schema,label in [(rules,RULE_SCHEMA,'운영규칙'),(guides,GUIDE_SCHEMA,'판정기준'),(pairs,PAIR_SCHEMA,'혼동쌍'),(cases,SCHEMA,'연습사례')]:
        Draft202012Validator.check_schema(schema)
        errors.extend(label+' '+str(list(e.path))+': '+e.message for e in Draft202012Validator(schema).iter_errors(data))
    if errors:return errors
    ref=taxonomy['taxonomy_id']+'@'+taxonomy['version'];h=sha(BASE/'01_공통용어/공통용어사전.json')
    terms={x['id']:x for x in taxonomy['terms']};active={k for k,v in terms.items() if v['status']!='deprecated'};axes={x['id'] for x in taxonomy['axes']}
    source_ids={x['id'] for x in sources['sources']}
    for name,d in [('운영규칙',rules),('판정기준',guides)]:
        if d.get('taxonomy_ref')!=ref or d.get('taxonomy_sha256')!=h:errors.append(name+' 분류사전 버전/해시 불일치')
    if cases['taxonomy_ref']!=ref:errors.append('연습사례 분류버전 불일치')
    if rules.get('status')!='project_draft' or rules.get('company_approval') is not False:errors.append('운영규칙을 승인 상태로 승격')
    if set(rules['axis_units'])!=axes:errors.append('8축 단위 매핑 누락/추가')
    kinds={x['id'] for x in rules['units']}
    if kinds!={'asset','segment','state','beat'} or len(rules['units'])!=4:errors.append('4단위 정의 누락/중복')
    if set(rules['states'])!={'classified','unknown','not_applicable','other_candidate','not_assessed'}:errors.append('5개 판정상태 변경/누락')
    if any(not u or len(u)!=len(set(u)) or not set(u)<=kinds for u in rules['axis_units'].values()):errors.append('축 단위 매핑 오류')
    gids=[x['term_id'] for x in guides['guides']]
    if len(gids)!=len(set(gids)) or set(gids)!=active:errors.append('현재75개 용어 가이드 누락/중복/폐기 혼입')
    for g in guides['guides']:
        t=terms.get(g['term_id'])
        if not t:continue
        if g['axis']!=t['axis'] or g['units']!=rules['axis_units'].get(t['axis']) or g['name_ko']!=t['name_ko']:errors.append('용어 명칭/축/단위 불일치 '+g['term_id'])
        if g['minimum_evidence'] not in rules['evidence_rules']:errors.append('없는 근거규칙 '+g['term_id'])
        required_evidence={'video_type':'whole_content_or_declared_context','communication_purpose':'visible_scope_and_message_context','information_relation':'visible_scope_and_message_context','layout':'visible_scope','motion_function':'temporal_change_plus_message_context','motion_property':'tracked_target_and_temporal_scope','timing':'tracked_target_and_temporal_scope','art_direction':'visible_scope'}[t['axis']]
        if t['id'].startswith('CURVE-'):required_evidence='quantity_and_temporal_samples'
        required_evidence={'LAYOUT-UI-ANNOTATION':'visible_ui_scope_and_verified_capture_source','STYLE-PHOTO':'visible_material_and_verified_photo_source','PROPERTY-OPACITY':'source_value_or_conditioned_opacity_estimate'}.get(t['id'],required_evidence)
        if g['minimum_evidence']!=required_evidence:errors.append('항목별 필수근거를 약한/다른 규칙으로 변경 '+g['term_id'])
        for key in ['positive_example','negative_example','abstain_when','claim_scope_note']:
            if not isinstance(g.get(key),str) or not g[key].strip():errors.append('용어 조건 누락 '+g['term_id']+' '+key)
        if g['example_origin']!='synthetic_example' or g['company_approved'] is not False or g.get('status')!='project_draft':errors.append('설명용 용어를 실제/승인으로 승격 '+g['term_id'])
        if not set(g['source_refs'])<=source_ids:errors.append('가이드 출처 없음 '+g['term_id'])
    pids=[p['id'] for p in pairs['pairs']]
    if not pids or pairs.get('origin')!='synthetic_example':errors.append('혼동쌍의 설명용 범위/최소항목 없음')
    if len(pids)!=len(set(pids)):errors.append('혼동쌍 ID 중복')
    for p in pairs['pairs']:
        if not set(p['term_ids'])<=set(terms):errors.append('혼동쌍 없는 용어')
        if p.get('status')!='project_draft':errors.append('혼동쌍을 승인 상태로 승격')
    cids=[c['id'] for c in cases['cases']]
    if len(cids)!=len(set(cids)):errors.append('사례ID 중복')
    for c in cases['cases']:
        us={u['id']:u for u in c['units']}
        if len(us)!=len(c['units']):errors.append(c['id']+' 단위ID 중복')
        if sum(u['kind']=='asset' for u in c['units'])!=1:errors.append(c['id']+' 영상전체 루트 하나 필요')
        for u in c['units']:
            parent=us.get(u['parent_id'])
            expected={'asset':None,'segment':'asset','state':'segment','beat':'segment'}[u['kind']]
            if expected is None:
                if u['parent_id'] is not None:errors.append(c['id']+' 영상전체에 상위 단위')
            elif not parent or parent['kind']!=expected:errors.append(c['id']+' 단위 계층 연결 오류')
        seen=set()
        for a in c['annotations']:
            if a['axis'] not in axes or a['unit_id'] not in us:errors.append(c['id']+' 없는 축/대상');continue
            if us[a['unit_id']]['kind'] not in rules['axis_units'][a['axis']]:errors.append(c['id']+' 축의 대상단위 불일치')
            key=(a['unit_id'],a['target_scope'].strip(),a['axis'],a['claim_scope'].strip())
            if key in seen:errors.append(c['id']+' 같은 대상/주장/축 판정 중복')
            seen.add(key)
            if len(a['term_ids'])!=len(set(a['term_ids'])):errors.append(c['id']+' 태그 중복')
            for tid in a['term_ids']:
                if tid not in active or terms[tid]['axis']!=a['axis']:errors.append(c['id']+' 없는/폐기/다른축 태그 '+tid)
            if a['status']=='classified':
                if not a['term_ids'] or a['reason_code'] is not None or a['candidate_text'] is not None:errors.append(c['id']+' 분류된 태그/상태 모순')
            else:
                if a['term_ids'] or a['reason_code'] not in rules['reason_codes']:errors.append(c['id']+' 미분류 태그/이유코드 모순')
                if a['status']=='not_assessed' and a['reason_code']!='not_assessed_yet':errors.append(c['id']+' 미검토 이유코드 혼동')
                if a['status']=='not_applicable' and a['reason_code']!='not_applicable_to_scope':errors.append(c['id']+' 비적용 이유코드 혼동')
                if a['status']=='other_candidate':
                    if a['reason_code']!='outside_vocabulary' or not (a['candidate_text'] or '').strip():errors.append(c['id']+' 미등록 후보 문구/이유 없음')
                elif a['candidate_text'] is not None:errors.append(c['id']+' 후보가 아닌 상태에 새 용어 문구')
    return errors
def validate(*args):
    try:return _validate(*args)
    except (KeyError,TypeError,AttributeError,ValueError) as e:return ['R2 필수 자료/자료형 오류: '+str(e)]
def load():return (read('01_공통용어/분류운영규칙.json'),read('01_공통용어/용어판정기준.json'),read('01_공통용어/혼동쌍사례.json'),read('01_공통용어/설명용분류사례.json'),read('05_출처와검토/R2_조사기록.json'),read('01_공통용어/공통용어사전.json'))
if __name__=='__main__':
    data=load();errors=validate(*data)
    print(json.dumps({'valid':not errors,'errors':errors,'counts':{'guides':len(data[1]['guides']),'pairs':len(data[2]['pairs']),'cases':len(data[3]['cases'])},'scope':'R2 참조·범위·설명용기록 검사. 의미분류/실영상성능검증아님.'},ensure_ascii=False,indent=2));raise SystemExit(1 if errors else 0)
