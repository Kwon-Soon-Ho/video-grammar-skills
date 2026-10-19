from pathlib import Path
import json,numpy as np
from PIL import Image
from fractions import Fraction
p=Path('phase01a-a3/runs/with_b/cases/자료005/blendnative');d=json.loads((p/'실행기록.json').read_text(encoding='utf-8'));frames=d['frames'];a=np.array(Image.open(frames[1]['path']),dtype=float);b=np.array(Image.open(frames[-1]['path']),dtype=float);delta=b-a; mask=np.abs(delta).mean(axis=2)>35;v=delta[mask];rows=[]
for f in frames:
 t=float(Fraction(f['actual_playback_seconds']));im=np.array(Image.open(f['path']),dtype=float);alpha=float(((im-a)[mask]*v).sum()/(v*v).sum());rows.append({'actual':f['actual_playback_seconds'],'new_scene_fraction_fit':round(alpha,4)})
Path('phase01a-a3/runs/with_b/T05_blend_measure.json').write_text(json.dumps({'method':'RGB linear least-squares fit of pixels with mean endpoint difference >35; endpoints actual 6 and 6.6; not original opacity','rows':rows,'error':'unknown; residual and gamma can bias'},indent=2),encoding='utf-8');print(rows)
