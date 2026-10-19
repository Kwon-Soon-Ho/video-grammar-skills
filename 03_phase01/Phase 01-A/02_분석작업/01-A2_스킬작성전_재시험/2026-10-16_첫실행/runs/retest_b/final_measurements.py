from pathlib import Path
from PIL import Image
import numpy as np,json
O=Path(__file__).resolve().parent
A=O.parent.parent/'analysis_input/cases/자료013/T02'
B=O.parent.parent/'analysis_input/cases/자료005/T05'
reads=[]
def arr(p):
 reads.append(str(p));return np.asarray(Image.open(p),dtype=np.float64)
a=arr(B/'f_00180_006.000.png');b=arr(B/'f_00198_006.600.png');d=b-a;den=np.sum(d*d)
mix=[]
for p in sorted(B.glob('f_*.png')):
 im=arr(p);alpha=float(np.sum((im-a)*d)/den);fit=a+alpha*d
 mix.append({'t':float(p.stem.split('_')[-1]),'source':str(p),'endpoint_mix_proxy':round(alpha,5),'fit_mean_abs_rgb_residual':round(float(np.abs(im-fit).mean()),4)})
axes=[]
for p in sorted(A.glob('f_*.png')):
 t=float(p.stem.split('_')[-1]);im=arr(p)[:1000,:1100];r,g,b=im.transpose(2,0,1)
 red=np.maximum(r-np.maximum(g,b),0);green=np.maximum(g-np.maximum(r,b)-20,0)
 redrow=red.sum(1);greencol=green.sum(0)
 if redrow.max()>100:
  y=int(redrow.argmax());x=int(greencol.argmax());axes.append({'t':t,'source':str(p),'axis_intersection_proxy_xy':[x,y],'red_row_weight':round(float(redrow.max()),2),'green_col_weight':round(float(greencol.max()),2)})
(O/'final_measurement_evidence.json').write_text(json.dumps({'T05_mix':mix,'T02_axes':axes,'files_read':reads},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'T05_mix':mix,'T02_axes':axes},ensure_ascii=False,indent=2))
