from pathlib import Path
from PIL import Image
r=Path('phase01a-a3/runs/v2_motion');d=r/'cases/자료005/chartdetail'
for fn in ['f_00180_006.000.png','f_00189_006.300.png','f_00282_009.400.png','f_00540_018.000.png']:
 im=Image.open(d/fn);im.crop((0,0,980,800)).save(r/('left_'+fn))
