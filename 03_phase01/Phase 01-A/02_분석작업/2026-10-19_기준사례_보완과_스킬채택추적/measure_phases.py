from pathlib import Path
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OUT=HERE/'inspection'
def load(p):return json.loads(Path(p).read_text('utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def frames(code):
 d={}
 for root in [WORK/'analysis-reliability-20261019/fresh/cases'/code,HERE/'extraction/cases'/code]:
  for p in root.glob('*/실행기록.json'):
   log=load(p)
   if log.get('complete_target_selection'):
    for f in log['frames']:d.setdefault(F(f['actual_playback_seconds']),f)
 return d
N=frames('NEW-N');P=frames('NEW-P');samples=[]
for t,row in sorted(N.items()):
 if not F(173)<=t<=F(175):continue
 with Image.open(row['path']) as im:a=np.asarray(im.crop((1000,230,3300,380)),dtype=np.int16)
 mask=(a[:,:,1]-a[:,:,0]>60)&(a[:,:,1]>130)&(a[:,:,1]*10>a[:,:,2]*8)
 xs=np.where(mask.sum(axis=0)>35)[0]
 if len(xs):samples.append({'time':str(t),'left_x':int(xs[0]+1000),'right_x':int(xs[-1]+1000),'separation_px':int(xs[-1]-xs[0]),'method':'cyan columns >35 pixels, native ROI (1000,230,3300,380); visible-bar extent, not AE text width'})
line=[]
for t,row in sorted(P.items()):
 if not F('42.4')<=t<=F('43.8'):continue
 with Image.open(row['path']) as im:a=np.asarray(im.crop((1908,605,1933,790)),dtype=np.int16)
 mask=(a[:,:,0]-a[:,:,1]>25)&(a[:,:,2]-a[:,:,1]>15)&(a[:,:,0]>70)
 ys=np.where(mask.sum(axis=1)>3)[0]
 line.append({'time':str(t),'colored_top_y':int(ys[0]+605) if len(ys) else None,'colored_pixels':int(mask.sum()),'method':'pink pixels in fixed native ROI (1908,605,1933,790); visible filled extent, not translation of a fixed glyph'})
# Compare repeating rendered poses to distinguish model sway from an alpha pulse.
pose=[];box=(900,900,2300,2050)
for t in [F(170),F('170.2'),F('170.5'),F('170.8'),F(171)]:
 with Image.open(N[t]['path']) as im:base=np.asarray(im.crop(box).resize((280,230)),dtype=np.int16)
 comparisons=[]
 for lag in [F('0.5'),F(1),F('1.5'),F(2)]:
  if t+lag not in N:continue
  with Image.open(N[t+lag]['path']) as im:a=np.asarray(im.crop(box).resize((280,230)),dtype=np.int16)
  comparisons.append({'lag_seconds':str(lag),'mean_abs_RGB_difference':float(np.abs(a-base).mean())})
 pose.append({'time':str(t),'roi_native':list(box),'comparisons':comparisons})
write(OUT/'phase-measurements.json',{'N_label_bars':samples,'P_line_growth':line,'N_pose_comparison':pose,'limitations':['8-bit decoded RGB; no source layer/keyframe knowledge','Color threshold extents can vary with antialiasing, compression and overlap','Pose patch includes model and nearby arcs; low difference supports a repeated rendering, not a uniquely recovered rotation angle or easing function']})
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',16)
spec=[]
def board(name,ts,box,thumb,cols):
 tiles=[]
 for t in ts:
  t=F(str(t));row=N[t]
  with Image.open(row['path']) as im:a=im.crop(box)
  p=OUT/f'{name}-{float(t)}.png';a.save(p);spec.append({'path':str(p),'parent_path':row['path'],'crop_xyxy_native_pixels':list(box)});a.thumbnail(thumb);tiles.append((t,a))
 w,h=thumb[0],thumb[1]+25;b=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),'#151515');d=ImageDraw.Draw(b)
 for i,(t,a) in enumerate(tiles):
  x=i%cols*w;y=i//cols*h;b.paste(a,(x,y+25));d.text((x+3,y+3),str(float(t)),font=font,fill='white')
 b.save(OUT/(name+'.jpg'),quality=95)
board('N-background-lower',[166,167,168,169,170,172,174,176,178,180],(7000,1580,7680,2100),(340,260),5)
board('N-pose-cycle',[170,170.5,171,171.5,172,172.5,173,173.5],(800,900,2500,2050),(425,288),4)
board('N-section-tail',[173,174,175,176,177,178,179,180,181,181.4],(4750,400,7000,1900),(450,300),5)
write(OUT/'phase-crop-inputs.json',spec)
print(json.dumps({'label_samples':len(samples),'line_samples':len(line),'pose_comparisons':pose},ensure_ascii=False))
