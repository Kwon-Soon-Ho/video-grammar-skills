from pathlib import Path
import json,sys,datetime
B=Path(__file__).resolve().parent
p=B/'execution-ledger.json'; d=json.loads(p.read_text(encoding='utf-8'))
for rid in sys.argv[1:]:
 if not any(x['run_id']==rid for x in d['primary_dispatched']):
  d['primary_dispatched'].append({'run_id':rid,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'utc_kind':'root dispatch recording time'})
d['primary_completed']=sum((x/'seal.json').exists() for x in (B/'trials').iterdir() if x.is_dir())
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('dispatched',len(d['primary_dispatched']),'sealed',d['primary_completed'])
