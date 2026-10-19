from pathlib import Path
import sys,json
sys.path.insert(0,str(Path.cwd()/'phase01a-a1/후보런타임'))
from PIL import Image
import numpy as np
D=Path(__file__).parent
result=[]
for t in [16.6,16.7,16.8,16.9,17,17.1,17.2,17.3,17.4,17.5,17.55,17.65]:
 p=D/f'crop-main-{t:.3f}.png'
 a=np.array(Image.open(p));m=(a[558:562,:,0]>180)&(a[558:562,:,1]>160)&(a[558:562,:,2]<70)
 xs=np.where(m.sum(axis=0)>=2)[0]
 result.append({'actual_seconds':str(t),'path':str(p),'measurement':'yellow_label_visible_width_at_crop_rows_558_561','unit':'native raster pixel','width':int(xs.max()-xs.min()+1) if xs.size else 0,'left_x_crop':int(xs.min()) if xs.size else None,'threshold':'R>180 G>160 B<70 in at least 2 of 4 rows','uncertainty_pixels':2})
(D/'measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
