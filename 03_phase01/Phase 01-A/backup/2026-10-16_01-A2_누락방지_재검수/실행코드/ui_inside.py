from pathlib import Path
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import json
HERE=Path(__file__).resolve().parent;OUT=HERE/'검수판';font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
run=json.loads((HERE/'cases/자료013/eg_late/실행기록.json').read_text(encoding='utf-8'));frames=[f for f in run['frames'] if F('7.7')<=F(f['actual_playback_seconds'])<=F('10.4')]
w=760;h=435;canvas=Image.new('RGB',(w*2,((len(frames)+1)//2)*(h+28)),'#20242c');d=ImageDraw.Draw(canvas)
for i,f in enumerate(frames):
    im=Image.open(f['path']).crop((90,100,850,535));x=i%2*w;y=i//2*(h+28);canvas.paste(im,(x,y+28));d.text((x+5,y+2),f'{float(F(f["actual_playback_seconds"])):.3f}s',font=font,fill='white')
canvas.save(OUT/'추가발견_UI내부_선택변화.jpg',quality=97)
print(len(frames))
