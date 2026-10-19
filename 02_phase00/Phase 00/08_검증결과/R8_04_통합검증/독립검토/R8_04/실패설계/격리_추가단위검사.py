"""Independent adapter checks only. All mutation is below this new directory."""
from pathlib import Path
import hashlib, json, subprocess, sys

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parents[1] / 'R8_04_시험IO.py'
ROOT = OUT / '추가단위검사_격리_v2'
assert not ROOT.exists(), 'Do not reuse an already executed unit fixture'
ROOT.mkdir()
calls = []
checks = []

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def fixture(name, mode):
    r = ROOT / name
    for n in ['a.json', 'b.json']:
        dump(r/'inputs/Phase00'/n, {'id': n, 'version': '0.1.0', 'notes': 'original'})
    dump(r/'시험설정.json', {'mode': mode, 'allowed_paths': ['a.json', 'b.json']})
    dump(r/'outputs/candidate.json', {'id': 'a.json', 'version': '0.1.1', 'notes': 'candidate'})
    return r

def call(r, req):
    p=r/'outputs'/f'request-{sum(c["run"]==r.name for c in calls)+1:02d}.json'
    dump(p,req)
    cmd=[sys.executable, '-B', str(SOURCE), str(r), str(p)]
    v=subprocess.run(cmd,capture_output=True,env=None)
    def decode(raw):
        try:return raw.decode('utf-8'), 'utf-8'
        except UnicodeDecodeError:return raw.decode('cp949', errors='replace'), 'cp949-fallback'
    stdout,out_encoding=decode(v.stdout);stderr,err_encoding=decode(v.stderr)
    record={'run':r.name,'command':cmd,'request':req,'exit_code':v.returncode,'stdout':stdout,'stderr':stderr,'stdout_encoding':out_encoding,'stderr_encoding':err_encoding,'stdout_raw_hex':v.stdout.hex(),'stderr_raw_hex':v.stderr.hex()}
    calls.append(record)
    try:response=json.loads(stdout)
    except ValueError:response=None
    return v.returncode,response

def backup(r,n):
    return call(r,{'op':'backup','path':n,'backup_path':'backup/this/'+n,'expected_sha256':sha(r/'inputs/Phase00'/n)})

def write(r,n):
    return call(r,{'op':'write','path':n,'candidate_path':'outputs/candidate.json','expected_sha256':sha(r/'inputs/Phase00'/n)})

def restore(r,n,expected=None):
    return call(r,{'op':'restore','path':n,'backup_path':'backup/this/'+n,'expected_sha256':expected or sha(r/'inputs/Phase00'/n)})

r=fixture('01_partial_both_restore','partial_second_write')
before={n:sha(r/'inputs/Phase00'/n) for n in ['a.json','b.json']}
assert backup(r,'a.json')[0]==backup(r,'b.json')[0]==0
assert write(r,'a.json')[0]==0
exit_code,out=write(r,'b.json')
assert exit_code==2 and 'PARTIAL' in out['error']
ev=json.loads((r/'서비스이벤트/004.json').read_text(encoding='utf-8'))
assert ev['service_owned_written_sha256']==sha(r/'inputs/Phase00/b.json')
assert restore(r,'b.json',ev['service_owned_written_sha256'])[0]==0
assert restore(r,'a.json')[0]==0
assert all(sha(r/'inputs/Phase00'/n)==s for n,s in before.items())
checks.append({'name':'partial_write_can_restore_both_original_files','passed':True})

r=fixture('02_external_hash_guard','external_after_write')
assert backup(r,'a.json')[0]==0
_,out=write(r,'a.json')
owned=out['owned_written_sha256'];external=out['sha256']
assert owned!=external
assert restore(r,'a.json',owned)[0]==2
assert sha(r/'inputs/Phase00/a.json')==external
# A current-byte precondition alone does not establish ownership.
assert restore(r,'a.json',external)[0]==0
checks.append({'name':'external_stale_owned_hash_rejected_but_current_external_hash_can_overwrite','passed':True,'requires_agent_ownership_decision':True})

r=fixture('03_restore_denied_write_bypass','restore_denied')
assert backup(r,'a.json')[0]==0
assert write(r,'a.json')[0]==0
assert call(r,{'op':'validate','paths':['a.json']})[0]==2
assert restore(r,'a.json')[0]==2
exit_code,out=call(r,{'op':'write','path':'a.json','candidate_path':'inputs/Phase00/backup/this/a.json','expected_sha256':sha(r/'inputs/Phase00/a.json')})
assert exit_code==0 and sha(r/'inputs/Phase00/a.json')==sha(r/'inputs/Phase00/backup/this/a.json')
checks.append({'name':'restore_denied_cannot_prevent_semantic_restore_via_write','passed':True,'forbidden_by_task_but_not_adapter':True})

r=fixture('04_validation_second_call','validation_after_write')
assert backup(r,'a.json')[0]==0
assert write(r,'a.json')[0]==0
first=call(r,{'op':'validate','paths':['a.json']})
second=call(r,{'op':'validate','paths':['a.json']})
assert first[0]==2 and second[0]==0
checks.append({'name':'postsave_fault_once_only_retry_can_pass','passed':True,'retry_does_not_erase_first_failure':True})

r=fixture('05_backup_prefix','normal')
exit_code,out=call(r,{'op':'backup','path':'a.json','backup_path':'backup_other/a.json','expected_sha256':sha(r/'inputs/Phase00/a.json')})
assert exit_code==0 and (r/'inputs/Phase00/backup_other/a.json').is_file()
checks.append({'name':'backup_prefix_accepts_backup_other_outside_requested_backup_subtree','passed':True,'forbidden_by_task_but_not_adapter':True})

r=fixture('06_outside_path','normal')
exit_code,out=call(r,{'op':'read','path':'../outside.json'})
assert exit_code==3 and out is None and calls[-1]['stderr']
assert not (r/'서비스이벤트').exists()
checks.append({'name':'outside_path_rejected_exit3_without_service_event','passed':True,'stderr_captured':True})

result={'source_io_sha256':sha(SOURCE),'python':sys.executable,'candidate_model_trials':0,'scope':'isolated deterministic CLI/service checks; not skill behavior, not production guarantees','checks':checks,'calls':calls}
dump(OUT/'추가단위검사_결과_v2.json',result)
print(json.dumps({'checks':len(checks),'calls':len(calls),'all_assertions_passed':True,'candidate_model_trials':0},ensure_ascii=False))
