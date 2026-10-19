from pathlib import Path
import json,math
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'검수판';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
records=[]
def sheet(name,frames,crop=None,cols=3,width=640):
    for part in range(math.ceil(len(frames)/12)):
        fs=frames[part*12:(part+1)*12];first=Image.open(fs[0]['path']);box=crop or (0,0,first.width,first.height)
        height=round((box[3]-box[1])*width/(box[2]-box[0]));canvas=Image.new('RGB',(cols*width,math.ceil(len(fs)/cols)*(height+26)),'#20242c');d=ImageDraw.Draw(canvas)
        for i,f in enumerate(fs):
            im=Image.open(f['path']).crop(box).resize((width,height),Image.Resampling.LANCZOS);x=i%cols*width;y=i//cols*(height+26);canvas.paste(im,(x,y));d.text((x+6,y+height+2),f"{float(F(f['actual_playback_seconds'])):.3f}s",font=font,fill='white')
        dest=OUT/f'{name}_{part+1}.jpg';canvas.save(dest,quality=96)
        records.append({'sheet':str(dest),'frame_pins':[{'path':f['path'],'sha256':f['sha256'],'seconds':f['actual_playback_seconds']} for f in fs],'source_crop':box,'derived_width':width,'order':'reverse' if '역순' in name else 'forward','colors':'unaltered'})
for group in ['eg_intro','eg_late','eg_model','jh_all']:
    aid='자료005' if group=='jh_all' else '자료013'
    run=json.loads((HERE/'cases'/aid/group/'실행기록.json').read_text(encoding='utf-8'));fs=run['frames']
    sheet(group,fs)
    if group=='eg_model':sheet('모델_원근형태',fs,(380,300,1180,880),cols=3,width=640)
    if group=='eg_late':
        sheet('문구_역순',list(reversed(fs)),(1100,420,1820,880),cols=3,width=640)
        sheet('E내부_역순',list(reversed(fs)),(240,0,1060,1080),cols=3,width=440)
# A global temporal change map is a search aid, not a list of recognized motions.
for aid in ['자료005','자료013']:
    folder=HERE.parent/'phase01a-a2-fullmotion/cases'/aid/'scan'
    arr=np.load(folder/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((folder/'전프레임_시각색인.json').read_text(encoding='utf-8'))
    rows=[]
    for sec in range(24 if aid=='자료005' else 16):
        chosen=[i for i,m in enumerate(idx) if F(sec)<=F(m['seconds'])<F(sec+1)]
        if len(chosen)<2:continue
        maximum=arr[chosen].max(0).astype(np.int16);minimum=arr[chosen].min(0).astype(np.int16);dif=(maximum-minimum).max(2)
        vals=[]
        for gy in range(3):
            for gx in range(6):
                tile=dif[gy*arr.shape[1]//3:(gy+1)*arr.shape[1]//3,gx*80:(gx+1)*80]
                vals.append({'grid':[gx,gy],'mean_range':float(tile.mean()),'fraction_range_gt_12':float((tile>12).mean()),'max_range':int(tile.max())})
        rows.append({'start':sec,'end':min(sec+1,float(F(idx[-1]['seconds']))),'grid_temporal_ranges':vals})
    (OUT/f'{aid}_구역별변화.json').write_text(json.dumps({'coordinate_space':list(arr.shape[1:3][::-1]),'method':'per-1sec RGB channel max-min, search aid only, threshold12 heuristic not calibrated','rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    # Time-space strips across an unobscured background and foreground E.
    if aid=='자료013':
        samples=[i for i,m in enumerate(idx) if i%6==0]
        for name,axis,pos,lo,hi in [('배경_수평단면','y',32,0,480),('E_세로단면','x',105,0,270)]:
            strips=np.stack([arr[i,pos,lo:hi] if axis=='y' else arr[i,lo:hi,pos] for i in samples])
            Image.fromarray(strips).resize((960,620)).save(OUT/f'{name}.png')
    del arr
(OUT/'검수판_시간연결.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(records),'sheets prepared')
