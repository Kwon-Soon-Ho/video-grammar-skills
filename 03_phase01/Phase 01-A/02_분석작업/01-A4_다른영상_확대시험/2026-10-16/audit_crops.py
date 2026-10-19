from pathlib import Path
import json
from fractions import Fraction
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parent
D=B/'root-audit';D.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
specs=[('A4-D','V01',[1.2,1.6,2,2.4],(100,80,1300,290)),('A4-D','V02',[130,130.8,132.8,135.2],(2050,460,3580,750)),('A4-L','V03',[98.75,99,99.25,99.5],(80,820,1370,1230)),('A4-L','V04',[298.5,298.75,299,301],(200,670,2620,1860)),('A4-G','V05',[1.2,1.6,2,2.8],(2300,620,3840,1300)),('A4-S','V06S',[236.5,237,237.5,238],(180,900,990,1800)),('A4-W','V06W',[240.5,241,248,248.5],(50,100,1550,2100))]
records=[]
for aid,cid,times,box in specs:
 frames=json.loads((B/'cases'/aid/cid/'실행기록.json').read_text(encoding='utf-8'))['frames']
 for t in times:
  row=min(frames,key=lambda f:abs(float(Fraction(f['actual_playback_seconds']))-t))
  assert abs(float(Fraction(row['actual_playback_seconds']))-t)<0.04
  im=Image.open(row['path']).crop(box)
  p=D/f'{cid}-{t}.png';im.save(p)
  records.append({'path':str(p),'source_frame':row['path'],'actual_seconds':row['actual_playback_seconds'],'crop_xyxy_native':box,'resize':None})
(D/'crop-map.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
