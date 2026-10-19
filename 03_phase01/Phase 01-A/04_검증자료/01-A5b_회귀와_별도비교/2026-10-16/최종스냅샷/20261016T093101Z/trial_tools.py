"""Condition-neutral A5b I/O harness. No reference content or answer feedback."""
from pathlib import Path
import json,sys,hashlib,subprocess,datetime,shutil
from fractions import Fraction
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(rid):
 r=next(x for x in read(B/'run-matrix.json') if x['run_id']==rid)
 return r,read(B/'inputs'/f"{r['case_id']}.json"),B/'trials'/rid
def resource():
 native=list((B/'cases').rglob('f_*.png'))
 size=sum(p.stat().st_size for p in B.rglob('*') if p.is_file())
 assert len(native)<=1000 and size<=8589934592,'global resource cap reached'
 return {'native_selected_images_including_repeated_times':len(native),'disk_bytes':size}
def extra(rid,round_no,targets_path):
 assert (B/'reference/seal.json').is_file(),'reference not sealed'
 assert not (B/'STOP.json').exists(),'batch stopped'
 r,c,d=row(rid);assert round_no in [1,2]
 req=read(Path(targets_path));ts=[Fraction(str(x)) for x in req]
 assert 0<len(ts)<=24 and ts==sorted(set(ts))
 assert all(Fraction(str(c['window_seconds'][0]))<=t<=Fraction(str(c['window_seconds'][1])) for t in ts)
 phase=rid+'-extra'+str(round_no);aid=c['source_id'];q=B/'requests'/f'{aid}-{phase}.json'
 assert not q.exists(),'extra round already attempted; preserve it and report technical failure to root'
 resource();save(q,req)
 start=now();p=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),aid,phase],capture_output=True,text=True,encoding='utf-8')
 record={'run_id':rid,'round':round_no,'targets':req,'start_utc':start,'end_utc':now(),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 save(d/f'extra-{round_no}.json',record);print(p.stdout)
 if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 log=B/'cases'/aid/phase/'실행기록.json';resource()
 print('LOG',log)
def finish(rid,crops_path):
 r,c,d=row(rid);out=d/'outputs';logs=[c['input_log']]
 for n in [1,2]:
  phase=rid+'-extra'+str(n);p=B/'cases'/c['source_id']/phase/'실행기록.json'
  if p.exists():logs.append(str(p))
 crops=read(Path(crops_path)) if crops_path else []
 assert len(crops)<=40
 sys.path.insert(0,str(B.parent/'phase01a-a1/후보런타임'));sys.path.insert(0,str(B/'common-tools'))
 from evidence_catalog import catalog
 from check_observations import check
 cat=catalog(logs,crops);save(d/'support/evidence-catalog.json',cat)
 obs=read(out/'observations.json');errors=check(obs,cat)
 save(d/'validation.json',{'structure_passed':not errors,'evidence_provenance_checked':True,'content_verified':False,'errors':errors})
 if errors:print(json.dumps(errors,ensure_ascii=False));raise SystemExit(1)
 save(d/'seal.json',{'utc':now(),'files':{n:sha(out/n) for n in ['observations.json','observations.md']},'first_output_no_content_feedback':True})
 print(json.dumps({'run_id':rid,'passed_structure_provenance':True,'crop_count':len(crops),'content_verified':False,'resources':resource()}))
if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='extra':extra(sys.argv[2],int(sys.argv[3]),sys.argv[4])
 elif cmd=='finish':finish(sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None)
 else:raise ValueError('unknown command')
