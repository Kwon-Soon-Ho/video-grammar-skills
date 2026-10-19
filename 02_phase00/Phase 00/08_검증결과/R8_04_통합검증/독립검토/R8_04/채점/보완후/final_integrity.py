from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=js(HERE/'direct_audit.json');issues=[];s=[]
for r in a:
 run=Path(r['run']);g=js(run/'grading.json');p=sum(x['passed'] for x in g['expectations']);n=len(g['expectations'])
 assert g['summary']=={'passed':p,'failed':n-p,'total':n,'pass_rate':p/n}
 for f in r['coverage']:
  if sha(run/f['path'])!=f['sha256']:issues.append(str(run/f['path']))
 s.append(g['summary'])
assert not issues,issues
v={'original_outputs_checked':sum(1 for r in a for f in r['coverage'] if f['path'].startswith('outputs')),'original_service_events_checked':sum(1 for r in a for f in r['coverage'] if f['path'].startswith('서비스이벤트')),'all_unchanged':True,'summary_arithmetic':{'passed':sum(x['passed'] for x in s),'failed':sum(x['failed'] for x in s),'total':sum(x['total'] for x in s)}}
(HERE/'최종무결성확인.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(v,ensure_ascii=False))
