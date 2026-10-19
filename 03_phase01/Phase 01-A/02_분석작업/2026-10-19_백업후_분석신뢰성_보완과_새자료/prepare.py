from pathlib import Path
from hashlib import sha256
import shutil,json
from PIL import Image
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
assert json.loads((HERE/'backup-publication.json').read_text(encoding='utf-8'))['verified']
candidate=HERE/'candidate/company-video-grammar-analyzer';assert not candidate.exists()
shutil.copytree(WORK/'analyzer-realuse-20261019/candidate/company-video-grammar-analyzer',candidate,ignore=shutil.ignore_patterns('__pycache__'))
protected=json.loads((WORK/'analyzer-realuse-20261019/protected-before.json').read_text(encoding='utf-8'))
receipt=json.loads((WORK/'implementation-audit-20261019/publication-receipt.json').read_text(encoding='utf-8'))
for op in receipt['published_files']:
 for key in ('source','destination'):protected.append({'path':op[key],'sha256':op['sha256']})
unique={i['path']:i for i in protected}
for i in unique.values():assert sha256(Path(i['path']).read_bytes()).hexdigest().lower()==i['sha256'].lower()
(HERE/'protected-before.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2),encoding='utf-8')
specs=[]
def crop(case,filename,box,label):
 parent=WORK/'phase01a-a5b/cases/A5-K'/case/filename
 dest=HERE/'evidence'/label;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists()
 with Image.open(parent) as im:im.crop(box).save(dest)
 specs.append({'path':str(dest),'parent_path':str(parent),'crop_xyxy_native_pixels':list(box)})
for stamp in ('025.400','026.200','028.200','029.000'):
 frame=round(float(stamp)*30)
 crop('H03',f'f_{frame:05d}_{stamp}.png',(2320,450,3450,1400),'highlight-'+stamp+'.png')
for stamp in ('066.000','066.400','066.800','067.200','067.600','072.800','075.600'):
 frame=round(float(stamp)*30)
 crop('H04',f'f_{frame:05d}_{stamp}.png',(3190,60,3760,900),'inset-'+stamp+'.png')
(HERE/'crop-inputs.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'protected':len(unique),'pixel_exact_crops':len(specs),'candidate':str(candidate)},ensure_ascii=False))
