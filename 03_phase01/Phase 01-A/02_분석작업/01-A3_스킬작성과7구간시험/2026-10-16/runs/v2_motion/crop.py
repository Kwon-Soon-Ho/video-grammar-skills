from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path('phase01a-a3/runs/v2_motion')
for aid,tag in [('자료005','chartdetail'),('자료013','motiondetail')]:
 d=root/'cases'/aid/tag
 j=json.loads((d/'실행기록.json').read_text(encoding='utf8'))
 print(aid, j['frames'][0]['raster'],j['frames'][0]['derived_size'])
 for f in j['frames']:
  im=Image.open(f['path']);t=float(__import__('fractions').Fraction(f['actual_playback_seconds']))
  if aid=='자료005':
   box=(0,0,3840,1080) if t<6.4 else ((980,290,1900,750) if t<10 else ((1940,290,2840,750) if t<16.7 else (2900,290,3800,750)))
  else: box=(200,250,2350,1650)
  crop=im.crop(box);dest=root/f'{aid}_{t:.3f}_roi.png';crop.save(dest)
  if aid=='자료013':
   crop.thumbnail((900,600))
  elif t<6.4:crop.thumbnail((1200,400))
  h=Image.new('RGB',(crop.width,crop.height+28),'#20252c');h.paste(crop,(0,28));ImageDraw.Draw(h).text((10,7),str(t),fill='white');h.save(root/f'{aid}_{t:.3f}_preview.jpg')
