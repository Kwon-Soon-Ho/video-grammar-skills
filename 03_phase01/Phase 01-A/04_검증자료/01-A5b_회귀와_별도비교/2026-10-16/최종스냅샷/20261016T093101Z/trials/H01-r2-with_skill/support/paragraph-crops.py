import sys,json
from pathlib import Path
sys.path.insert(0,'phase01a-a1/후보런타임')
from PIL import Image
B=Path('phase01a-a5b').resolve();R=B/'trials/H01-r2-with_skill';S=R/'support';c=json.loads((S/'crops.json').read_text(encoding='utf-8'))
for n in ['f_00168_005.600.png','f_00180_006.000.png']:
 p=B/'cases/A5-T/H01'/n;d=S/f'crop_{n[8:15]}_detail.png';box=[1900,1370,3350,1760];Image.open(p).convert('RGB').crop(box).save(d);c.append({'path':str(d),'parent_path':str(p),'crop_xyxy_native_pixels':box});print(d)
(S/'crops.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
