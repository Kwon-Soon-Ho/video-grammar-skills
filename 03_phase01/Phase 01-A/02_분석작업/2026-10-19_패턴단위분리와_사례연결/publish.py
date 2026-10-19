from pathlib import Path
from datetime import datetime,timezone
import sys,json,shutil
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'tools'))
from archive_pdf import ARCHIVE_ROOT,archive_pdf,digest,write_atomic
D=ARCHIVE_ROOT.parent
TARGET=D/'Phase 01-A/02_분석작업/2026-10-19_패턴단위분리와_사례연결'
SKILL=D/'Phase 01-A/03_분석스킬/수정후보/2026-10-19_draft5/company-video-grammar-analyzer'
preflight=json.loads((HERE/'publication-preflight.json').read_text(encoding='utf-8-sig'))
protected=json.loads((HERE/'protected-before.json').read_text(encoding='utf-8'))
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
operations=[]
for source in HERE.rglob('*'):
    if not source.is_file() or '__pycache__' in source.parts or source.name in ('publication-receipt.json','publication-preflight.json'):continue
    relative=source.relative_to(HERE)
    if relative.parts[0]=='candidate':dest=SKILL/Path(*relative.parts[2:])
    else:dest=TARGET/relative
    assert dest.resolve().is_relative_to(D.resolve())
    h=digest(source)
    if dest.exists():assert digest(dest)==h,f'Existing different file: {dest}'
    operations.append({'source':str(source),'destination':str(dest),'sha256':h})
rules=D/'AGENTS.md';rule_before=digest(rules);rule_after=digest(WORK/'AGENTS.md')
assert rule_before in (preflight['old_D_rule_sha256'],rule_after)
backup=TARGET/'publication-backup/AGENTS.before.md'
if not backup.exists():
    assert rule_before==preflight['old_D_rule_sha256'];backup.parent.mkdir(parents=True,exist_ok=True)
    with backup.open('xb') as f:f.write(rules.read_bytes())
assert digest(backup)==preflight['old_D_rule_sha256']
for op in operations:
    source=Path(op['source']);dest=Path(op['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        with dest.open('xb') as output,source.open('rb') as incoming:shutil.copyfileobj(incoming,output)
    assert digest(dest)==op['sha256']
if rule_before!=rule_after:write_atomic(rules,(WORK/'AGENTS.md').read_bytes())
assert digest(rules)==rule_after
pdf=archive_pdf(WORK/'output/pdf/20261019_pattern_composition_decision.pdf','01_제출보고서/Phase 01-A/2026-10-19_패턴단위와_사례연결',name='2026-10-19_전체사례와_독립패턴_연결_draft5_반영결과.pdf',classification='중요 분기점 / 사용자 분류 결정·패턴 분리·검증 결과')
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
receipt={'published_utc':datetime.now(timezone.utc).isoformat(),'candidate':str(SKILL),'records':str(TARGET),'pdf':pdf,'published_files':operations,'published_file_count':len(operations),'protected_files_unchanged':len(protected),'default_skill_replaced':False,'D_project_rules_updated':True}
encoded=json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8')
write_atomic(TARGET/'publication-receipt.json',encoded)
(HERE/'publication-receipt.json').write_bytes(encoded)
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False))
