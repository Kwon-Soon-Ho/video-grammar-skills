import json,numpy as np
from pathlib import Path
from PIL import Image
from fractions import Fraction
r=Path.cwd()/'phase01a-a4';o=r/'retest-variant';crops=json.loads((o/'crops.json').read_text('utf-8'))
features=[
('S_safety_photo','V06S',237.4,[236.4,236.6,236.8,237,237.2,237.4],(480,1000,610,1150)),
('S_quality_photo','V06S',239,[238.1,238.2,238.3,238.4,238.6,238.8,239],(1500,850,1760,1030)),
('S_schedule_document','V06S',240.2,[239.2,239.3,239.4,239.6,239.8,240,240.2],(2070,800,2200,1000)),
('S_schedule_monitor','V06S',240.2,[239.2,239.3,239.4,239.6,239.8,240,240.2],(2430,1100,2630,1230)),
('S_schedule_label','V06S',240.2,[239.3,239.4,239.6,239.8,240,240.2],(2240,1525,2450,1660)),
('S_eff_people','V06S',242,[240.6,240.8,241,241.2,241.5,242],(3120,1080,3230,1200)),
('W_safety_photo','V06W',242,[241.1,241.2,241.3,241.4,241.6,241.8,242],(2300,740,2500,970)),
('W_quality_photo','V06W',243.6,[242.6,242.8,243,243.2,243.4,243.6],(4020,450,4350,650)),
('W_schedule_document','V06W',245.2,[244.2,244.4,244.6,244.8,245,245.2],(4900,450,5100,690)),
('W_schedule_monitor','V06W',245.2,[244.2,244.4,244.6,244.8,245,245.2],(5400,850,5700,1050)),
('W_schedule_label','V06W',245.2,[244.2,244.4,244.6,244.8,245,245.2],(5210,1690,5530,1860))]
fs={}
for sid,c in [('A4-S','V06S'),('A4-W','V06W')]:
 a=[]
 for ph in [c,c+'_retest_more']:a+=json.loads((r/'cases'/sid/ph/'실행기록.json').read_text('utf-8'))['frames']
 fs[c]={float(Fraction(f['actual_playback_seconds'])):f for f in a}
results=[]
for name,c,anchor,ts,b in features:
 im=np.asarray(Image.open(fs[c][anchor]['path']).convert('L'),dtype=np.float32);x1,y1,x2,y2=b;tmpl=im[y1:y2,x1:x2];v=tmpl-tmpl.mean();norm=np.sqrt((v*v).sum());samples=[]
 for t in ts:
  f=fs[c][t];im=np.asarray(Image.open(f['path']).convert('L'),dtype=np.float32);best=(-2,None,None)
  for dx in [-2,0,2]:
   for dy in range(-10,161):
    a=im[y1+dy:y2+dy,x1+dx:x2+dx];z=a-a.mean();score=float((z*v).sum()/max(1e-6,np.sqrt((z*z).sum())*norm))
    if score>best[0]:best=(score,dx,dy)
  samples.append(dict(actual_seconds=f['actual_playback_seconds'],path=f['path'],dy_native_pixels=best[2],dx_native_pixels=best[1],ncc=round(best[0],5)))
 results.append(dict(target=name,feature_box_at_anchor=list(b),anchor_seconds=anchor,method='fixed-size grayscale zero-mean normalized cross correlation; integer y offsets -10..160, x offsets -2/0/2; relative to settled template; photometric mixing and partial reveal can bias',tracking_uncertainty='at least 2 px; non-rigid/reveal low NCC cases not treated as translation',samples=samples))
 print(name,[(float(Fraction(s['actual_seconds'])),s['dy_native_pixels'],s['ncc']) for s in samples])
(o/'measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8')
