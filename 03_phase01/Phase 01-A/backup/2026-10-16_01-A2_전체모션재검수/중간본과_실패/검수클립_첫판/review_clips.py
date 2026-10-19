from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a1/후보런타임'))
import av
OUT=HERE/'추가검수_화면';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
specs=[('N1','자료005','5.9','6.6','장헌_장면전환'),('N2','자료005','7.8','9.5','장헌_막대와_원형진행'),('N3','자료005','21.1','22.7','장헌_매출처도넛'),('N4','자료013','1.8','3.8','EG_제목공개와_교체'),('N5','자료013','6.7','8.3','EG_첫화면진입'),('N6','자료013','10.6','12.3','EG_창재배치와_다음화면'),('N7','자료013','12.8','14.5','EG_모델확대와_이동'),('N8','자료013','14.2','15.5','EG_빛띠_밝기변화')]
records=[];qa=Image.new('RGB',(1440,8*310),'#20242c');d=ImageDraw.Draw(qa)
for aid in ['자료005','자료013']:
    p=HERE/'cases'/aid/'scan';data=np.load(p/'영상관측_저해상도배열.npz',allow_pickle=False)['rgb'];idx=json.loads((p/'전프레임_시각색인.json').read_text(encoding='utf-8'));run=json.loads((p/'실행기록.json').read_text(encoding='utf-8'));rate=30 if aid=='자료005' else 60
    assert all((int(b['reported_pts'])*F(b['time_base'])-int(a['reported_pts'])*F(a['time_base']))==F(1,rate) for a,b in zip(idx,idx[1:]))
    for key,asset,start,end,label in specs:
        if asset!=aid:continue
        chosen=[i for i,m in enumerate(idx) if F(start)<=F(m['seconds'])<=F(end)]
        dest=OUT/f'{key}_{label}.mp4'
        if dest.exists():raise ValueError('preserve_existing_clip')
        header=21 if aid=='자료005' else 22;height=data.shape[1]+header
        frames=[]
        with av.open(str(dest),mode='w',format='mp4',options={'movflags':'+faststart'}) as c:
            s=c.add_stream('libx264',rate=rate);s.width=480;s.height=height;s.pix_fmt='yuv420p';s.options={'crf':'16','preset':'fast'}
            for n,j in enumerate(chosen):
                canvas=Image.new('RGB',(480,height),'#20242c');canvas.paste(Image.fromarray(data[j]),(0,header));ImageDraw.Draw(canvas).text((5,1),f'{key} | source {float(F(idx[j]["seconds"])):.3f}s | {rate} fps',font=font,fill='white')
                f=av.VideoFrame.from_ndarray(np.asarray(canvas),format='rgb24');f.pts=n;f.time_base=F(1,rate)
                for packet in s.encode(f):c.mux(packet)
                if n in {0,len(chosen)//2,len(chosen)-1}:frames.append(canvas.copy())
            for packet in s.encode():c.mux(packet)
        with av.open(str(dest),mode='r') as c:
            decoded=list(c.decode(video=0));assert len(decoded)==len(chosen);assert all(f.width==480 and f.height==height for f in decoded)
            assert all(f.pts*f.time_base==F(i,rate) for i,f in enumerate(decoded))
        slot=int(key[1:])-1
        for n,canvas in enumerate(frames):qa.paste(canvas,(n*480,slot*310))
        # Still strip lets non-video previews show the selected temporal progression.
        strip=Image.new('RGB',(1440,height),'#20242c')
        for n,canvas in enumerate(frames):strip.paste(canvas,(n*480,0))
        strip.save(OUT/f'{key}_{label}_표본.jpg',quality=95)
        records.append({'id':key,'asset_id':aid,'source_sha256':run['input_sha256'],'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source_first_seconds':idx[chosen[0]]['seconds'],'source_last_seconds':idx[chosen[-1]]['seconds'],'frame_count':len(chosen),'source_frame_rate_in_window':str(rate),'source_proxy_sha256':run['tracking_proxy']['sha256'],'normalization':'clip0 = source first selected PTS; preserves equal source frame spacing, no interpolation or speed change','display_transform':{'resize':'source raster -> 480px motion proxy (swscale BILINEAR, see run)','header_padding':[0,header],'canvas':[480,height],'text_added':'source time label in added header only','SAR':'source unknown; raw-raster aspect preserved; not display-aspect verification'},'audio':'not included, not decoded or evaluated','codec':'libx264/yuv420p, lossy preview; source frame PNG/NPZ remain evidence','decoded_export_verified':True,'source_frame_pins':[{'ordinal':idx[i]['ordinal'],'reported_pts':idx[i]['reported_pts'],'time_base':idx[i]['time_base'],'seconds':idx[i]['seconds']} for i in chosen]})
    del data
qa.save(OUT/'검수영상_첫중간끝_QA.jpg',quality=94)
(OUT/'검수영상_파생기록.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'id':r['id'],'frames':r['frame_count'],'verified':r['decoded_export_verified']} for r in records],ensure_ascii=False))
