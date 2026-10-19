import json,shutil
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent/'R7_02_초기후보';OUT.mkdir(exist_ok=True)
d=json.loads((BASE/'08_검증결과/R7_02_작성확인.json').read_text(encoding='utf-8'))
for r in list(d['output_hashes'])+['08_검증결과/R7_02_작성확인.json','08_검증결과/R7_02_입력보존.json']:
 p=OUT/r;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(BASE/r,p)
