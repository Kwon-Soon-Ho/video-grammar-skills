from pathlib import Path
import sys,json,subprocess,hashlib
from fractions import Fraction
from PIL import Image
from prepare import write,preflight
from extract import BoundedReader,LIMITS,RUNTIME,registered,memory_limit
B=Path(__file__).resolve().parent
def verify(aid):
 job=memory_limit();sys.path.insert(0,str(RUNTIME));import av
 row=registered(aid);preflight(Path(row['path']))
 seeklog=json.loads((B/'cases'/aid/'adaptercheck'/'실행기록.json').read_text(encoding='utf-8'))
 targets={Fraction(f['actual_playback_seconds']):f for f in seeklog['frames']}
 result=[];reader=BoundedReader(row['path'])
 with av.open(reader,format='mov',options={'enable_drefs':'0','use_absolute_path':'0','protocol_whitelist':'file','max_pixels':str(LIMITS['max_pixels'])}) as c:
  c.flags &= ~av.container.Flags.gen_pts.value
  s=c.streams.video[0];s.codec_context.thread_count=1
  for i,f in enumerate(c.decode(s)):
   if i>100:raise ValueError('sequential_budget')
   t=f.pts*f.time_base
   if t in targets:
    actual=hashlib.sha256(f.to_image().tobytes()).hexdigest()
    want=hashlib.sha256(Image.open(targets[t]['path']).tobytes()).hexdigest()
    result.append({'actual_seconds':str(t),'sequential_vs_seek_RGB_equal':actual==want})
   if t>=max(targets):break
 assert len(result)==len(targets) and all(r['sequential_vs_seek_RGB_equal'] for r in result)
 write(B/f'adaptercheck_{aid}.json',result)
 print(aid,'sequential vs seek',len(result),'PASS')
if __name__=='__main__':
 if len(sys.argv)>1:verify(sys.argv[1])
 else:
  for aid in ['A4-G','A4-W']:
   write(B/'requests'/f'{aid}-adaptercheck.json',[0,0.117,0.433,0.967])
   subprocess.run([sys.executable,'-B','-X','utf8',str(B/'extract.py'),aid,'adaptercheck'],check=True,timeout=65)
   subprocess.run([sys.executable,'-B','-X','utf8',__file__,aid],check=True,timeout=30)
