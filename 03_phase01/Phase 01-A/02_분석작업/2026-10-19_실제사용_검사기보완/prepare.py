from pathlib import Path
from hashlib import sha256
import shutil,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OLD=WORK/'skill-pattern-linking-20261019'
target=HERE/'candidate/company-video-grammar-analyzer'
assert not target.exists()
shutil.copytree(OLD/'candidate/company-video-grammar-analyzer',target,ignore=shutil.ignore_patterns('__pycache__'))
protected=json.loads((OLD/'protected-before.json').read_text(encoding='utf-8'))
receipt=json.loads((OLD/'publication-receipt.json').read_text(encoding='utf-8'))
for op in receipt['published_files']:
    for key in ('source','destination'):
        p=Path(op[key]);h=sha256(p.read_bytes()).hexdigest();assert h==op['sha256'],p;protected.append({'path':str(p),'sha256':h})
unique={r['path']:r for r in protected}
for row in unique.values():assert sha256(Path(row['path']).read_bytes()).hexdigest().lower()==row['sha256'].lower()
(HERE/'protected-before.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'scope.json').write_text(json.dumps({'scope':'분석 신뢰성 범주의 실제 영상 개발 실행과 발견 오류 수정','full_research_adopted':False,'expert_judgment_and_reconstruction_completed':False,'default_application':'사용자 범위 정정에 따라 보류; 이 단계에서 기본 설치/승격하지 않음','cases':['K-GEO H03 25~35s','K-GEO H04 66~76s'],'exposure':'기존 기준답안 준비 때 노출된 자료; 새 홀드아웃·독립 비교 아님','third_party_or_paid_api_execution':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'protected':len(unique),'candidate':str(target)},ensure_ascii=False))
