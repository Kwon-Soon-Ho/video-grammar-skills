import sys,json
from pathlib import Path
sys.path.insert(0,'phase01a-a1/후보런타임');from PIL import Image
import numpy as np
s=Path('phase01a-a5b/trials/H01-r1-with_skill/support').resolve();p=s/'motion-measurements.json';r=json.loads(p.read_text(encoding='utf-8'))
r['tagline_position']['samples'][0]['native_rightmost_text_x']=None;r['tagline_position']['samples'][0]['note']='4.2초 문구 미검출. x2815는 A 외곽이므로 영어 문구 측정에서 제외.'
for name,x,times in [('O',400,[3.5,3.6,3.7,3.8,3.9,4]),('V',600,[3.6,3.7,3.8,3.9,4,4.1]),('A',850,[3.7,3.8,3.9,4,4.1,4.2])]:
 a=[]
 for t in times:
  im=np.asarray(Image.open(s/f'logo_{t:.1f}.png').convert('RGB'));ys=np.where((im[:340,x,:]>210).all(axis=1))[0];a.append({'seconds':t,'native_top_y':int(ys[0])+1200 if len(ys) else None})
 r['logo_'+name+'_position']={'method':f'같은 글자 고정 native x{1900+x} 열의 RGB 모두>210 첫 y. 상부 윤곽 추적. 약2-5px 오차 추정; 실제 AE 좌표 아님.','samples':a}
p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k in ['logo_O_position','logo_V_position','logo_A_position']},ensure_ascii=False,indent=2))
