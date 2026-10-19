"""R6-2 읽기 전용 연결 검사. 실행/권리/신원 인증을 수행하지 않는다."""
from pathlib import Path
import json, hashlib, copy, math
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

FOLDER='05_출처와검토/검수와사용범위/'
INDEX=FOLDER+'출처와사용범위_연결목록.json'
SCHEMA=FOLDER+'출처와사용범위_연결규격.json'
INPUTS={
 'legacy_sources':'05_출처와검토/출처목록.json',
 'file_reviews':'05_출처와검토/스킬심층검토/검토파일목록.json',
 'skill_cards':'05_출처와검토/스킬심층검토/스킬심층검토정본.json',
 'assets':'10_공용자산/자산목록.json',
 'legacy_policy':'05_출처와검토/사용자결정.json',
 'legacy_decisions':'05_출처와검토/검수결정.json',
 'recovery':FOLDER+'원문경로_복구연결.json',
 'human_intake_policy':FOLDER+'사람검수_접수정책.json',
 'r5_policy':'05_출처와검토/R5_적용정책_결정.json',
}
RESEARCH=['R2_조사기록.json','R3_모션_조사기록.json','R3_레이아웃_조사기록.json','R4_시간프레임_조사기록.json','R4_근거주장_조사기록.json','R4_좌표변환_조사기록.json','R4_통합이관_조사기록.json','R5_조사기록.json']
for n,p in enumerate(RESEARCH): INPUTS['research_'+str(n)]='05_출처와검토/'+p
INPUTS['research_r6']=FOLDER+'R6_조사기록.json'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def unique_pairs(pairs):
    d={}
    for key,value in pairs:
        if key in d:raise ValueError('duplicate JSON key: '+repr(key))
        d[key]=value
    return d
def read_snapshot(p):
    raw=p.read_bytes()
    def reject_constant(s):raise ValueError('non-finite JSON number')
    d=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=reject_constant)
    validate_json_values(d)
    return d,hashlib.sha256(raw).hexdigest()
def validate_json_values(value,depth=0):
    if depth>128:raise ValueError('JSON nesting exceeds 128')
    if isinstance(value,str):
        if any(0xD800<=ord(c)<=0xDFFF for c in value):raise ValueError('unpaired Unicode surrogate')
    elif isinstance(value,float) and not math.isfinite(value):raise ValueError('non-finite JSON number')
    elif isinstance(value,dict):
        for k,v in value.items():validate_json_values(k,depth+1);validate_json_values(v,depth+1)
    elif isinstance(value,list):
        for v in value:validate_json_values(v,depth+1)
def read(p): return read_snapshot(p)[0]
def local(base, rel):
    if not isinstance(rel,str) or not rel.strip() or Path(rel).is_absolute(): raise ValueError('relative path required')
    p=(base/rel).resolve()
    if not p.is_relative_to(base.resolve()):raise ValueError('outside project')
    return p
def pin(base,rel):
    p=local(base,rel);d=read(p)
    if not isinstance(d,dict):raise ValueError('source root must be object: '+rel)
    return {'path':rel,'version':d.get('version',d.get('record_version',d.get('schema_version','unversioned'))),'sha256':digest(p)}
def pointer(data,part):
    for bit in part.strip('/').split('/') if part else []:
        bit=bit.replace('~1','/').replace('~0','~');data=data[int(bit)] if isinstance(data,list) else data[bit]
    return data
def build(base):
    docs={k:read(local(base,v)) for k,v in INPUTS.items()}
    rows=[]
    def add(kind,key,ptr,raw):
        rows.append({'link_id':f'R6-LINK-{len(rows)+1:04}','kind':kind,'source_key':key,'pointer':ptr,'original_record':copy.deepcopy(raw),'fresh_content_review':False,'permission_grant_created':False})
    for i,r in enumerate(docs['legacy_sources']['sources']):add('legacy_source','legacy_sources',f'/sources/{i}',r)
    for key in INPUTS:
        if key.startswith('research_'):
            doc=docs[key]
            # 출처 행과 별도로 문서 전체의 조사 범위·깊이·제한을 보존한다.
            add('research_context',key,'',doc)
            for field in ['sources','web_sources','local_sources']:
                if isinstance(doc.get(field),list):
                    for i,r in enumerate(doc[field]):add('research_source',key,f'/{field}/{i}',r)
    aliases={r['old_record_path']:r for r in docs['recovery']['aliases']}
    files=[]
    for i,r in enumerate(docs['file_reviews']['records']):
        add('file_review','file_reviews',f'/records/{i}',r)
        alias=aliases.get(r['path']) or aliases.get(r.get('absolute_path'))
        original=Path(r['path']) if Path(r['path']).is_absolute() else local(base,r['path'])
        recovery=alias['preserved_snapshot'] if alias else None
        files.append({'review_pointer':f'/records/{i}','original_path':r['path'],'sha256':r['sha256'],'preserved_snapshot':recovery,
                      'reported_depth':r['depth'],'execution_declared':r['executed'],'review_scope':'original_file_ledger_only','runtime_effectiveness_verified':False})
    for i,r in enumerate(docs['skill_cards']['cards']):add('skill_card','skill_cards',f'/cards/{i}',r)
    for i,r in enumerate(docs['legacy_policy']['decisions']):add('workflow_policy','legacy_policy',f'/decisions/{i}',r)
    for key in ['human_intake_policy','r5_policy']:add('workflow_policy',key,'',docs[key])
    usage=[]
    for i,r in enumerate(docs['assets']['records']):
        usage.append({'asset_id':r['asset_id'],'record_version':r['record_version'],'source_pointer':f'/records/{i}',
                      'recorded_usage':copy.deepcopy(r['usage']),'file':copy.deepcopy(r['file']),
                      'interpretation':'documented_internal_reference_context','broader_use_confirmed':False})
    return {'id':'r6-source-use-links','version':'0.1.0','scope':'bounded_reference_index_not_permission_or_content_approval',
            'source_pins':{k:pin(base,v) for k,v in INPUTS.items()},'links':rows,'file_checks':files,'asset_usage':usage,
            'coverage':'초기20출처·지정9조사문서·544파일행·40후보·135자산·중앙8정책과R5/R6정책. 분산R4정책의 개별결정 색인은R6-3에서 다룸. 회사/자료전체 전수목록 아님.',
            'identity_authenticated':False,'company_approved':False,'operational_release':False}

def inspect(base,data=None,verify_artifacts=True):
    base=Path(base).resolve();errors=[]
    result={'structural_valid':False,'errors':errors,'identity_authenticated':False,'content_verified':False,'company_approved':False,'permission_granted':False,'operational_release':False,'artifact_identity_checked':False,'artifact_rows_checked':0}
    if type(verify_artifacts) is not bool:
        errors.append('verify_artifacts requires boolean');return result
    try:
        d=read(local(base,INDEX)) if data is None else copy.deepcopy(data)
        validate_json_values(d)
        schema=read(local(base,SCHEMA))
        if not isinstance(schema,dict):raise ValueError('schema root must be object')
        Draft202012Validator.check_schema(schema)
        errors.extend('schema: '+e.message for e in Draft202012Validator(schema).iter_errors(d))
        if errors:return result
        for k,rel in INPUTS.items():
            if d['source_pins'].get(k)!=pin(base,rel):errors.append('stale_source: '+k)
        if errors:return result
        expected=build(base)
        if d!=expected:errors.append('derived_index_differs_from_pinned_originals');return result
        if verify_artifacts:
            cache={}
            for f in d['file_checks']:
                original=Path(f['original_path']) if Path(f['original_path']).is_absolute() else local(base,f['original_path'])
                # Prefer original if present. An altered original cannot hide behind a recovery snapshot.
                p=original if original.is_file() else local(base,f['preserved_snapshot']) if f['preserved_snapshot'] else original
                if str(p) not in cache:cache[str(p)]=digest(p) if p.is_file() else None
                if cache[str(p)]!=f['sha256']:errors.append('artifact_missing_or_changed: '+f['review_pointer'])
                result['artifact_rows_checked']+=1
            for a in d['asset_usage']:
                p=local(base,a['file']['path'])
                if digest(p)!=a['file']['sha256']:errors.append('asset_file_changed: '+a['asset_id'])
            result['artifact_identity_checked']=not errors
        # 단순 확인-읽기 사이의 입력 변경을 감지한다. 원자적 잠금/스냅샷은 아니다.
        for k,rel in INPUTS.items():
            if d['source_pins'].get(k)!=pin(base,rel):errors.append('source_changed_during_check: '+k)
        result['structural_valid']=not errors
    except (OSError,ValueError,TypeError,KeyError,IndexError,RecursionError,SchemaError) as e:errors.append(type(e).__name__+': '+str(e))
    return result

def assess_use(base,asset_id,action,context):
    """Scopes a request against recorded context, never grants rights or performs the action."""
    out={'recorded_context_match':False,'state':'needs_scope_review','permission_granted':False,'company_approved':False,'performed':False}
    if not all(isinstance(x,str) and x.strip() for x in [asset_id,action,context]):return {**out,'state':'invalid_request'}
    try:
        candidate,index_hash=read_snapshot(Path(base)/INDEX)
    except (OSError,ValueError,TypeError,RecursionError) as e:return {**out,'state':'invalid_or_stale_index','errors':[str(e)]}
    valid=inspect(base,candidate)
    if not valid['structural_valid']:return {**out,'state':'invalid_or_stale_index','errors':valid['errors']}
    allowed_actions=['internal_reference','design_draft','external_api_upload','distribute','copy_code','execute_code']
    if action not in allowed_actions:return {**out,'state':'unknown_action'}
    # 검증한 같은 사본에서 반환한다. 변경된 색인을 재독해 사용하지 않는다.
    try:
        if digest(Path(base)/INDEX)!=index_hash:return {**out,'state':'index_changed_during_check'}
    except OSError as e:return {**out,'state':'invalid_or_stale_index','errors':[str(e)]}
    assets=candidate['asset_usage'];a=next((a for a in assets if a['asset_id']==asset_id),None)
    if a is None:return {**out,'state':'unknown_asset'}
    if action=='internal_reference' and context in a['recorded_usage']['contexts']:
        out.update(recorded_context_match=True,state='documented_reference_context')
    return {**out,'recorded_usage':a['recorded_usage'],'next':'일치는 기존 작업 맥락의 기록만 뜻함. 새 용도는 구체 대상·행위·근거·범위의 사람 검토 필요. R5 초안 선택 정책을 확대하지 않음.'}

if __name__=='__main__':
    import argparse
    cli=argparse.ArgumentParser();cli.add_argument('--base',type=Path,default=Path(__file__).resolve().parents[1]);args=cli.parse_args()
    result=inspect(args.base)
    # 진단은 어떤 콘솔 인코딩에서도 출력 가능하게 escape한다. 입력은 수정하지 않는다.
    print(json.dumps(result,ensure_ascii=True,indent=2))
    raise SystemExit(0 if result['structural_valid'] else 1)
