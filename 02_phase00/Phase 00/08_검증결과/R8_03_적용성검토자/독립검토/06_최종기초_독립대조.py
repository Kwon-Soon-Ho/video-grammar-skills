from pathlib import Path
import hashlib,json,math

C=Path(r'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기')
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
W=C/'phase00-build/R8_시험/video-guidance-reviewer-workspace'
A=C/'phase00-build/R8_03_독립검토'
def io(p):
    text=str(p.resolve())
    return Path(text if text.startswith('\\\\?\\') else '\\\\?\\'+text)
def digest(p):return hashlib.sha256(io(p).read_bytes()).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate key: '+k)
        d[k]=v
    return d
def invalid_constant(v):raise ValueError('nonfinite '+v)
def read(p):return json.loads(io(p).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid_constant)
def fmap(root):return {p.relative_to(root).as_posix():digest(p) for p in root.rglob('*') if p.is_file()}
def bools(value,path=''):
    result=[]
    if isinstance(value,dict):
        for k,v in value.items():result.extend(bools(v,path+'/'+k))
    elif isinstance(value,list):
        for i,v in enumerate(value):result.extend(bools(v,path+'/'+str(i)))
    elif value is True:result.append(path)
    return result

initial=read(D/'08_검증결과/R8_03_입력보존.json')['source_hashes']
expected_changed={'00_시작안내.md','01_진행현황.md','14_스킬재구성/진행상태.json','08_검증결과/R8_02_기록관리자/00_결과안내.md'}
changed={p:{'initial':h,'current':digest(D/p)} for p,h in initial.items() if digest(D/p)!=h}
backups={p: digest(D/'backup/2026-10-15_R8_03_착수/입력정본'/p) for p in initial}
backup_errors=[p for p,h in initial.items() if backups[p]!=h]
pins=read(D/'13_품질검수/연결과인계/현재연결_입력고정.json')['pins']
pin_errors=[p['path'] for p in pins if digest(D/p['path'])!=p['sha256']]
old14={p:h for p,h in initial.items() if p.startswith('06_맞춤스킬/') and '재구성후보/' not in p}
old_errors=[p for p,h in old14.items() if digest(D/p)!=h]
candidate_root=D/'06_맞춤스킬/재구성후보/video-guidance-reviewer'
candidate_expected=read(A/'02_후보draft2_SHA256.json')['files']
candidate_errors=[f['path'] for f in candidate_expected if digest(candidate_root/f['path'])!=f['sha256']]
completion=read(W/'실행완료_기록.json')
runs=[]
for rel,receipt in completion['runs'].items():
    run=W/rel;root=run/'inputs/Phase00';before=read(run/'fixture_before.json')['files'];current=fmap(root)
    errors=[p for p in sorted(set(before)|set(current)) if before.get(p)!=current.get(p)]
    artifact_errors=[]
    if digest(run/'task.txt')!=receipt['task_sha256']:artifact_errors.append('task')
    if digest(run/'transcript.md')!=receipt['transcript_sha256']:artifact_errors.append('transcript')
    for p,h in receipt['output_hashes'].items():
        if digest(run/p)!=h:artifact_errors.append(p)
    output_json=read(run/'outputs/검토기록.json')
    outputs=sorted(p.name for p in (run/'outputs').iterdir())
    run_files=sorted(p.relative_to(run).as_posix() for p in run.rglob('*') if p.is_file() and not p.is_relative_to(root))
    allowed={'task.txt','fixture_before.json','dispatch.json','timing.json','transcript.md','grading.json','eval_metadata.json','outputs/검토기록.json','outputs/검토결과.md'}
    display_metadata=read(run/'eval_metadata.json')
    source_metadata=read(run.parent.parent/'eval_metadata.json')
    assert set(display_metadata)=={'eval_id','eval_name','prompt'} and display_metadata=={key:source_metadata[key] for key in display_metadata}
    runs.append({'run':rel,'input_count':len(current),'input_byte_mismatches':errors,'artifact_receipt_mismatches':artifact_errors,'output_files':outputs,'unexpected_run_files':[p for p in run_files if p not in allowed],'strict_output_json_parse_valid':True,'true_boolean_paths':bools(output_json),'actual_completion_notification_recorded':receipt['actual_completion_notification_received'],'telemetry_unavailable':all(receipt[k] is None for k in ['total_tokens','duration_ms','telemetry_in_notification'])})
result={'stage':'R8-3','kind':'independent_byte_and_strict_json_audit_not_content_or_model_trial','initial174_count':len(initial),'current_changed_paths':changed,'only_expected4_changes_before_publication':set(changed)==expected_changed,'initial174_backup_mismatches':backup_errors,'R7_pin_count':len(pins),'R7_pin_mismatches':pin_errors,'old_skill_file_count':len(old14),'old_skill_mismatches':old_errors,'candidate_instruction_file_count':len(candidate_expected),'candidate_mismatches':candidate_errors,'run_count':len(runs),'runs':runs,'limits':['start/end bytes do not prove no temporary mutation','transcripts are executor-authored process accounts, not independently captured complete tool traces','notification receipt flags are main-observed metadata, not identity authentication','no D helper/query executed by this audit','no grading files read by this script']}
io(A/'06_최종기초_독립대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['current_changed_paths','runs']},ensure_ascii=False))
print(json.dumps([{'run':r['run'],'input_count':r['input_count'],'input_errors':r['input_byte_mismatches'],'receipt_errors':r['artifact_receipt_mismatches'],'unexpected':r['unexpected_run_files'],'true_bools':r['true_boolean_paths']} for r in runs],ensure_ascii=False,indent=2))
