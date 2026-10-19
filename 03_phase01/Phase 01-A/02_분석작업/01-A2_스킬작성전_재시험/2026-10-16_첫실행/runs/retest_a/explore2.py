from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
ROOT=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT=ROOT/'runs/retest_a';audit=[]
def load(p):
    audit.append(str(p));return Image.open(p).convert('RGB')
def sheet(items,name,cols=2):
    w=max(im.width for label,im in items);h=max(im.height for label,im in items)+25
    board=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*h),(28,31,36));d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(items):
        x=(i%cols)*w;y=(i//cols)*h;board.paste(im,(x,y+25));d.text((x+4,y+6),label,fill='white')
    board.save(OUT/name)
base=ROOT/'analysis_input/cases/자료013/T01';a01=[]
for p in sorted(base.glob('f_*.png')):
    im=load(p);a=np.asarray(im);t=float(p.stem.split('_')[-1]);entry={'time':t}
    for name,box in [('title',(2230,1040,3320,1320)),('subtitle',(2250,1340,3320,1450)),('body_top',(2250,1470,3700,1610)),('body_bottom',(2250,1610,3700,1810))]:
        x1,y1,x2,y2=box;ar=a[y1:y2,x1:x2];mask=(ar.min(axis=2)>160);ys,xs=np.where(mask)
        entry[name]={'bbox':[int(xs.min()+x1),int(ys.min()+y1),int(xs.max()+x1),int(ys.max()+y1)] if len(xs) else None,'bright_pixels':int(mask.sum()),'bright_mean':float(ar[mask].mean()) if len(xs) else None}
    for y in [100,400,900,1400,2000]:
        row=a[y,:2250];mask=row[:,1]>60;xx=np.where(mask)[0]
        entry[f'row{y}_green_gt60_span']=[int(xx.min()),int(xx.max())] if len(xx) else None
    a01.append(entry)
(OUT/'T01_geometry_exploratory.json').write_text(json.dumps(a01,ensure_ascii=False,indent=2),encoding='utf8')

extra=OUT/'cases/자료005/extra1';transition=[];c1=[];c2=[];c3=[];imgs={}
for p in sorted(extra.glob('f_*.png')):
    im=load(p);t=float(p.stem.split('_')[-1]);imgs[t]=np.asarray(im)
    if t<=6.5:transition.append((f'{t:.3f}s full frame 25pct',im.resize((960,270))))
    if 7.8<=t<=9.2:c1.append((f'{t:.3f}s native card 1',im.crop((980,170,1900,760))))
    if 14.8<=t<=16.8:c2.append((f'{t:.3f}s native card 2',im.crop((1940,170,2860,760))))
    if 16.4<=t<=18:c3.append((f'{t:.3f}s native card 3',im.crop((2900,170,3820,760))))
sheet(transition,'T04_transition_sequence.png',2)
sheet(c1,'T04_card1_native_sequence.png',2)
sheet(c2,'T04_card2_native_sequence.png',2)
sheet(c3,'T04_card3_native_sequence.png',2)
comparisons=[]
for ta,tb in [(8,9.2),(9.2,14.8),(14.8,15.2),(16.8,18)]:
    aa=imgs[ta].astype('int16');bb=imgs[tb].astype('int16')
    for name,box in [('left_text',(0,0,960,760)),('sky',(0,0,3840,170)),('bottom_city_water',(0,780,3840,1080)),('card1',(980,170,1900,760)),('card2',(1940,170,2860,760)),('card3',(2900,170,3820,760))]:
        x1,y1,x2,y2=box;diff=np.abs(aa[y1:y2,x1:x2]-bb[y1:y2,x1:x2]);comparisons.append({'a':ta,'b':tb,'region':name,'mean_abs_rgb_difference':float(diff.mean()),'fraction_pixels_any_channel_gt10':float((diff.max(axis=2)>10).mean())})
(OUT/'T04_hold_diff_exploratory.json').write_text(json.dumps(comparisons,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'explore2_reads.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared native T04 card and transition sequences; T01 geometry estimates')
