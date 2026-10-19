from PIL import Image
import json
from pathlib import Path
from fractions import Fraction
root=Path.cwd()/'phase01a-a4'; dest=root/'retest-variant'; crops=[]
for sid,case,ts,regions in [
('A4-S','V06S',[237,238.5,239,240,241,242,244,244.5,245,245.5,246], {'cards':(100,650,3750,1750),'title':(1260,150,2600,500),'subtitle':(300,1920,3400,2070)}),
('A4-W','V06W',[236,239,241,242,243,244,245,246,247,248,249,249.5,250],{'cards':(1800,150,7600,1900),'title':(0,0,1600,2150),'subtitle':(2200,1920,5500,2070)})]:
 log=json.loads((root/'cases'/sid/case/'실행기록.json').read_text('utf-8-sig'))
 for f in log['frames']:
  t=float(Fraction(f['actual_playback_seconds']))
  if t not in ts:continue
  im=Image.open(f['path']).convert('RGB')
  for name,box in regions.items():
   if name=='cards':
    # split four cards into native crops
    boxes=[(100,650,1000,1750),(1000,650,1900,1750),(1900,650,2800,1750),(2800,650,3750,1750)] if sid=='A4-S' else [(1800,150,3200,1900),(3200,150,4600,1900),(4600,150,6050,1900),(6050,150,7600,1900)]
   else: boxes=[box]
   for k,b in enumerate(boxes):
    p=dest/f'{case}_{t:g}_{name}{k}.png'; im.crop(b).save(p)
    crops.append(dict(path=str(p),parent_path=f['path'],crop_xyxy_native_pixels=list(b)))
(dest/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),'utf-8')
