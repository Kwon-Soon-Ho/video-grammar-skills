import json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path.cwd()/ 'phase01a-a4'
for sid,case in [('A4-S','V06S'),('A4-W','V06W')]:
 log=json.loads((root/'cases'/sid/case/'실행기록.json').read_text('utf-8-sig'))
 frames=log['frames']; print(case,len(frames),[(f['actual_playback_seconds'],Path(f['path']).name) for f in frames])
 for part in range(0,len(frames),10):
  subset=frames[part:part+10]; cw=768; ch=255 if sid=='A4-W' else 455
  sheet=Image.new('RGB',(cw*2,ch*5),'#dddddd'); d=ImageDraw.Draw(sheet)
  for j,f in enumerate(subset):
   im=Image.open(f['path']); im.thumbnail((cw,ch-25)); x=(j%2)*cw;y=(j//2)*ch
   sheet.paste(im,(x,y+25)); d.text((x+4,y+3),case+' '+f['actual_playback_seconds'],fill='black')
  sheet.save(root/'retest-variant'/f'{case}_base_{part}.jpg')
