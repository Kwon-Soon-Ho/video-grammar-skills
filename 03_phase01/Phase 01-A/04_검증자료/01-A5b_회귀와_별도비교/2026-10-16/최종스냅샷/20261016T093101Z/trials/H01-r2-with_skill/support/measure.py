import sys,json
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'phase01a-a1/후보런타임')
import numpy as np
from PIL import Image
S=Path('phase01a-a5b/trials/H01-r2-with_skill/support').resolve();rows={float(Fraction(f['actual_playback_seconds'])):f for f in json.loads((S/'rows.json').read_text(encoding='utf-8'))}
ms={}
for t in [3.3,3.4,3.5,3.6,3.7,3.8,4.0,4.2]:
 a=np.asarray(Image.open(rows[t]['path']).convert('RGB'));m=(a[1100:1540,1930:2230].min(axis=2)>200);ys,xs=np.where(m);ms.setdefault('logo_T_top_y_native',[]).append([t,int(1100+ys.min()) if len(ys) else None])
for t in [4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.0]:
 a=np.asarray(Image.open(rows[t]['path']).convert('RGB'));m=(a[1490:1540,2810:3330].max(axis=2)>180);ys,xs=np.where(m);ms.setdefault('tagline_right_x_native',[]).append([t,int(2810+xs.max()) if len(xs) else None])
for t in [6.5,6.6,6.7,6.8,6.9,7.0,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,8.0]:
 a=np.asarray(Image.open(rows[t]['path']).convert('RGB')).astype(int)
 for y in [700,1000]:
  q=a[y];m=(q.min(axis=1)>130)&((q.max(axis=1)-q.min(axis=1))<12);xs=np.where(m)[0];ms.setdefault(f'map_left_x_at_y{y}_native',[]).append([t,int(xs.min()) if len(xs) else None])
ms['method']='RGB native pixels. T: minimum white y in [1930,1100,2230,1540]. Tagline: maximum bright x in [2810,1490,3330,1540]. Map: first near-neutral bright pixel at fixed row, threshold minRGB>130 and channel spread<12. Compression/blur threshold uncertainty approx 2-8px except onset/overlap. These measurements do not recover AE curves.'
(S/'measurements.json').write_text(json.dumps(ms,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(ms,ensure_ascii=False,indent=2))
