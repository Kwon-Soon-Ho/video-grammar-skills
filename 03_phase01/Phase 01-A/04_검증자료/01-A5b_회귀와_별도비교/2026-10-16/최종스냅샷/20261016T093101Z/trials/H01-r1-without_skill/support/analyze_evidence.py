from pathlib import Path
import sys,json,hashlib
from fractions import Fraction
sys.path.insert(0,str(Path.cwd()/'phase01a-a1/후보런타임'))
from PIL import Image
import numpy as np
B=Path.cwd()/'phase01a-a5b'; R=B/'trials/H01-r1-without_skill'; S=R/'support'
logs=[B/'cases/A5-T/H01/실행기록.json',B/'cases/A5-T/H01-r1-without_skill-extra1/실행기록.json',B/'cases/A5-T/H01-r1-without_skill-extra2/실행기록.json']
data=[json.loads(p.read_text(encoding='utf-8')) for p in logs]
rows=[r for d in data for r in d['frames']]
bytime={Fraction(r['actual_playback_seconds']):r for r in rows}
crops=[]
def crop(row,box,label):
 p=Path(row['path']); q=S/(label+'.png'); im=Image.open(p).convert('RGB'); im.crop(box).save(q)
 crops.append({'path':str(q),'parent_path':str(p),'crop_xyxy_native_pixels':list(box)})
for t in ['4.3','4.4','4.5','4.6','4.8']:
 crop(bytime[Fraction(t)],(2750,1460,3350,1550),'subtitle_'+t)
for t in ['5.2','5.6','6','6.4']:
 crop(bytime[Fraction(t)],(1940,1560,3300,1710),'body_'+t)
for t in ['1.6','2.4','2.8']:
 crop(bytime[Fraction(t)],(300,800,1850,1560),'curl_'+t)
metrics=[]
for r in data[2]['frames']:
 im=np.array(Image.open(r['path']).convert('RGB'))
 # T map stem left edge at y=1000; only map has all RGB channels above 140 here.
 inds=np.where((im[1000,:,:].min(axis=1)>140))[0]
 x=int(inds[0]) if len(inds) else None
 inds_top=np.where((im[800,:,:].min(axis=1)>140))[0]
 xt=int(inds_top[0]) if len(inds_top) else None
 # fixed row cannot show stem before it enters the frame.
 if x is None: box=(1800,650,3800,1050)
 else:
  l=max(0,min(1840,x-500)); box=(l,750,l+2000,1100)
 t=r['actual_playback_seconds']; crop(r,box,'map_'+t.replace('/','_'))
 metrics.append({'actual_seconds':t,'stem_left_x_at_native_y1000':x,'topbar_left_x_at_native_y800':xt,'unit':'native_RGB_pixels','evidence_parent':r['path']})
(S/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),encoding='utf-8')
(S/'map-measurements.json').write_text(json.dumps({'method':'각 PNG native RGB y=1000행에서 RGB 최솟값>140인 첫 x. T 내부 지도 선은 임계값보다 어둡기에 시작 경계 1~수 픽셀 오차 가능. 글자/설명문은 y>1200이라 해당하지 않음. SAR 미상, 디스플레이 물리 단위 아님. 첫 진입 전 None.','rows':metrics},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'crops':len(crops),'metrics':metrics},ensure_ascii=False,indent=2))
