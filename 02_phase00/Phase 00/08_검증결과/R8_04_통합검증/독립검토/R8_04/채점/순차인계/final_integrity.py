from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=js(HERE/'direct_audit.json');issues=[];tot={'passed':0,'failed':0,'total':0}
for r in rows:
 run=Path(r['run'])
 for p in r['coverage']:
  if sha(run/p['path'])!=p['sha256']:issues.append(str(run/p['path']))
 g=js(run/'grading.json');p=sum(x['passed'] for x in g['expectations']);n=len(g['expectations']);assert g['summary']=={'passed':p,'failed':n-p,'total':n,'pass_rate':p/n}
 for k in tot:tot[k]+=g['summary'][k]
assert not issues,issues
result={'original_output_files':sum(len(r['coverage']) for r in rows),'all_unchanged':True,'grading_summary_arithmetic':tot}
(HERE/'최종무결성확인.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
