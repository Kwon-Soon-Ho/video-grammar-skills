from pathlib import Path
import shutil
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent/'R7_03_1_초기후보'
rels=['13_품질검수/평가계획/00_진행방식_검토안.md','13_품질검수/평가계획/01_정답과_판정단위.md','13_품질검수/평가계획/02_표본과_유출방지.md','13_품질검수/06_평가계획_읽는순서.md','08_검증결과/R7_03_입력보존.json','08_검증결과/R7_03_1_작성확인.json']
for r in rels:
 p=O/r;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(B/r,p)
