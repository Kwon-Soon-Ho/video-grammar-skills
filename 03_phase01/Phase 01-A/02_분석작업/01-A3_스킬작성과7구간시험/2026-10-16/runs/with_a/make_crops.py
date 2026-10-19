from pathlib import Path
from PIL import Image,ImageDraw
import json
from fractions import Fraction
root=Path.cwd(); out=root/'phase01a-a3/runs/with_a'; out.mkdir(parents=True,exist_ok=True)
cat=json.loads((out/'catalog.json').read_text(encoding='utf-8'))['frames']
sets=[('T01','inner',[4.3,4.7,5.1,5.5],(600,700,1600,1400)),('T01','text',[3.5,3.6,4.5,5.5],(2250,1020,3350,1800)),('T02','cross',[.85,.95,1.05,1.15,1.25,1.35],(0,0,650,850)),('T03','cross',[1.0,1.2,1.4,1.6,1.8,1.9],(0,0,1000,900)),('T03','reveal',[1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],(550,450,3400,1200)),('T03','exit',[3.0,3.1,3.2,3.3,3.4,3.5,3.6],(550,450,3400,1800))]
manifest=[]
for case,tag,times,box in sets:
    ims=[]
    for t in times:
        f=next(f for f in cat if f['frame_id'].split('-')[1]==case and Fraction(f['actual_playback_seconds'])==Fraction(str(t)))
        im=Image.open(f['path']).crop(box); p=out/f'{case}_{tag}_{t:.2f}.png'; im.save(p)
        manifest.append({'case':case,'time':t,'source':f['path'],'crop_path':str(p),'crop_xyxy':box,'resize':None})
        # Native crops <=1100 wide; wide ROIs half size in supplemental contact sheet.
        if im.width>1100: im=im.resize((im.width//2,im.height//2))
        tile=Image.new('RGB',(im.width,im.height+28),(30,30,30));tile.paste(im,(0,28));ImageDraw.Draw(tile).text((10,5),f'{case} {t:.2f}s crop {box}',fill='white');ims.append(tile)
    cols=2; w=max(i.width for i in ims);h=max(i.height for i in ims);board=Image.new('RGB',(w*cols,h*((len(ims)+1)//2)),(30,30,30))
    for n,im in enumerate(ims):board.paste(im,((n%cols)*w,(n//cols)*h))
    board.save(out/f'{case}_{tag}_board.jpg')
(out/'crops_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('saved',len(manifest),'crops')
