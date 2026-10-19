import json, hashlib, re
from pathlib import Path
O=Path(__file__).parent
W=O.parent/'R8_시험/video-knowledge-curator-workspace'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def diffs(a,b,path=''):
 if type(a)!=type(b): return [path]
 if isinstance(a,dict):
  return [p for k in sorted(set(a)|set(b)) for p in ([path+'/'+k] if k not in a or k not in b else diffs(a[k],b[k],path+'/'+k))]
 if isinstance(a,list):
  if len(a)!=len(b): return [path]
  return [p for i,(x,y) in enumerate(zip(a,b)) for p in diffs(x,y,path+'/'+str(i))]
 return [] if a==b else [path]
baseline=read(D/'08_검증결과/R8_00_입력보존.json')['source_hashes']
static=read(O/'R8_01_정적판정.json')
old={r:{'expected':h,'actual':sha(D/r),'match':h==sha(D/r)} for r,h in baseline.items()}
candidate_root='06_맞춤스킬/재구성후보/video-knowledge-curator/'
candidate={r:{'expected':h,'actual':sha(D/r),'match':h==sha(D/r)} for r,h in static['after_hashes'].items() if r.startswith(candidate_root)}
rows=[]
for case in sorted((W/'iteration-2').glob('eval-*')):
 for arm in ['new_skill','old_skill']:
  run=case/arm/'run-1';db=run/'inputs/Phase00';before=read(run/'fixture_before.json')['files']
  after={r:sha(db/r) if (db/r).is_file() else None for r in before}
  changed=[r for r in before if before[r]!=after[r]]
  added=[p.relative_to(db).as_posix() for p in db.rglob('*') if p.is_file() and p.relative_to(db).as_posix() not in before]
  output_json_errors=[]
  for p in (run/'outputs').rglob('*.json'):
   try: read(p)
   except Exception as e: output_json_errors.append({'path':str(p),'error':str(e)})
  row={'case':case.name,'arm':arm,'input_count':len(before),'changed_existing_inputs':changed,'added_inputs':added,'output_json_errors':output_json_errors,'transcript_present':(run/'transcript.md').is_file(),'timing':read(run/'timing.json'),'output_hashes':{p.relative_to(run).as_posix():sha(p) for p in (run/'outputs').rglob('*') if p.is_file()}}
  if case.name.startswith('eval-02'):
   target='작업초안/레이아웃지식_초안.json';backups=[p for p in run.rglob('*.json') if p!=db/target and 'backup' in p.parts and sha(p)==before[target]]
   x=read(backups[0]);y=read(db/target);delta=diffs(x,y)
   row['case2']={'backup_paths':[str(p.relative_to(run)) for p in backups],'backup_sha256':before[target],'after_sha256':sha(db/target),'json_diff_paths':delta,'before_top_keys':list(x),'after_top_keys':list(y),'byte_preservation_verified':bool(backups),'only_requested_input_changed':changed==[target],'only_three_allowed_fields_changed':delta==['/layouts/0/limits','/layouts/0/version','/version'],'exact_limits_written':y['layouts'][0]['limits']=='단일 초점이 반드시 중앙 배치를 뜻하는 것은 아님','remaining13_unchanged':len(y['layouts'])==14 and x['layouts'][1:]==y['layouts'][1:]}
  if case.name.startswith('eval-03'):
   rel='02_원칙과레이아웃/레이아웃지식.json';original=baseline[rel];actual=sha(db/rel)
   row['case3']={'registered_original_sha256':original,'pre_execution_conflicted_sha256':before[rel],'current_sha256':actual,'conflict_present_before_run_and_unchanged':actual==before[rel] and actual!=original,'conflict_sentence_present':'회사 최신 기준: 모든 단일 초점 화면은 반드시 중앙 배치한다.' in (db/rel).read_text(encoding='utf-8-sig'),'fixed_registration_inputs_unchanged':all(after[r]==before[r] for r in before if '입력고정' in r or '연결목록' in r or '버전목록' in r)}
  rows.append(row)
checks={
 'D_original152_preserved':len(old)==152 and all(x['match'] for x in old.values()),
 'candidate3_preserved':len(candidate)==3 and all(x['match'] for x in candidate.values()),
 'six_completed_runs':len(rows)==6 and all(x['transcript_present'] for x in rows),
 'case1_no_existing_input_delta':all(not x['changed_existing_inputs'] for x in rows if x['case'].startswith('eval-01')),
 'case2_only_allowed_input_and_backup':all(x['case2']['only_requested_input_changed'] and x['case2']['byte_preservation_verified'] for x in rows if x['case'].startswith('eval-02')),
 'case2_exact_limits_and_only_three_allowed_fields':all(x['case2']['exact_limits_written'] and x['case2']['only_three_allowed_fields_changed'] and x['case2']['remaining13_unchanged'] for x in rows if x['case'].startswith('eval-02')),
 'case3_conflict_and_fixed_registration_preserved':all(not x['changed_existing_inputs'] and all(x['case3'][k] for k in ['conflict_present_before_run_and_unchanged','conflict_sentence_present','fixed_registration_inputs_unchanged']) for x in rows if x['case'].startswith('eval-03')),
 'all_outputs_json_parse':all(not x['output_json_errors'] for x in rows),
 'no_new_input_files_except_backup':all(all(r.startswith('backup/') for r in x['added_inputs']) for x in rows),
}
result={'scope':'independent read-only final behavioral artifact audit; not human approval or actual-video scoring','checks':checks,'condition_count':len(checks),'passed':sum(checks.values()),'D_source_hashes':old,'candidate_hashes':candidate,'runs':rows}
(O/'R8_01_최종행동_대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'case2':[x['case2'] for x in rows if 'case2' in x],'timing':[x['timing'] for x in rows]},ensure_ascii=True,indent=2))
