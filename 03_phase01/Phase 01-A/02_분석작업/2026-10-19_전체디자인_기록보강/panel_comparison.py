from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
items=[];sheet=Image.new('RGB',(1500,1200),'#182235');draw=ImageDraw.Draw(sheet)
for i,t in enumerate([44,46,47,48,50,53]):
    if t<=48:p=ROOT/f'analysis-reliability-20261019/fresh/cases/NEW-P/window/f_{t*30:05d}_{t:03d}.000.png'
    elif t==50:p=ROOT/'case-benchmarks-20261019/extraction/cases/NEW-P/tail1/f_01500_050.000.png'
    else:p=ROOT/'case-benchmarks-20261019/extraction/cases/NEW-P/scout/f_01590_053.000.png'
    box=[1400,60,2440,1060] if t<53 else [2760,60,3800,1060]
    im=Image.open(p).crop(box);im.thumbnail((495,565));x=(i%3)*500;y=(i//3)*600
    sheet.paste(im,(x,y+26));draw.text((x+10,y+5),f'{t}s / native ROI {box}',fill='white')
    items.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':t,'box_ltrb':box})
sheet.save(OUT/'inspection/P-panel-comparison.jpg',quality=94)
(OUT/'panel-comparison-inputs.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
