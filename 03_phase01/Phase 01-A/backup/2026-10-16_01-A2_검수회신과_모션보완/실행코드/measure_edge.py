from pathlib import Path
from PIL import Image
from fractions import Fraction as F
import json,statistics,hashlib
HERE=Path(__file__).resolve().parent
RUN=HERE.parent/'phase01a-a2/cases/자료013/motion_review'
record=json.loads((RUN/'실행기록.json').read_text(encoding='utf-8'))
rows=[]
for f in record['frames']:
    im=Image.open(f['path']).convert('L');pix=im.load()
    # Large middle E piece's right vertical boundary, within the derived raster only.
    # Averaging a vertical strip suppresses thin horizontal decorative strokes.
    stripe=[sum(pix[x,y] for y in range(470,551))/81 for x in range(1920)]
    candidates=[(sum(stripe[x-8:x-3])/5-sum(stripe[x+3:x+8])/5,x) for x in range(300,1100)]
    strength,x=max(candidates)
    rows.append({'seconds':f['actual_playback_seconds'],'derived_right_edge_x_candidate':x,'edge_contrast':round(strength,3),'frame_id':f['frame_id'],'image_sha256':f['sha256']})
result={'purpose':'diagnostic edge candidate, requires visual correspondence check','coordinate_space':'derived 1920x1080 raster; not original pixel coordinates or display coordinates','roi_strip_y':[470,551],'x_search':[300,1100],'method':'strongest signed luma edge across ±3..8px after 81-row mean','uncertainty':'unknown; texture, glow, occlusion and changing color may bias boundary; no fit to AE easing curve','samples':rows}
(HERE/'E_가운데조각_경계진단.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
