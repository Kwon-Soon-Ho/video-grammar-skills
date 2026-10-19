from pathlib import Path
from PIL import Image,ImageDraw
from fractions import Fraction
import numpy as np,json
ROOT=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest');OUT=ROOT/'runs/retest_a';audit=[]
def load(p):
    audit.append(str(p));return Image.open(p).convert('RGB')
def sheet(items,name,cols=2):
    w=max(im.width for label,im in items);h=max(im.height for label,im in items)+25
    board=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*h),(28,31,36));d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(items):
        x=(i%cols)*w;y=(i//cols)*h;board.paste(im,(x,y+25));d.text((x+4,y+6),label,fill='white')
    board.save(OUT/name)
extra=OUT/'cases/자료013/extra1';pLog=extra/'실행기록.json';audit.append(str(pLog));log=json.loads(pLog.read_text(encoding='utf8'))
artifact=[];textures=[];frames={}
for f in log['frames']:
    t=float(Fraction(f['actual_playback_seconds']));im=load(Path(f['path']));frames[t]=np.asarray(im)
    if t<=3.6:artifact.append((f'{t:.6f}s native x2550..3650 y880..1250',im.crop((2550,880,3650,1250))))
    if t>=4.8:textures.append((f'{t:.3f}s native E texture x650..1350 y850..1450',im.crop((650,850,1350,1450))))
sheet(artifact,'T01_subframe_artifact_sequence.png',2)
sheet(textures,'T01_held_texture_sequence.png',2)
summary=[]
for ta,tb in [(4.8,5.0),(5.0,5.1),(5.1,5.3),(5.3,5.5)]:
    a=frames[ta].astype('int16');b=frames[tb].astype('int16')
    for name,box in [('e_texture',(650,850,1350,1450)),('e_toptexture',(800,0,1800,250)),('background_right',(3320,0,3840,850)),('background_left',(0,300,400,650)),('background_value',(2300,500,3200,1000)),('body',(2250,1470,3700,1810))]:
        x1,y1,x2,y2=box;d=np.abs(a[y1:y2,x1:x2]-b[y1:y2,x1:x2]);summary.append({'a':ta,'b':tb,'region':name,'mean_abs_rgb_difference':float(d.mean()),'fraction_any_channel_gt10':float((d.max(axis=2)>10).mean())})
(OUT/'T01_hold_diff_exploratory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
# Larger small-print and supporting detail crop from T04 full native frame.
im=load(OUT/'cases/자료005/extra1/f_00195_006.500.png');im.crop((0,0,980,820)).save(OUT/'T04_left_detail_native.png')
(OUT/'explore3_reads.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'T01_extra_complete':log['complete_target_selection'],'timing':log['timing_status'],'count':len(log['frames'])}))
