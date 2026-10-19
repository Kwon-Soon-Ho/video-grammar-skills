from pathlib import Path
from hashlib import sha256
import json,re
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
skill=HERE/'candidate/company-video-grammar-analyzer';links=[]
for p in skill.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  resolved=(p.parent/target.split('#')[0]).resolve();assert resolved.is_file(),(p,target);links.append({'from':str(p),'target':str(resolved)})
for p in (skill/'scripts').glob('*.py'):compile(p.read_text(encoding='utf-8'),str(p),'exec')
protected=load(HERE/'protected-before.json')
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
fresh=[load(HERE/'fresh/results'/c/'first-seal.json') for c in ('NEW-N','NEW-P')]
for c,seal in zip(('NEW-N','NEW-P'),fresh):assert digest(HERE/'fresh/results'/c/'first-observations.json')==seal['observation_sha256']
corrections=[load(HERE/'cases-r3'/c/'validation.json') for c in ('H03','H04')]
tests=[load(HERE/'validation-review/checks.json'),load(HERE/'validation-core/checks.json'),load(HERE/'validation-composition/checks.json')]
backup=load(HERE/'backup/backup-manifest.json');publication=load(HERE/'backup-publication.json')
for f in publication['files']:assert digest(f['source'])==digest(f['backup'])==f['sha256']
result={'user_authorization':'기존 스킬은 백업하고 수정 작업 계속 진행하자','scope':'첫 범주인 분석 신뢰성·근거 기록의 보완과 새 사내 영상 두 구간 개발 실행','version':'0.1.0-draft.7','backup_files':backup['file_count'],'backup_verified':True,'correction_records':{'cases':['H03','H04'],'tracked_findings':sum(x['finding_counts']['addressed'] for x in corrections),'previous_findings':7,'additional_review_findings':2,'claims_after':75,'addressed_means':'해당 지적에 답하는 보완 관측과 근거 연결. 자동 진실성·독립 평가 합격 아님.'},'new_material':{'cases':['NEW-N 166–174s','NEW-P 40–48s'],'videos':2,'first_claims':sum(x['claims'] for x in fresh),'first_objects':sum(x['objects'] for x in fresh),'outputs_preserved':True,'structure_and_provenance_passed':True,'independent_evaluation':False,'accuracy_score':None},'checks':[{'scope':x['scope'],'passed':x['passed'],'total':x['total']} for x in tests],'basic_skill_format_check':'passed','relative_links_checked':len(links),'protected_files_unchanged_before_working_update':len(protected),'working_update_plan':'백업된 프로젝트 기존 작업본을 draft.7 개발 작업본으로 갱신. 동결 A5b·기존 후보·이전 실패는 보존하며 전역 설치나 회사 승인 승격은 하지 않음.','whole_research_completed':False,'remaining':['새 자료의 독립 내용 검수와 미발견 요소 분모','목적에 필요한 정확 좌표·수치·타이밍·가감속','조건 기반 패턴 후보 검색·현재 장면 대조·차이 검수','실제 전문가 대안·선택·비평·재평가','편집 가능한 재제작과 렌더 비교·내용 변경 재사용']}
save(HERE/'result.json',result);save(HERE/'reference-links-check.json',links)
print(json.dumps(result,ensure_ascii=False))
