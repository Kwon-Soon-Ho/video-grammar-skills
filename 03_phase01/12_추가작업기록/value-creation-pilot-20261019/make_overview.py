from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;OUT=HERE/'inspection';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
allframes=[]
for phase in ['overview1','overview2','overview3']:
 p=HERE/'extraction/cases/VALUE'/phase/'실행기록.json'
 if not p.exists():continue
 d=json.loads(p.read_text(encoding='utf-8'));frames=d['frames'];allframes+=frames
 w=640;h=210;im=Image.new('RGB',(w*3,h*math.ceil(len(frames)/3)),(233,238,242));dr=ImageDraw.Draw(im)
 for i,f in enumerate(frames):
  tile=Image.open(f['path']).convert('RGB');tile.thumbnail((w,180));x=(i%3)*w;y=(i//3)*h;im.paste(tile,(x,y+28));dr.text((x+10,y+3),str(f['actual_playback_seconds'])+'s',font=font,fill=(20,40,50))
 im.save(OUT/f'{phase}.jpg',quality=94)
(OUT/'overview-index.json').write_text(json.dumps(allframes,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'frames':len(allframes)}))
