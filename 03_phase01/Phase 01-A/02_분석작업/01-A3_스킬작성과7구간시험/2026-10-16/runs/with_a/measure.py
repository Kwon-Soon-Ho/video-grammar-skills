from pathlib import Path
from PIL import Image
import numpy as np,json
from fractions import Fraction
r=Path.cwd();o=r/'phase01a-a3/runs/with_a';fs=json.loads((o/'catalog.json').read_text(encoding='utf8'))['frames']; results={}
for case in ['T01','T02','T03']:
 rows=[]
 for f in [f for f in fs if f['frame_id'].split('-')[1]==case]:
  t=float(Fraction(f['actual_playback_seconds']));a=np.asarray(Image.open(f['path']),dtype=np.int16)
  row={'t':t}
  if case=='T01':
   # left-to-right boundary against black at original y=100 (top bar)
   line=a[100,:,0].astype(float); grad=np.diff(line); ix=np.where(grad[:2400]<-15)[0];row['top_bar_right_candidates']=ix.tolist()[-8:]
   row['midpatch_mean_RGB']=np.mean(a[850:950,900:1000],axis=(0,1)).round(2).tolist()
  if case in ['T02','T03'] and .8<=t<=3.0:
   red=a[:1500,:,0]-np.maximum(a[:1500,:,1],a[:1500,:,2]);green=a[:1500,:,1]-np.maximum(a[:1500,:,0],a[:1500,:,2]);
   row['cross_y']=int(np.argmax(np.maximum(red,0).sum(axis=1)));row['cross_x']=int(np.argmax(np.maximum(green-30,0).sum(axis=0)))
  rows.append(row)
 results[case]=rows
(o/'measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(results,ensure_ascii=False))
