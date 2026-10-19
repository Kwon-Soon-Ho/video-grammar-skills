from pathlib import Path
import json,sys,math
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
case=sys.argv[1];groups=json.loads((HERE/'groups.json').read_text(encoding='utf-8'));aid=groups[case]['id']
folder=HERE/'cases'/aid/case;run=json.loads((folder/'실행기록.json').read_text(encoding='utf-8'));records=[]
for part in range(math.ceil(len(run['frames'])/12)):
    fs=run['frames'][part*12:part*12+12];w=800 if aid=='자료005' else 640;h=225 if aid=='자료005' else 360;cols=2 if aid=='자료005' else 3
    canvas=Image.new('RGB',(cols*w,math.ceil(len(fs)/cols)*(h+26)),'#20242c');d=ImageDraw.Draw(canvas)
    for i,f in enumerate(fs):
        x=i%cols*w;y=i//cols*(h+26);im=Image.open(f['path']).resize((w,h),Image.Resampling.LANCZOS);canvas.paste(im,(x,y));d.text((x+5,y+h+2),f'{float(F(f["actual_playback_seconds"])):.3f}s',font=font,fill='white')
    dest=folder/f'board_{part+1}.jpg';canvas.save(dest,quality=96);records.append(str(dest))
(folder/'boards.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(json.dumps(records))
