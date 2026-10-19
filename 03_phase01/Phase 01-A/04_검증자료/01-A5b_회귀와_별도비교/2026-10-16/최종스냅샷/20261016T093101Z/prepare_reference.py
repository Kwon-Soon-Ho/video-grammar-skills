from pathlib import Path
import json,subprocess,sys,datetime
B=Path(__file__).resolve().parent
selections={
'H01':('A5-T',['1.4','1.6','1.8','2.2','2.6','3','3.4','3.8','4.2','4.6','5','5.4','6.6','6.9','7.1','7.3']),
'H02':('A5-A',['12.2','12.6','13','13.4','13.8','14.2','14.6','15','16.2','17','17.4','17.8','18.2','18.5','18.6','18.7']),
'H03':('A5-K',['25.2','26','27.2','28','29.6','29.7','29.9','30','30.1','30.3','31.6','31.7','31.9','32','32.1','32.3']),
'H04':('A5-K',['67','67.1','67.3','67.4','67.5','67.7','67.8','67.9','71.3','71.4','71.5','72.2','73','74.2','75','75.8'])}
assert sum(len(v[1]) for v in selections.values())==64
for cid,(aid,times) in selections.items():
 phase='REF-'+cid
 (B/'requests'/f'{aid}-{phase}.json').write_text(json.dumps(times),encoding='utf-8')
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),aid,phase],capture_output=True,text=True,encoding='utf-8')
 print(r.stdout,flush=True)
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
 subprocess.run([sys.executable,'-B','-X','utf8',str(B/'boards.py'),str(B/'cases'/aid/phase)],check=True,capture_output=True)
(B/'reference-preparation.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_extra_native_frames':64,'source_selection':selections,'dispute_extra_native_budget_remaining':0,'purpose':'reference before primary outputs; no answer examples supplied to trial agents'},ensure_ascii=False,indent=2),encoding='utf-8')
