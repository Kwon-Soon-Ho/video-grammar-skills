from pathlib import Path
import json,numpy as np
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
src=(HERE/'curve_more.py').read_text(encoding='utf-8');start=src.index('def fit(');end=src.index('def store(',start);ns={'np':np};exec(src[start:end],ns);fit=ns['fit']
t=np.linspace(0,1,61)
tests=[]
for expected,v in [('linear',t),('ease-in',t*t),('ease-out',1-(1-t)**2),('ease-in-out',np.where(t<.5,2*t*t,1-(-2*t+2)**2/2))]:
    r=fit(t,v*100,0,1);picked=r['rank'][0]['candidate'];tests.append({'expected':expected,'observed':picked,'pass':picked.startswith(expected) if expected!='ease-in' else picked.startswith('ease-in_')})
r=fit(t,np.ones_like(t)*50,0,1);tests.append({'expected':'constant insufficient','observed':r['status'],'pass':r['status']=='insufficient'})
assert all(x['pass'] for x in tests)
eg=json.loads((HERE/'EG_이동과_공개_곡선진단.json').read_text(encoding='utf-8'));ts=np.array([float(F(s['time'])) for s in eg['samples']]);additional=[]
tr=json.loads((HERE/'EG_전면창_재배치진단.json').read_text(encoding='utf-8'))['samples'];tt=np.array([float(F(s['time'])) for s in tr])
additional.append({'id':'EG-UI2-enter','property':'front screen right boundary after it becomes separable','fit':fit(tt,np.array([s['front_right_candidate'] for s in tr]),11.4,12.2)})
additional.append({'id':'EG-front-relayout2','property':'rightmost visible front-left vertical yellow edge, older frame can show behind','fit':fit(tt,np.array([s['front_left_candidate'] if s['front_left_candidate'] is not None else np.nan for s in tr]),13.8,14.6)})
# Perturbing the window by one frame checks obvious family instability.
sensitivity=[]
for item in eg['fits']:
    if item['id']=='EG-UI1-enter':v=np.array([s['screenshot1_right_candidate'] for s in eg['samples']]);lo,hi=7,8
    elif item['id']=='EG-title-reveal':v=np.array([s['white_bbox'][2] if s['white_bbox'] else np.nan for s in eg['samples']]);lo,hi=1.9,2.4
    elif item['id']=='EG-model-grow':v=np.sqrt([s['model_gray_area_candidate'] for s in eg['samples']]);lo,hi=12.9,13.8
    else:continue
    candidates=[]
    for shift in [-1/60,0,1/60]:
        z=fit(ts,v,lo+shift,hi+shift);candidates.append(z['rank'][0]['candidate'] if 'rank' in z else z['status'])
    sensitivity.append({'id':item['id'],'one_frame_shift_candidate_results':candidates,'interpretation':'family only; individual exponent is not identified'})
connected=json.loads((HERE/'EG_모델면_연결성보완진단.json').read_text(encoding='utf-8'))['samples']
ct=np.array([float(F(s['time'])) for s in connected]);cv=np.sqrt([s['largest_face_component_area'] for s in connected])
sensitivity.append({'id':'EG-model-connected-face-current','one_frame_shift_candidate_results':[fit(ct,cv,13.1+d,13.8+d)['rank'][0]['candidate'] for d in [-1/60,0,1/60]],'interpretation':'current connected-face proxy; replaces fixed-caption-contaminated earlier size proxy'})
letters=json.loads((HERE/'EG_작은제목_문자간격진단.json').read_text(encoding='utf-8'));lt=np.array([float(F(s['time'])) for s in letters]);lv=np.array([s['left'] if s['left'] is not None else np.nan for s in letters])
additional.append({'id':'EG-caption-spacing-settle','property':'leftmost bright caption edge; only short visible tail and pixel quantization','fit':fit(lt,lv,2.9,3.5),'confidence':'candidate, threshold/letter visibility can move edge by one pixel'})
result={'scope':'technical checks of curve-family comparator and timing-window sensitivity; not video recognition accuracy','analytic_curve_controls':tests,'extra_fits':additional,'window_sensitivity':sensitivity,'exclusions':['no original AE handles','no exact exponent/preset claim','no single total score']}
(HERE/'곡선분류_자체진단과_민감도.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
