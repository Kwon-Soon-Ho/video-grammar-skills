from pathlib import Path
import json,hashlib,importlib.util,copy
HERE=Path(__file__).resolve().parent
W=HERE.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):return [d for k in sorted(a.keys()|b.keys()) for d in (diff(a[k],b[k],p+'/'+k) if k in a and k in b else [{'path':p+'/'+k,'before':a.get(k),'after':b.get(k)}])]
    if isinstance(a,list):return ([{'path':p,'before':a,'after':b}] if len(a)!=len(b) else [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,p+'/'+str(i))])
    return [] if a==b else [{'path':p,'before':a,'after':b}]
for variant in ['new_skill','old_skill']:
    run=W/'iteration-2/eval-02-지정백업_실패와_승인범위'/variant/'run-1';base=run/'inputs/Phase00';before=read(run/'fixture_before.json')['files']
    inventory={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    active=base/'작업초안/디자인적용_초안.json';original=read(active);backup=base/'backup/사용자지정백업'
    report={'variant':variant,'fixture_count':len(before),'changed_files':[k for k in before if inventory.get(k)!=before[k]],'added_files':[k for k in inventory if k not in before],'missing_files':[k for k in before if k not in inventory],
      'active_sha256':sha(active),'active_version':original['version'],'backup_is_regular_file':backup.is_file(),'backup_sha256':sha(backup),'backup_matches_fixture':sha(backup)==before['backup/사용자지정백업']}
    candidate_path=run/('outputs/디자인적용_미반영수정안_v0.1.1.json' if variant=='new_skill' else 'outputs/디자인적용_초안_v0.1.1_미적용수정안.json');candidate=read(candidate_path)
    report['proposal_representation']='full_candidate';report['candidate_sha256']=sha(candidate_path)
    if variant=='old_skill':
        proposal=read(run/'outputs/변경안.json');patch_candidate=copy.deepcopy(original)
        assert proposal['base_sha256']==sha(active)
        for op in proposal['operations']:
            assert op['op']=='replace';patch_candidate[op['path'].removeprefix('/')]=op['value']
        report['patch_matches_full_candidate']=patch_candidate==candidate
    report['candidate_json_diff']=diff(original,candidate)
    assert [x['path'] for x in report['candidate_json_diff']]==['/purpose','/version']
    assert candidate['purpose']=='삼안 강조색 후보를 비교하는 검토용 초안.' and candidate['version']=='0.1.1'
    p=base/'07_실행도구/R5_디자인적용검사.py';s=importlib.util.spec_from_file_location('case2_readonly_'+variant,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    report['independent_active_check']=m.inspect(original,base=base);report['independent_proposal_check']=m.inspect(candidate,base=base)
    reply=base/'05_출처와검토/검수와사용범위/사람답변원문/2026-10-15_8회사CI_최신자료와산하AI부재.json'
    report['reply_sha256']=sha(reply);report['reply_actual_data']=read(reply)
    report['inspection_did_not_change_inputs']=inventory=={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    report['output_files']=[p.relative_to(run).as_posix() for p in (run/'outputs').rglob('*') if p.is_file()]
    (HERE/('steward_iteration2_case2_'+variant+'_observation.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(variant,json.dumps({k:v for k,v in report.items() if not k.startswith('independent_') and k not in ['reply_actual_data','output_files']},ensure_ascii=False))
    print('checks',report['independent_active_check']['valid'],report['independent_proposal_check']['valid'])
