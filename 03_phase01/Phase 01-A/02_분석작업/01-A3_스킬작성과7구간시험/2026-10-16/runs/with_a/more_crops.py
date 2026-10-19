from pathlib import Path
from PIL import Image,ImageDraw
import json
from fractions import Fraction
r=Path.cwd();o=r/'phase01a-a3/runs/with_a';fs=json.loads((o/'catalog.json').read_text(encoding='utf8'))['frames']
manifest=json.loads((o/'crops_manifest.json').read_text(encoding='utf8'))
for case,tag,ts,box in [('T01','eglow',[4.7,4.9,5.1,5.3,5.5],(450,0,2200,2160)),('T02','toplight',[.2,.4,.6,.8,1.,1.2,1.4],(0,150,3840,450))]:
 ims=[]
 for t in ts:
  f=next(f for f in fs if f['frame_id'].split('-')[1]==case and Fraction(f['actual_playback_seconds'])==Fraction(str(t)));im=Image.open(f['path']).crop(box);p=o/f'{case}_{tag}_{t:.2f}.png';im.save(p);manifest.append({'case':case,'time':t,'source':f['path'],'crop_path':str(p),'crop_xyxy':box,'resize':None})
  im.thumbnail((700,800));tile=Image.new('RGB',(im.width,im.height+25),(30,30,30));tile.paste(im,(0,25));ImageDraw.Draw(tile).text((8,4),str(t),fill='white');ims.append(tile)
 cols=3 if case=='T01' else 1;w=max(i.width for i in ims);h=max(i.height for i in ims);b=Image.new('RGB',(cols*w,((len(ims)+cols-1)//cols)*h))
 for i,im in enumerate(ims):b.paste(im,((i%cols)*w,(i//cols)*h))
 b.save(o/f'{case}_{tag}_board.jpg')
(o/'crops_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
