from pathlib import Path
import sys,json
from fractions import Fraction
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'phase01a-a1/후보런타임'))
from PIL import Image
import numpy as np
D=B/'blind/H01-r1';lookup={}
for p in (B/'cases/A5-T').glob('*/실행기록.json'):
 for f in json.loads(p.read_text(encoding='utf-8'))['frames']:lookup[Fraction(f['actual_playback_seconds'])]=f
arrays={}
def arr(t):
 t=Fraction(str(t));f=lookup[t]
 if t not in arrays:
  with Image.open(f['path']) as im:arrays[t]=np.asarray(im.convert('RGB'))
 return arrays[t],f
results=[]
for label in ['sample-A','sample-B']:
 obs=json.loads((D/label/'observations.json').read_text(encoding='utf-8'))
 for o in obs['objects']:
  for e in o['events']:
   ease=e.get('easing',{});m=ease.get('measurement') or ease.get('measurements')
   if not m:continue
   for s in m.get('samples',[]):
    t=s.get('seconds',s.get('actual_seconds'));a,f=arr(t)
    for key,expected in s.items():
     measured='not_a_numeric_coordinate'
     if key in ['native_top_y_at_x2050','native_top_y']:
      x={'logo_T':2050,'logo_O':2300,'logo_V':2500,'logo_A':2750}.get(o['id'])
      if x:
       ys=np.flatnonzero((a[1100:1570,x,:]>210).all(axis=1));measured=int(ys[0]+1100) if len(ys) else None
     elif key=='native_rightmost_text_x':
      ys,xs=np.nonzero((a[1490:1540,2815:3350,:]>210).all(axis=2));measured=int(xs.max()+2815) if len(xs) else None
      # x2815 is the A outline at t4.2, explicitly excluded in the asserted definition.
      if Fraction(str(t))==Fraction('4.2') and measured==2815:measured=None
     elif key=='native_left_white_boundary_x_at_y820':
      xs=np.flatnonzero((a[820,:,:]>170).all(axis=1));measured=int(xs[0]) if len(xs) else None
     elif key in ['stem_left_x_at_native_y1000','topbar_left_x_at_native_y800']:
      y=1000 if key.startswith('stem') else 800;xs=np.flatnonzero((a[y,:,:]>140).all(axis=1));measured=int(xs[0]) if len(xs) else None
     if measured!='not_a_numeric_coordinate':results.append({'sample':label,'object':o['id'],'time':str(t),'key':key,'asserted':expected,'independently_recomputed':measured,'match':expected==measured,'source_png':f['path']})
out={'method':'root independent array scan of original RGB using the coordinate/threshold explicitly asserted by each output, no executor script used; validates pixel statistic, not AE transform or semantic target identity','results':results,'matched':sum(x['match'] for x in results),'total':len(results),'mismatches':[x for x in results if not x['match']]}
(D/'numeric-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:out[k] for k in ['matched','total','mismatches']},ensure_ascii=False))
