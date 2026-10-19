from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent;R=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
records=json.loads((B.parent/'phase01a-a5a/protected-records.before.json').read_text(encoding='utf-8'))
out=[]
for x in records:
 p=R/x['path'];h=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 if h!=x['sha256']:out.append({'path':x['path'],'expected':x['sha256'],'actual':h})
pins=json.loads((B/'candidate-pins.json').read_text(encoding='utf-8'))
for x in pins['snapshot_files']:
 p=B/'candidate/company-video-grammar-analyzer'/x['relative']
 if hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:out.append({'candidate_modified':x['relative']})
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protected_historical_records':len(records),'skill_snapshot_files':len(pins['snapshot_files']),'changes':out,'passed':not out}
(B/'preservation-check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(data,ensure_ascii=False))
assert not out
