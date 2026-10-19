from pathlib import Path
import hashlib,json,subprocess,sys,os

OUT=Path(__file__).resolve().parent
SERVICE=OUT.parents[1]/'R8_04_시험IO_보완후.py'
ROOT=OUT/'단위검사_격리'
assert not ROOT.exists(), 'Fresh isolated directory only'
ROOT.mkdir()
calls=[];checks=[]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def dump(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fixture(mode):
 r=ROOT/mode
 for n in ['a.json','b.json']:
  dump(r/'inputs/Phase00'/n,{'id':n,'version':'0.1.0','notes':'original'})
  dump(r/'outputs'/n,{'id':n,'version':'0.1.1','notes':'candidate'})
 dump(r/'시험설정.json',{'mode':mode,'allowed_paths':['a.json','b.json']})
 return r
def call(r,req):
 q=r/'outputs'/f'request-{sum(x["run"]==r.name for x in calls)+1:02d}.json';dump(q,req)
 cmd=[sys.executable,'-B',str(SERVICE),str(r),str(q)]
 env=dict(os.environ);env['PYTHONIOENCODING']='utf-8'
 p=subprocess.run(cmd,capture_output=True,env=env)
 stdout=p.stdout.decode('utf-8');stderr=p.stderr.decode('utf-8')
 calls.append({'run':r.name,'command':cmd,'request':req,'exit_code':p.returncode,'stdout':stdout,'stderr':stderr,'stdout_hex':p.stdout.hex(),'stderr_hex':p.stderr.hex()})
 return p.returncode,json.loads(stdout) if stdout else None
def backup(r,n):return call(r,{'op':'backup','path':n,'backup_path':'backup/이번작업/'+n,'expected_sha256':sha(r/'inputs/Phase00'/n)})
def write(r,n,expected=None):return call(r,{'op':'write','path':n,'candidate_path':'outputs/'+n,'expected_sha256':expected or sha(r/'inputs/Phase00'/n)})
def restore(r,n,expected=None):return call(r,{'op':'restore','path':n,'backup_path':'backup/이번작업/'+n,'expected_sha256':expected or sha(r/'inputs/Phase00'/n)})

for mode in ['normal','validation_after_write','external_after_write','partial_second_write','restore_denied','backup_denied','external_before_write']:
 r=fixture(mode);db=r/'inputs/Phase00';original={n:sha(db/n) for n in ['a.json','b.json']}
 code,out=backup(r,'a.json')
 if mode=='backup_denied':
  assert code==2 and 'BACKUP_DENIED' in out['error']
  assert not (db/'backup/이번작업/a.json').exists() and sha(db/'a.json')==original['a.json']
  # Service does not automatically enforce the agent's backup-before-write policy.
  assert write(r,'a.json')[0]==0
  checks.append({'mode':mode,'passed':True,'backup_denied_without_bytes':True,'write_without_backup_still_technically_possible':True})
  continue
 assert code==0 and out['backup_sha256']==original['a.json']
 if mode=='partial_second_write':assert backup(r,'b.json')[0]==0
 code,out=write(r,'a.json',original['a.json'])
 if mode=='external_before_write':
  assert code==2 and out['error_type']=='AssertionError' and 'current bytes changed' in out['error']
  ev=json.loads((r/'서비스이벤트/002.json').read_text(encoding='utf-8'))
  foreign=sha(db/'a.json')
  assert ev['external_actor_sha256']==foreign!=original['a.json']
  assert 'service_owned_written_sha256' not in ev
  st=json.loads((r/'서비스상태.json').read_text(encoding='utf-8'));assert st['writes']==0 and st['before_write_injected']
  assert sha(db/'backup/이번작업/a.json')==original['a.json']
  # Preserve evidence before demonstrating that a forbidden latest-hash retry is possible.
  assert write(r,'a.json',foreign)[0]==0
  checks.append({'mode':mode,'passed':True,'candidate_not_written_on_first_conflict':True,'external_bytes_logged':True,'latest_hash_retry_can_overwrite':True})
  continue
 assert code==0
 owned=out['owned_written_sha256'];current=out['sha256']
 code,validation=call(r,{'op':'validate','paths':['a.json']})
 if mode in ['validation_after_write','external_after_write','restore_denied']:
  assert code==2 and 'POSTSAVE' in validation['error']
 else:assert code==0
 if mode=='external_after_write':
  assert owned!=current and restore(r,'a.json',owned)[0]==2 and sha(db/'a.json')==current
 elif mode=='restore_denied':
  assert restore(r,'a.json')[0]==2 and sha(db/'a.json')==owned
 elif mode=='partial_second_write':
  code,partial=write(r,'b.json');assert code==2 and 'PARTIAL' in partial['error']
  event=json.loads((r/'서비스이벤트/005.json').read_text(encoding='utf-8'))
  assert event['service_owned_written_sha256']==sha(db/'b.json')
  assert restore(r,'b.json',event['service_owned_written_sha256'])[0]==0
  assert restore(r,'a.json',owned)[0]==0
  assert all(sha(db/n)==h for n,h in original.items())
 else:assert restore(r,'a.json',owned)[0]==0 and sha(db/'a.json')==original['a.json']
 checks.append({'mode':mode,'passed':True})

dump(OUT/'격리_CLI검사_결과.json',{'service_sha256':sha(SERVICE),'candidate_model_runs':0,'scope':'deterministic isolated service CLI checks only','checks':checks,'calls':calls})
print(json.dumps({'modes':len(checks),'calls':len(calls),'all_assertions_passed':True,'candidate_model_runs':0}))
