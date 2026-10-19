from pathlib import Path
from PIL import Image
r=Path.cwd();p=r/'phase01a-a2-retest/analysis_input/cases/자료013/T01/f_00240_004.000.png';Image.open(p).crop((2250,1000,3700,1810)).save(r/'phase01a-a3/runs/with_a/T01_text_full.png')
