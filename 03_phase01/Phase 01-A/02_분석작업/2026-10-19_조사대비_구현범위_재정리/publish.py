from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;REAL=WORK/'analyzer-realuse-20261019'
sys.path.insert(0,str(WORK/'tools'))
from archive_pdf import ARCHIVE_ROOT,archive_pdf
D=ARCHIVE_ROOT.parent
AUDIT=D/'Phase 01-A/02_분석작업/2026-10-19_조사대비_구현범위_재정리'
RUNS=D/'Phase 01-A/02_분석작업/2026-10-19_실제사용_검사기보완'
SKILL=D/'Phase 01-A/03_분석스킬/수정후보/2026-10-19_draft6/company-video-grammar-analyzer'
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
protected=json.loads((REAL/'protected-before.json').read_text(encoding='utf-8'))
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
qa=json.loads((HERE/'report-qa.json').read_text(encoding='utf-8'));assert qa['visual_review'].startswith('all 3')
operations=[]
for base,target in [(HERE,AUDIT),(REAL,RUNS)]:
 for source in base.rglob('*'):
  if not source.is_file() or '__pycache__' in source.parts or source.name=='publication-receipt.json':continue
  relative=source.relative_to(base)
  dest=SKILL/Path(*relative.parts[2:]) if base==REAL and relative.parts[0]=='candidate' else target/relative
  assert dest.resolve().is_relative_to(D.resolve())
  h=digest(source)
  if dest.exists():assert digest(dest)==h,('different existing target',dest)
  operations.append({'source':str(source),'destination':str(dest),'sha256':h})
for op in operations:
 source=Path(op['source']);dest=Path(op['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  with source.open('rb') as incoming,dest.open('xb') as output:shutil.copyfileobj(incoming,output)
 assert digest(dest)==op['sha256']
pdf=archive_pdf(qa['pdf'],'01_제출보고서/Phase 01-A/2026-10-19_조사대비_구현범위_재정리',name='2026-10-19_조사대비_구현범위와_남은_작업.pdf',classification='중요 분기점 / 전체 반영 오해 정정·실제 구현 범위·개발 실패와 후속 범주')
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
receipt={'published_utc':datetime.now(timezone.utc).isoformat(),'candidate':str(SKILL),'audit':str(AUDIT),'development_records':str(RUNS),'pdf':pdf,'published_file_count':len(operations),'published_files':operations,'protected_files_unchanged':len(protected),'default_installed_or_replaced':False,'whole_research_implemented':False}
data=json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8')
for p in (HERE/'publication-receipt.json',AUDIT/'publication-receipt.json',RUNS/'publication-receipt.json'):
 assert not p.exists();p.write_bytes(data)
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False))
