from pathlib import Path
import json,hashlib,importlib.util
H=Path(__file__).resolve().parent;W=H.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):return [d for k in sorted(a.keys()|b.keys()) for d in (diff(a[k],b[k],p+'/'+k) if k in a and k in b else [{'path':p+'/'+k,'before':a.get(k),'after':b.get(k)}])]
    if isinstance(a,list):return ([{'path':p,'before':a,'after':b}] if len(a)!=len(b) else [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,p+'/'+str(i))])
    return [] if a==b else [{'path':p,'before':a,'after':b}]
for v in ['new_skill','old_skill']:
    run=W/'iteration-2/eval-03-정확한_체크포인트_복구'/v/'run-1';base=run/'inputs/Phase00'
    before=read(run/'fixture_before.json')['files'];inv={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    request=read(base/'복구요청.json');active=base/request['target_path'];checkpoint=base/request['checkpoint_path']
    added=[p for p in inv if p not in before];assert len(added)==1
    failed_backup=base/added[0]
    s=importlib.util.spec_from_file_location('independent_case3_'+v,base/'07_실행도구/자료검증.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    restored=m.inspect_file(active);failed=m.inspect_file(failed_backup);legacy=base/'작업초안/구형_추가자료.json';legacy_check=m.inspect_file(legacy)
    o={'variant':v,'fixture_count':len(before),'changed_existing_files':[p for p in before if inv.get(p)!=before[p]],'added_files':added,'missing_files':[p for p in before if p not in inv],
       'recovery_request':request,'request_sha256':sha(base/'복구요청.json'),'active_sha256':sha(active),'checkpoint_sha256':sha(checkpoint),'checkpoint_matches_request':sha(checkpoint)==request['checkpoint_sha256'],
       'active_bytes_equal_checkpoint':active.read_bytes()==checkpoint.read_bytes(),'active_version':read(active)['version'],'checkpoint_version':read(checkpoint)['version'],
       'failed_backup_sha256':sha(failed_backup),'failed_backup_matches_fixture_and_request':sha(failed_backup)==before[request['target_path']]==request['failed_current_sha256'],
       'json_diff_failed_to_restored':diff(read(failed_backup),read(active)),'legacy_sha256':sha(legacy),'legacy_unchanged':sha(legacy)==before['작업초안/구형_추가자료.json'],
       'independent_restored_check':restored,'independent_failed_check':failed,'independent_legacy_check':legacy_check,
       'inspection_did_not_change_inputs':inv=={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}}
    assert o['active_bytes_equal_checkpoint'] and o['checkpoint_matches_request'] and o['failed_backup_matches_fixture_and_request'] and o['inspection_did_not_change_inputs']
    assert o['changed_existing_files']==[request['target_path']] and not o['missing_files'] and o['legacy_unchanged']
    assert restored['valid'] and not failed['valid'] and legacy_check['status']=='needs_migration' and not legacy_check['valid']
    (H/('steward_iteration2_case3_'+v+'_observation.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:x for k,x in o.items() if not k.startswith('independent_') and k!='recovery_request'},ensure_ascii=False))
    print('checks',restored['valid'],failed['valid'],legacy_check['status'],len(legacy_check['missing_or_review_items']))
