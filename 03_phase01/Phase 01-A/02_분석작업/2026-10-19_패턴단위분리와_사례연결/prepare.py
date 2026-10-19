from pathlib import Path
from hashlib import sha256
import json,shutil
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OLD=WORK/'skill-revision-20261019'
candidate=HERE/'candidate/company-video-grammar-analyzer'
assert not candidate.exists(),'Existing revision must not be overwritten'
shutil.copytree(OLD/'candidate/company-video-grammar-analyzer',candidate,ignore=shutil.ignore_patterns('__pycache__'))
protected=json.loads((OLD/'protected-before.json').read_text(encoding='utf-8'))
receipt=json.loads((OLD/'publication-receipt.json').read_text(encoding='utf-8'))
for op in receipt['published_files']:
    for key in ('source','destination'):
        path=Path(op[key]);h=sha256(path.read_bytes()).hexdigest();assert h==op['sha256'],path
        protected.append({'path':str(path),'sha256':h})
for root in (OLD/'knowledge',OLD/'review-round1'):
    for p in root.rglob('*'):
        if p.is_file():protected.append({'path':str(p),'sha256':sha256(p.read_bytes()).hexdigest()})
unique={r['path']:r for r in protected}
for row in unique.values():assert sha256(Path(row['path']).read_bytes()).hexdigest().lower()==row['sha256'].lower()
(HERE/'protected-before.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'decision-D4.json').write_text(json.dumps({'date':'2026-10-19 Asia/Seoul','id':'D4','kind':'pattern_granularity_choice','selected':1,'original_answer':'① 전체 사례를 보존하고, 레이아웃·전체 흐름·독립적으로 재사용할 세부 동작을 각각 번호로 연결한다 (추천)','meaning':'전체 사례는 유지하고 독립 재사용 단위에 번호를 배정하며 조합 관계를 기록','approval_scope':'기록 구조 선택; 실제 관측 내용·회사 공통 문법·정확도에 대한 승인 아님'},ensure_ascii=False,indent=2),encoding='utf-8')
for path in candidate.rglob('*.md'):
    text=path.read_text(encoding='utf-8-sig').replace('0.1.0-draft.4','0.1.0-draft.5').replace('video-observation-0.2','video-observation-0.3')
    path.write_text(text,encoding='utf-8')
checker=candidate/'scripts/check_record.py'
text=checker.read_text(encoding='utf-8')
text=text.replace("need(d['schema_version']=='video-observation-0.2','unsupported schema; historical observations must stay unchanged')\n    need(d['skill_version']=='0.1.0-draft.4','skill version mismatch')", "versions={'video-observation-0.2':'0.1.0-draft.4','video-observation-0.3':'0.1.0-draft.5'}\n    need(d['schema_version'] in versions,'unsupported observation schema')\n    need(d['skill_version']==versions[d['schema_version']],'skill version mismatch')")
text=text.replace('def check(d,catalog=None):\n    try:_check(d,catalog);return []',"def check(d,catalog=None,allow_historical=False):\n    try:\n        need(isinstance(d,dict),'expected JSON object')\n        need(allow_historical or d.get('schema_version')=='video-observation-0.3','historical record: preserved source, not a current-format pass')\n        _check(d,catalog)\n        if d['schema_version']=='video-observation-0.3':\n            from reuse_map import check_reuse_map\n            check_reuse_map(d)\n        return []")
checker.write_text(text,encoding='utf-8')
print(json.dumps({'protected_files':len(unique),'new_candidate':str(candidate)},ensure_ascii=False))
