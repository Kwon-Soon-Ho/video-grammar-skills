from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
HERE=Path(__file__).resolve().parent
def load(aid):
    p=HERE/'cases'/aid/'scan';return np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'],json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'))
def fit(t,v,lo,hi,mode='increasing'):
    t=np.asarray(t);v=np.asarray(v,dtype=float);m=(t>=lo)&(t<=hi)&np.isfinite(v);t=t[m];v=v[m]
    if mode=='decreasing':v=-v
    # Keep declared window, so a slow start is not discarded by active-threshold trimming.
    if len(v)<8 or np.median(v[-3:])-np.median(v[:3])<1:return {'status':'insufficient'}
    b=float(np.median(v[:3]));e=float(np.median(v[-3:]));p=np.clip((v-b)/(e-b),0,1);u=(t-t[0])/(t[-1]-t[0])
    c={'linear':u}
    for n in [2,3,4]:
        c[f'ease-in_{n}']=u**n;c[f'ease-out_{n}']=1-(1-u)**n;c[f'ease-in-out_{n}']=np.where(u<.5,(2*u)**n/2,1-(-2*u+2)**n/2)
    scores=sorted([{'candidate':k,'rmse':float(np.sqrt(np.mean((p-x)**2)))} for k,x in c.items()],key=lambda x:x['rmse'])
    return {'window':[lo,hi],'rank':scores[:4],'progress_quarters':[float(np.interp(q,u,p)) for q in [.25,.5,.75]],'limitation':'diagnostic curve family, no original preset/handle recovery; window/segmentation/opacity can change estimates'}
def store(name,x):(HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
a,idx=load('자료005');t=np.array([float(F(x['seconds'])) for x in idx]);results=[]
# Test the static intro against each decoded proxy frame, not just endpoints.
intro=a[t<=6];delta=np.abs(intro.astype(np.int16)-intro[0].astype(np.int16))
results.append({'id':'J-static','frames':len(intro),'max_mean_abs_delta':float(delta.mean(axis=(1,2,3)).max()),'max_pixel_channel_delta':int(delta.max()),'max_pixels_over10':int((delta.max(3)>10).sum(axis=(1,2)).max()),'classification':'no detectable intended motion at480px; do not call a pan/zoom'})
del delta,intro
for name,lo,hi in [('J-crossfade-1',6,6.4),('J-crossfade-2',21,21.4)]:
    def frame(time):return a[np.argmin(abs(t-time)),:,:120].astype(float)
    old=frame(lo);new=frame(hi);d=new-old;den=float((d*d).sum());trace=[]
    for im,tm in zip(a,t):
        if lo<=tm<=hi:
            alpha=float(((im[:,:120].astype(float)-old)*d).sum()/den)
            trace.append({'time':float(tm),'blend_progress_proxy':alpha})
    results.append({'id':name,'property':'least-squares image blend progress in left title ROI','trace':trace,'fit':fit([v['time'] for v in trace],[v['blend_progress_proxy']*100 for v in trace],lo,hi)})
store('장헌_정지와_전환곡선.json',results);print('J',json.dumps(results,ensure_ascii=False))
del a

a,idx=load('자료013');t=np.array([float(F(x['seconds'])) for x in idx]);tr=[]
for im,tm in zip(a,t):
    r,g,b=[im[...,i].astype(float) for i in range(3)]
    white=(r>190)&(g>190)&(b>180)
    region=white[55:138,80:440];ys,xs=np.where(region)
    # Screenshot-1 right border line: vertical yellow excess with symmetric local contrast.
    yellow=(r+g-2*b)[37:127].mean(0)
    line=np.array([yellow[x]-np.mean(yellow[[x-4,x-3,x+3,x+4]]) for x in range(135,210)])
    xr=int(line.argmax())+135
    # Screenshot-1 top/left bounds during the isolated shrink transition, before new frame appears.
    strict=(r>175)&(g>175)&(abs(r-g)<28)&(b<95);strict[:30]=False;strict[135:]=False;strict[:,225:]=False
    by,bx=np.where(strict);box=[int(bx.min()),int(by.min()),int(bx.max()),int(by.max())] if len(bx)>12 else None
    # High-intensity neutral face of emerging model; ROI avoids the fixed model diagram above-left.
    gray=(abs(r-g)<16)&(abs(g-b)<16)&(r>110)
    gray[:100]=False;gray[225:]=False;gray[:,:130]=False;gray[:,295:]=False
    ys2,xs2=np.where(gray)
    # Area/extent diagnostics only; not certified segmentation of the whole foreground model.
    modelbox=[int(xs2.min()),int(ys2.min()),int(xs2.max()),int(ys2.max())] if len(xs2)>8 else None
    tr.append({'time':str(F(tm).limit_denominator(60000)),'white_bbox':([int(xs.min()+80),int(ys.min()+55),int(xs.max()+80),int(ys.max()+55)] if len(xs)>5 else None),'white_count':int(region.sum()),'screenshot1_right_candidate':xr,'edge_strength':float(line.max()),'screenshot_bbox':box,'model_gray_area_candidate':int(gray.sum()),'model_gray_bbox_candidate':modelbox,'model_light_mean':float(im[125:165,145:235].mean())})
def series(key,default=np.nan):return np.array([v[key] if v[key] is not None else default for v in tr])
def comp(key,j):return np.array([v[key][j] if v[key] else np.nan for v in tr])
fits=[{'id':'EG-title-reveal','property':'right extent of visible white title','fit':fit(t,comp('white_bbox',2),1.9,2.4)},
 {'id':'EG-title-wipe-out','property':'white title area disappearing; composite reveal/visibility, not translation','fit':fit(t,series('white_count'),3.15,3.55,'decreasing')},
 {'id':'EG-UI1-enter','property':'right yellow border candidate','fit':fit(t,series('screenshot1_right_candidate'),7.0,8.0)},
 {'id':'EG-UI1-relayout','property':'left border moves right during shrink; only isolated old frame10.7–11.3','fit':fit(t,comp('screenshot_bbox',0),10.7,11.3)},
 {'id':'EG-model-grow','property':'sqrt gray-face pixel count; size proxy with segmentation caveat','fit':fit(t,np.sqrt(series('model_gray_area_candidate')),12.9,13.8)},
 {'id':'EG-light-brighten','property':'mean in fixed light ROI, confounded by model motion; diagnostic only','fit':fit(t,series('model_light_mean'),14.3,15.0)}]
store('EG_이동과_공개_곡선진단.json',{'samples':tr,'fits':fits,'limits':'Pixel diagnostics; no original AE inputs. Some combined masks/visibility cause non-identifiability; validate matching feature on individual images.'})
print('EG',json.dumps(fits,ensure_ascii=False))
print('UI',[(v['time'],v['screenshot1_right_candidate'],v['edge_strength']) for v in tr if F(v['time']) in {F(7),F('7.1'),F('7.2'),F('7.3'),F('7.4'),F('7.5'),F('7.6'),F('7.8'),F(8)}])
