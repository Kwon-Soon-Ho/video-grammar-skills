"""Publish a reviewed local draft after a complete, hash-verified backup. No deletions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,tempfile,os
O=Path(__file__).resolve().parent;R=O.parent
META=json.loads((O/'backup-manifest.json').read_text(encoding='utf-8'))
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
ACTIVE=Path(META['source']).resolve();CANDIDATE=Path(META['candidate']).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def safe(p):
 p=Path(p).resolve()
 assert p.is_relative_to(D) and p!=D,p
 return p
def copy_new(p,q):
 q=safe(q);q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert sha(p)==sha(q),'different preserved destination: '+str(q)
 else:
  with p.open('rb') as a,q.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(p)==sha(q)
 return {'relative':q.relative_to(D).as_posix(),'sha256':sha(q)}
def replace_from(p,q):
 q=safe(q);q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists() and sha(p)==sha(q):return
 with tempfile.NamedTemporaryFile(dir=q.parent,delete=False) as f:
  temp=Path(f.name);f.write(p.read_bytes())
 os.replace(temp,q);assert sha(p)==sha(q)
safe(ACTIVE)
assert ACTIVE==D/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
assert load(O/'validation-summary.json')['required_local_checks_passed']
ITER=O/'company-video-grammar-analyzer-workspace/iteration-1'
assert all((ITER/e/c/'grading.json').is_file() for e in ['eval-1-new-section','eval-2-repeated-components'] for c in ['with_skill','old_skill'])
for x in META['files']:assert sha(ACTIVE/x['relative'])==x['sha256'],'active skill changed since backup'
current_files={p.relative_to(ACTIVE).as_posix() for p in ACTIVE.rglob('*') if p.is_file()}
assert current_files=={x['relative'] for x in META['files']},'active file set changed'
assert sha(META['root_agents']['source'])==META['root_agents']['sha256'],'root rules changed since backup'
manifest=[{'relative':p.relative_to(CANDIDATE).as_posix(),'sha256':sha(p)} for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
package_hash=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest()
BACK=safe(D/('99_백업/2026-10-19_draft9_수집규칙반영전/'+META['files'][0]['sha256'][:12]))
STAGE=safe(D/('Phase 01-A/03_분석스킬/후보보관/2026-10-19_draft10_'+package_hash[:12]))
backup_files=[]
for x in META['files']:backup_files.append(copy_new(ACTIVE/x['relative'],BACK/'company-video-grammar-analyzer'/x['relative']))
copy_new(Path(META['root_agents']['source']),BACK/'AGENTS.md')
for x in manifest:copy_new(CANDIDATE/x['relative'],STAGE/'company-video-grammar-analyzer'/x['relative'])
state={'utc':datetime.now(timezone.utc).isoformat(),'state':'backup_and_stage_verified_before_activation','backup':str(BACK),'stage':str(STAGE),'package_hash':package_hash}
(O/'publication-status.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
# Update the entrypoint last; preserve all old and candidate records elsewhere.
ordered=sorted(manifest,key=lambda x:x['relative']=='SKILL.md')
changed=[]
for x in ordered:
 dest=ACTIVE/x['relative']
 if not dest.exists() or sha(dest)!=x['sha256']:changed.append(x['relative'])
 replace_from(CANDIDATE/x['relative'],dest)
replace_from(R/'AGENTS.md',D/'AGENTS.md')
assert all(sha(ACTIVE/x['relative'])==x['sha256'] for x in manifest)
notice=O/'03_수정결과와_다음작업.md'
copy_new(notice,D/'Phase 01-A/00_진행안내/2026-10-19_draft10_수집규칙_수정결과.md')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'state':'draft10_active_hash_verified','active':str(ACTIVE),'previous_version':'0.1.0-draft.9','current_version':'0.1.0-draft.10','backup':str(BACK),'staged_candidate':str(STAGE),'package_hash':package_hash,'files':manifest,'changed_files':changed,'root_rules_updated':True,'canonical_pattern_db_changed':False,'past_analysis_or_failure_records_changed':False,'new_visual_or_pdf_generated':False,'human_output_review':'pending','independent_forward_tests':'two tasks x old/new, one run each; no general performance conclusion','standard_quick_validate':load(O/'validation-summary.json')['standard_quick_validate']}
(O/'publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
copy_new(O/'publication-receipt.json',STAGE/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['files','changed_files']},ensure_ascii=False))
