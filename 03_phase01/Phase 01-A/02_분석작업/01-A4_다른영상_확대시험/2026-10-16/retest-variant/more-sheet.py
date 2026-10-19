from pathlib import Path
from PIL import Image,ImageDraw
import json
from fractions import Fraction
root=Path.cwd()/'phase01a-a4';out=root/'retest-variant'
for sid,c in [('A4-S','V06S'),('A4-W','V06W')]:
 fs=json.loads((root/'cases'/sid/(c+'_retest_more')/'실행기록.json').read_text('utf-8'))['frames']
 for p in range(0,len(fs),10):
  cw=768;ch=455 if sid=='A4-S' else 245
  sheet=Image.new('RGB',(cw*2,ch*5),'#dddddd');d=ImageDraw.Draw(sheet)
  for j,f in enumerate(fs[p:p+10]):
   im=Image.open(f['path']);im.thumbnail((cw,ch-22));x=j%2*cw;y=j//2*ch;sheet.paste(im,(x,y+22));d.text((x+4,y+3),c+' '+f['actual_playback_seconds'],fill='black')
  sheet.save(out/f'{c}_more_{p}.jpg')
