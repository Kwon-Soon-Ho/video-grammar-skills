from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parent
p=B/'extract.py';s=p.read_text(encoding='utf-8').replace("'max_pixels':3840*2160","'max_pixels':7680*2160").replace("'memory_process_bytes':1536*1024**2","'memory_process_bytes':2048*1024**2")
p.write_text(s,encoding='utf-8')
(B/'requests').mkdir(exist_ok=True)
jobs={'A4-D':list(range(0,231,15)),'A4-L':list(range(0,391,20)),'A4-S':list(range(0,571,30)),'A4-W':list(range(0,571,30)),'A4-G':list(range(0,11))}
for aid,targets in jobs.items():
 (B/'requests'/f'{aid}-overview.json').write_text(json.dumps(targets),encoding='utf-8')
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),aid,'overview'],capture_output=True,text=True,encoding='utf-8')
 print(r.stdout,flush=True)
