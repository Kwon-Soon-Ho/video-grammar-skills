"""Measure a projected aperture edge, not a recovered 3D/AE rotation."""
from pathlib import Path
from fractions import Fraction as F
from collections import deque
from PIL import Image
import numpy as np,json,math
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
frames={}
for p in (WORK/'analysis-reliability-20261019/fresh/cases/NEW-N').glob('*/실행기록.json'):
 for f in json.loads(p.read_text('utf-8'))['frames']:frames.setdefault(F(f['actual_playback_seconds']),f)
rows=[]
for t,f in sorted(frames.items()):
 if not F('169.5')<=t<=F('173.5') or t.denominator not in (1,2,5,10):continue
 with Image.open(f['path']) as im:a=np.asarray(im.crop((1100,1100,2200,2050)).convert('L').resize((220,190)))
 mask=a<35;seen=np.zeros_like(mask,dtype=bool);components=[]
 for yy,xx in zip(*np.where(mask)):
  if seen[yy,xx]:continue
  q=deque([(int(yy),int(xx))]);seen[yy,xx]=True;points=[];edge=False
  while q:
   y,x=q.popleft();points.append((y,x));edge|=y in (0,189) or x in (0,219)
   for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    ny,nx=y+dy,x+dx
    if 0<=ny<190 and 0<=nx<220 and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;q.append((ny,nx))
  if not edge and len(points)>300:components.append(points)
 if not components:raise ValueError(('aperture not found',str(t)))
 points=np.array(max(components,key=len));y,x=points[:,0],points[:,1];x0,x1=int(x.min()),int(x.max())
 xs=np.arange(x0+int((x1-x0)*.2),x0+int((x1-x0)*.8))
 ys=np.array([y[x==col].min() for col in xs]);slope,intercept=np.polyfit(xs,ys,1);residual=np.abs(ys-(slope*xs+intercept))
 rows.append({'time':str(t),'projected_top_edge_angle_deg':math.degrees(math.atan(slope)),'edge_fit_mean_abs_residual_px_at_1over5':float(residual.mean()),'component_bbox_xyxy_native':[int(x.min()*5+1100),int(y.min()*5+1100),int((x.max()+1)*5+1100),int((y.max()+1)*5+1100)],'source_frame':f['path']})
result={'method':'Native ROI (1100,1100,2200,2050), grayscale threshold<35 at 1/5 scale, largest enclosed dark component, least-squares top edge of middle60% x. Visual aperture must be checked separately.','meaning':'Projected dark aperture upper-edge orientation, not actual 3D axis/angle, not AE keyframes. Approximate visual measure; threshold/fit systematic error not calibrated.','samples':rows}
(HERE/'inspection/pose-geometry.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([(r['time'],round(r['projected_top_edge_angle_deg'],2),round(r['edge_fit_mean_abs_residual_px_at_1over5'],2)) for r in rows],ensure_ascii=False))
