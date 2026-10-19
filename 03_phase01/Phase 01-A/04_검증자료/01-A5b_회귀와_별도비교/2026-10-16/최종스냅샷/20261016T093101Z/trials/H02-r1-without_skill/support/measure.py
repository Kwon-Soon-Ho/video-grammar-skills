from pathlib import Path
import sys,json
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
import numpy as np
from fractions import Fraction
B=Path('phase01a-a5b').resolve(); d=B/'trials/H02-r1-without_skill/support'
rows=[]
for p in [B/'cases/A5-A/H02/실행기록.json',B/'cases/A5-A/H02-r1-without_skill-extra1/실행기록.json']:
 rows+=json.loads(p.read_text(encoding='utf-8'))['frames']
r={float(Fraction(x['actual_playback_seconds'])):x for x in rows}
out=[]
for t in [12,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,17.8,17.9,18,18.1,18.2,18.3,18.4]:
 a=np.array(Image.open(r[t]['path']));m=(a[:,:,0]>180)&(a[:,:,1]>160)&(a[:,:,2]<110)
 box=[1000,900,3100,1800] if t<13 else [700,900,2800,1700]
 x0,y0,x1,y1=box;s=m[y0:y1,x0:x1];counts=s.sum(1);yy=np.flatnonzero(counts>max(counts.max()*.85,30));
 # The longest yellow horizontal stroke belongs to the active screenshot frame in this ROI.
 if len(yy):
  y=int(yy[0])+y0;xx=np.flatnonzero(m[y,x0:x1])+x0
  out.append({'actual_seconds':r[t]['actual_playback_seconds'],'path':r[t]['path'],'yellow_top_stroke_x_min':int(xx.min()),'yellow_top_stroke_x_max':int(xx.max()),'yellow_top_stroke_y':y,'center_x':round((int(xx.min())+int(xx.max()))/2,1),'stroke_span_px':int(xx.max()-xx.min()+1)})
res={'method':'RGB threshold R>180,G>160,B<110; ROI별 최장 수평 노란 선의 85% 이상 행 중 첫 행 좌우 끝. 무배율 원본 픽셀 좌표. 모션블러 및 압축 때문에 실제 레이어 경계와 차이 있을 수 있다. 경계 오차 미측정. 각 값은 검출값이며 AE 좌표가 아니다.','rows':out}
(d/'yellow-border-measurements.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
