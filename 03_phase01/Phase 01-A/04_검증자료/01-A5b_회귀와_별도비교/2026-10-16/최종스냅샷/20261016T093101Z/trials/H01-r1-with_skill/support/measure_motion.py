import sys,json
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'phase01a-a1/후보런타임');from PIL import Image
import numpy as np
b=Path('phase01a-a5b').resolve();s=b/'trials/H01-r1-with_skill/support';logs=[b/'cases/A5-T/H01/실행기록.json',b/'cases/A5-T/H01-r1-with_skill-extra1/실행기록.json',b/'cases/A5-T/H01-r1-with_skill-extra2/실행기록.json'];fs={Fraction(x['actual_playback_seconds']):x for l in logs for x in json.loads(l.read_text(encoding='utf-8'))['frames']}
results={}
a=[]
for t in [3.4,3.5,3.6,3.7,3.8,3.9,4,4.1]:
 im=np.asarray(Image.open(s/f'logo_{t:.1f}.png').convert('RGB'));ys=np.where((im[:360,150,:]>210).all(axis=1))[0];a.append({'seconds':t,'native_top_y_at_x2050':int(ys[0])+1200 if len(ys) else None})
results['logo_T_position']={'method':'고정 native x2050 열에서 RGB 각 채널>210인 최초 y. ROI 원본 무배율. 블러 경계/압축에 따라 수 픽셀 오차 가능; 실제 AE 위치값 아님.','samples':a}
a=[]
for t in [4.2,4.3,4.4,4.5,4.6,4.8]:
 im=np.asarray(Image.open(s/f'logo_{t:.1f}.png').convert('RGB'));part=im[290:340,915:,:];xs=np.where((part>180).all(axis=2))[1];a.append({'seconds':t,'native_rightmost_text_x':int(xs.max())+915+1900 if len(xs) else None})
results['tagline_position']={'method':'native ROI y1490:1540,x2815:3350의 밝은 영어 문구 오른쪽 끝 x. 같은 마지막 t를 추적. 약 2-5px 경계 오차.','samples':a}
a=[]
for t in [6.5,6.6,6.7,6.8,6.9,7,7.1,7.2,7.3,7.4,7.6,8]:
 f=fs[Fraction(str(t))];im=np.asarray(Image.open(f['path']).convert('RGB'));xs=np.where((im[820,:,:]>170).all(axis=1))[0];a.append({'seconds':t,'native_left_white_boundary_x_at_y820':int(xs.min()) if len(xs) else None,'path':f['path']})
results['map_T_position']={'method':'native y820 행의 RGB 채널 모두>170인 가장 왼쪽 x. T 가로획 좌하단 인접 동일 높이 경계. 화면밖으로 나간 후 x=0은 추적 제외. 압축/경계 2-5px 정도 오차 가능.','samples':a}
(s/'motion-measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(results,ensure_ascii=False,indent=2))
