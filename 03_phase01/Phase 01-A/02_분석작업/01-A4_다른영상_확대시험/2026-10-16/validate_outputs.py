from pathlib import Path
import sys,json
from prepare import write
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'skill-draft3/scripts'))
from evidence_catalog import catalog
from check_observations import check
logs=list((B/'cases').glob('*/*/실행기록.json'))
crops={}
for p in (B/'company-video-grammar-analyzer-workspace').glob('iteration-*/eval-*/*/outputs/observations.json'):
 for e in json.loads(p.read_text(encoding='utf-8'))['evidence']:
  parent=e.get('parent_path',e.get('source_path'))
  box=e.get('crop_xyxy_native_pixels',e.get('crop_xyxy_native'))
  if not box:
   for tr in e.get('transforms',[]):
    if tr.get('op')=='crop' and tr.get('resize') is None:box=tr.get('xyxy')
  if parent and box:crops[e['path']]={'path':e['path'],'parent_path':parent,'crop_xyxy_native_pixels':box}
write(B/'normalized-crop-provenance.json',list(crops.values()))
cat=catalog(logs,list(crops.values()));write(B/'all-evidence-catalog.json',cat)
res=[]
for p in (B/'company-video-grammar-analyzer-workspace').glob('iteration-*/eval-*/*/outputs/observations.json'):
 try:
  d=json.loads(p.read_text(encoding='utf-8'));errors=check(d,cat)
 except Exception as e:errors=[repr(e)]
 res.append({'path':str(p),'errors':errors,'content_verified':False})
write(B/'output-validation.json',res)
for r in res:print(str(Path(r['path']).relative_to(B)),r['errors'])
