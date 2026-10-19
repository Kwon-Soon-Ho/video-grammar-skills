import sys,json
from pathlib import Path
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
b=Path('phase01a-a5b').resolve();d=b/'trials/H01-r1-with_skill';s=d/'support';s.mkdir(exist_ok=True)
logs=[b/'cases/A5-T/H01/실행기록.json',b/'cases/A5-T/H01-r1-with_skill-extra1/실행기록.json']
from fractions import Fraction
frames={Fraction(f['actual_playback_seconds']):f for l in logs for f in json.loads(l.read_text(encoding='utf-8'))['frames']}
crops=[]
sets=[('title',[1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8,3,3.2,3.3],[250,950,1800,1570]),('logo',[3.4,3.5,3.6,3.7,3.8,4,4.4,4.8,5.2,5.6,6.4],[1900,1200,3350,1710])]
for name,times,box in sets:
 for t in times:
  f=frames[Fraction(str(t))];p=s/f'{name}_{t:.1f}.png'
  Image.open(f['path']).convert('RGB').crop(box).save(p)
  crops.append({'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':box})
(s/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),encoding='utf-8')
print('created',len(crops))
