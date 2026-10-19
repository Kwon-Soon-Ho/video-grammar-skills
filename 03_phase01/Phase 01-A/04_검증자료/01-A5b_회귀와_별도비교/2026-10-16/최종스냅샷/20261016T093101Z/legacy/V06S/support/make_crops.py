import json
from pathlib import Path
from PIL import Image
base=Path.cwd(); run=base/'phase01a-a5b/legacy/V06S'; inp=json.loads((run/'input.json').read_text('utf-8-sig'))
frames=[]
for log in inp['raw_extraction_logs']:frames+=json.loads(Path(log).read_text('utf-8-sig'))['frames']
from fractions import Fraction as F
by={float(F(x['actual_playback_seconds'])):x for x in frames}
spec=[]
def add(t,box,name):spec.append((t,box,name))
for t in [235.1,235.2,235.4,235.6,235.8,236,236.2,236.4]:add(t,[1300,150,2550,570],'title')
for t in [236.6,236.8,237,237.4,238]:add(t,[100,650,1150,1660],'safety')
for t in [238.1,238.2,238.4,239]:add(t,[950,650,1950,1660],'quality')
for t in [239.1,239.2,239.4,240]:add(t,[1850,650,2800,1660],'schedule')
for t in [240.1,240.2,240.4,241,242.5]:add(t,[2780,650,3800,1660],'efficiency')
for t in [244,244.2,244.3,244.5]:add(t,[650,1920,3230,2100],'subtitle')
for t in [245,245.4,245.6,245.8,245.9,245.96666666666667]:add(t,[100,700,1900,1700],'exit')
crops=[]
for i,(t,box,name) in enumerate(spec):
 f=by[t];p=run/'support'/f'c{i+1:02}_{name}_{t:.3f}.png';im=Image.open(f['path']);im.crop(box).convert('RGB').save(p);crops.append({'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':box,'actual_seconds':f['actual_playback_seconds']})
(run/'support/crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),'utf-8')
print(len(crops))
