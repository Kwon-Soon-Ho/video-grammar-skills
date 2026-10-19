from pathlib import Path
import json,numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def load(aid):
    p=HERE/'cases'/aid/'scan';return np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'],json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'))
def fit_curve(values,times,lo,hi):
    t=np.array(times);v=np.array(values,dtype=float);selection=(t>=lo)&(t<=hi)
    tt=t[selection];vv=v[selection];base=float(np.median(vv[:3]));end=float(np.median(vv[-5:]));span=end-base
    if span<=3:return {'status':'insufficient_signal','base':base,'end':end}
    p=np.clip((vv-base)/span,0,1)
    active=np.where((p>.025)&(p<.99))[0]
    if len(active)<6:return {'status':'too_short_or_quantized'}
    t0=tt[max(0,active[0]-1)];t1=tt[min(len(tt)-1,active[-1]+2)]
    u=np.clip((tt-t0)/(t1-t0),0,1)
    candidates={'linear':u}
    for n in [2,3,4,5]:
        candidates[f'ease-in_p{n}']=u**n
        candidates[f'ease-out_p{n}']=1-(1-u)**n
        candidates[f'ease-in-out_p{n}']=np.where(u<.5,(2*u)**n/2,1-(-2*u+2)**n/2)
    scores=sorted([{'candidate':k,'rmse':float(np.sqrt(np.mean((p-v)**2)))} for k,v in candidates.items()],key=lambda x:x['rmse'])
    return {'status':'diagnostic_candidate_only','measurement':'normalized proxy pixel count','estimated_window':[float(t0),float(t1)],'candidate_ranking':scores[:5],'linear_rmse':next(x['rmse'] for x in scores if x['candidate']=='linear'),'progress_quarters':[float(np.interp(t0+(t1-t0)*q,tt,p)) for q in [.25,.5,.75]],'position_uncertainty':'unknown; segmentation/rounding/start-end choice affect curve; no original AE preset recovery'}

data,idx=load('자료005');times=[float(F(i['seconds'])) for i in idx];H,W=data.shape[1:3];yy,xx=np.mgrid[:H,:W]
metrics=[]
for name,cx,window in [('수주',211,(7.5,10)),('매출',331,(15,16.9)),('영업이익',451,(16.5,18.5))]:
    ring=((xx-cx)**2+(yy-70)**2>=10**2)&((xx-cx)**2+(yy-70)**2<=16**2)
    counts=[]
    for im in data:
        r,g,b=im[...,0].astype(float),im[...,1].astype(float),im[...,2].astype(float)
        blue=(b>140)&(g>90)&(b>r*1.5)&(g>r*1.8)
        counts.append(int((blue&ring).sum()))
    metrics.append({'element':name+' 원형 진행표시','center_proxy_px':[cx,70],'annulus_radii_proxy_px':[10,16],'signal':[{'time':i['seconds'],'blue_pixel_count':v} for i,v in zip(idx,counts)],'fit':fit_curve(counts,times,*window)})
redring=((xx-302)**2+(yy-62)**2>=10**2)&((xx-302)**2+(yy-62)**2<=23**2)
counts=[]
for im in data:
    r,g,b=im[...,0].astype(float),im[...,1].astype(float),im[...,2].astype(float)
    counts.append(int(((r>150)&(r>g*1.3)&(r>b*1.3)&redring).sum()))
metrics.append({'element':'매출처 도넛 공개','signal':[{'time':i['seconds'],'red_pixel_count':v} for i,v in zip(idx,counts)],'fit':fit_curve(counts,times,21.0,23.5)})
save('장헌_차트_시간곡선진단.json',{'coordinate_space':'480px width motion proxy, not display/original coordinates','metrics':metrics})
print('JH',json.dumps([{'name':x['element'],'fit':x['fit']} for x in metrics],ensure_ascii=False))
del data

data,idx=load('자료013');times=[float(F(i['seconds'])) for i in idx]
boxes=[]
for im,i in zip(data,idx):
    r,g,b=im[...,0].astype(int),im[...,1].astype(int),im[...,2].astype(int)
    # Yellow screenshot frames: actual raster bounds, not inferred layer transforms.
    mask=(r>155)&(g>145)&(b<130)&(r<g*1.65)
    mask[:25]=False;mask[:,275:]=False
    ys,xs=np.where(mask)
    box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs)>10 else None
    # White title envelope, excludes later EG-BIM caption at bottom right.
    w=(r>190)&(g>190)&(b>180);w[:70]=False;w[160:]=False;w[:,370:]=False
    wy,wx=np.where(w)
    wb=[int(wx.min()),int(wy.min()),int(wx.max()),int(wy.max())] if len(wx)>8 else None
    boxes.append({'time':i['seconds'],'yellow_border_bbox_candidate':box,'white_title_bbox_candidate':wb})
save('EG_경계와_제목_시간색인.json',{'coordinate_space':'480x270 proxy','uncertainty':'unknown; color segmentation is diagnostic and can merge multiple rectangles/light; manual verification needed','samples':boxes})
for t in [1.8,2,2.1,2.2,2.3,2.4,2.5,3,3.25,3.5,6.8,7,7.2,7.4,7.6,8,10,10.5,11,11.2,11.5,12,13,14,14.5,15]:
    j=min(range(len(times)),key=lambda j:abs(times[j]-t));print('EG',boxes[j])
