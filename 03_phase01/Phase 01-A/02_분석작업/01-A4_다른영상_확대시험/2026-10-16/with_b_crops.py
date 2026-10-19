from pathlib import Path
import json,hashlib
from fractions import Fraction
from PIL import Image
root=Path(__file__).parent
out=root/'with-b-roi';out.mkdir(exist_ok=True)
spec=[('A4-L','V03_with_more',None,(180,800,1500,1150)),('A4-L','V03',[101,104],(2900,790,3570,1530)),('A4-L','V04_with_more',None,(1300,750,2450,1850)),('A4-L','V04',[301.25,301.5,301.75,302],(350,970,1420,1150)),('A4-S','V06S',[237,239,242,244,246],(1950,900,3660,1830)),('A4-W','V06W',[242,244.5,247,249,250],(4600,200,7400,1800))]
records=[]
for aid,case,times,box in spec:
 logpath=root/'cases'/aid/case/'실행기록.json'
 log=json.loads(logpath.read_text(encoding='utf-8'))
 for f in log['frames']:
  t=float(Fraction(f['actual_playback_seconds']))
  if times is not None and t not in times:continue
  p=out/(case+'_'+str(t)+'.png')
  Image.open(f['path']).crop(box).save(p)
  records.append({'id':p.stem,'path':str(p.resolve()),'source_path':f['path'],'source_frame_id':f['frame_id'],'actual_seconds':f['actual_playback_seconds'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'crop_xyxy_native':box,'resize':None,'extraction_log':str(logpath.resolve())})
(out/'roi-log.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(records))
