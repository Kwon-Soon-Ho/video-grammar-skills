from pathlib import Path
import json,datetime,sys
B=Path(__file__).resolve().parent
p=B/'effort-events.json'
events=json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
action,category,label=sys.argv[1:4]
events.append({'action':action,'category':category,'label':label,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actor':'root_AI','time_kind':'elapsed workflow time; not human active labor'})
p.write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8')
print(action,category,label)
