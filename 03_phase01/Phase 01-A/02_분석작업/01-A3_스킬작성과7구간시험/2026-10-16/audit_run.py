from pathlib import Path
from fractions import Fraction as F
import json,hashlib,datetime
B=Path(__file__).resolve().parent;W=B/'company-video-grammar-analyzer-workspace'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
packet=json.loads((B/'analysis_input/cases.json').read_text(encoding='utf-8'));sources={c['media_path']:c['media_sha256'] for c in packet['cases']};errors=[]
for p,h in sources.items():
    if sha(p)!=h:errors.append('source hash '+p)
for pin in json.loads((B/'knowledge-pins.json').read_text(encoding='utf-8')):
    if sha(pin['path'])!=pin['sha256']:errors.append('knowledge changed '+pin['path'])
fresh=[]; reused=[]
for p in sorted((B/'runs').rglob('실행기록.json')):
    d=json.loads(p.read_text(encoding='utf-8'))
    if d.get('complete_target_selection'):
        for f in d['frames']:
            if sha(f['path'])!=f['sha256']:errors.append('frame hash '+f['path'])
            if F(f['reported_pts'])*F(f['time_base'])!=F(f['actual_playback_seconds']):errors.append('PTS '+f['path'])
            fresh.append((d['id'],f['actual_playback_seconds'],f['path']))
for c in packet['cases'][:6]:
    d=json.loads((Path(c['evidence_folder'])/'실행기록.json').read_text(encoding='utf-8'))
    for f in d['frames']:
        if sha(f['path'])!=f['sha256']:errors.append('reused frame hash '+f['path'])
        reused.append((d['id'],f['actual_playback_seconds']))
seals=[]
for p in (W/'seals').rglob('*.json'):
    d=json.loads(p.read_text(encoding='utf-8'));case,mode=p.stem.split('-',1)
    iteration=p.parent.name if p.parent.name.startswith('iteration-') else 'iteration-1'
    for n,h in d['files'].items():
        if sha(W/iteration/('eval-'+case)/mode/'outputs'/n)!=h:errors.append('sealed output changed '+str(p))
    seals.append(iteration+'/'+p.stem)
result={'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'source_files':len(sources),'knowledge_files_unchanged':len(json.loads((B/'knowledge-pins.json').read_text(encoding='utf-8'))),'fresh_selected_pngs':len(fresh),'fresh_unique_source_times':len(set((a,t) for a,t,p in fresh)),'reused_base_pngs':len(reused),'sealed_cases':seals,'counts_note':'fresh includes repeated native/adaptive extraction; reused baseline PNGs not counted as new; crops/boards excluded','full_playback_reviewed':False,'audio_reviewed':False,'SAR_known':False,'absolute_color_validated':False,'per_case_telemetry_available':False}
(B/'execution-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
