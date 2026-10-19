from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys,os,tempfile
O=Path(__file__).resolve().parent;R=O.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
pub=json.loads((O/'publication-receipt.json').read_text(encoding='utf-8'))
OUT=D/'Phase 01-A/05_결과보고/2026-10-19_draft10_수집규칙'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def safe(p):
 p=Path(p).resolve();assert p.is_relative_to(D) and p!=D;return p
def cp(p,q):
 q=safe(q);q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert sha(p)==sha(q),'preserve existing different file '+str(q)
 else:
  with p.open('rb') as a,q.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(p)==sha(q)
 return {'path':str(q),'sha256':sha(q)}
assert all(sha(Path(pub['active'])/x['relative'])==x['sha256'] for x in pub['files'])
validation=json.loads((O/'validation-summary.json').read_text(encoding='utf-8'))
assert validation['standard_quick_validate'].startswith('passed')
docs=[]
for n in ['00_작업기록.md','01_제작방식과_시험계획.md','02_호환성_확인.md','03_수정결과와_다음작업.md','변경파일.md','평가에서_발견한_내용오류.md','review.html','publication-receipt.json','validation-summary.json']:
 docs.append(cp(O/n,OUT/n))
IT=O/'company-video-grammar-analyzer-workspace/iteration-1'
for name in ['eval-1-new-section','eval-2-repeated-components']:
 docs.append(cp(IT/name/'paired-review.md',OUT/'실제비교'/name/'paired-review.md'))
 for config in ['with_skill','old_skill']:
  for f in ['collection.md','execution.md']:docs.append(cp(IT/name/config/'outputs'/f,OUT/'실제비교'/name/config/f))
docs.append(cp(IT/'benchmark.md',OUT/'실제비교/benchmark.md'))
NOTICE=safe(D/'Phase 01-A/00_진행안내/2026-10-19_draft10_수집규칙_수정결과.md')
cp(NOTICE,Path(pub['backup'])/'진행안내_표준형식검사완료전.md')
with tempfile.NamedTemporaryFile(dir=NOTICE.parent,delete=False) as f:
 t=Path(f.name);f.write((O/'03_수정결과와_다음작업.md').read_bytes())
os.replace(t,NOTICE)
sys.path.insert(0,str(R/'tools'));from archive_pdf import archive_pdf
items=[('20261019_video_knowledge_purpose_replanning.pdf','01_제출보고서/공통 기획/2026-10-19_목적복원과_스킬적용_재기획','2026-10-19_영상지식DB_목적복원과_스킬적용_재기획검토안.pdf'),('20261019_value_creation_knowledge_and_design_pilot.pdf','01_제출보고서/Phase 01-A/2026-10-19_가치창출_새기록과_화면시범','2026-10-19_가치창출영상_새지식기록과_화면모션시범.pdf'),('20261019_value_creation_source_language_review.pdf','01_제출보고서/Phase 01-A/2026-10-19_DB수집범위_원본언어검토','2026-10-19_DB수집범위_정리와_원본비교기록.pdf')]
pdfs=[archive_pdf(R/'output/pdf'/p,category=c,name=n) for p,c,n in items]
receipt={'utc':datetime.now(timezone.utc).isoformat(),'state':'active_draft10_standard_validation_passed_and_records_published','active':pub['active'],'active_hashes_rechecked':True,'standard_quick_validate':'passed on both local candidate and active D skill','standard_validator_dependency':'PyYAML 6.0.3 installed inside local task only','records_destination':str(OUT),'records':docs,'previous_pdfs_archived':pdfs,'new_pdf_generated':False,'new_design_generated':False,'human_output_review':'pending'}
(O/'post-publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');cp(O/'post-publication-receipt.json',OUT/'post-publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k!='records'},ensure_ascii=False))
