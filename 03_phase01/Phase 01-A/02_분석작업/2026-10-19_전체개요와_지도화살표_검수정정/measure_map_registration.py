"""Estimate screen-space landmark drift; does not recover an AE camera or layer rig."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;BASE=WORK/'analysis-reliability-20261019/fresh/cases/NEW-P/window'
OUT=HERE/'probes';OUT.mkdir(exist_ok=True)
def ncc(image,template):
    H,W=image.shape;h,w=template.shape;kernel=template-template.mean();shape=(H+h-1,W+w-1)
    corr=np.fft.irfft2(np.fft.rfft2(image,shape)*np.conj(np.fft.rfft2(kernel,shape)),shape)[:H-h+1,:W-w+1]
    def sums(a):
        s=np.pad(a,((1,0),(1,0))).cumsum(0).cumsum(1)
        return s[h:,w:]-s[:-h,w:]-s[h:,:-w]+s[:-h,:-w]
    norm=np.sqrt(np.maximum(sums(image*image)-sums(image)**2/(h*w),1e-12))*np.linalg.norm(kernel)
    score=corr/norm;y,x=np.unravel_index(np.argmax(score),score.shape);return int(x),int(y),float(score[y,x])
# Verify the correlation convention against a known inserted patch, not our video result.
test=np.random.default_rng(42).normal(size=(30,40));patch=test[9:16,12:21].copy();x,y,score=ncc(test,patch);assert (x,y)==(12,9) and score>.999999
first=Image.open(BASE/'f_01200_040.000.png').convert('RGB');last=Image.open(BASE/'f_01440_048.000.png').convert('RGB')
scale=4;A=np.asarray(first.resize((960,540)).convert('L'),dtype=float);B=np.asarray(last.resize((960,540)).convert('L'),dtype=float)
boxes=[('map-north',[1910,230,2200,430]),('map-west-south',[1400,1440,1760,1680]),('map-east-south',[2840,1560,3240,1820]),('police-card',[440,850,930,1010]),('policy-panel',[330,270,1000,380])]
results=[];font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18);tiles=[]
for name,box in boxes:
    x0,y0,x1,y1=[int(v/scale) for v in box];patch=A[y0:y1,x0:x1];pad=70;sx0=max(0,x0-pad);sy0=max(0,y0-pad);sx1=min(B.shape[1],x1+pad);sy1=min(B.shape[0],y1+pad)
    dx,dy,quality=ncc(B[sy0:sy1,sx0:sx1],patch);dest=[(sx0+dx)*scale,(sy0+dy)*scale,(sx0+dx+patch.shape[1])*scale,(sy0+dy+patch.shape[0])*scale]
    src=[x0*scale,y0*scale,x1*scale,y1*scale];row={'name':name,'source_box':src,'matched_box':dest,'NCC':quality,'source_center':[(src[0]+src[2])/2,(src[1]+src[3])/2],'matched_center':[(dest[0]+dest[2])/2,(dest[1]+dest[3])/2]};results.append(row)
    left=first.crop(src);right=last.crop(dest);w=left.width;h=left.height;tile=Image.new('RGB',(w*2,h+30),'#181818');tile.paste(left,(0,30));tile.paste(right,(w,30));ImageDraw.Draw(tile).text((4,3),name+' / 40s then 48s / NCC '+str(round(quality,3)),font=font,fill='white');tiles.append(tile)
width=max(t.width for t in tiles);height=sum(t.height+10 for t in tiles);sheet=Image.new('RGB',(width,height),'#181818');cursor=0
for t in tiles:sheet.paste(t,(0,cursor));cursor+=t.height+10
sheet.save(OUT/'map-landmark-matches.jpg',quality=95)
accepted=[r for r in results if r['NCC']>=.7];fit=None
if len(accepted)>=3:
    src=np.asarray([r['source_center'] for r in accepted]);dst=np.asarray([r['matched_center'] for r in accepted]);X=np.column_stack([src,np.ones(len(src))]);matrix=np.linalg.lstsq(X,dst,rcond=None)[0];pred=X@matrix
    fit={'affine_2d_row_matrix':matrix.tolist(),'residual_pixels':np.linalg.norm(pred-dst,axis=1).tolist(),'landmark_names':[r['name'] for r in accepted],'limitation':'Coarse 4px image sampling; no scale search, no rig/camera identification. Approximate matching must be visually reviewed.'}
output={'method':'quarter-size grayscale normalized cross-correlation of fixed templates and coarse affine least squares','sources':[str(BASE/'f_01200_040.000.png'),str(BASE/'f_01440_048.000.png')],'matches':results,'fit':fit,'visual_review':'pending','AE_rig_recovered':False}
(OUT/'map-registration.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(output,ensure_ascii=False))
