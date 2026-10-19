from pathlib import Path
import sys,json
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'phase01a-a1/후보런타임'))
from PIL import Image
from fractions import Fraction
jobs={
'H01':('A5-T',[(1.8,[250,1300,1100,1780]),(2.2,[250,1300,1100,1780]),(2.6,[250,1300,1800,1780]),(3,[250,1100,1800,1780]),(3.4,[1900,1450,3200,1830]),(3.8,[1900,1450,3200,1830]),(4.6,[1900,1450,3350,1870]),(5.6,[1900,1450,3350,1950]),(6.4,[1900,1450,3350,1950]),(6.9,[2700,0,3840,800]),(7.3,[0,0,3840,1000])]),
'H02':('A5-A',[(12,[700,850,1900,1650]),(12.6,[650,700,1900,1650]),(13,[650,700,1900,1650]),(13.4,[650,700,1900,1650]),(14.6,[650,700,1900,1650]),(16.8,[650,700,1900,1650]),(17.4,[650,700,1900,1650]),(18.2,[650,700,2500,1650]),(18.6,[650,700,3300,1900])]),
'H03':('A5-K',[(25,[50,20,1000,250]),(25,[450,1450,3350,2050]),(25.2,[2400,400,3420,1480]),(28,[2400,400,3420,1480]),(29.8,[0,0,3840,2160]),(30.1,[20,20,1050,250]),(31.6,[0,1810,3840,2160]),(32.3,[0,1810,3840,2160])]),
'H04':('A5-K',[(66,[3180,70,3790,1010]),(67,[0,20,1200,260]),(67.3,[0,20,1200,260]),(67.5,[0,20,1200,260]),(67.8,[0,20,1200,260]),(67,[1100,1880,2600,2160]),(67.7,[1100,1880,2600,2160]),(71.4,[0,0,3840,2160]),(71.5,[0,0,3840,2160]),(75,[3180,70,3790,1010])])}
out=B/'reference';out.mkdir(exist_ok=True);ledger=[]
for cid,(aid,j) in jobs.items():
 frames=[]
 for phase in [cid,'REF-'+cid]:frames+=json.loads((B/'cases'/aid/phase/'실행기록.json').read_text(encoding='utf-8'))['frames']
 for i,(t,box) in enumerate(j):
  f=next(x for x in frames if Fraction(x['actual_playback_seconds'])==Fraction(str(t)))
  p=out/f'{cid}-c{i+1:02}.png'
  with Image.open(f['path']) as im:im.convert('RGB').crop(box).save(p)
  ledger.append({'case_id':cid,'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':box,'actual_seconds':f['actual_playback_seconds']})
(out/'crops.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
print('reference crops',len(ledger))
