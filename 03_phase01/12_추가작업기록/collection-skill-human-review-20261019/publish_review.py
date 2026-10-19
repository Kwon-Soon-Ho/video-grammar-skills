from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,re

R=Path(__file__).resolve().parent
BASE=R.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
OUT=D/'Phase 01-A/05_결과보고/2026-10-19_실제기록_사용자검토'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):return {x.relative_to(p).as_posix():sha(x) for x in sorted(p.rglob('*')) if x.is_file()}

old=json.loads((BASE/'collection-skill-review-20261019/backup-manifest.json').read_text(encoding='utf-8'))
assert manifest(Path(old['source']))==old['files'],'Active skill changed unexpectedly'
cand=BASE/'collection-skill-review-20261019/candidate/company-video-grammar-analyzer'
cm=json.loads((BASE/'collection-skill-review-20261019/candidate-manifest.json').read_text(encoding='utf-8'))
assert manifest(cand)==cm,'Candidate changed unexpectedly'
doc=R/'00_실제기록_사용자검토안.md'
for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
    if link.startswith('evidence/'):assert (R/link).is_file(),link
files=[doc,R/'evidence-manifest.json',*sorted((R/'evidence').glob('*.png'))]
copied=[]
for src in files:
    dest=(OUT/src.relative_to(R)).resolve()
    assert dest.is_relative_to(D) and dest!=D
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():assert sha(dest)==sha(src),'Preserved file differs'
    else:
        with src.open('rb') as a,dest.open('xb') as b:shutil.copyfileobj(a,b)
    assert sha(dest)==sha(src)
    copied.append({'path':str(dest),'sha256':sha(dest)})
receipt={'utc':datetime.now(timezone.utc).isoformat(),'review':str(OUT/doc.name),'status':'awaiting_user_feedback','active_version':'draft.10 unchanged, full file hashes verified','candidate_version':'draft.11 unchanged, full file hashes verified','new_skill_execution':False,'new_design_or_pdf':False,'files':copied}
p=R/'publication-receipt.json'
p.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dest=OUT/p.name
if dest.exists():assert sha(p)==sha(dest),'Existing receipt preserved'
else:
    with p.open('rb') as a,dest.open('xb') as b:shutil.copyfileobj(a,b)
assert sha(p)==sha(dest)
print(json.dumps({k:v for k,v in receipt.items() if k!='files'},ensure_ascii=False))
