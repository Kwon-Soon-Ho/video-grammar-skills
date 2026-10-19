from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
issues=[];pins=read(B/'trial-harness-pins.json')
refseal=read(B/'reference/seal.json')
for rel,key in [('reference.json','reference_sha256'),('audit.json','audit_sha256')]:
 if sha(B/'reference'/rel)!=refseal[key]:issues.append({'reference_changed':rel})
for rel,h in pins['sha256'].items():
 if sha(B/rel)!=h:issues.append({'harness_changed':rel})
logs=[];frames=0
for p in sorted((B/'cases').glob('**/실행기록.json')):
 d=read(p);n=len(d.get('frames',[]));frames+=n;logs.append({'path':str(p),'native_frames':n})
disk=sum(p.stat().st_size for p in B.rglob('*') if p.is_file())
ledger=read(B/'execution-ledger.json');matrix=read(B/'run-matrix.json');started={x['run_id'] for x in ledger['primary_dispatched']};sealed=[]
for m in matrix:
 p=B/'trials'/m['run_id']/'seal.json'
 if p.exists():
  sealed.append(m['run_id']);d=read(p)
  for rel,h in d.get('files',{}).items():
   if isinstance(h,str) and len(h)==64:
    q=B/'trials'/m['run_id']/'outputs'/rel
    if not q.exists() or sha(q)!=h:issues.append({'seal_changed':str(q)})
partial=sorted(started-set(sealed));notstarted=sorted({x['run_id'] for x in matrix}-started)
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_started=len(started),primary_sealed_completed=len(sealed),primary_interrupted=partial,primary_not_started=notstarted,planned=16,new_selected_native_frames=frames,new_selected_native_cap=1000,local_phase_disk_bytes=disk,disk_cap_bytes=8589934592,reference_extra_frames=64,reference_extra_cap=64,issues=issues,extraction_logs=logs,fully_validated_seal_keys='files: all sealed observations.json/md SHA256 rechecked',all_seal_record_keys=sorted(set(k for rid in sealed for k in read(B/'trials'/rid/'seal.json'))))
assert frames<=1000 and disk<=8589934592 and not issues,out
(B/'final-integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['extraction_logs']},ensure_ascii=False))
