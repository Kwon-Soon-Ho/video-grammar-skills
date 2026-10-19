from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
from fractions import Fraction
import json
import numpy as np

BASE=Path(r'C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT=BASE/'runs/retest_b'
CROPS=OUT/'crops'
CROPS.mkdir(exist_ok=True)
sources={'T02':BASE/'analysis_input/cases/자료013/T02','T05':BASE/'analysis_input/cases/자료005/T05','T05extra':OUT/'cases/자료005/extra1'}
read=[]
frames={}
for case,folder in sources.items():
    lp=folder/'실행기록.json'; read.append(str(lp))
    log=json.loads(lp.read_text(encoding='utf-8'))
    frames[case]=[]
    for f in log['frames']:
        p=Path(f['path']); read.append(str(p))
        im=Image.open(p).convert('RGB')
        frames[case].append((float(Fraction(f['actual_playback_seconds'])),p,im))

def nearest(case,t):return min(frames[case],key=lambda a:abs(a[0]-t))
def board(case,times,box,name,scale=1,boost=1,cols=2):
    w=round((box[2]-box[0])*scale); h=round((box[3]-box[1])*scale)
    result=Image.new('RGB',(w*cols,(h+30)*((len(times)+cols-1)//cols)), '#20242c')
    d=ImageDraw.Draw(result)
    for j,t in enumerate(times):
        real,p,im=nearest(case,t)
        crop=im.crop(box)
        if boost!=1:crop=ImageEnhance.Brightness(crop).enhance(boost)
        crop=crop.resize((w,h),Image.Resampling.LANCZOS)
        x=(j%cols)*w;y=(j//cols)*(h+30)
        result.paste(crop,(x,y));d.text((x+8,y+h+6),f'{case} {real:.6f}s | crop {box} | gain {boost}',fill='white')
    result.save(CROPS/name)

board('T02',[0,.15,.3,.45,.6,.75,.9,1.05,1.2,1.4],(0,0,2800,650),'T02_top_progress.jpg',.5,2)
board('T02',[.25,.45,.65,.85,1.05,1.4],(0,700,2600,2160),'T02_lower_progress.jpg',.4,2)
board('T02',[.9,1,1.1,1.2,1.3,1.4],(0,0,1000,1000),'T02_axes_native.jpg',1,2)
board('T02',[.3,.6,.9,1.4],(2300,200,3500,1400),'T02_grid_native.jpg',.75,2)
board('T05extra',[5.9,6,6.033333,6.066667,6.1,6.2,6.3,6.4,6.5,6.6],(0,0,1000,1080),'T05_title_progress.jpg',.65)
board('T05extra',[6.1,6.2,6.3,6.4,6.5,6.6],(980,140,1900,780),'T05_card1_native.jpg',1)
board('T05extra',[6.1,6.3,6.6],(2900,140,3780,780),'T05_card3_native.jpg',1,1,1)

metrics={}
for case,fs in frames.items():
    ms=[]
    prev=None
    for t,p,im in fs:
        a=np.asarray(im,dtype=np.float32)
        row={'t':t,'file':str(p),'size':list(im.size),'mean_rgb':a.mean((0,1)).round(4).tolist()}
        if prev is not None:
            diff=np.abs(a-prev)
            row['mean_abs_difference_from_previous']=float(diff.mean())
            row['fraction_pixels_max_rgb_diff_gt3']=float((diff.max(2)>3).mean())
        if case=='T02':
            for key,xy in {'center':(1920,1080),'corner':(3700,2100),'left':(100,1000)}.items():
                x,y=xy;row[key+'_median_rgb']=np.median(a[y-10:y+11,x-10:x+11],(0,1)).tolist()
        ms.append(row);prev=a
    metrics[case]=ms
(OUT/'exploration_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'exploration_files_read.json').write_text(json.dumps(read,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'read_count':len(read),'crops':[str(p) for p in CROPS.iterdir()]},ensure_ascii=False,indent=2))
