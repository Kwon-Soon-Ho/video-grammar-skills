from pathlib import Path
import json,subprocess,sys,shutil
from prepare import write,sha,ROOT
B=Path(__file__).resolve().parent
manifest={x['id']:x for x in json.loads((B/'manifest.json').read_text(encoding='utf-8'))}
specs=[('V01','A4-D',0,8,0.4,'DOC063'),('V02','A4-D',130,138,0.4,'DOC063'),('V03','A4-L',98,104,0.25,'DOC066'),('V04','A4-L',296,302,0.25,'DOC066'),('V05','A4-G',0,10.9666666667,0.4,None),('V06S','A4-S',232,246,0.5,'DOC071'),('V06W','A4-W',236,250,0.5,'DOC071')]
cases=[]
for cid,aid,start,end,step,doc in specs:
 targets=[round(start+i*step,6) for i in range(int((end-start)/step)+1)]
 if cid=='V05':targets.append(10.933333)
 write(B/'requests'/f'{aid}-{cid}.json',targets)
 cases.append({'case_id':cid,'source':{k:manifest[aid][k] for k in ['id','path','sha256']},'window_seconds':[start,end],'input_log':str(B/'cases'/aid/cid/'실행기록.json'),'document':str(B/'documents'/f'{doc}.txt') if doc else None,'document_record':str(B/'documents'/f'{doc}.json') if doc else None})
write(B/'case-plan.json',{'stage':'A4','selection':'Whole-video sparse overview followed by selected motion windows; not exhaustive whole-video review.','same_group':['V01/V02','V03/V04','V06S/V06W','V05 same homepage family as A3'], 'audio_scope':'not decoded/listened; visual test only','cases':cases,'variant_comparison':['V06S','V06W'],'baseline':'Same prompt, files and host tools; skill only treatment. No numerical general accuracy claim; no exposed model/token telemetry.'})
shutil.copy2(B/'skill-draft2/references/output-contract.md',B/'output-format.md')
for c in cases:
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),c['source']['id'],c['case_id']],capture_output=True,text=True,encoding='utf-8')
 print(r.stdout,flush=True)
 if r.returncode:continue
 subprocess.run([sys.executable,'-B','-X','utf8',str(B/'boards.py'),str(Path(c['input_log']).parent)])
write(B/'document-verification.json',[{'id':doc,'source_sha_match':sha(ROOT/json.loads((B/'documents'/f'{doc}.json').read_text(encoding='utf-8'))['path'])==json.loads((B/'documents'/f'{doc}.json').read_text(encoding='utf-8'))['sha256'],'text_sha256':sha(B/'documents'/f'{doc}.txt'),'layout_reviewed':False} for doc in ['DOC063','DOC066','DOC071']])
