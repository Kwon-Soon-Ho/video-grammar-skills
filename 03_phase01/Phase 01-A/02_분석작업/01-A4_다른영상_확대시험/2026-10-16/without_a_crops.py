from pathlib import Path
import json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
out=root/'without_a_review';out.mkdir(exist_ok=True)
records=[]
for aid,case,times,box,name in [('A4-D','V01_without_more',None,(100,50,1250,300),'title'),('A4-G','V05',[6.4,7.2,7.6,8,8.4,8.8,9.2,9.6,10,10.4,10.8,10.933333333333334],(350,650,2200,1300),'ui')]:
    log=json.loads((root/'cases'/aid/case/'실행기록.json').read_text(encoding='utf-8'))
    from fractions import Fraction
    frames=[f for f in log['frames'] if times is None or any(abs(float(Fraction(f['actual_playback_seconds']))-t)<.001 for t in times)]
    if name=='title':
        board=Image.new('RGB',(1150,len(frames)*280),'#222222');d=ImageDraw.Draw(board)
    for i,f in enumerate(frames):
        crop=Image.open(f['path']).crop(box)
        p=out/f'{name}_{f["display_ordinal_zero_based"]}.png';crop.save(p)
        records.append({'path':str(p),'source':f['path'],'actual_seconds':f['actual_playback_seconds'],'crop_xyxy_native_pixels':box,'transform':'crop only, no resize'})
        if name=='title':
            board.paste(crop,(0,i*280+30));d.text((5,i*280+5),f['actual_playback_seconds'],fill='white')
    if name=='title':board.save(out/'title-board.png')
(out/'crop-log.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
