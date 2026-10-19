from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil, sys
O=Path(__file__).resolve().parent;R=O.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=(D/'Phase 01-A/02_분석작업/2026-10-19_가치창출_새기록과_화면시범').resolve()
assert DEST.is_relative_to(D) and DEST!=D
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def copy(p,q):
 q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert sha(p)==sha(q),'different existing file: '+str(q)
 else:
  with p.open('rb') as a,q.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(p)==sha(q)
 return {'source':str(p),'destination':str(q),'sha256':sha(q)}
assert read(O/'validation.json')['passed']
pdf=R/'output/pdf/20261019_value_creation_knowledge_and_design_pilot.pdf'
assert read(O/'report-qa.json')['pdf_sha256']==sha(pdf)
sys.path.insert(0,str(R/'tools'));from archive_pdf import archive_pdf
prior=archive_pdf(R/'output/pdf/20261019_video_knowledge_purpose_replanning.pdf',category='01_제출보고서/공통 기획/2026-10-19_목적복원과_스킬적용_재기획',name='2026-10-19_영상지식DB_목적복원과_스킬적용_재기획검토안.pdf')
current=archive_pdf(pdf,category='01_제출보고서/Phase 01-A/2026-10-19_가치창출_새기록과_화면시범',name='2026-10-19_가치창출영상_새지식기록과_화면모션시범.pdf')
names=['00_먼저읽기.md','decision.json','effective-scenario.json','effective-scenario.txt','knowledge-cards.json','numeric-baseline-ledger.json','research-application.json','motion-proposals.json','validation.json','report-build.json','report-qa.json','proof-index.json','build_records.py','draw_proofs.py','build_report.py','finalize.py','publish.py']
files=[copy(O/n,DEST/n) for n in names]
files.extend(copy(p,DEST/'proofs'/p.name) for p in sorted((O/'proofs').glob('*.png')))
receipt={'utc':datetime.now(timezone.utc).isoformat(),'state':'archived_and_hash_verified','prior_pdf':prior,'current_pdf':current,'records_destination':str(DEST),'files':files,'active_skill_changed':False,'canonical_patterns_changed':False,'prior_replanning_full_record_publication':'not performed by this publisher; prior PDF archived only','source_media_copied':False}
(O/'publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
copy(O/'publication-receipt.json',DEST/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'},ensure_ascii=False))
