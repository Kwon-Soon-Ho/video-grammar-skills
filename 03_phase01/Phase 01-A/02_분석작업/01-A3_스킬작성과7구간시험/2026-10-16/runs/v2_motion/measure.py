import json,numpy as np
from pathlib import Path
from PIL import Image
from fractions import Fraction
r=Path('phase01a-a3/runs/v2_motion');j=json.loads((r/'cases/자료013/motiondetail/실행기록.json').read_text(encoding='utf8'))
for f in j['frames']:
 a=np.array(Image.open(f['path']));z=a[:1300,:1900].astype(float);m=(z[:,:,0]>170)&(z[:,:,1]>140)&(z[:,:,2]<120)&(z[:,:,0]>z[:,:,2]*1.6)
 ys=np.where(m.sum(1)>700)[0];groups=[]
 for y in ys:
  if not groups or y>groups[-1][-1]+1:groups.append([])
  groups[-1].append(y)
 print(str(Fraction(f['actual_playback_seconds'])),[(int(g[len(g)//2]),int(np.where(m[g[len(g)//2]])[0].min()),int(np.where(m[g[len(g)//2]])[0].max())) for g in groups])
