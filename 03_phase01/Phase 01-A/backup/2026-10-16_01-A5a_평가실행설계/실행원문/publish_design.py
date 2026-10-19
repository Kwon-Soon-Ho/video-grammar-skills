from pathlib import Path
import json,hashlib,shutil,datetime
B=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for v in iter(lambda:f.read(1024*1024),b''):h.update(v)
 return h.hexdigest()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
check=json.loads((B/'design-checks.json').read_text(encoding='utf-8'));assert check['all_passed']
mapping=json.loads((B/'staged/delivery-map.json').read_text(encoding='utf-8'))
dest=ROOT/mapping['design'];backup=ROOT/mapping['backup'];review=ROOT/mapping['review']
assert not dest.exists() and not backup.exists() and not review.exists(),'do not overwrite an existing A5a delivery'
protected=json.loads((B/'protected-records.before.json').read_text(encoding='utf-8'))
assert all(sha(ROOT/x['path'])==x['sha256'] for x in protected)
staged=[p for p in (B/'staged').rglob('*') if p.is_file() and p.name!='delivery-map.json']
backed=[]
for p in staged:
 rel=p.relative_to(B/'staged');target=ROOT/rel
 if target.exists():
  old=backup/'변경전'/rel;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,old)
  assert sha(target)==sha(old);backed.append({'path':str(rel),'before_sha256':sha(target)})
exec_backup=backup/'실행원문';exec_backup.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(B,exec_backup,ignore=shutil.ignore_patterns('__pycache__'))
design_files=['contract-v1.json','candidate-pins.json','materials-metadata.json','windows.json','run-matrix.json','legacy-regression-plan.json','exposure.json','common-task.md','common-output-format.md','A5-run-record-template.json','reference-thread.json','protected-records.before.json','design-checks.json','자체검토.md']
dest.mkdir(parents=True)
for name in design_files:shutil.copy2(B/name,dest/name)
shutil.copytree(B/'candidate',dest/'candidate')
published=[]
for p in staged:
 rel=p.relative_to(B/'staged');target=ROOT/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 assert sha(p)==sha(target);published.append({'path':str(rel),'sha256':sha(target)})
review.mkdir(parents=True)
for name in ['자체검토.md','design-checks.json','protected-records.before.json']:
 shutil.copy2(B/name,review/name)
assert all(sha(ROOT/x['path'])==x['sha256'] for x in protected)
for name in design_files:assert sha(B/name)==sha(dest/name)
for p in (B/'candidate').rglob('*'):
 if p.is_file():assert sha(p)==sha(dest/'candidate'/p.relative_to(B/'candidate'))
pins=json.loads((B/'candidate-pins.json').read_text(encoding='utf-8'))
assert all(sha(ROOT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'/x['relative'])==x['sha256'] for x in pins['snapshot_files'])
state=json.loads((ROOT/'Phase 01-A/00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8'))
assert state['current_stage']=='01-A5a' and not state['A5b_authorized'] and state['actual_scores'] is None
record={'at':datetime.datetime.now().astimezone().isoformat(),'status':'A5a_design_published_no_A5b_execution','design':str(dest),'report':str(ROOT/mapping['report']),'contract':str(ROOT/mapping['protocol']),'changed_files':published,'backed_up':backed,'protected_records_unchanged':len(protected),'candidate_unchanged':True,'A5b_runs':0,'new_video_pixel_observations':0,'checks':'design-checks.json; design consistency only, not recognition accuracy','backup':str(backup),'self_review':str(review),'design_files':[{'path':str(p.relative_to(dest)),'sha256':sha(p)} for p in dest.rglob('*') if p.is_file()]}
write(B/'publication.json',record);write(dest/'publication.json',record);write(review/'저장검증.json',record);write(backup/'게시완료.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in ['design_files','changed_files','backed_up']},ensure_ascii=False))
