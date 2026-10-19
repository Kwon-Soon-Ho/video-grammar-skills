"""C-only unit probes. Publisher main/prepare/sources are never called."""
from pathlib import Path
import ast,hashlib,importlib.util,json,sys
O=Path(__file__).resolve().parent;L=O.parents[2];sys.path.insert(0,str(L));P=L/'R8_04_최종게시.py';text=P.read_text(encoding='utf-8');script_sha=hashlib.sha256(P.read_bytes()).hexdigest()
s=importlib.util.spec_from_file_location('publish_synthetic_v2',P);p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
R=O/'합성_최종집합';assert not R.exists();R.mkdir(parents=True)
def guard(q):
 q=q.resolve();assert q.is_relative_to(R.resolve());return q
def serial(v):return ((json.dumps(v,ensure_ascii=False,indent=2)+'\n') if not isinstance(v,str) else (v.strip()+'\n')).encode('utf-8')
def save(rel,v,stage):q=guard(R/rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(serial(v))
p.BASE=R;p.L=R;p.safe=guard;p.base_save=save;p.OWN.clear();p.ATTEMPTS.clear();p.CTX.clear();results=[]
def record(name,passed,**detail):results.append({'name':name,'passed':bool(passed),**detail})
def refused(fn):
 try:fn();return False,None
 except Exception as e:return True,type(e).__name__+': '+str(e)
src=R/'source.txt';src.write_bytes(b'frozen');h=p.sha(src)
record('longprefix_idempotent',p.io(p.io(src))==p.io(src) and p.sha(p.io(src))==h)
src.write_bytes(b'changed-after-freeze');archive={};bad,error=refused(lambda:p.exact(src,'archive/source.txt',archive,h));record('exact_rejects_postfreeze_changed_source',bad and not (R/'archive/source.txt').exists(),error=error)
src.write_bytes(b'frozen');p.exact(src,'archive/source.txt',archive,h);record('exact_frozen_copy',p.sha(R/'archive/source.txt')==h)
deep=R/('긴경로'*10)/('검증'*15)/('합성'*15)/('중간'*15)/('추가'*20)/('연결'*20)/'원문.txt';p.io(deep.parent).mkdir(parents=True,exist_ok=True);p.io(deep).write_bytes(b'long path');p.exact(deep,'archive/long.txt',archive,p.sha(deep));record('long_path_exact_copy',len(str(deep))>260 and p.sha(R/'archive/long.txt')==p.sha(deep),source_path_length=len(str(deep)))
target=p.OUT+'/00_최종보고.md';marker=p.OUT+'/게시상태.json';p.CTX.update({'freeze':{'D_before':{target:None,marker:None}},'started':True,'archive':{}});p.owned(marker,{'publication_state':'in_progress'})
def partial(rel,v,stage):
 if rel==target:
  q=guard(R/rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b'PARTIAL');raise OSError('synthetic partial write')
 save(rel,v,stage)
p.base_save=partial
try:p.owned(target,'new report')
except OSError as e:p.record_failure(e)
failure=json.loads((R/marker).read_text(encoding='utf-8'));entry=failure['partial_owned_files'].get(target)
record('partial_failure_journaled_without_overwrite',entry is not None and entry['attempt']['completed'] is False and entry['actual']==p.sha(R/target) and (R/target).read_bytes()==b'PARTIAL' and failure['publication_state']=='failed')
p.base_save=save;p.OWN.clear();p.ATTEMPTS.clear();bad,error=refused(lambda:p.owned(marker,{'publication_state':'in_progress'}));record('same_freeze_retry_refuses_partial_publication',bad,error=error)

# Extract only the nested read/assert function; no main body, processes or D paths execute.
tree=ast.parse(text);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');func=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='final_integrity')
reviewed=R/'read/봉인보고.md';reviewed.parent.mkdir(parents=True,exist_ok=True);reviewed.write_bytes(b'sealed');report=R/'pub/report.md';report.parent.mkdir(parents=True,exist_ok=True);report.write_bytes(b'published')
freeze=R/'synthetic_freeze.json';freeze.write_bytes(b'freeze');ctx=R/p.F/'현재후보_입력고정.json';ctx.parent.mkdir(parents=True,exist_ok=True);ctx.write_text('{"files":{}}',encoding='utf-8')
f={'source_files':[{'source':str(src),'sha256':p.sha(src)}],'candidate_hashes':{},'D_read_snapshot':{'read/봉인보고.md':p.sha(reviewed),'read/absent.json':None}}
ns={'BASE':R,'OWN':{'pub/report.md':p.sha(report)},'sha':p.sha,'current':p.current,'read':p.read,'f':f,'FREEZE':freeze,'audit':{'freeze_sha256':p.sha(freeze)},'judgment_hashes':{},'F':p.F,'init':{'read/봉인보고.md':p.sha(reviewed)},'allowed':{'read/봉인보고.md'},'archive':{},'Path':Path}
exec(compile(ast.fix_missing_locations(ast.Module(body=[func],type_ignores=[])),'<read-only final_integrity>','exec'),ns)
bad,error=refused(ns['final_integrity']);record('final_integrity_baseline_with_absent_snapshot',not bad,error=error)
for label,q,new in [('owned_report',report,b'external report'),('C_source',src,b'external source'),('allowed_sealed_report',reviewed,b'external sealed')]:
 old=q.read_bytes();q.write_bytes(new);bad,error=refused(ns['final_integrity']);record('final_integrity_rejects_'+label,bad and error.startswith('AssertionError:'),error=error);q.write_bytes(old)
absent=R/'read/absent.json';absent.write_bytes(b'new');bad,error=refused(ns['final_integrity']);record('final_integrity_rejects_absent_new_file',bad and error.startswith('AssertionError:'),error=error)
absent.unlink();extra=R/'06_맞춤스킬/재구성후보/unreviewed/extra.txt';extra.parent.mkdir(parents=True,exist_ok=True);extra.write_bytes(b'unreviewed')
bad,error=refused(ns['final_integrity']);record('final_integrity_rejects_added_candidate_file',bad and 'Candidate file set changed' in error,error=error)
out={'publication_script_sha256':script_sha,'script_unchanged_during_probes':hashlib.sha256(P.read_bytes()).hexdigest()==script_sha,'scope':'synthetic helper sequences only; no publisher main/prepare/sources; D untouched; model trials0','cases':results}
(O/'04_후보최종집합_합성재확인.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
