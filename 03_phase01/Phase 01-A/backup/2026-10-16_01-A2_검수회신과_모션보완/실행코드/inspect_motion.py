from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fractions import Fraction as F
import json
HERE=Path(__file__).resolve().parent
RUN=HERE.parent/'phase01a-a2/cases/자료013/motion_review'
r=json.loads((RUN/'실행기록.json').read_text(encoding='utf-8'))
selected=[x for x in r['frames'] if F(x['actual_playback_seconds']) in [F(str(t)) for t in [4,4.1,4.2,4.3,4.4,4.5,4.6,4.8,5,5.5]]]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
im=Image.new('RGB',(1920,4*390),'#20242c');draw=ImageDraw.Draw(im)
for i,f in enumerate(selected):
    x=i%3*640;y=i//3*390;frame=Image.open(f['path']).resize((640,360),Image.Resampling.LANCZOS);im.paste(frame,(x,y+30));draw.text((x+8,y+3),str(float(F(f['actual_playback_seconds'])))+'s',font=font,fill='white')
im.save(HERE/'E_진입_상세표본.jpg',quality=95)
print(HERE/'E_진입_상세표본.jpg')
