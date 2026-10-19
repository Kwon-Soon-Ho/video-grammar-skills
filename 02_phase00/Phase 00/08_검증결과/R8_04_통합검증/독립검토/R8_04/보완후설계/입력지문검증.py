from pathlib import Path
import json,hashlib,datetime,re
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1];W=BASE/'R8_04_시험'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=read(W/'4_실행전기대항목.json');freeze=read(W/'4_고정기록.json')
allruns=[];unique_skills={};issues=[]
for n,c in e['cases'].items():
 r=Path(c['run']);db=r/'inputs/Phase00'
 files={p.relative_to(db).as_posix():sha(p) for p in db.rglob('*') if p.is_file()}
 fixture=read(r/'fixture_before.json')
 checks={k:sha(r/p)==c[k] for k,p in [('task_sha256','task.txt'),('config_sha256','시험설정.json'),('io_sha256','시험IO.py')]}
 skillroot=db/'실행스킬'/c['skill']
 skill_actual={p.relative_to(skillroot).as_posix():sha(p) for p in skillroot.rglob('*') if p.is_file()}
 skills_match=skill_actual==c['skill_hashes']
 for p,h in skill_actual.items():
  key=c['skill']+'/'+p
  assert key not in unique_skills or unique_skills[key]==h
  unique_skills[key]=h
 config=read(r/'시험설정.json')
 assert config['mode']==c['mode'] and config['allowed_paths']==c['allowed']
 main=(skillroot/'SKILL.md').read_text(encoding='utf-8')
 version=re.search(r'version: "([^"]+)"',main).group(1)
 prohibited=[];scores=[]
 for p in db.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(db).as_posix()
  if any(x in rel.split('/') for x in ['evals','평가계획','08_검증결과','06_맞춤스킬']):prohibited.append(rel)
  if p.suffix in ['.md','.json','.txt'] and any(x in p.read_text(encoding='utf-8-sig') for x in ['11/12','8/8']):scores.append(rel)
 local_corrections=[]
 for rec in read(db/'14_스킬재구성/현재상태_정정표.json')['records']:
  refs=[rec['source']]+rec['basis']
  local_corrections.append({'id':rec['id'],'refs':[{'path':x['path'],'exists':(db/x['path']).is_file(),'hash_matches':sha(db/x['path'])==x['sha256'] if (db/x['path']).is_file() else None} for x in refs]})
 row={'case':n,'mode':c['mode'],'classification':c['classification'],'version':version,'run':str(r),'metadata_matches':checks,'skill_hashes_match':skills_match,'fixture_hash':sha(r/'fixture_before.json'),'fixture_map_matches_actual':fixture==files,'file_count':len(files),'prohibited_file_names':prohibited,'historical_score_matches':scores,'local_correction_references':local_corrections,'input_hashes':files}
 if not all(checks.values()) or not skills_match or fixture!=files or prohibited or scores:issues.append(n)
 allruns.append(row)
old_helpers=[BASE/'R8_04_시험IO.py']+list((W/'2_실제쓰기').glob('*/candidate/시험IO.py'))
result={'recorded_at':datetime.datetime.now().astimezone().isoformat(),'expectations_sha256':sha(W/'4_실행전기대항목.json'),'expectations_matches_freeze':sha(W/'4_실행전기대항목.json')==freeze['expectations_sha256'],'freeze_sha256':sha(W/'4_고정기록.json'),'preparation_sha256':sha(BASE/'R8_04_보완후준비.py'),'new_helper_sha256':sha(BASE/'R8_04_시험IO_보완후.py'),'new_helper_matches_freeze':sha(BASE/'R8_04_시험IO_보완후.py')==freeze['new_helper_sha256'],'old_helper_hashes':{str(p):sha(p) for p in old_helpers},'old_helpers_all_match_original':all(sha(p)=='b2a94872abd17cff5c337ff2feb1a3e4d4e967154013074be5e94290d43729f0' for p in old_helpers),'unique_candidate_skill_hashes':unique_skills,'candidate_model_runs_by_reviewer':0,'candidate_model_runs_declared_at_freeze':freeze['actual_runs_at_freeze'],'global_model_execution_history_independently_read':False,'issues':issues,'runs':allruns}
dump(OUT/'실행전_입력해시검증.json',result)
print(json.dumps({'cases':len(allruns),'input_files':sum(x['file_count'] for x in allruns),'unique_candidate_files':len(unique_skills),'issues':issues,'expectations_sha256':result['expectations_sha256'],'freeze_sha256':result['freeze_sha256'],'new_helper_sha256':result['new_helper_sha256'],'preparation_sha256':result['preparation_sha256'],'old_helpers_unchanged':result['old_helpers_all_match_original']}))
