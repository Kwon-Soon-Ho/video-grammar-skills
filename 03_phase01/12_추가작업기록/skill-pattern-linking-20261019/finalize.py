from pathlib import Path
from datetime import datetime,timezone
import json,sys,re
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,digest,check
from pattern_library import select
root=HERE/'candidate/company-video-grammar-analyzer'
library=load(HERE/'knowledge/pattern-library.json')
rows=['# 패턴 색인 - 전체 사례와 독립 재사용 단위','','원본 한 사례에서 분리한 개발 초안이다. 새 장면 적합성·내용 정확도·회사 승인과 구분한다.','','| 번호 | 역할 | 이름 | 상태 |','|---|---|---|---|']
for p in library['patterns']:
    role='과거 통합 항목 보존' if 'definition' not in p else ('전체 레이아웃' if p['category']=='LAYOUT' else '전체 흐름' if p['category']=='FLOW' else '독립 세부 동작')
    rows.append(f'| {p["id"]} | {role} | {p["name"]} | draft |')
rows+=['','전체 사례: development/H02/observations-linked.json 및 .md. 최초 상세 관측: observations-first-detail.json. 새 분리 정의는 과거 PAT-CARD-0001에서 유래했으며 그 번호의 뜻을 바꾸지 않았다.','','테두리만 조회한 결과: development/H02/selected-outline-only.json. 관련 주장 c022/c023/c024와 근거 8개, 미해결을 포함한다. 전체 레이아웃 정의는 포함하지 않는다. 새 장면 적용 실험 결과가 아니다.']
(HERE/'knowledge/00_패턴색인.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
records=[]
for item in load(HERE/'protected-before.json'):
    h=digest(item['path']);assert h.lower()==item['sha256'].lower(),item['path'];records.append({**item,'unchanged':True})
links=0
for p in root.rglob('*.md'):
    for relative in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
        if '://' not in relative and not relative.startswith('#'):
            assert (p.parent/relative.split('#')[0]).is_file(),relative;links+=1
core=load(HERE/'validation-core-retry1/checks.json');composition=load(HERE/'validation-composition/checks.json')
case=load(HERE/'development/H02/observations-linked.json');assert not check(case)
result={'utc':datetime.now(timezone.utc).isoformat(),'version':'0.1.0-draft.5','observation_schema':'video-observation-0.3','library_schema':'video-pattern-library-0.2','user_decision':'D4 option 1: whole case plus separate layout/flow/independent detail patterns','new_patterns':[p['id'] for p in library['patterns'] if 'definition' in p],'preserved_legacy_pattern':'PAT-CARD-0001','tests':{'core_regression':{'passed':core['passed'],'total':core['total'],'mode':'shared core with explicit historical source access; current renderer fixture normalized'},'composition':{'passed':composition['passed'],'total':composition['total']},'initial_fixture_adjustment':'The old repetition fixture failed the intentional current-schema composition requirement, then the old renderer fixture was adapted. Failed artifacts retained under validation-core and retry1.'},'source_content_approval':False,'fresh_video_comparison':False,'accuracy_or_effort_improvement_proven':False,'content_precision':None,'precision_reason':'독립 새 자료·전체 고유 주장 분모 검수 미실행','old_A5b_resumed':False,'installed_or_promoted':False,'reference_links_checked':links,'protected_files_unchanged':len(records),'protected_files':records,'candidate_files':[{'relative':p.relative_to(root).as_posix(),'sha256':digest(p)} for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts]}
(HERE/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('protected_files','candidate_files')},ensure_ascii=False))

