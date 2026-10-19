from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil
HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OLD=WORK/'phase01a-a5b/candidate/company-video-grammar-analyzer'
NEW=HERE/'candidate/company-video-grammar-analyzer'
assert not NEW.exists(),'Do not overwrite an existing revision candidate'
protected=json.loads((WORK/'research/ponytail-rea-20261019/protected-before-report.json').read_text(encoding='utf-8-sig'))
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
matches=list((D/'Phase 01-A/03_분석스킬').rglob('company-video-grammar-analyzer/SKILL.md'))
assert len(matches)==1,matches
for p in matches[0].parent.rglob('*'):
    if p.is_file():protected.append({'path':str(p),'sha256':sha256(p.read_bytes()).hexdigest()})
for r in protected:assert sha256(Path(r['path']).read_bytes()).hexdigest().lower()==r['sha256'].lower()
(HERE/'protected-before.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copytree(OLD,NEW)
(HERE/'decisions.json').write_text(json.dumps({'date':'2026-10-19','decisions':[{'id':'D1','kind':'user_scope_choice','selected':1,'meaning':'분석 정확도와 근거 기록 우선; 전문가 판단·재제작 인계 형식 연결','original_answer':'① 분석 정확도·근거 기록을 먼저 보완하고, 전문가 판단·재제작에 넘길 기록 형식까지 연결한다 (추천)','authorization_scope':'별도 수정 후보 개발; 회사 문법 승인·실전 성능 합격 아님'}]},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'candidate':str(NEW),'protected_files':len(protected),'old_version':'0.1.0-draft.3','new_target':'0.1.0-draft.4'},ensure_ascii=False))
