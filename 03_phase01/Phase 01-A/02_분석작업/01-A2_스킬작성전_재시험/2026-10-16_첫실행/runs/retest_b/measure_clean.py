from pathlib import Path
from PIL import Image
import numpy as np,json
O=Path(__file__).resolve().parent
A=O.parent.parent/'analysis_input/cases/자료013/T02'
rows=[]
def peaks(a,lo,hi,n=5,sep=10):
    ids=np.argsort(a[lo:hi])[::-1]+lo;keep=[]
    for i in ids:
        if all(abs(i-j)>sep for j in keep):keep.append(int(i))
        if len(keep)>=n:break
    return [{'p':i,'v':round(float(a[i]),3)} for i in keep]
for p in sorted(A.glob('f_*.png')):
 a=np.asarray(Image.open(p),dtype=np.float32);g=a[:,:,1];t=float(p.stem.split('_')[-1])
 line=g[350:430,:].mean(0);dg=np.convolve(np.diff(line),np.ones(7)/7,'same')
 row={'t':t,'upper_right':peaks(-dg,300,2800,3,60)}
 if t>=.3:
  x=row['upper_right'][0]['p']-100
  line=g[:1000,max(0,x-30):x+30].mean(1);dg=np.convolve(np.diff(line),np.ones(5)/5,'same')
  row['upper_y_edges']=peaks(np.abs(dg),0,900,6,60)
 if t>=.6:
  line=g[:700,2900:3200].mean(1);smooth=np.convolve(line,np.ones(51)/51,'same');hp=line-smooth
  row['grid_top']=peaks(hp,200,400,3,20)
  line=g[700:1300,2300:3200].mean(0);hp=line-np.convolve(line,np.ones(51)/51,'same');hp[:50]=0;hp[-50:]=0
  ac=np.correlate(hp,hp,'full')[len(hp)-1:];row['grid_period_candidates']=peaks(ac,90,135,2,8)
 rows.append(row)
(O/'clean_measurements.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows[6::3],ensure_ascii=False,indent=2))
