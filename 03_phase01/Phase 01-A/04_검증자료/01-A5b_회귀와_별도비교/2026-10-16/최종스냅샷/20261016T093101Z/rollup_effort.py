from pathlib import Path
import json, datetime
B=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8'))
events=read(B/'effort-events.json'); opened={}; segments=[]
for e in events:
 k=(e['category'],e['label'])
 if e['action']=='start': opened[k]=e['utc']
 elif k in opened:
  start=opened.pop(k); elapsed=(datetime.datetime.fromisoformat(e['utc'])-datetime.datetime.fromisoformat(start)).total_seconds()
  segments.append(dict(category=k[0],label=k[1],seconds=elapsed,start_utc=start,end_utc=e['utc']))
def elapsed(d):
 for k in ['ai_elapsed_seconds_including_validation','ai_elapsed_seconds_including_verification','ai_elapsed_seconds','elapsed_seconds','total_ai_elapsed_seconds','elapsed_wall_seconds']:
  if isinstance(d.get(k),(float,int)): return d[k]
 for sk,ek in [('start_utc','end_utc'),('started_utc','ended_utc')]:
  if d.get(sk) and d.get(ek): return (datetime.datetime.fromisoformat(d[ek].replace('Z','+00:00'))-datetime.datetime.fromisoformat(d[sk].replace('Z','+00:00'))).total_seconds()
 return None
runs=[]
for p in sorted((B/'trials').glob('*/run-effort.json')):
 d=read(p); runs.append(dict(run_id=p.parent.name,seconds=elapsed(d),source=str(p),sealed=(p.parent/'seal.json').exists()))
legacy=[]
for p in sorted((B/'legacy').glob('*/outputs/run-effort.json')):
 legacy.append(dict(run_id=p.parent.parent.name,seconds=elapsed(read(p)),source=str(p)))
grades=[]
for p in sorted((B/'blind').glob('*/grading.json')):
 t=read(p).get('timing',{}); sec=t.get('total_review_seconds');supp=p.parent/'timing-supplement.json'
 if supp.exists():sec=read(supp)['total_review_seconds_including_metadata']
 grades.append(dict(pair=p.parent.name,seconds=sec,first_save_seconds=t.get('total_review_seconds'),sample_review_seconds=t.get('sample_review_seconds'),shared_seconds=t.get('shared_review_seconds'),source=str(p)))
totals={c:sum(s['seconds'] for s in segments if s['category']==c) for c in ['technical','reference','review','dispute']}
totals['blind_AI_review']=sum(x['seconds'] for x in grades if isinstance(x['seconds'],(int,float)))
totals['primary_AI_execution']=sum(x['seconds'] for x in runs if isinstance(x['seconds'],(int,float)))
totals['legacy_AI_execution']=sum(x['seconds'] for x in legacy if isinstance(x['seconds'],(int,float)))
audit=read(B/'reference/audit.json')
totals['reference_independent_AI_audit']=elapsed(audit)
if (B/'critical-confirmation.json').exists():totals['dispute']+=read(B/'critical-confirmation.json')['elapsed_seconds']
data=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),time_kind='AI task elapsed seconds, overlapping actors summed; not human labor',measured_segments=segments,root_open_segments=[dict(category=k[0],label=k[1],start_utc=v) for k,v in opened.items()],primary=runs,legacy=legacy,blind_reviews=grades,measured_seconds=totals,unsegmented_root_orchestration_seconds=None,technical_total_complete=False,human_verification_requested=0,new_human_content_approval=0,actual_human_reading_or_review_seconds=None,exact_tokens=None,paid_external_API_calls=0,limits=dict(primary_seconds=14400,legacy_seconds=1800,technical_seconds=1800,reference_seconds=2400,blind_review_seconds=1920,dispute_seconds=1080,review_total_seconds=5400,total_task_seconds=23400),caveat='Missing telemetry is null. Measured technical segments are a lower bound; no fabricated active time or human savings.')
(B/'effort-rollup.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'runs':len(runs),'grades':len(grades),'measured_seconds':totals},ensure_ascii=False))
