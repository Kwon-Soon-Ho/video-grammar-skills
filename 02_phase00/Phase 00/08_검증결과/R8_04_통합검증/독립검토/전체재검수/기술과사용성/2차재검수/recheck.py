from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,subprocess,re
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
L=Path(r'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build')
O=Path(__file__).resolve().parent;PY=D/'.환경/Scripts/python.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snap(b):return {p.relative_to(b).as_posix():sha(p) for p in b.rglob('*') if p.is_file()}
past=read(O.parent/'07_R8게시영수증_현재성감사.json');first=read(D/'08_검증결과/R8_04_통합검증/1차보완_확인.json');second=read(D/'08_검증결과/R8_04_통합검증/2차보완_확인.json')
sealed=[]
for row,fix in zip(past,first['sealed_reports']):
 current=D/row['report_path'];receipt=D/row['receipt_path'];side=D/fix['current_sidecar'];preserved=D/fix['append_version_preserved'];expected=row['receipt_report_fields'][0]['value']
 sealed.append({'stage':row['stage'],'report_matches_original_receipt':sha(current)==expected,'receipt_unchanged':sha(receipt)==row['current_receipt_sha256'],'append_preserved_exactly':sha(preserved)==row['current_report_sha256'],'sidecar_exists':side.is_file(),'sidecar_has_actual_feedback_link':'검토답변.json)' in side.read_text(encoding='utf-8'),'original_bytes_prefix':preserved.read_bytes().startswith(current.read_bytes()),'sidecar_sha256':sha(side)})
marker=read(D/'08_검증결과/R8_03_적용성검토자/게시상태.json');marker_ok=marker['receipt_sha256']==sha(D/marker['receipt_path'])
errata=read(D/'14_스킬재구성/현재상태_정정표.json');refs=[]
for row in errata['records']:
 for ref in [row['source']]+row['basis']:refs.append({'id':row['id'],'path':ref['path'],'match':sha(D/ref['path'])==ref['sha256']})
historical=read(O.parent/'01_격리와도구안전.json')['C_sha256_map'];original_c=L/'R8_04_시험/고정문맥_검증전용/Phase00';original_c_ok=snap(original_c)==historical
r7rel='13_품질검수/연결과인계/현재연결_입력고정.json';r6rel='05_출처와검토/검수와사용범위/통합검수_입력고정.json';manifest=read(D/r7rel)
pins=[]
for p in manifest['pins']:pins.append({'path':p['path'],'current_matches_pin':sha(D/p['path'])==p['sha256'],'original_C_matches_D':sha(original_c/p['path'])==sha(D/p['path'])})
aliases=read(D/'05_출처와검토/검수와사용범위/원문경로_복구연결.json')['aliases'];recovery=[]
for a in aliases:
 p=Path(a['old_record_path']);q=D/a['preserved_snapshot'];host=Path(a['current_equal_bytes_path']);recovery.append({'old_path':str(p),'old_present':p.is_file(),'snapshot_matches':sha(q)==a['expected_sha256']==a['snapshot_sha256'],'current_host_present':host.is_file(),'current_host_matches':sha(host)==a['expected_sha256'] if host.is_file() else None,'approval':a['redistribution_permission_verified'],'activated':a['activated_as_skill']})
changes={x['path']:x for x in first['changes']+second['changes']};change_checks=[{'path':p,'matches_latest_after':sha(D/p)==r['after']} for p,r in changes.items()]
write(O/'01_문서보완_직접대조.json',{'sealed_reports':sealed,'R8_3_marker_receipt_exact':marker_ok,'latest_changed_hashes':change_checks,'errata_source_basis':refs,'original_C800_unchanged':original_c_ok,'R7_manifest_unchanged':sha(D/r7rel)==historical[r7rel],'R6_manifest_unchanged':sha(D/r6rel)==historical[r6rel],'R7_pin_count':len(pins),'R7_pins':pins,'R6_recovery':recovery,'D_new_helper_present':(D/'07_실행도구/R8_후보연결확인.py').exists()})
print('document evidence saved',len(pins),flush=True)

# Existing source tools were inspected previously. Recheck their exact bytes before read-only live checks.
runs=[]
for tool in ['R6_출처사용검사.py','R6_사람검수.py','R6_통합조회.py','R7_연결확인.py']:
 rel='07_실행도구/'+tool;assert sha(D/rel)==historical[rel]
 p=subprocess.run([str(PY),'-B','-X','utf8',str(D/rel),'--base',str(D)],cwd=O,capture_output=True,text=True,encoding='utf-8',timeout=90)
 runs.append({'tool':tool,'base':str(D),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'writes_requested':False});print(tool,p.returncode,flush=True)
write(O/'02_영향현재성_실재실행.json',{'runs':runs,'note':'source D read-only with exact tool bytes, -B. Original287 regressions not rerun or recounted. No R8 behavior output opened.'})

P=L/'R8_후보연결확인.py';spec=importlib.util.spec_from_file_location('candidate_checker_independent',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
source=L/'R8_04_독립검토/후보문맥_자체검사_v2/정상/Phase00';before=snap(source);W=O/'isolated';assert not W.exists();base=W/'baseline/Phase00';shutil.copytree(source,base);c=read(base/m.CONTEXT);out=[]
def save_repin(root,rel,data):
 write(root/rel,data);ctx=read(root/m.CONTEXT);ctx['files'][rel]=sha(root/rel);write(root/m.CONTEXT,ctx)
def case(name,expected,mutate=None):
 root=base if mutate is None else W/name/'Phase00'
 if mutate is not None:shutil.copytree(base,root);mutate(root)
 prior=snap(root)
 try:r=m.inspect(root);got=r['valid'];exc=None
 except Exception as e:r=None;got=None;exc=repr(e)
 out.append({'name':name,'expected_valid':expected,'actual_valid':got,'expectation_met':got==expected,'result':r,'exception':exc,'input_unchanged':prior==snap(root)})
def alter_errata(root,fn):
 e=read(root/m.EXTRA[0]);fn(e);save_repin(root,m.EXTRA[0],e)
def alter_receipt(root,fn):
 e=read(root/m.EXTRA[3]);fn(e);save_repin(root,m.EXTRA[3],e)
def dup(root):
 p=root/m.CONTEXT;t=p.read_text(encoding='utf-8');p.write_text(t.replace('{','{"version":"9.9.9",',1),encoding='utf-8')
def nan(root):
 p=root/m.CONTEXT;t=p.read_text(encoding='utf-8');p.write_text(t.replace('"candidate_only": true','"candidate_only": NaN'),encoding='utf-8')
def oldpin(root):
 rel=next(iter(m.FOUNDATION));save_repin(root,rel,{'changed':True})
case('normal',True)
case('source_file_missing',False,lambda r:(r/read(r/m.EXTRA[0])['records'][0]['source']['path']).unlink())
case('basis_file_missing',False,lambda r:(r/read(r/m.EXTRA[0])['records'][0]['basis'][0]['path']).unlink())
case('source_ref_missing_after_repin',False,lambda r:alter_errata(r,lambda e:e['records'][0].pop('source')))
case('empty_basis_after_repin',False,lambda r:alter_errata(r,lambda e:e['records'][0].update(basis=[])))
case('source_hash_mismatch_after_repin',False,lambda r:alter_errata(r,lambda e:e['records'][0]['source'].update(sha256='0'*64)))
case('basis_hash_mismatch_after_repin',False,lambda r:alter_errata(r,lambda e:e['records'][0]['basis'][0].update(sha256='0'*64)))
case('other_receipt_foundation_after_repin',False,lambda r:alter_receipt(r,lambda e:e.update(copy_R7_manifest_sha256='0'*64)))
case('other_receipt_inventory_after_repin',False,lambda r:alter_receipt(r,lambda e:e.update(inventory_sha256='0'*64)))
case('historical_pin_replaced_and_repinned',False,oldpin)
case('duplicate_json',False,dup)
case('NaN_json',False,nan)
case('candidate_adopted',False,lambda r:write(r/m.CONTEXT,{**c,'candidate_adopted':True}))
case('company_approval_context',False,lambda r:write(r/m.CONTEXT,{**c,'company_approved':True}))
case('restricted_permission_after_repin',False,lambda r:save_repin(r,m.EXTRA[2],{**read(r/m.EXTRA[2]),'permission_granted':True}))
case('receipt_claims_performer_full_after_repin',False,lambda r:alter_receipt(r,lambda e:e.update(behavior_performer_read_full_copy=True)))
# Additional publication guards beyond the author's12. These are not skill/model trials.
case('empty_all_errata_records_after_repin',False,lambda r:alter_errata(r,lambda e:e.update(records=[])))
case('errata_company_approval_after_repin',False,lambda r:alter_errata(r,lambda e:e.update(company_approved=True)))
case('errata_operational_release_after_repin',False,lambda r:alter_errata(r,lambda e:e.update(operational_release=True)))
case('four_duplicate_read_receipts_after_repin',False,lambda r:alter_receipt(r,lambda e:e.update(read_checks=[e['read_checks'][0]]*4)))
case('boolean_exit_code_after_repin',False,lambda r:alter_receipt(r,lambda e:[x.update(exit_code=False) for x in e['read_checks']]))
write(O/'03_새R8검사기_독립반례.json',{'checker_sha256':sha(P),'cases':out,'count':len(out),'expectation_met':sum(x['expectation_met'] for x in out),'source_v2_normal_unchanged':before==snap(source),'model_trials':0,'limits':'Reference checks only; prior receipt declaration, no live R6R7, rights or content verification. Deliberate repin only in new isolated C roots, no D/canonical pin changes.'})
print('independent',len(out),'expected',sum(x['expectation_met'] for x in out),'unexpected',[x['name'] for x in out if not x['expectation_met']],flush=True)
