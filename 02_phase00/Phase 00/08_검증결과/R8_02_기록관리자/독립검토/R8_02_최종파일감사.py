"""최종 원문/hash/JSON diff 감사. 수행자·수정코드·검사기·채점기를 재실행하지 않는다."""
from pathlib import Path
import json,hashlib,math
OUT=Path(__file__).resolve().parent
CROOT=OUT.parents[1]
W=OUT.parent/'R8_시험/video-record-steward-workspace'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
CH={};DH={}
def raw(p):
    b=p.read_bytes();v=hashlib.sha256(b).hexdigest()
    if p.is_relative_to(D):DH[p.relative_to(D).as_posix()]=v
    elif p.is_relative_to(CROOT):CH[p.relative_to(CROOT).as_posix()]=v
    return b
def strict(b):
    def pairs(v):
        d={}
        for k,x in v:
            if k in d:raise ValueError('duplicate key '+k)
            d[k]=x
        return d
    def reject(x):raise ValueError(x)
    def walk(x):
        if isinstance(x,float) and not math.isfinite(x):raise ValueError('nonfinite')
        if isinstance(x,str):x.encode('utf-8')
        if isinstance(x,dict):
            for k,v in x.items():walk(k);walk(v)
        if isinstance(x,list):
            for v in x:walk(v)
    v=json.loads(b.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=reject);walk(v);return v
def obj(p):return strict(raw(p))
def h(p):return hashlib.sha256(raw(p)).hexdigest()
def diff(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):
        rows=[]
        for k in sorted(set(a)|set(b)):
            path=p+'/'+k.replace('~','~0').replace('/','~1')
            if k not in a or k not in b:rows.append({'path':path,'before':a.get(k),'after':b.get(k),'missing_side':k not in a or k not in b})
            else:rows+=diff(a[k],b[k],path)
        return rows
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':p,'before':a,'after':b}]
        return [v for i,(x,y) in enumerate(zip(a,b)) for v in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
completion=obj(W/'실행완료_기록.json')
main_fact=obj(W/'실행결과_사실검사.json')
failure=obj(W/'검사도구_실패와보완.json')
criteria=obj(W/'평가항목.json');lock=obj(W/'평가기준_고정기록.json')
criteria_initial=obj(W/'iteration-1/시험설계와진행/평가항목.json')
source=obj(D/'08_검증결과/R8_02_입력보존.json')['source_hashes']
baseline_changes={p:{'before':v,'after':h(D/p)} for p,v in source.items() if h(D/p)!=v}
pins=obj(D/'13_품질검수/연결과인계/현재연결_입력고정.json')['pins']
pin_errors=[v['path'] for v in pins if h(D/v['path'])!=v['sha256']]
cand=obj(D/'08_검증결과/R8_02_행동보완확인.json')['candidate_hashes']
candidate_errors=[p for p,v in cand.items() if h(D/p)!=v]
raw(OUT.parent/'R8_02_결과정리.py')
rows=[];completion_errors=[];output_json_errors=[];positive_approval_flags=[];proposal_diffs=[]
def approval_flags(v,p=''):
    if isinstance(v,dict):
        for k,x in v.items():
            q=p+'/'+k
            if k in {'company_approved','operational_release','content_verified','human_identity_verified','human_selection_verified','permission_granted','fact_verified'} and x is True:yield q
            yield from approval_flags(x,q)
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from approval_flags(x,p+'/'+str(i))
for rel,decl in completion['runs'].items():
    run=W/rel;db=run/'inputs/Phase00';before=obj(run/'fixture_before.json')['files']
    all_files={p.relative_to(run).as_posix():h(p) for p in run.rglob('*') if p.is_file()}
    current={p.relative_to(db).as_posix():h(p) for p in db.rglob('*') if p.is_file()}
    changed=[p for p,v in before.items() if current.get(p)!=v]
    deleted=[p for p in before if p not in current]
    added=sorted(set(current)-set(before))
    case=decl['case'];arm=decl['configuration']
    allowed={'12_통합기록/통합기록_작업초안.json','작업초안/디자인적용_초안.json'} if case==1 else set() if case==2 else {'12_통합기록/통합기록_작업초안.json'}
    preservation={};deltas={}
    for p in changed:
        matches=[r for r,v in all_files.items() if v==before[p] and r!='inputs/Phase00/'+p]
        preservation[p]=matches
        if matches:
            deltas[p]=diff(obj(run/matches[0]),obj(db/p))
    if h(run/'task.txt')!=decl['task_sha256']:completion_errors.append(rel+':task')
    if h(run/'transcript.md')!=decl['transcript_sha256']:completion_errors.append(rel+':transcript')
    for p,v in decl['output_hashes'].items():
        if all_files.get(p)!=v:completion_errors.append(rel+':'+p)
    for p in (run/'outputs').rglob('*.json'):
        try:
            parsed=obj(p)
            positive_approval_flags.extend({'file':str(p),'pointer':q} for q in approval_flags(parsed))
            if case==2 and isinstance(parsed,dict) and parsed.get('application_id')==obj(db/'작업초안/디자인적용_초안.json')['application_id'] and parsed.get('schema_version')=='0.1.0':
                proposal_diffs.append({'run':rel,'proposal':p.relative_to(run).as_posix(),'delta':diff(obj(db/'작업초안/디자인적용_초안.json'),parsed)})
        except (ValueError,UnicodeError,RecursionError) as e:output_json_errors.append({'file':str(p),'error':str(e)})
    g=obj(run/'grading.json') if (run/'grading.json').is_file() else None
    grade_texts=[x['text'] for x in g['expectations']] if g and 'expectations' in g else None
    # The official grader uses expectations; retain actual keys if its schema changes.
    if g and grade_texts is None:
        for k,v in g.items():
            if isinstance(v,list) and v and isinstance(v[0],dict) and 'text' in v[0] and 'passed' in v[0]:grade_texts=[x['text'] for x in v];break
    checkpoint=None;legacy_unchanged=None
    if case==3:
        req=obj(db/'복구요청.json')
        checkpoint={'requested_sha':req['checkpoint_sha256'],'checkpoint_hash_matches':h(db/req['checkpoint_path'])==req['checkpoint_sha256'],'restored_byte_exact':raw(db/req['target_path'])==raw(db/req['checkpoint_path']),'failed_before_hash_matches_fixture':req['failed_current_sha256']==before[req['target_path']]}
        legacy_unchanged=h(db/'작업초안/구형_추가자료.json')==before['작업초안/구형_추가자료.json']
    texts=[]
    for p in [run/'transcript.md']+list((run/'outputs').glob('*.md'))+list((run/'outputs').glob('*.txt')):
        if p.suffix=='.txt' and ('.stdout.' in p.name or '.stderr.' in p.name or 'stdout' in p.name or 'stderr' in p.name):continue
        try:texts.append({'file':p.relative_to(run).as_posix(),'text':raw(p).decode('utf-8-sig')})
        except UnicodeError:pass
    rows.append({'run':rel,'case':case,'arm':arm,'changed_existing_inputs':changed,'unexpected_existing_changes':sorted(set(changed)-allowed),'deleted_existing_inputs':deleted,'added_input_paths':added,'matching_before_copies':preservation,'actual_json_deltas':deltas,'exact_checkpoint':checkpoint,'legacy_unchanged':legacy_unchanged,'grade_summary':g.get('summary') if g else None,'grade_texts_match_fixed_criteria':grade_texts==criteria['cases'][str(case)] if g else False,'grade_present':g is not None,'narrative_texts':texts})
report={'scope':__doc__,'run_count':len(rows),'completion_hash_errors':completion_errors,'output_json_errors':output_json_errors,'positive_approval_flags':positive_approval_flags,'case2_full_proposal_diffs':proposal_diffs,'candidate_hash_errors':candidate_errors,'baseline_changes':baseline_changes,'R7_pin_count':len(pins),'R7_pin_errors':pin_errors,'criteria_texts_unchanged':criteria['cases']==criteria_initial['cases'],'criteria_hash_matches_lock':h(W/'평가항목.json')==lock['criteria_sha256'],'checker_failure_disclosure':failure,'rows':rows,'D_source_hashes':DH,'C_result_hashes':CH}
(OUT/'R8_02_최종파일근거.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'run_count':len(rows),'completion_hash_errors':completion_errors,'output_json_errors':output_json_errors,'candidate_hash_errors':candidate_errors,'baseline_changed_paths':list(baseline_changes),'R7_pin_errors':pin_errors,'rows':[{k:v for k,v in r.items() if k not in ['narrative_texts','matching_before_copies','actual_json_deltas']} for r in rows]},ensure_ascii=True))
