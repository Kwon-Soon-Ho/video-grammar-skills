import sys,json
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'phase01a-a1/후보런타임');from PIL import Image
b=Path('phase01a-a5b').resolve();s=b/'trials/H01-r1-with_skill/support'
logs=[b/'cases/A5-T/H01/실행기록.json',b/'cases/A5-T/H01-r1-with_skill-extra1/실행기록.json',b/'cases/A5-T/H01-r1-with_skill-extra2/실행기록.json']
f={Fraction(x['actual_playback_seconds']):x for l in logs for x in json.loads(l.read_text(encoding='utf-8'))['frames']}
c=json.loads((s/'crops.json').read_text(encoding='utf-8'))
for name,times,box in [('logo',[3.9,4.1,4.2,4.3,4.5,4.6,5,5.4,5.8],[1900,1200,3350,1710]),('dim',[3.6,4,4.8],[250,950,1800,1570]),('overlap',[7.2,7.4,8],[900,1150,2000,1580])]:
 for t in times:
  q=f[Fraction(str(t))];p=s/f'{name}_{t:.1f}.png';Image.open(q['path']).convert('RGB').crop(box).save(p);c.append({'path':str(p),'parent_path':q['path'],'crop_xyxy_native_pixels':box})
(s/'crops.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8');print('crops',len(c))
print(json.dumps([{'actual':q['actual_playback_seconds'],'path':q['path']} for q in json.loads(logs[-1].read_text(encoding='utf-8'))['frames']],ensure_ascii=False))
