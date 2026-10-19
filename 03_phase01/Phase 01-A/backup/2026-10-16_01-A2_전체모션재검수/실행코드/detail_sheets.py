from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fractions import Fraction as F
import json,math
HERE=Path(__file__).resolve().parent;font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for aid,group in [('자료005','jh_detail'),('자료013','eg_title'),('자료013','eg_screens'),('자료013','eg_model')]:
    r=json.loads((HERE/'cases'/aid/group/'실행기록.json').read_text(encoding='utf-8'))
    for part in range(math.ceil(len(r['frames'])/15)):
        fs=r['frames'][15*part:15*(part+1)];w=640;h=180 if aid=='자료005' else 360
        im=Image.new('RGB',(1920,math.ceil(len(fs)/3)*(h+28)),'#20242c');d=ImageDraw.Draw(im)
        for i,f in enumerate(fs):
            x=i%3*w;y=i//3*(h+28);p=Image.open(f['path']).resize((w,h),Image.Resampling.LANCZOS);im.paste(p,(x,y));d.text((x+7,y+h+3),f"{float(F(f['actual_playback_seconds'])):.3f}s",font=font,fill='white')
        dest=HERE/f'{group}_상세표본_{part+1}.jpg';im.save(dest,quality=95);print(dest)
