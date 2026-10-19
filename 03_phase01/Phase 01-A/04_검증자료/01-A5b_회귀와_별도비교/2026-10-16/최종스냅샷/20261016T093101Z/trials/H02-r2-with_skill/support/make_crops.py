from pathlib import Path
import json,sys
from fractions import Fraction
sys.path.insert(0,str(Path.cwd()/'phase01a-a1/후보런타임'))
from PIL import Image
B=Path.cwd()/'phase01a-a5b'
D=B/'trials/H02-r2-with_skill/support'
rows=[]
for folder, times in [('H02',[13.2,13.6,14,14.4,14.8,15.2,15.6,16,16.4,16.8,17.2]),('H02-r2-with_skill-extra1',[13.1,13.3,13.4,13.5,17,17.1,17.3,17.4])]:
 log=json.loads((B/'cases/A5-A'/folder/'실행기록.json').read_text(encoding='utf-8'))
 for f in log['frames']:
  t=float(Fraction(f['actual_playback_seconds']))
  if t not in times:continue
  path=D/f'crop-main-{t:.3f}.png'; box=[750,920,1730,1700]
  with Image.open(f['path']) as im:im.crop(box).save(path)
  rows.append(dict(path=str(path),parent_path=f['path'],crop_xyxy_native_pixels=box))
(D/'crops.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
