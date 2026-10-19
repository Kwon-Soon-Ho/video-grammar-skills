from pathlib import Path
import sys,json
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
B=Path('phase01a-a5b').resolve(); d=B/'trials/H02-r1-without_skill/support'
base=json.loads((B/'cases/A5-A/H02/실행기록.json').read_text(encoding='utf-8'))['frames'];extra=json.loads((B/'cases/A5-A/H02-r1-without_skill-extra1/실행기록.json').read_text(encoding='utf-8'))['frames']
from fractions import Fraction
rows={float(Fraction(x['actual_playback_seconds'])):x for x in base+extra}
specs=[('main',t,[740,900,1740,1710]) for t in [13.0,13.2,13.6,14.4,16.8,17.1,17.3,17.4,17.5,17.8]]
specs += [('title',13.6,[1870,450,3240,1320])]
specs += [('small',t,[2450,1490,2950,1800]) for t in [12.0,12.8,13.6,14.4,16.8,17.4]]
reg=[]
for i,(name,t,box) in enumerate(specs,1):
 p=d/f'crop-{i:02d}-{name}-{t:.1f}.png';parent=Path(rows[t]['path']);im=Image.open(parent).convert('RGB');im.crop(box).save(p)
 reg.append({'path':str(p),'parent_path':str(parent),'crop_xyxy_native_pixels':box})
(d/'crops.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'path':x['path']} for x in reg],ensure_ascii=False))
