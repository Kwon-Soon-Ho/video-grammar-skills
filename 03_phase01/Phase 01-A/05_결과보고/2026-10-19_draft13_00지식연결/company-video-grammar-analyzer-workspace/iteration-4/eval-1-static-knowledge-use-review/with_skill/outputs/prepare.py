from pathlib import Path
import json, shutil, hashlib
from PIL import Image
O=Path(__file__).resolve().parent
W=next(p for p in O.parents if (p/'AGENTS.md').exists())
I=W/'knowledge-linked-skill-20261019/eval-inputs'
for d in ['prior','evidence','queries']: (O/d).mkdir(exist_ok=True)
for p in (I/'static').glob('*.md'): shutil.copy2(p,O/'prior'/p.name)
shutil.copy2(I/'input.md',O/'prior/input.md')
for t in [134,172]: shutil.copy2(I/f'static/evidence/{t}.png',O/f'evidence/{t}.png')
rois={'e1_logos':(134,(1000,1000,2750,1910)), 'e1_roles':(134,(4750,660,6700,1380)), 'e1_arrows':(134,(2900,930,4700,1740)), 'e1_work':(134,(4500,1350,7200,2010)), 'e2_logos':(172,(2500,910,4800,1510)), 'e2_value':(172,(350,540,2470,840)), 'e2_building':(172,(4790,640,7440,1790)), 'e2_number':(172,(0,850,2450,1640))}
manifest=[]
for name,(t,box) in rois.items():
    src=O/f'evidence/{t}.png'; dest=O/f'evidence/{name}.png'
    with Image.open(src) as im: im.crop(box).save(dest)
    manifest.append({'id':name,'path':str(dest),'source':str(src),'box_ltrb_exclusive':box,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'operation':'crop only; no resize/recolor/rotation'})
(O/'roi-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
c=json.loads((O/'knowledge-catalog.json').read_text(encoding='utf-8'))
ids=['REL-PARALLEL','REL-CORRELATION','REL-SPACE','LAYOUT-SPLIT','LAYOUT-SPLIT-COMPARE','LAYOUT-NETWORK','LAYOUT-SPACE-CALLOUT','LAYOUT-CARD-GROUP','STYLE-3D','STYLE-ISOMETRIC','SCREEN-GROUP','SCREEN-HIERARCHY','SCREEN-COLOR','SCREEN-DATA','SCREEN-TIME-READ','IP-04','MR-03','KNOW-LAYOUT-NETWORK','KNOW-LAYOUT-SPLIT','KNOW-LAYOUT-SPACE-CALLOUT','Q-INFO-02','Q-INFO-03','Q-SCREEN-01','Q-TRUST-01','Q-TRUST-02','Q-BRAND-01','Q-MOTION-01']
selected=[r for r in c['concepts'] if r['id'] in ids]
(O/'queries/selected-concept-source.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(selected,ensure_ascii=False,indent=2))
