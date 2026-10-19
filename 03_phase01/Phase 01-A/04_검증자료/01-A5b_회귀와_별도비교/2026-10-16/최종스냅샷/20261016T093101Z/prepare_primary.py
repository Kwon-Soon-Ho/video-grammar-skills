from pathlib import Path
import sys,json,shutil,subprocess,datetime
B=Path(__file__).resolve().parent;A=B.parent/'phase01a-a5a'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
guard=read(B/'legacy-decision.json')
assert guard['all_passed'] and guard['runs_completed']==3,'New videos must stay closed until regression passes'
for name in ['prepare.py','extract.py','boards.py']:shutil.copy2(A/'candidate/tool'/name,B/name)
from prepare import ROOT,sha,preflight
materials=read(B/'materials-metadata.json');windows=read(B/'windows.json');manifest=[]
for aid,filename in [('A5-T','01_(T).mp4'),('A5-A','04_(A).mp4'),('A5-K','K-GEO FESTA_250919_3.mp4')]:
 m=next(x for x in materials if Path(x['path']).name==filename)
 p=ROOT/m['path'];assert sha(p)==m['sha256']
 manifest.append({'id':aid,'path':str(p),'registered_relative_path':m['path'],'sha256':m['sha256'],'preflight':preflight(p)})
write(B/'manifest.json',manifest)
write(B/'adapter-scope.json',{'files_allowlisted':[m['path'] for m in manifest],'contract':'contract-v1.json','no_code_changes':True})
for c in windows:
 m=next(x for x in manifest if x['registered_relative_path']==c['path'])
 write(B/'requests'/f"{m['id']}-{c['case_id']}.json",c['base_targets_seconds'])
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),m['id'],c['case_id']],capture_output=True,text=True,encoding='utf-8')
 print(r.stdout,flush=True)
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
 subprocess.run([sys.executable,'-B','-X','utf8',str(B/'boards.py'),str(B/'cases'/m['id']/c['case_id'])],check=True,capture_output=True)
 c['source_id']=m['id'];c['source_path']=m['path'];c['input_log']=str(B/'cases'/m['id']/c['case_id']/'실행기록.json');c['base_preparation_start_utc']=start
 write(B/'inputs'/f"{c['case_id']}.json",c)
write(B/'primary-preparation.json',{'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_selected_images':sum(len(c['base_targets_seconds']) for c in windows),'cases':windows,'code_pins_unchanged':True})
