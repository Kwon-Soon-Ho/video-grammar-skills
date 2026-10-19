import json
from pathlib import Path
from PIL import Image,ImageDraw
from fractions import Fraction
r=Path.cwd()/'phase01a-a4';o=r/'retest-variant';crops=json.loads((o/'crops.json').read_text('utf-8'))
features=[
('S_title',[235.4,235.6,235.8,236,236.2,236.4],(1450,245,2350,450)),
('S_safe',[236.4,236.6,236.8,237,237.2,237.4],(250,740,850,1340)),
('S_safehold',[237.4,238.5,240,242,244,245],(250,780,850,1380)),
('S_quality',[238.1,238.2,238.3,238.4,238.6,238.8],(1000,600,1600,1100)),
('S_qualityhold',[239,240,241,242,244,245],(1000,600,1600,1100)),
('S_schedule',[239.1,239.2,239.3,239.4,239.6,239.8],(2070,1180,2670,1730)),
('S_schedulehold',[240,241,242,243,244,245],(2070,1180,2670,1730)),
('S_effscreen',[240.4,240.6,240.8,241,241.2,242],(3130,780,3730,1250)),
('S_effhold',[241,242,243,244,245,245.8],(3020,1180,3520,1630)),
('S_bubbles',[241,241.5,242,243,244,245],(2890,900,3490,1230)),
('W_title',[240.4,240.6,240.8,241,249,249.4],(220,820,1450,1330)),
('W_effscreen',[245.8,246,246.2,246.4,246.6,247],(6650,550,7450,1200)),
('W_effhold',[247,247.5,248,248.5,249,249.5],(6530,1090,7050,1610)),
('W_schedulehold',[245,246,247,248,249,249.5],(5100,1100,5600,1620)),
('W_safehold',[242,243,244,246,248,249.5],(2000,300,2700,920)),
('W_qualityhold',[243,244,245,246,248,249.5],(3200,150,3900,750))]
cache={}
for sid,case in [('A4-S','V06S'),('A4-W','V06W')]:
 fs=[]
 for phase in [case,case+'_retest_more']:fs+=json.loads((r/'cases'/sid/phase/'실행기록.json').read_text('utf-8'))['frames']
 cache[case]={float(Fraction(f['actual_playback_seconds'])):f for f in fs}
for name,ts,b in features:
 case='V06'+name[0];fs=cache[case];w=b[2]-b[0];h=b[3]-b[1];cols=2 if w>900 else 3
 sheet=Image.new('RGB',(w*cols,(h+25)*((len(ts)+cols-1)//cols)),'#dddddd');d=ImageDraw.Draw(sheet)
 for j,t in enumerate(ts):
  f=fs[t];im=Image.open(f['path']).convert('RGB').crop(b);p=o/f'{name}_{t:g}.png';im.save(p);crops.append(dict(path=str(p),parent_path=f['path'],crop_xyxy_native_pixels=list(b)))
  x=j%cols*w;y=j//cols*(h+25);sheet.paste(im,(x,y+25));d.text((x+3,y+3),f'{name} {t:g}',fill='black')
 sheet.save(o/f'{name}_native.jpg')
(o/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),'utf-8')
