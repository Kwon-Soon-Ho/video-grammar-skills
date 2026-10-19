import sys,json,runpy
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
B=Path('phase01a-a5b').resolve();R=B/'trials/H01-r2-with_skill';S=R/'support'
L=B/'cases/A5-T/H01-r2-with_skill-extra2/실행기록.json';new=json.loads(L.read_text(encoding='utf-8'))['frames'];rows=json.loads((S/'rows.json').read_text(encoding='utf-8'))+new;(S/'rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');rows={float(Fraction(f['actual_playback_seconds'])):f for f in rows}
c=json.loads((S/'crops.json').read_text(encoding='utf-8'))
for t,kind in [(4.3,'logo'),(4.5,'logo'),(4.7,'logo'),(4.9,'logo'),(7.0,'title'),(7.1,'title'),(7.3,'title'),(7.4,'title'),(7.5,'title'),(7.7,'title')]:
 box=(1830,1170,3350,1670) if kind=='logo' else (280,1150,1900,1580)
 f=rows[t];p=S/f'crop_{t:.1f}_{kind}.png';Image.open(f['path']).convert('RGB').crop(box).save(p);c.append({'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':list(box)})
(S/'crops.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
sys.argv=[str(B/'boards.py'),str(L.parent)];runpy.run_path(sys.argv[0],run_name='__main__')
print('crops total',len(c))
