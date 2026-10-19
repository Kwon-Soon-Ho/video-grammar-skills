from pathlib import Path
from datetime import datetime,timezone
import json,sys,shutil
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'tools'))
from archive_pdf import ARCHIVE_ROOT,archive_pdf,digest,write_atomic
D=ARCHIVE_ROOT.parent
TARGET=D/'Phase 01-A/02_분석작업/2026-10-19_전문가판단_역설계_수정후보'
SKILL=D/'Phase 01-A/03_분석스킬/수정후보/2026-10-19_draft4/company-video-grammar-analyzer'

def preflight():
    operations=[]
    for p in (HERE/'candidate/company-video-grammar-analyzer').rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:operations.append((p,SKILL/p.relative_to(HERE/'candidate/company-video-grammar-analyzer')))
    for name in ('plan.md','decisions.json','result.json','adoption-map.md','report-qa.json','protected-before.json','prepare.py','write_references.py','validate_revision.py','build_development_case.py','final_checks.py','build_milestone_report.py','publish_revision.py'):
        operations.append((HERE/name,TARGET/name))
    for folder in ('development','knowledge','validation'):
        for p in (HERE/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:operations.append((p,TARGET/p.relative_to(HERE)))
    plan=[]
    for source,dest in operations:
        assert dest.resolve().is_relative_to(D.resolve())
        h=digest(source)
        if dest.exists():assert digest(dest)==h,f'Existing different candidate file: {dest}'
        plan.append({'source':str(source),'destination':str(dest),'sha256':h})
    return plan

plan=preflight()
for p in json.loads((HERE/'protected-before.json').read_text(encoding='utf-8')):assert digest(p['path']).lower()==p['sha256'].lower()
rules=D/'AGENTS.md';old_rule=rules.read_bytes();local_rules=(WORK/'AGENTS.md').read_bytes()
expected=json.loads((HERE/'publication-preflight.json').read_text(encoding='utf-8'))
assert digest(rules) in (expected['old_D_rule_sha256'],digest(WORK/'AGENTS.md'))
backup=TARGET/'publication-backup/AGENTS.before.md'
if not backup.exists():
    assert digest(rules)==expected['old_D_rule_sha256'];backup.parent.mkdir(parents=True,exist_ok=True)
    with backup.open('xb') as f:f.write(old_rule)
assert digest(backup)==expected['old_D_rule_sha256']
published=[]
for op in plan:
    source=Path(op['source']);dest=Path(op['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        with dest.open('xb') as out,source.open('rb') as incoming:shutil.copyfileobj(incoming,out)
    assert digest(dest)==op['sha256'];published.append(op)
if rules.read_bytes()!=local_rules:write_atomic(rules,local_rules)
assert digest(rules)==digest(WORK/'AGENTS.md')
pdf=archive_pdf(WORK/'output/pdf/20261019_analyzer_draft4_milestone.pdf','01_제출보고서/Phase 01-A/2026-10-19_전문가판단_역설계_수정',name='2026-10-19_분석스킬_draft4_수정후보와_검증범위.pdf',classification='중요 분기점 / 사용자 결정·수정 후보·검증 범위')
for p in json.loads((HERE/'protected-before.json').read_text(encoding='utf-8')):assert digest(p['path']).lower()==p['sha256'].lower()
receipt={'published_utc':datetime.now(timezone.utc).isoformat(),'candidate_path':str(SKILL),'working_records':str(TARGET),'pdf':pdf,'copied_files':len(published),'published_files':published,'old_protected_files_unchanged':17,'default_skill_replaced':False,'user_decisions_are_not_content_approval':True,'D_project_rules_updated':True}
write_atomic(TARGET/'publication-receipt.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
(HERE/'publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False))
