from pathlib import Path
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OLD=WORK/'analysis-reliability-20261019/fresh';OUT=HERE/'probes';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
spec=[]
def frames(aid,phases):
    result={}
    for phase in phases:
        log=json.loads((OLD/'cases'/aid/phase/'실행기록.json').read_text(encoding='utf-8'))
        for f in log['frames']:result[F(f['actual_playback_seconds'])]=f
    return result
N=frames('NEW-N',['window','detail1','detail2','detail3']);P=frames('NEW-P',['window','detail1','detail2','detail3'])
def board(name,items,box,columns=4,thumb=None):
    crops=[]
    for t,source in items:
        with Image.open(source['path']) as im:crop=im.crop(box)
        p=OUT/(name+'-'+str(float(t))+'.png');crop.save(p)
        spec.append({'path':str(p),'parent_path':source['path'],'crop_xyxy_native_pixels':list(box)})
        if thumb:crop.thumbnail(thumb)
        crops.append((t,crop))
    w=max(i.width for _,i in crops);h=max(i.height for _,i in crops)+27
    sheet=Image.new('RGB',(columns*w,((len(crops)+columns-1)//columns)*h),'#171717');draw=ImageDraw.Draw(sheet)
    for k,(t,crop) in enumerate(crops):
        x=k%columns*w;y=k//columns*h;sheet.paste(crop,(x,y+27));draw.text((x+4,y+3),f'{float(t):.3f}',font=font,fill='white')
    sheet.save(OUT/(name+'.jpg'),quality=95)
board('N-rear',[(F(str(t)),N[F(str(t))]) for t in (168.5,169,169.5,170,170.5,171,171.5,172,172.5,173,173.5,174)],(2800,0,3840,750),3,(520,375))
board('N-background-right',[(F(t),N[F(t)]) for t in (166,168,170,172,174)],(7150,0,7680,1400),5,(265,700))
board('N-background-left',[(F(t),N[F(t)]) for t in (166,168,170,172,174)],(0,300,500,1400),5,(250,550))
board('P-connector',[(F(str(t)),P[F(str(t))]) for t in (43.8,43.9,44,44.1,44.2,44.3,44.4,44.5,45,45.1,45.2,45.3)],(1860,620,1980,850),6)
# Pixel differences are an aid for choosing visual probes, never a motion verdict.
stats=[]
for label,box in [('right',(7150,0,7680,1400)),('left',(0,300,500,1400))]:
    base=None
    for t in (166,168,170,172,174):
        with Image.open(N[F(t)]['path']) as im:a=np.asarray(im.crop(box),dtype=np.int16)
        if base is None:base=a
        delta=np.abs(a-base);stats.append({'region':label,'time':t,'mean_abs_rgb_difference_from_166':float(delta.mean()),'max_difference':int(delta.max()),'interpretation':'pixel difference only; compression and actual change not separated'})
(OUT/'pixel-difference-aid.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'crop-inputs.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'crops':len(spec),'contact_sheets':4},ensure_ascii=False))
