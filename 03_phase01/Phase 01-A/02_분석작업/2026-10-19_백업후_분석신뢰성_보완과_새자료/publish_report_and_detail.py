from pathlib import Path
from hashlib import sha256
import json,shutil,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'tools'))
from archive_pdf import ARCHIVE_ROOT,archive_pdf
D=ARCHIVE_ROOT.parent
prior=json.loads((HERE/'working-update.json').read_text(encoding='utf-8'));RECORDS=Path(prior['records']);CAND=Path(prior['candidate_snapshot']);CANON=Path(prior['working_copy'])
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
for op in prior['published_files']:assert digest(op['source'])==digest(op['destination'])==op['sha256'],op['source']
for item in prior['new_working_files']:assert digest(CANON/item['relative'])==item['sha256']
qa=json.loads((HERE/'report-qa.json').read_text(encoding='utf-8'));assert qa['visual_review'].startswith('all 4')
operations=[]
for source in HERE.rglob('*'):
 if not source.is_file() or '__pycache__' in source.parts or source.name in ('publication-receipt.json','working-update.json') or 'backup' in source.relative_to(HERE).parts:continue
 relative=source.relative_to(HERE);dest=CAND/Path(*relative.parts[2:]) if relative.parts[0]=='candidate' else RECORDS/relative
 dest.parent.mkdir(parents=True,exist_ok=True);h=digest(source)
 if dest.exists():assert digest(dest)==h,dest
 else:
  with source.open('rb') as incoming,dest.open('xb') as output:shutil.copyfileobj(incoming,output)
 assert digest(dest)==h;operations.append({'source':str(source),'destination':str(dest),'sha256':h})
rules=D/'AGENTS.md';backup=D/'99_백업/2026-10-19_분석스킬_수정전/AGENTS.before-detail-policy.md'
if not backup.exists():
 with backup.open('xb') as f:f.write(rules.read_bytes())
assert rules.read_bytes()==backup.read_bytes()
rules.write_bytes((WORK/'AGENTS.md').read_bytes());assert digest(rules)==digest(WORK/'AGENTS.md')
notice=D/'Phase 01-A/00_진행안내/2026-10-19_스킬수정_현재작업본.md';notice.parent.mkdir(parents=True,exist_ok=True);assert not notice.exists();notice.write_bytes((HERE/'현재_작업_안내.md').read_bytes())
pdf=archive_pdf(qa['pdf'],'01_제출보고서/Phase 01-A/2026-10-19_백업후_분석스킬수정과_세부검수',name='2026-10-19_백업후_분석스킬수정과_사내영상_세부검수.pdf',classification='중요 분기점 / 기존 스킬 백업·작업본 반영·새 사내 영상 검토·정밀 검수 우선 결정')
for item in prior['relocated']:assert digest(item['preserved_at']).lower()==item['sha256'].lower()
protected=json.loads((HERE/'protected-before.json').read_text(encoding='utf-8'));relocated={i['path'] for i in prior['relocated']}
for item in protected:
 if item['path'] not in relocated:assert digest(item['path']).lower()==item['sha256'].lower()
receipt={'working_update':str(RECORDS/'working-update.json'),'working_skill':str(CANON),'version':'0.1.0-draft.7','current_notice':str(notice),'records':str(RECORDS),'pdf':pdf,'published_file_count':len(operations),'published_files':operations,'whole_research_completed':False,'whole_internal_video_analysis_complete':False,'user_priority':'사내 영상 세부 검수 먼저','project_rules_updated':True,'protected_original_paths_unchanged':prior['protected_unchanged'],'prior_working_paths_preserved_in_backup':len(prior['relocated'])}
data=json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8');(HERE/'publication-receipt.json').write_bytes(data);(RECORDS/'publication-receipt.json').write_bytes(data)
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False))
