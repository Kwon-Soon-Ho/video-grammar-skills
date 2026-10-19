from pathlib import Path
from fractions import Fraction as F
import json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;OUT=HERE/'검수판';font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
run=json.loads((HERE/'cases/자료013/eg_fine/실행기록.json').read_text(encoding='utf-8'));fs={F(f['actual_playback_seconds']):f for f in run['frames']}
times=['12.9','13.1','13.4','13.8','14.5','15'];crop=(400,200,2350,1700);w=640;h=492
canvas=Image.new('RGB',(1920,2*(h+30)),'#20242c');d=ImageDraw.Draw(canvas)
for i,t in enumerate(times):
    im=Image.open(fs[F(t)]['path']).crop(crop).resize((w,h),Image.Resampling.LANCZOS);x=i%3*w;y=i//3*(h+30);canvas.paste(im,(x,y+30));d.text((x+5,y+2),f'{t}s | connector behind model',font=font,fill='white')
canvas.save(OUT/'추가발견_모델_연결면.jpg',quality=96)
# Simple readable second-pass sheets, not fabricated source playback.
for aid,group,name in [('자료005','jh_all','장헌_역순'),('자료013','eg_intro','EG도입_역순')]:
    rr=json.loads((HERE/'cases'/aid/group/'실행기록.json').read_text(encoding='utf-8'));chosen=list(reversed(rr['frames']))[::3]
    cw=800 if aid=='자료005' else 640;ch=225 if aid=='자료005' else 360;cols=2 if aid=='자료005' else 3
    can=Image.new('RGB',(cols*cw,((len(chosen)+cols-1)//cols)*(ch+26)),'#20242c');draw=ImageDraw.Draw(can)
    for i,f in enumerate(chosen):
        im=Image.open(f['path']).resize((cw,ch),Image.Resampling.LANCZOS);x=i%cols*cw;y=i//cols*(ch+26);can.paste(im,(x,y));draw.text((x+6,y+ch+2),f'{float(F(f["actual_playback_seconds"])):.3f}s',font=font,fill='white')
    can.save(OUT/(name+'_전체.jpg'),quality=96)
