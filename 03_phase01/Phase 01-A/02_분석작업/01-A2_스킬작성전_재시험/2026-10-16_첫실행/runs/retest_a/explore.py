from pathlib import Path
from PIL import Image,ImageDraw
import json
import numpy as np

ROOT=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT=ROOT/'runs/retest_a'
IN=ROOT/'analysis_input/cases'
audit=[]

def load(p):
    audit.append(str(p));return Image.open(p).convert('RGB')

def sheet(items,name,cols=2):
    w=max(im.width for label,im in items);h=max(im.height for label,im in items)+30
    board=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*h),(28,31,36));d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(items):
        x=(i%cols)*w;y=(i//cols)*h
        board.paste(im,(x,y+30));d.text((x+4,y+7),label,fill='white')
    p=OUT/name;board.save(p);return str(p)

t01=IN/'자료013/T01'
files=sorted(t01.glob('f_*.png'))
summary=[]
artifact=[];body=[];left=[]
for p in files:
    im=load(p);a=np.asarray(im);t=float(p.stem.split('_')[-1]);entry={'time':t,'path':str(p),'size':im.size}
    for name,box in [('bg_left',(0,300,650,700)),('bg_topright',(2300,0,3300,650)),('title',(2260,1060,3300,1320)),('subtitle',(2260,1340,3300,1450)),('body',(2260,1470,3700,1790))]:
        x1,y1,x2,y2=box;ar=a[y1:y2,x1:x2];entry[name+'_mean_rgb']=[round(float(v),3) for v in ar.mean(axis=(0,1))]
    # gold pixels, only useful after the color change starts
    ar=a[:,:2200];mask=(ar[:,:,0]>ar[:,:,1]*1.12)&(ar[:,:,0]>ar[:,:,2]*1.45)&(ar[:,:,0]>65)
    ys,xs=np.where(mask)
    entry['gold_bbox']= [int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None
    summary.append(entry)
    if t<=4.0:
        artifact.append((f'{t:.3f}s native crop x3100..3700 y850..1250',im.crop((3100,850,3700,1250))))
        body.append((f'{t:.3f}s native crop x2250..3700 y1460..1800',im.crop((2250,1460,3700,1800))))
    if t in [3.5,3.6,3.7,3.8,3.9,4.0,4.2,4.4,4.6,4.8,5.0,5.5]:
        left.append((f'{t:.3f}s left half 50pct overview',im.crop((0,0,2200,2160)).resize((550,540))))
sheet(artifact,'T01_artifact_native_sequence.png',2)
sheet(body,'T01_body_native_sequence.png',1)
sheet(left,'T01_left_sequence.png',3)
(OUT/'T01_measurements_exploratory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'explore_reads.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared T01 crops and measurements from',len(files),'assigned PNGs')
