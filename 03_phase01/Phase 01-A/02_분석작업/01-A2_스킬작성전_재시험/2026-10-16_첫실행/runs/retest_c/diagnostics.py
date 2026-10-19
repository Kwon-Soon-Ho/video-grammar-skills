from pathlib import Path
from PIL import Image
import numpy as np,json
BASE=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT=BASE/'runs/retest_c/crops'
def arr(case,n):
 p=next((BASE/'analysis_input/cases/자료013'/case).glob(f'f_{n:05d}_*.png'))
 return np.asarray(Image.open(p).convert('RGB')).astype(np.int16)
rows=[]
for n in range(60,229,6):
 a=arr('T03',n)
 red=(a[:,:,0]>a[:,:,1]*1.2)&(a[:,:,0]>a[:,:,2]*1.4)&(a[:,:,0]>15)
 y,x=np.where(red)
 rows.append(dict(ordinal=n,seconds=n/60,red_bbox=None if not len(x) else [int(x.min()),int(y.min()),int(x.max()),int(y.max())],red_center_x=None if not len(x) else float((x.min()+x.max())/2),red_peak_y=None if not len(x) else int(np.argmax(red.sum(axis=1)))))
regions={'T06_right_text':(2250,1050,3400,1720),'T06_back_gold':(610,1300,1000,1900),'T06_grid_top':(2400,30,3150,230),'T06_cad_held':(480,470,1660,1050),'T06_model_top':(1100,840,2150,1100),'T03_grid':(2500,1500,3100,2000),'T03_panel':(100,900,500,1100)}
pairs=[('T06',636,771,['T06_right_text','T06_back_gold','T06_grid_top']),('T06',729,771,['T06_cad_held','T06_right_text','T06_back_gold','T06_grid_top']),('T06',863,930,['T06_right_text','T06_back_gold','T06_grid_top','T06_model_top']),('T03',60,108,['T03_grid','T03_panel']),('T03',144,180,['T03_grid','T03_panel'])]
diffs=[]
for c,n,m,labels in pairs:
 a,b=arr(c,n),arr(c,m)
 for label in labels:
  x0,y0,x1,y1=regions[label]; d=np.abs(a[y0:y1,x0:x1]-b[y0:y1,x0:x1]); q=np.max(d,axis=2)
  diffs.append(dict(case=c,ordinals=[n,m],seconds=[n/60,m/60],region=label,box=list(regions[label]),mean_abs_rgb=float(d.mean()),max_abs_rgb=int(d.max()),fraction_pixels_delta_gt_5=float((q>5).mean()),fraction_pixels_delta_gt_20=float((q>20).mean())))
json.dump({'T03_crosshair_red_threshold':rows,'region_differences':diffs},open(OUT/'diagnostics.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
for n in [60,66,72,78,84,90,96,102,108]:
 p=next((BASE/'analysis_input/cases/자료013/T03').glob(f'f_{n:05d}_*.png')); Image.open(p).crop((0,0,1000,1000)).save(OUT/f'T03_{n:05d}_crosshair_native.png')
for n in [636,771,863,930]:
 p=next((BASE/'analysis_input/cases/자료013/T06').glob(f'f_{n:05d}_*.png')); Image.open(p).crop((600,1300,1600,2100)).save(OUT/f'T06_{n:05d}_gold_native.png')
print(json.dumps({'crosshair':rows,'diffs':diffs},ensure_ascii=False,indent=2))
