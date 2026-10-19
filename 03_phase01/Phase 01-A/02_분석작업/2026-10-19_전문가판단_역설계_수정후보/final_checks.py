from pathlib import Path
from datetime import datetime,timezone
import sys,json,re,subprocess
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;CANDIDATE=HERE/'candidate/company-video-grammar-analyzer'
sys.path.insert(0,str(CANDIDATE/'scripts'))
from check_record import load,check,digest
from copy import deepcopy

source=HERE/'development/H02/observations.json'
record=load(source)
catalog=load(WORK/'phase01a-a5b/trials/H02-r1-with_skill/support/evidence-catalog.json')
assert not check(record,catalog)
false_record=deepcopy(record)
obj=next(o for o in false_record['objects'] if o['id']=='glyph')
obj['identity']['label']='큰 숫자 4'
cid=obj['identity']['claim_ids'][0]
next(c for c in false_record['claims'] if c['id']==cid)['statement']='배경은 큰 숫자 4다.'
assert not check(false_record,catalog),'A structural validator must not pretend to be a visual recognizer'
boundary={'case':'known A relabeled 4 with self-declared supported state','structure_passed':True,'content_truth':False,'tool_content_verified':False,'meaning':'타입·해시·supported 표식만으로 대상 정답을 판정할 수 없음. 실제 ROI 내용 검수가 필요하다.'}
(HERE/'validation/semantic-boundary.json').write_text(json.dumps(boundary,ensure_ascii=False,indent=2),encoding='utf-8')
preserved=[]
for item in load(HERE/'protected-before.json'):
    value=digest(item['path']);assert value.lower()==item['sha256'].lower(),item['path']
    preserved.append({**item,'unchanged':True})
links=[]
for path in CANDIDATE.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8-sig')):
        if '://' in target or target.startswith('#'):continue
        need_path=(path.parent/target.split('#')[0]).resolve();assert need_path.is_file(),str(need_path);links.append(str(need_path))
pins=[]
for path in CANDIDATE.rglob('*'):
    if path.is_file() and '__pycache__' not in path.parts:pins.append({'relative':path.relative_to(CANDIDATE).as_posix(),'sha256':digest(path),'bytes':path.stat().st_size})
checks=load(HERE/'validation/checks.json')
result={'utc':datetime.now(timezone.utc).isoformat(),'candidate_version':'0.1.0-draft.4','status':'development_candidate_not_promoted','synthetic_checks_passed':checks['passed'],'synthetic_checks_total':checks['total'],'skill_quick_validate':'passed; PyYAML 6.0.3 installed only in local validation dependency folder','development_case':'previously exposed H02; AI manual reinspection, no blind trial','development_objects':len(record['objects']),'development_claims':len(record['claims']),'development_unknowns':len(record['unknowns']),'pattern_registration':load(HERE/'development/H02/pattern-registration.json'),'content_precision':None,'content_precision_reason':'전체 고유 주장 분모·독립 검수 미완료','accuracy_improvement_proven':False,'effort_reduction_proven':False,'production_or_company_approval':None,'old_A5b_resumed':False,'installed_or_promoted':False,'protected_files_verified_unchanged':len(preserved),'protected_files':preserved,'relative_reference_links_checked':len(links),'candidate_files':pins,'next_gate':'사용자가 실제 기록의 밀도·패턴 분류를 확인하거나 새 비교 검증 범위를 선택'}
(HERE/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('candidate_files','protected_files','pattern_registration')},ensure_ascii=False))
