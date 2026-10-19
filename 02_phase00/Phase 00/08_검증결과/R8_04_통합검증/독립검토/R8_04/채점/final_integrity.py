from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=js(HERE/'direct_audit.json');issues=[];summaries=[]
for r in a:
 run=Path(r['run']);g=js(run/'grading.json')
 p=sum(x['passed'] for x in g['expectations']);n=len(g['expectations'])
 assert g['summary']=={'passed':p,'failed':n-p,'total':n,'pass_rate':p/n}
 for o in r['coverage']:
  if sha(run/o['path'])!=o['sha256']:issues.append(str(run/o['path']))
 assert sha(run/'task.txt')==r['task_sha256']
 summaries.append({'run':str(run),'summary':g['summary']})
assert not issues,issues
v={'existing_output_files_checked':sum(len(r['coverage']) for r in a),'all_existing_outputs_unchanged':not issues,'grading_arithmetic_verified':True,'runs':summaries,'scope':'grade sibling and separate audit files only; original output coverage at audit start vs end'}
(HERE/'최종무결성확인.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in v.items() if k!='runs'},ensure_ascii=False))
