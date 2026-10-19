from pathlib import Path
import json
from fractions import Fraction
from PIL import Image,ImageDraw
B=Path(__file__).resolve().parent
O=B/'company-video-grammar-analyzer-workspace/iteration-2/eval-V05/with_skill/outputs'
O.mkdir(parents=True,exist_ok=True)
logs=[B/'cases/A4-G/V05/실행기록.json',B/'cases/A4-G/V05_retest_more/실행기록.json']
frames={float(Fraction(f['actual_playback_seconds'])):f for l in logs for f in json.loads(l.read_text(encoding='utf-8'))['frames']}
extra=json.loads(logs[1].read_text(encoding='utf-8'))['frames']
for offset in range(0,len(extra),10):
    sheet=Image.new('RGB',(1600,5*480),'#151515');d=ImageDraw.Draw(sheet)
    for i,f in enumerate(extra[offset:offset+10]):
        im=Image.open(f['path']);im.thumbnail((800,450));x=i%2*800;y=i//2*480
        sheet.paste(im,(x,y+30));d.text((x+10,y+5),str(f['actual_playback_seconds']),fill='white')
    sheet.save(O/f'extra-board-{offset//10+1}.jpg')
specs=[]
def crop(t,box,tag):
    f=frames[t];p=O/f'roi-{tag}-{t:.3f}.png';Image.open(f['path']).crop(box).save(p)
    specs.append({'path':str(p),'source':f['path'],'actual_seconds':f['actual_playback_seconds'],'crop_xyxy':box,'resize':False})
for t in [1.4,1.8,2.2,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4]:crop(t,(2250,700,3830,1350),'title')
for t in [5.8,6.0,6.2,6.4,6.8,7.2,7.6,7.8,8.0,8.2,8.4,9.2,10.0,10.933333333333334]:crop(t,(380,730,2160,1450),'ui')
crop(8.8,(2350,970,3540,1420),'copy')
for t in [0.0,0.4,0.8,1.2,1.6,2.0,2.4,3.2,5.6,8.8,10.933333333333334]:crop(t,(2010,370,3470,840),'bg-select')
for t in [0.2,0.6,1.0]:crop(t,(2250,900,3650,1250),'korean')
for t in [6.0,6.1,6.2,6.3,6.4,6.6,6.8,7.0]:crop(t,(300,400,1300,1260),'ui-entry')
for t in [3.6,3.8,4.0,4.2,4.6,5.0,5.4,5.8]:crop(t,(1050,0,2400,850),'g-top')
(O/'roi-map.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
