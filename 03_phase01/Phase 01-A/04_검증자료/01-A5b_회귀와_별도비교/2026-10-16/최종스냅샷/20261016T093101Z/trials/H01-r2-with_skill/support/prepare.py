import sys,json,hashlib
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
B=Path('phase01a-a5b').resolve(); R=B/'trials/H01-r2-with_skill'; S=R/'support'
logs=[B/'cases/A5-T/H01/실행기록.json',B/'cases/A5-T/H01-r2-with_skill-extra1/실행기록.json']
rows={float(Fraction(f['actual_playback_seconds'])):f for l in logs for f in json.loads(l.read_text(encoding='utf-8'))['frames']}
requests=[(1.4,'left'),(1.8,'left'),(2.2,'left'),(2.6,'left'),(3.0,'left'),(3.2,'left'),(3.4,'logo'),(3.6,'logo'),(3.8,'logo'),(4.0,'logo'),(4.6,'logo'),(5.4,'detail'),(5.8,'detail'),(6.4,'detail'),(7.2,'overlap'),(7.6,'overlap')]
boxes={'left':(250,850,1950,1620),'logo':(1830,1170,3350,1670),'detail':(1900,1370,3350,1760),'overlap':(1200,0,2800,1650)}
crops=[]
for t,kind in requests:
 f=rows[t]; box=boxes[kind]; p=S/f'crop_{t:.1f}_{kind}.png'; im=Image.open(f['path']).convert('RGB'); im.crop(box).save(p); crops.append({'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':list(box)})
(S/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),encoding='utf-8')
(S/'rows.json').write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print('crops',len(crops));print('source sha256',hashlib.sha256(Path(json.loads((R/'input.json').read_text(encoding='utf-8'))['source_path']).read_bytes()).hexdigest())
