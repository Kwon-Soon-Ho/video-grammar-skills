from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
p=HERE/'cases/자료013/scan';a=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'));rows=[]
for im,i in zip(a,idx):
    r,g,b=[im[...,j].astype(float) for j in range(3)]
    m=(r>175)&(g>175)&(np.abs(r-g)<28)&(b<95);m[:25]=False;m[185:]=False;m[:,275:]=False
    ys,xs=np.where(m)
    bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs)>12 else None
    rows.append({'time':i['seconds'],'bbox':bb,'pixels':len(xs)})
(HERE/'EG_사진테두리_정제진단.json').write_text(json.dumps({'method':'bright near-yellow screenshot outline segmentation; excludes orange E via R-G difference; can merge two frames','coordinate_space':'480x270 proxy','unknown_uncertainty':True,'samples':rows},ensure_ascii=False,indent=2),encoding='utf-8')
for t in [6.9,7,7.1,7.2,7.3,7.4,7.5,7.6,7.8,8,8.2,10.7,10.8,10.9,11,11.1,11.2,11.3,11.4,11.5,11.6,11.7,11.8,12,13.6,13.8,14,14.2,14.4,14.6]:
    j=min(range(len(idx)),key=lambda j:abs(float(F(idx[j]['seconds']))-t));print(rows[j])
# Native 1920px derivative outlines for correspondence and small-value checks.
for group in ['eg_screens']:
    run=json.loads((HERE/'cases/자료013'/group/'실행기록.json').read_text(encoding='utf-8'))
    out=[]
    for f in run['frames']:
        im=np.asarray(Image.open(f['path']).convert('RGB'));r,g,b=[im[...,j].astype(float) for j in range(3)]
        m=(r>180)&(g>180)&(np.abs(r-g)<25)&(b<95);m[:100]=False;m[730:]=False;m[:,1100:]=False
        ys,xs=np.where(m);bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs)>40 else None
        out.append({'time':f['actual_playback_seconds'],'bbox_candidate':bb,'source_png_sha256':f['sha256'],'frame_id':f['frame_id']})
    (HERE/'EG_사진테두리_1920진단.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
