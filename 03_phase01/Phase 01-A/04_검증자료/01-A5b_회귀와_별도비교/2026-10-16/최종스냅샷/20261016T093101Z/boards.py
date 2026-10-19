from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
from fractions import Fraction
B=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
for folder in [Path(x) for x in sys.argv[1:]] or list((B/'cases').glob('*/overview')):
 log=folder/'실행기록.json'
 if not log.exists():continue
 rows=json.loads(log.read_text(encoding='utf-8'))['frames']
 for part in range(0,len(rows),12):
  selected=rows[part:part+12];cols=3;w=640;h=220 if selected[0]['raster'][0]/selected[0]['raster'][1]>3 else 390
  out=Image.new('RGB',(w*cols,h*((len(selected)+2)//3)), '#181818');d=ImageDraw.Draw(out)
  for i,row in enumerate(selected):
   im=Image.open(row['path']);im.thumbnail((w,h-30))
   x=(i%cols)*w;y=(i//cols)*h;out.paste(im,(x,y+30))
   d.text((x+5,y+3),f"{folder.parent.name}/{folder.name}  t={float(Fraction(row['actual_playback_seconds'])):.3f}",font=font,fill='white')
  out.save(folder/f'board-{part//12+1}.jpg',quality=92)
  print(str(folder/f'board-{part//12+1}.jpg'))
