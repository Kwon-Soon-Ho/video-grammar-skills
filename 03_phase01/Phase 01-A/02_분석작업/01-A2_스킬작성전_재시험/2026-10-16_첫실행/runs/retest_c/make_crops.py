from pathlib import Path
from PIL import Image, ImageDraw
import json
import numpy as np
BASE = Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
OUT = BASE/'runs/retest_c/crops'
records=[]
def crop(case, ordinal, box, tag):
    p=next((BASE/'analysis_input/cases/자료013'/case).glob(f'f_{ordinal:05d}_*.png'))
    im=Image.open(p).convert('RGB')
    dst=OUT/f'{case}_{ordinal:05d}_{tag}.png'
    im.crop(box).save(dst)
    records.append(dict(output=str(dst),source=str(p),ordinal=ordinal,actual_seconds=ordinal/60,box_native=list(box),resize=False))
for ordinal in [60,78,96,108,114,120,126,132,138,144,150,156,162,168,174,180,186,192,198,204,210,216,222,228]:
    crop('T03',ordinal,(500,450,1800,1250),'left_title')
for ordinal in [162,168,174,180,186,192,198,204,210,216,228]:
    crop('T03',ordinal,(2150,1000,3450,1750),'brand_detail')
for ordinal in [636,653,662,670,678,687,695,704,712,720,729,737,746,754,762,771,779,788,796,804,813,821,830,838,846,855,863,872,880,888,897,905,914,922,930]:
    crop('T06',ordinal,(200,250,1800,1250),'screens')
for ordinal in [771,779,788,796,804,813,821,830,838,846,855,863,872,880,888,897,905,914,922,930]:
    crop('T06',ordinal,(950,700,2350,1700),'model')
json.dump(records,open(OUT/'crop_manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
for case in ['T03','T06']:
    rows=[]
    for p in sorted((BASE/'analysis_input/cases/자료013'/case).glob('f_*.png')):
        a=np.asarray(Image.open(p).convert('RGB'))
        if case=='T03':
            y,x=np.where((a[:,:,0]>175)&(a[:,:,1]>175)&(a[:,:,2]>175))
            rows.append({'frame':p.name,'bright_bbox':None if not len(x) else [int(x.min()),int(y.min()),int(x.max()),int(y.max())]})
        else:
            mask=(a[:,:,0]>175)&(a[:,:,1]>155)&(a[:,:,2]<75)
            y,x=np.where(mask & (np.indices(mask.shape)[1]<1900))
            rows.append({'frame':p.name,'yellow_bbox':None if not len(x) else [int(x.min()),int(y.min()),int(x.max()),int(y.max())]})
    json.dump(rows,open(OUT/f'{case}_pixel_summaries.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print(json.dumps({'crop_count':len(records),'manifest':str(OUT/'crop_manifest.json')},ensure_ascii=False))
