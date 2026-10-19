from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for aid in ['자료005','자료013']:
    folder=HERE/'cases'/aid/'scan'
    if not (folder/'실행기록.json').exists():continue
    run=json.loads((folder/'실행기록.json').read_text(encoding='utf-8'));frames=run['frames']
    # Split overview so labels and artwork are not reduced into a single tall sheet.
    for part in range(math.ceil(len(frames)/12)):
        picked=frames[part*12:(part+1)*12];cols=2 if aid=='자료005' else 3;w=800 if cols==2 else 640;h=225 if cols==2 else 360
        sheet=Image.new('RGB',(cols*w,math.ceil(len(picked)/cols)*(h+28)),'#20242c');draw=ImageDraw.Draw(sheet)
        for i,f in enumerate(picked):
            x=i%cols*w;y=i//cols*(h+28);im=Image.open(f['path']).resize((w,h),Image.Resampling.LANCZOS);sheet.paste(im,(x,y));draw.text((x+5,y+h+3),f"{float(F(f['actual_playback_seconds'])):.3f}s",font=font,fill='white')
        sheet.save(HERE/f'{aid}_전체동작_{part+1}.jpg',quality=94)
    proxy=np.load(folder/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb']
    dif=np.array([np.abs(proxy[i].astype(np.int16)-proxy[i-1].astype(np.int16)).mean() for i in range(1,len(proxy))])
    index=json.loads((folder/'전프레임_시각색인.json').read_text(encoding='utf-8'))
    moving=[{'time':index[i+1]['seconds'],'global_mean_abs_pixel_delta':round(float(d),4)} for i,d in enumerate(dif)]
    (HERE/f'{aid}_프레임간변화.json').write_text(json.dumps(moving,ensure_ascii=False,indent=2),encoding='utf-8')
    print(aid,run['tracking_proxy']['shape'],'max delta',float(dif.max()),'max time',index[int(dif.argmax())+1]['seconds'])
