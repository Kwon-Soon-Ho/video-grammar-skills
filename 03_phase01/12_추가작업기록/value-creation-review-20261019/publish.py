from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil, sys
O=Path(__file__).resolve().parent;R=O.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=(D/'Phase 01-A/02_분석작업/2026-10-19_DB수집범위_원본언어검토').resolve()
assert DEST.is_relative_to(D) and DEST!=D
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def cp(p,q):
 q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert sha(p)==sha(q),'Different existing file: '+str(q)
 else:
  with p.open('rb') as a,q.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(p)==sha(q)
 return {'source':str(p),'destination':str(q),'sha256':sha(q)}
assert read(O/'report-qa.json')['pdf_sha256']==sha(R/'output/pdf/20261019_value_creation_source_language_review.pdf')
assert read(O/'scope-decision.json')['scope_correction']
sys.path.insert(0,str(R/'tools'));from archive_pdf import archive_pdf
items=[
 ('20261019_video_knowledge_purpose_replanning.pdf','01_제출보고서/공통 기획/2026-10-19_목적복원과_스킬적용_재기획','2026-10-19_영상지식DB_목적복원과_스킬적용_재기획검토안.pdf'),
 ('20261019_value_creation_knowledge_and_design_pilot.pdf','01_제출보고서/Phase 01-A/2026-10-19_가치창출_새기록과_화면시범','2026-10-19_가치창출영상_새지식기록과_화면모션시범.pdf'),
 ('20261019_value_creation_source_language_review.pdf','01_제출보고서/Phase 01-A/2026-10-19_DB수집범위_원본언어검토','2026-10-19_DB수집범위_정리와_원본비교기록.pdf')]
pdfs=[archive_pdf(R/'output/pdf'/p,category=c,name=n) for p,c,n in items]
files=[cp(p,DEST/p.name) for p in sorted(O.iterdir()) if p.is_file() and p.suffix in ['.json','.md','.py'] and p.name not in ['publication-receipt.json','publication-status.json']]
receipt={'utc':datetime.now(timezone.utc).isoformat(),'state':'archived_and_hash_verified','pdfs':pdfs,'records':files,'records_destination':str(DEST),'active_skill_changed':False,'canonical_db_changed':False,'older_full_record_dossiers_published':False}
(O/'publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');cp(O/'publication-receipt.json',DEST/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k!='records'},ensure_ascii=False))
