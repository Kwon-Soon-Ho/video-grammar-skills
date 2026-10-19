"""Build pixel-exact ROI evidence and descriptive temporal measurements."""
from pathlib import Path
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OUT=HERE/'inspection';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',16)
def load(p):return json.loads(Path(p).read_text('utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def frames(code):
    result={}
    roots=[WORK/'analysis-reliability-20261019/fresh/cases'/code,HERE/'extraction/cases'/code]
    for root in roots:
        for p in root.glob('*/실행기록.json'):
            d=load(p)
            if d.get('complete_target_selection'):
                for f in d['frames']:result.setdefault(F(f['actual_playback_seconds']),f)
    return result
N=frames('NEW-N');P=frames('NEW-P');spec=[]
def board(name,items,box,cols,thumb):
    tiles=[]
    for t,row in items:
        with Image.open(row['path']) as im:crop=im.crop(box)
        p=OUT/(name+'-'+str(float(t))+'.png');crop.save(p)
        spec.append({'path':str(p),'parent_path':row['path'],'crop_xyxy_native_pixels':list(box)})
        crop.thumbnail(thumb);tiles.append((t,crop))
    w=thumb[0];h=thumb[1]+26;out=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),'#151515');draw=ImageDraw.Draw(out)
    for i,(t,im) in enumerate(tiles):
        x=i%cols*w;y=i//cols*h;out.paste(im,(x,y+26));draw.text((x+3,y+3),f'{float(t):.3f}',font=font,fill='white')
    out.save(OUT/(name+'.jpg'),quality=95)
def pick(data,ts):return [(F(str(t)),data[F(str(t))]) for t in ts]
board('N-left-label',pick(N,[173,173.2,173.4,173.6,173.8,174,174.2,174.4,174.6,175]),(1050,160,3300,500),2,(675,102))
board('N-tail-states',pick(N,[174.5,175,175.5,176,176.5,177,177.5,178,178.5,179,179.5,180,180.5,181,181.2,181.4]),(650,0,3900,2050),4,(520,328))
board('N-arcs-paired',pick(N,[168,168.5,169,169.5,170,170.5,171,171.5,172,172.5,173,173.5,174,174.5,175,176]),(500,500,2800,2160),4,(460,332))
board('P-late-layout',pick(P,[48,49,50,51,51.5,52,52.5,53,53.4]),(0,0,2800,1450),3,(560,290))
board('P-line-birth',pick(P,[42.4,42.5,42.6,42.7,42.8,42.9,43,43.1,43.2,43.3,43.4,43.5]),(1830,580,2020,880),6,(190,300))
board('P-policy-phases',pick(P,[40,40.5,41,41.5,42,42.5,43,43.5,44,44.5,45,45.5,46,46.5,47,47.5,48,48.5,49,49.5,50,50.5,51]),(170,100,2420,630),3,(750,177))
# Descriptive pixel signals, not opacity or AE curve recovery. Keep native ROIs fixed.
metrics=[]
for code,data,start,end,regions in [
 ('N',N,F(166),F('181.4'),{'bg-left':(0,300,500,1400),'bg-right':(7150,0,7680,1400),'front-arcs':(500,500,2800,2160),'rear-arcs':(2800,0,3840,750),'section-arcs':(4800,400,7000,1850)}),
 ('P',P,F(40),F(51),{'police-row1':(320,320,1050,360),'police-row2':(320,465,1050,505),'regional-row1':(1520,250,2250,290),'regional-row2':(1520,440,2250,480)})]:
    for t,row in sorted(data.items()):
        if not start<=t<=end:continue
        if t.denominator not in (1,2,5,10):continue
        with Image.open(row['path']) as im:
            for name,box in regions.items():
                a=np.asarray(im.crop(box),dtype=np.int16);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
                mask=(g-r>50)&(g>140)&(g*10>b*9)
                metrics.append({'source':code,'actual_seconds':str(t),'region':name,'box':box,'mean_RGB':a.mean(axis=(0,1)).tolist(),'bright_cyan_count':int(mask.sum()),'positive_green_minus_red_energy':float(np.maximum(g-r-40,0).sum()),'parent_path':row['path']})
write(OUT/'temporal-signals.json',{'method':'Fixed native ROI mean 8-bit RGB and cyan threshold counts; compression, overlap and area changes are not separated. No actual opacity/easing or motion truth inferred automatically.','samples':metrics})
write(OUT/'crop-inputs.json',spec)
print(json.dumps({'crops':len(spec),'metric_rows':len(metrics)},ensure_ascii=False))
