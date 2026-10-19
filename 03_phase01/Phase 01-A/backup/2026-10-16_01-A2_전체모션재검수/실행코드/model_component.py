from pathlib import Path
from fractions import Fraction as F
import numpy as np,json
HERE=Path(__file__).resolve().parent
src=(HERE/'curve_more.py').read_text(encoding='utf-8');ns={'np':np};exec(src[src.index('def fit('):src.index('def store(')],ns);fit=ns['fit']
p=HERE/'cases/자료013/scan';a=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'));rows=[]
for im,i in zip(a,idx):
    t=F(i['seconds'])
    if not F('12.8')<=t<=F('14.2'):continue
    crop=im[90:230,120:280].astype(int);r,g,b=[crop[...,j] for j in range(3)]
    mask=(abs(r-g)<16)&(abs(g-b)<16)&(r>110);seen=np.zeros(mask.shape,bool);components=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        stack=[(y,x)];seen[y,x]=True;points=[]
        while stack:
            cy,cx=stack.pop();points.append((cy,cx))
            for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                ny,nx=cy+dy,cx+dx
                if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;stack.append((ny,nx))
        if len(points)>5:components.append(points)
    if components:
        z=np.array(max(components,key=len));box=[int(z[:,1].min()+120),int(z[:,0].min()+90),int(z[:,1].max()+120),int(z[:,0].max()+90)];area=len(z);center=[float(z[:,1].mean()+120),float(z[:,0].mean()+90)]
    else:box=None;area=0;center=None
    rows.append({'time':str(t),'largest_face_component_area':area,'bbox':box,'centroid':center})
result={'method':'largest connected neutral-bright component in model ROI, excluding right caption and upper-left fixed diagram','coordinate_space':'480x270 proxy','measurement':'visible bright face area/centroid, not complete model or object transform','uncertainty':'unknown; early identity is ambiguous before foreground dominates; silhouette/holes/occlusion can change area','supersedes':'earlier whole-neutral-area proxy included fixed caption pixels and was not used as a whole-model trajectory','samples':rows,'fit':fit([float(F(s['time'])) for s in rows],np.sqrt([s['largest_face_component_area'] for s in rows]),13.1,13.8)}
(HERE/'EG_모델면_연결성보완진단.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('fit',json.dumps(result['fit'],ensure_ascii=False))
print([s for s in rows if F(s['time']) in {F(13),F('13.1'),F('13.2'),F('13.4'),F('13.6'),F('13.8')}])
