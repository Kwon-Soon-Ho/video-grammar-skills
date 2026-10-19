from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
from prepare import OUT,write,sha
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for aid in ['자료005','자료013']:
    for phase in ['initial','detail']:
        p=OUT/'cases'/aid/phase/'실행기록.json'
        if not p.exists():continue
        r=json.loads(p.read_text(encoding='utf-8'));frames=r['frames'];cols=2 if aid=='자료005' else 3
        w=800 if aid=='자료005' else 640;h=225 if aid=='자료005' else 360
        sheet=Image.new('RGB',(cols*w,math.ceil(len(frames)/cols)*(h+30)),(25,25,25));draw=ImageDraw.Draw(sheet)
        for i,f in enumerate(frames):
            im=Image.open(f['path']).resize((w,h),Image.Resampling.LANCZOS);x=i%cols*w;y=i//cols*(h+30);sheet.paste(im,(x,y));draw.text((x+6,y+h+4),f"{float(__import__('fractions').Fraction(f['actual_playback_seconds'])):.3f}s | ordinal {f['display_ordinal_zero_based']}",font=font,fill='white')
        dest=p.parent/'검토용_연락시트.jpg';sheet.save(dest,quality=92)
        write(p.parent/'연락시트_파생기록.json',{'path':str(dest),'sha256':sha(dest),'sources':[f['sha256'] for f in frames],'scope':'layout preview only; text verified on individual derived PNG','resampling':'LANCZOS','added_labels':'tool reported presentation time and ordinal'})
        print(dest)
