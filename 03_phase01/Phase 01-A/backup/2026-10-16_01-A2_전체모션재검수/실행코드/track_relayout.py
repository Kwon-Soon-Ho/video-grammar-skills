from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
HERE=Path(__file__).resolve().parent
p=HERE/'cases/자료013/scan';a=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'))
rows=[]
for im,i in zip(a,idx):
    t=F(i['seconds'])
    if not F('11.35')<=t<=F('14.7'):continue
    r,g,b=[im[...,j].astype(float) for j in range(3)]
    yellow=r+g-2*b
    # Foreground screenshot's right edge, below the older screenshot's bottom edge.
    stripe=yellow[133:145].mean(0)
    cand=[(float(stripe[x]-np.mean(stripe[[x-4,x-3,x+3,x+4]])),x) for x in range(195,230)]
    right=max(cand)[1]
    # Foreground left border; older left border can become visible behind it.
    stripe=yellow[80:115].mean(0)
    cand=[(float(stripe[x]-np.mean(stripe[[x-4,x-3,x+3,x+4]])),x) for x in range(45,104)]
    maximum=max(v for v,x in cand);valid=[x for v,x in cand if v>max(20,maximum*.6)]
    left=max(valid) if valid else None
    rows.append({'time':str(t),'front_right_candidate':right,'front_left_candidate':left,'left_edge_strength':maximum})
(HERE/'EG_전면창_재배치진단.json').write_text(json.dumps({'coordinate_space':'480x270 proxy','unknown_uncertainty':True,'identity_check':'left/right boundary checked against selected native PNGs; earlier yellow union was not an individual object trajectory','samples':rows},ensure_ascii=False,indent=2),encoding='utf-8')
for row in rows:
    if F(row['time']) in {F(str(x)) for x in [11.4,11.5,11.6,11.7,11.8,12,12.2,13.8,13.9,14,14.1,14.2,14.3,14.4,14.5]}:print(row)
