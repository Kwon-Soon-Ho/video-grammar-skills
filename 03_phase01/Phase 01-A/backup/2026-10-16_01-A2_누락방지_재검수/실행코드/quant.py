from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;OUT=HERE/'검수판';font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
p=HERE.parent/'phase01a-a2-fullmotion/cases/자료013/scan';a=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'))
samples=[]
for im,m in zip(a,idx):
    t=F(m['seconds'])
    if F('4.4')<=t<=F('10'):
        samples.append({'time':str(t),'E_unobscured_mean_RGB':im[155:225,78:116].mean((0,1)).tolist()})
for s in samples:
    if F(s['time'])*5==int(F(s['time'])*5):print('E',s['time'],round(np.mean(s['E_unobscured_mean_RGB']),2))
def ncc(x,y):
    x=x.astype(float).ravel();y=y.astype(float).ravel();x-=x.mean();y-=y.mean();return float(x@y/np.sqrt((x@x)*(y@y)))
lookup={F(m['seconds']):i for i,m in enumerate(idx)}
texture=[]
for s,t in [(6,8),(8,10),(6,10)]:
    x=a[lookup[F(s)],155:225,78:116].mean(2);y=a[lookup[F(t)],155:225,78:116].mean(2)
    texture.append({'times':[s,t],'brightness_normalized_ncc':ncc(x,y),'gradient_ncc':ncc(np.diff(x,axis=1),np.diff(y,axis=1))})
(OUT/'E_광량과_내부질감진단.json').write_text(json.dumps({'roi_proxy480':[78,155,116,225],'samples':samples,'texture_fixed_ROI_comparison':texture,'limitations':'single unobscured ROI only; cannot prove every texture feature static or exact AE opacity'},ensure_ascii=False,indent=2),encoding='utf-8')
print('texture',texture)
# Additional reverse scan for JH, and focused text entrance/transparent connector crops.
from boards import sheet,records
run=json.loads((HERE/'cases/자료005/jh_all/실행기록.json').read_text(encoding='utf-8'))
sheet('장헌_역순',list(reversed(run['frames']))[::3],cols=2,width=800)
old=HERE.parent/'phase01a-a2-fullmotion/cases/자료013/eg_title/실행기록.json'
fs=json.loads(old.read_text(encoding='utf-8'))['frames']
sheet('본문_등장순서',[f for f in fs if F('2.8')<=F(f['actual_playback_seconds'])<=F('3.6')],(1050,450,1830,900),cols=2,width=780)
native=json.loads((HERE/'cases/자료013/eg_fine/실행기록.json').read_text(encoding='utf-8'))['frames']
sheet('연결면_원본크롭',[f for f in native if F('12.9')<=F(f['actual_playback_seconds'])<=F('14.5')],(1100,550,2300,1600),cols=2,width=600)
sheet('도입_작은요소_역순',list(reversed([f for f in native if F(f['actual_playback_seconds'])<=F('1.4')])),(0,0,3840,2160),cols=3,width=640)
(OUT/'추가검수판_시간연결.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
