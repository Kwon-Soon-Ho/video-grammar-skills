from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import label,find_objects
import json
BASE=Path(r'C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT=BASE/'runs/retest_b'
A=BASE/'analysis_input/cases/자료013/T02'
B=BASE/'analysis_input/cases/자료005/T05'
reads=[]
def arr(p):
    reads.append(str(p));return np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
rows=[]
for p in sorted(A.glob('f_*.png')):
    a=arr(p);t=float(p.stem.split('_')[-1]);r,g,b=a[:1000,:1100,:].transpose(2,0,1)
    row={'t':t}
    for name,mask in [('red',(r-g>6)&(r-b>6)),('green',(g-r>35)&(g-b>35))]:
        ys,xs=np.where(mask)
        if len(xs):row[name]={'bbox_xyxy':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'pixels':len(xs),'median_xy':[float(np.median(xs)),float(np.median(ys))]}
    line=a[110:190,:,1].mean(0);grad=np.convolve(np.diff(line),np.ones(5)/5,'same')
    inds,_=find_peaks(np.abs(grad),distance=60,prominence=.3)
    row['upper_rectangle_edge_candidates']=[{'x':int(i),'gradient':round(float(grad[i]),3)} for i in sorted(inds,key=lambda i:abs(grad[i]),reverse=True)[:4]]
    for name,ys,lim in [('lower_rect',(1430,1550),(300,2800)),('mid_rect',(800,1000),(0,1200))]:
        line=a[ys[0]:ys[1],:,1].mean(0);grad=np.convolve(np.diff(line),np.ones(5)/5,'same')
        inds,_=find_peaks(np.abs(grad),distance=50,prominence=.6)
        inds=[i for i in inds if lim[0]<=i<lim[1]]
        row[name+'_edge_candidates']=[{'x':int(i),'gradient':round(float(grad[i]),3)} for i in sorted(inds,key=lambda i:abs(grad[i]),reverse=True)[:4]]
    # Right grid top border: vertically oriented change averaged over clean right-side range.
    line=a[:600,2900:3200,1].mean(1)
    smooth=np.convolve(line,np.ones(3)/3,'same')
    inds,_=find_peaks(smooth,distance=20,prominence=.4)
    row['grid_top_y_candidates']=[{'y':int(i),'g':round(float(smooth[i]),2)} for i in inds if 100<i<500]
    # Locate clean right grid verticals, allowing observation of spacing.
    line=a[650:1000,2400:3500,1].mean(0)
    inds,_=find_peaks(line,distance=50,prominence=.5)
    row['grid_x_line_candidates']=[int(i+2400) for i in inds]
    rows.append(row)

diffs=[]
for bef,aft in [('f_00193_006.433.png','f_00194_006.467.png'),('f_00197_006.567.png','f_00198_006.600.png')]:
    before=arr(B/bef);after=arr(B/aft);d=np.abs(after-before).max(2);mask=d>3
    labs,n=label(mask);objs=find_objects(labs);comps=[]
    for i,sl in enumerate(objs):
        if sl is None:continue
        count=int((labs[sl]==i+1).sum())
        if count>=3:comps.append({'box_xyxy':[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop],'pixels':count})
    diffs.append({'before':bef,'after':aft,'components':sorted(comps,key=lambda c:c['pixels'],reverse=True)[:30]})
    viz=np.zeros((*mask.shape,3),dtype=np.uint8);viz[:,:,0]=np.minimum(d*10,255).astype(np.uint8)
    Image.fromarray(viz).save(OUT/'crops'/('T05_diff_'+aft))
(OUT/'tracking_measurements.json').write_text(json.dumps({'T02':rows,'T05_changes':diffs,'files_read':reads},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'T02':rows[::3], 'T05_changes':diffs},ensure_ascii=False,indent=2))
