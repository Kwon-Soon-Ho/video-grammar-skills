from pathlib import Path
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import json
HERE=Path(__file__).resolve().parent;OUT=HERE/'detail-review';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
for aid,box,w,h,per in [('NEW-N',(4900,140,7200,700),600,170,27),('NEW-P',(1400,40,2500,1280),360,430,12)]:
 for phase in ('detail1','detail2','detail3'):
  log=HERE/'cases'/aid/phase/'실행기록.json'
  if not log.exists():continue
  frames=json.loads(log.read_text(encoding='utf-8'))['frames']
  for start in range(0,len(frames),per):
   batch=frames[start:start+per];sheet=Image.new('RGB',(w*3,h*((len(batch)+2)//3)),'#181818');draw=ImageDraw.Draw(sheet)
   for k,f in enumerate(batch):
    with Image.open(f['path']) as im:region=im.crop(box);region.thumbnail((w,h-25));x=k%3*w;y=k//3*h;sheet.paste(region,(x,y+25));draw.text((x+5,y+2),f'{aid}  {float(F(f["actual_playback_seconds"])):.3f}',fill='white',font=font)
   dest=OUT/(aid+'-'+phase+'-'+str(start//per+1)+'.jpg');sheet.save(dest,quality=94)
print('detail contact sheets created; visual observation required')
