import shutil,json
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent/'R7_03_2_초기후보';W=json.loads((B/'08_검증결과/R7_03_2_작성확인.json').read_text(encoding='utf-8'))
for r in list(W['outputs'])+['08_검증결과/R7_03_2_작성확인.json']:
 p=O/r;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(B/r,p)
