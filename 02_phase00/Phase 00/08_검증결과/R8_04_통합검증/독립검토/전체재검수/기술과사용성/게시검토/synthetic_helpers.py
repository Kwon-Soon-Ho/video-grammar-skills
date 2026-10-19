"""Synthetic helper probes only. Never call publisher main/prepare/sources."""
from pathlib import Path
import importlib.util,sys,json,hashlib,shutil
O=Path(__file__).resolve().parent;L=O.parents[2];sys.path.insert(0,str(L));P=L/'R8_04_최종게시.py'
spec=importlib.util.spec_from_file_location('publication_helper_synthetic',P);pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
R=O/'synthetic';assert not R.exists();R.mkdir(parents=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2) if not isinstance(obj,str) else obj,encoding='utf-8')
def guard(p):
 p=p.resolve();assert p.is_relative_to(R.resolve());return p
pub.BASE=R;pub.L=R;pub.safe=guard
def save(rel,v,stage):write(guard(R/rel),v)
pub.base_save=save
results=[]
# Caller performed freeze precheck, then source changed before exact-copy helper.
src=R/'source.txt';src.write_bytes(b'frozen');expected=sha(src);assert sha(src)==expected;src.write_bytes(b'later content');archives={};pub.exact(src,'archive/source.txt',archives)
results.append({'name':'source_changes_after_freeze_precheck','frozen_sha256':expected,'copied_sha256':sha(R/'archive/source.txt'),'archive_matches_freeze':sha(R/'archive/source.txt')==expected,'copy_was_accepted':True})
# The original path API precheck does not reject a caller's postcheck external modification.
pub.OWN.clear();target=pub.OUT+'/00_최종보고.md';marker=pub.OUT+'/게시상태.json';pub.CTX.clear();pub.CTX.update({'freeze':{'D_before':{target:None,marker:None}},'started':True,'archive':{}})
pub.owned(marker,{'publication_state':'in_progress'})
def partial(rel,v,stage):
 if rel==target:
  p=guard(R/rel);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'PARTIAL');raise OSError('synthetic write failed after bytes')
 save(rel,v,stage)
pub.base_save=partial
try:pub.owned(target,'reviewed report')
except OSError as e:pub.record_failure(e)
failed=json.loads((R/marker).read_text(encoding='utf-8'))
results.append({'name':'partial_write_is_not_journaled_as_owned','target_partial_bytes_preserved':(R/target).read_bytes()==b'PARTIAL','failed_target_in_OWN':target in pub.OWN,'failed_target_in_failure_detail':target in failed['partial_owned_files'],'marker_state':failed['publication_state']})
# Restart with original freeze reproduces fail-stop; no implicit safe resume exists.
pub.base_save=save;pub.OWN.clear()
try:pub.owned(marker,{'publication_state':'in_progress'});error=None
except Exception as e:error=type(e).__name__+': '+str(e)
results.append({'name':'retry_original_freeze_after_failure','refused':error is not None,'error':error})
# Existing owned report can change after its one-time check and be accepted by later receipt calculation.
pub.OWN.clear();p=R/'another/report.md';pub.CTX['freeze']={'D_before':{'another/report.md':None,'another/receipt.json':None,'another/marker.json':None}};pub.owned('another/report.md','reviewed');own=pub.OWN['another/report.md'];p.write_bytes(b'external modification')
pub.owned('another/receipt.json',{'report_sha256':pub.sha(p)})
pub.owned('another/marker.json',{'publication_state':'complete','receipt_sha256':pub.sha(R/'another/receipt.json')})
results.append({'name':'external_owned_report_change_before_complete','owned_report_hash':own,'actual_report_hash':pub.sha(p),'receipt_contains_external_hash':json.loads((R/'another/receipt.json').read_text())['report_sha256']==pub.sha(p),'marker_complete':json.loads((R/'another/marker.json').read_text())['publication_state']=='complete'})
out={'publication_script_sha256':sha(P),'scope':'four helper call sequences in synthetic C root only; original main/prepare/sources never invoked; no D mutation; not model/behavior trial evidence','results':results}
write(O/'01_합성보조함수_확인.json',out)
print(json.dumps(out,ensure_ascii=False,indent=2))
