import json
from pathlib import Path
b=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');d=json.loads((b/'13_품질검수/품질항목_정본.json').read_text(encoding='utf-8'))
for x in d['cards']:
 if x['id'] in ['Q-MOTION-04','Q-SCREEN-03','Q-TRUST-01','Q-CAP-02','Q-CAP-01']:print(json.dumps(x,ensure_ascii=False,indent=2))
