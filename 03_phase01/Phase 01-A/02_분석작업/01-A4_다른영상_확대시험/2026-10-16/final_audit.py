from pathlib import Path
from fractions import Fraction
import json,ast,datetime
from prepare import sha,write
B=Path(__file__).resolve().parent
manifest=json.loads((B/'manifest.json').read_text(encoding='utf-8'))
sources=[{'id':s['id'],'path':s['path'],'expected_sha256':s['sha256'],'actual_sha256':sha(Path(s['path']))} for s in manifest]
assert all(s['actual_sha256']==s['expected_sha256'] for s in sources)
logs=[];unique=set()
for p in sorted((B/'cases').glob('*/*/실행기록.json')):
 d=json.loads(p.read_text(encoding='utf-8'))
 assert d['complete_target_selection'] and d['input_sha256']==d['input_sha256_after']
 for f in d['frames']:unique.add((d['input_sha256'],Fraction(f['actual_playback_seconds'])))
 logs.append({'source':p.parent.parent.name,'job':p.parent.name,'selected_pngs':len(d['frames']),'sha_consistent':True})
sealed=[]
for p in (B/'company-video-grammar-analyzer-workspace').glob('iteration-*/eval-*/*/output-seal.json'):
 d=json.loads(p.read_text(encoding='utf-8'))
 assert all(sha(Path(f['path']))==f['sha256'] for f in d['files'])
 assert {Path(f['path']).name for f in d['files']}=={q.name for q in (p.parent/'outputs').iterdir() if q.is_file()},'new output file after seal'
 sealed.append(str(p.relative_to(B)))
line=next(l for l in (B/'extract.py').read_text(encoding='utf-8').splitlines() if l.startswith('LIMITS='))
# Arithmetic is a fixed local literal; importing the script would trigger its CLI.
limits=eval(line.split('=',1)[1],{'__builtins__':{}},{})
scope=json.loads((B/'adapter-scope.json').read_text(encoding='utf-8'));scope['worker_limits']=limits
scope['adapter_sha256']=sha(B/'extract.py');scope['time_mapping']='STTS+CTTS+single ELST; every decoded PTS matched to reconstructed samples; seek vs sequential RGB equality on eight test frames'
write(B/'adapter-scope.json',scope)
write(B/'final-audit.json',{'at':datetime.datetime.now().astimezone().isoformat(),'sources':sources,'source_hashes_unchanged':True,'extraction_jobs':logs,'selected_png_count':sum(x['selected_pngs'] for x in logs),'unique_source_times':len(unique),'count_scope':'all A4 overview/base/adaptive and adapter diagnostic jobs; crops/contact sheets excluded; does not mean all viewed or whole video decoded','sealed_outputs':sealed,'skill_files':[{'path':str(p.relative_to(B/'skill-draft3')),'sha256':sha(p)} for p in sorted((B/'skill-draft3').rglob('*')) if p.is_file()]})
print('unchanged sources',len(sources),'jobs',len(logs),'sealed outputs',len(sealed))
