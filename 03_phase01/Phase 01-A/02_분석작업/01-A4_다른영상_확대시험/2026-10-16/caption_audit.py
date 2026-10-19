from pathlib import Path
from PIL import Image
import json
B=Path(__file__).resolve().parent
rows=[]
for aid,cid,times,box in [('A4-S','V06S',[244,244.2,244.5],(400,1850,3500,2160)),('A4-W','V06W',[249,249.4,249.5],(1300,1850,6500,2160))]:
 log=json.loads((B/'cases'/aid/cid/'실행기록.json').read_text(encoding='utf-8'))
 log['frames']+=json.loads((B/'cases'/aid/(cid+'_retest_more')/'실행기록.json').read_text(encoding='utf-8'))['frames']
 from fractions import Fraction
 for t in times:
  f=next(x for x in log['frames'] if Fraction(x['actual_playback_seconds'])==Fraction(str(t)))
  out=B/'root-audit'/f'{cid}-caption-{t}.png'
  with Image.open(f['path']) as im:im.crop(box).save(out)
  rows.append({'path':str(out),'parent_path':f['path'],'actual_seconds':f['actual_playback_seconds'],'crop_xyxy_native_pixels':list(box)})
(B/'root-audit/caption-crop-map.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
