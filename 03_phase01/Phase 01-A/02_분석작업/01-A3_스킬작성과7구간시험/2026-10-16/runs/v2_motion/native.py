from pathlib import Path
from PIL import Image
import json
r=Path('phase01a-a3/runs/v2_motion');j=json.loads((r/'cases/자료013/motiondetail/실행기록.json').read_text(encoding='utf8'))
for f in j['frames']:
 t=float(__import__('fractions').Fraction(f['actual_playback_seconds']));im=Image.open(f['path'])
 if t in [10.6,11.2,11.6,12,12.8,14,14.2,14.4,14.8,15.4]:
  im.crop((250,280,1650,1100)).save(r/f'ui_{t:.1f}.png')
 if t in [13,13.2,13.4,14.5,14.6,14.7,14.8,14.9,15,15.2,15.4,15.5]:im.crop((1000,850,2450,1550)).save(r/f'model_{t:.1f}.png')
 if t==12: im.crop((2200,1000,3400,1730)).save(r/'copy.png')
