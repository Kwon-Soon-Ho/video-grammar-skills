from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=js(HERE/'direct_audit.json');issues=[];tot={'passed':0,'failed':0,'total':0}
for r in rows:
 run=Path(r['run'])
 for f in r['coverage']:
  if sha(run/f['path'])!=f['sha']:issues.append(str(run/f['path']))
 g=js(run/'grading.json');p=sum(x['passed'] for x in g['expectations']);n=len(g['expectations']);assert g['summary']=={'passed':p,'failed':n-p,'total':n,'pass_rate':p/n}
 for k in tot:tot[k]+=g['summary'][k]
assert not issues,issues
v={'original_output_files_checked':sum(1 for r in rows for f in r['coverage'] if f['path'].startswith('outputs')),'original_service_event_files_checked':sum(1 for r in rows for f in r['coverage'] if f['path'].startswith('서비스이벤트')),'all_original_outputs_events_unchanged':True,'summary_arithmetic':tot,'direct_checks':sum(len(r['checks']) for r in rows),'direct_check_failures':sum(not c['passed'] for r in rows for c in r['checks'])}
(HERE/'최종무결성확인.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(v,ensure_ascii=False))
