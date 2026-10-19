from pathlib import Path
import sys,json
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
import numpy as np
from fractions import Fraction
B=Path('phase01a-a5b').resolve();d=B/'trials/H02-r1-without_skill/support';rows=[]
for p in [B/'cases/A5-A/H02/실행기록.json',B/'cases/A5-A/H02-r1-without_skill-extra1/실행기록.json']:rows+=json.loads(p.read_text(encoding='utf-8'))['frames']
r={float(Fraction(x['actual_playback_seconds'])):x for x in rows}
out=[]
for t,yp in [(12,632),(12.1,668),(12.2,714),(12.3,761),(12.4,804),(12.5,847),(12.6,889),(12.7,919),(12.8,941),(13,939)]:
 a=np.array(Image.open(r[t]['path'])); best=(0,0,0,0)
 for y in range(yp-15,yp+16):
  m=(a[y,500:1800,:3].max(1)<30); diff=np.diff(np.r_[False,m,False].astype(int));starts=np.flatnonzero(diff==1);ends=np.flatnonzero(diff==-1)
  for x,e in zip(starts,ends):
   if e-x>best[0]:best=(int(e-x),int(x+500),int(e+499),y)
 length,x,e,y=best
 out.append({'actual_seconds':r[t]['actual_playback_seconds'],'path':r[t]['path'],'detected_dark_run_xyxy':[x,y,e,y],'span_px':length,'center_x_px':(x+e)/2})
result={'method':'시각 검사한 패널 윗변 부근 +-15행에서 RGB 각 채널<30인 최장 연속 수평선 검출. x검색500:1800. 원본 무배율 RGB 픽셀. y초기값은 각 전체 프레임을 본 뒤 수동근사. 압축/블러 때문에 이 선은 레이어의 정확한 외곽이 아니며 오차 미측정.','rows':out}
(d/'entry-measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
