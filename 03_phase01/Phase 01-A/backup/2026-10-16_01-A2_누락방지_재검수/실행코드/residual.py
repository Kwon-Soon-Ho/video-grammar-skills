from pathlib import Path
from fractions import Fraction as F
import json,numpy as np,math
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;OUT=HERE/'검수판';font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
events={
 '자료005':{6:['J-transition'],8:['J-order-actual','J-order-ring','J-order-numbers'],9:['J-order-ring','J-order-numbers'],15:['J-sales-actual','J-sales-ring','J-sales-numbers'],16:['J-sales-actual','J-sales-ring','J-sales-numbers','J-profit-actual','J-profit-ring','J-profit-numbers'],17:['J-profit-actual','J-profit-ring','J-profit-numbers'],21:['J-transition','J-sector-ring','J-sector-percent'],22:['J-sector-ring','J-sector-percent']},
 '자료013':{0:['E-early-upper','E-early-middle','E-early-lower','E-grid','E-outline-light'],1:['E-cursor','E-selection','E-value','E-grid','E-outline-light'],2:['E-selection','E-value','E-title','E-subtitle','E-cursor'],3:['E-selection','E-value','E-title','E-subtitle','E-body-upper','E-body-lower','E-hero-upper','E-hero-middle','E-hero-lower'],4:['E-hero-upper','E-hero-middle','E-hero-lower','E-texture'],5:['E-hero-dim','E-texture'],6:['E-hero-dim','E-ui1'],7:['E-ui1','E-hero-dim'],8:['E-ui1-inside','E-outline-light'],9:['E-ui1-inside','E-outline-light'],10:['E-ui1'],11:['E-ui1','E-ui2'],12:['E-ui2','E-ui2-inside','E-model','E-connector'],13:['E-model','E-connector'],14:['E-ui1','E-ui2','E-model','E-connector','E-flare'],15:['E-flare','E-connector']}}
result=[]
for aid in ['자료005','자료013']:
    p=HERE.parent/'phase01a-a2-fullmotion/cases'/aid/'scan';a=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'))
    mapped=json.loads((OUT/f'{aid}_구역별변화.json').read_text(encoding='utf-8'))
    for part in range(math.ceil(len(mapped['rows'])/8)):
        chosen_rows=mapped['rows'][8*part:8*(part+1)];h=a.shape[1];canvas=Image.new('RGB',(960,(h+28)*len(chosen_rows)),'#20242c');d=ImageDraw.Draw(canvas)
        for i,row in enumerate(chosen_rows):
            sec=row['start'];chosen=[k for k,m in enumerate(idx) if F(sec)<=F(m['seconds'])<F(sec+1)];pixels=a[chosen];delta=(pixels.max(0).astype(np.int16)-pixels.min(0).astype(np.int16)).max(2)
            heat=np.repeat(np.minimum(delta*6,255).astype(np.uint8)[...,None],3,2)
            y=i*(h+28);canvas.paste(Image.fromarray(a[chosen[len(chosen)//2]]),(0,y));canvas.paste(Image.fromarray(heat),(480,y))
            for gx in range(1,6):d.line((480+gx*80,y,480+gx*80,y+h),fill='#3b6b8c')
            for gy in range(1,3):d.line((480,y+gy*h//3,960,y+gy*h//3),fill='#3b6b8c')
            d.text((5,y+h+3),f'{sec}~{row["end"]}s | source midpoint / temporal range x6 (search aid)',font=font,fill='white')
            owners=events[aid].get(sec,[])
            if aid=='자료013' and sec in [8,9,10]:owners=list(dict.fromkeys(owners+['E-ui1-row','E-ui1-thumb']))
            result.append({'asset':aid,'window':[sec,row['end']],'candidate_subject_ids':owners,'visual_disposition':'동일 구간 검수판 및 대상별 검수표에 연결. 별도 새 동작 후보를 더 발견하지 못함.' if owners else '검수판에서 유지 구간으로 대조. 새 독립 동작을 발견하지 못함. 압축·미세 변화의 부재 증명은 아님.','top_change_tiles':sorted(row['grid_temporal_ranges'],key=lambda x:x['mean_range'],reverse=True)[:3],'remaining_limit':'동일 구역에 여러 대상이 겹칠 수 있어 소유권 자동 판별이나 residual=0 주장을 하지 않음.'})
        canvas.save(OUT/f'{aid}_구역변화_대조_{part+1}.jpg',quality=94)
    del a
(HERE/'03_변화구역_대조.json').write_text(json.dumps({'method':'whole-scope 1s temporal range triage, 6x3 spatial search; manual candidate subject association','not_pixel_explanation_or_accuracy_score':True,'windows':result},ensure_ascii=False,indent=2),encoding='utf-8')
print('triaged',len(result),'windows')
