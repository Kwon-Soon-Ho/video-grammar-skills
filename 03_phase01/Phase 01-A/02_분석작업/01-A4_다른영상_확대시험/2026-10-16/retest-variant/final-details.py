import json
from pathlib import Path
from PIL import Image,ImageDraw
from fractions import Fraction
r=Path.cwd()/'phase01a-a4';o=r/'retest-variant';crops=json.loads((o/'crops.json').read_text('utf-8'))
sets=[('S_effentry','A4-S','V06S',[240.3,240.4,240.6,240.8,241,241.2],(3010,1180,3520,1730)),('W_effentry','A4-W','V06W',[245.6,245.8,246,246.2,246.4,246.6],(6470,1070,7160,1860)),('S_safeexit','A4-S','V06S',[245,245.2,245.4,245.6,245.8,246],(200,740,940,1740)),('W_effbubbles','A4-W','V06W',[246.4,246.8,247,248,249,249.5],(6200,650,7140,1190))]
for name,sid,c,ts,b in sets:
 fs=[]
 for ph in [c,c+'_retest_more']:fs+=json.loads((r/'cases'/sid/ph/'실행기록.json').read_text('utf-8'))['frames']
 fs={float(Fraction(f['actual_playback_seconds'])):f for f in fs};w=b[2]-b[0];h=b[3]-b[1];sheet=Image.new('RGB',(w*3,(h+25)*2),'#ddd');d=ImageDraw.Draw(sheet)
 for j,t in enumerate(ts):
  f=fs[t];im=Image.open(f['path']).convert('RGB').crop(b);p=o/f'{name}_{t:g}.png';im.save(p);crops.append(dict(path=str(p),parent_path=f['path'],crop_xyxy_native_pixels=list(b)));x=j%3*w;y=j//3*(h+25);sheet.paste(im,(x,y+25));d.text((x+3,y+3),f'{name} {t:g}',fill='black')
 sheet.save(o/f'{name}_native.jpg')
(o/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),'utf-8')
