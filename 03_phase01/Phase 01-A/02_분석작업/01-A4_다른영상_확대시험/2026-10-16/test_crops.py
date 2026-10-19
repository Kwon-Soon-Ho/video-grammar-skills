from pathlib import Path
import sys,json,copy
from prepare import write
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'skill-draft3/scripts'))
from evidence_catalog import catalog
logs=list((B/'cases').glob('*/*/실행기록.json'))
crops=json.loads((B/'normalized-crop-provenance.json').read_text(encoding='utf-8'))
base=crops[0];results=[]
for label,mut in [('valid',lambda c:None),('wrong_size',lambda c:c['crop_xyxy_native_pixels'].__setitem__(0,c['crop_xyxy_native_pixels'][0]+1)),('wrong_pixels_same_size',lambda c:c.update(crop_xyxy_native_pixels=[v+1 if i in [0,2] else v for i,v in enumerate(c['crop_xyxy_native_pixels'])])),('unknown_parent',lambda c:c.update(parent_path='not_registered.png')),('out_of_bounds',lambda c:c['crop_xyxy_native_pixels'].__setitem__(2,9000))]:
 c=copy.deepcopy(base);mut(c)
 try:catalog(logs,[c]);accepted=True;detail='accepted'
 except ValueError as e:accepted=False;detail=str(e)
 results.append({'test':label,'expected_accept':label=='valid','accepted':accepted,'correct':accepted==(label=='valid'),'detail':detail})
write(B/'root-audit/crop-tests.json',results)
assert all(r['correct'] for r in results)
print('5/5 crop provenance cases correct')
