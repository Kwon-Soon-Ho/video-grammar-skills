from pathlib import Path
from hashlib import sha256
import json,re
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
gaps=[
 ('H03','c019','수신기 3의 강조가 약해졌다 강해지는 반복을 단순 등장으로 축약','반복 표본의 대비와 문구·외곽·표 강조를 나눠 재확인'),
 ('H03','c039','아래 표제와 비행 조건 상자의 선후·중첩을 충분히 구분하지 않음','표제 등장과 조건 상자 등장을 별도 속성·시간으로 기록'),
 ('H04','c017','인셋 내부 드론의 위치 변화만 적고 왼쪽 세로 경로를 따라 위로 가는 방향과 상단 체류를 누락','패널 기준의 방향과 정착 구간 재확인'),
 ('H04','c004','표제 교체만 적고 가느다란 청록 띠에서 폭이 커지는 중간 형태를 누락','전환 중간 표본의 형태·크기와 내용 변화를 분리'),
 ('H04','c004 / c021','착륙 문구와 새 상단 표제 완성의 선후 관계를 연결하지 않음','같은 프레임 시각으로 두 대상의 등장·완료 순서를 연결'),
 ('H04',None,'인셋 드론 주변 반투명 원형 빛의 변화 누락','주변 효과를 대상으로 추가하고 면적·밝기 변화를 구분'),
 ('H04',None,'실사 드론 상단의 작은 붉은 빛 누락','원본 크기 표본에서 빛의 존재·시간 범위를 재확인')]
review={'scope':'실제 영상 첫 기록과 이미 노출된 기준 기록의 개발용 대조. 독립 평가·새 홀드아웃·전수 의미 채점 아님','findings':[{'case':a,'first_claim':b,'gap':c,'next_work':d,'state':'open','reviewer':'same AI context'} for a,b,c,d in gaps],'first_records_preserved':True,'overall_accuracy':None,'content_complete':False,'note':'구조 통과 이후에도 내용 보완이 필요함을 보여주는 발견 목록. 7개를 전체 오류 수나 정밀도·재현율 분모로 사용하지 않는다.'}
save(HERE/'content-review-gaps.json',review)
tests=[load(HERE/'validation-changes.json'),load(HERE/'validation-core/checks.json'),load(HERE/'validation-composition/checks.json')]
skill=HERE/'candidate/company-video-grammar-analyzer';links=[]
for path in skill.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  resolved=(path.parent/target.split('#')[0]).resolve();assert resolved.is_file(),(path,target);links.append({'from':str(path),'target':str(resolved)})
protected=load(HERE/'protected-before.json')
for item in protected:assert sha256(Path(item['path']).read_bytes()).hexdigest().lower()==item['sha256'].lower()
result={'scope':'조사 전체의 구현 현황 정정 및 분석 신뢰성 일부의 개발 후보 보완','candidate_version':'0.1.0-draft.6','whole_research_implemented':False,'default_installed_or_replaced':False,'fresh_holdout':False,'actual_cases':2,'first_pass_claims':62,'record_and_provenance_checks_passed':True,'content_review_complete':False,'content_gaps_recorded':len(gaps),'tests':[{'scope':x['scope'],'passed':x['passed'],'total':x['total']} for x in tests],'basic_skill_format_check':'passed','relative_markdown_links_checked':len(links),'protected_files_unchanged':len(protected),'remaining_large_categories':['分析 신뢰성의 내용 누락 보완과 새 자료 확인'.replace('分析','분석'),'조건 기반 패턴 검색·실제 반복 장면 매칭 검증','목적·제약에 따른 대안·선택·비평·재평가','편집 가능한 재제작·렌더 대조·내용 변경 재사용 시험'],'interpretation':'서로 다른 표 셀의 구분과 키워드 검색을 추가했으며, 의미 정확도·재사용 적합성·제작 품질을 입증한 것은 아니다.'}
save(HERE/'result.json',result);save(HERE/'reference-links-check.json',links)
progress={'baseline_audit':'implementation-audit.json / draft.5의 41개 조사 포인트 상태 보존','latest_candidate':result,'scope_correction':'조사는 채택 완료가 아니다. 코드 일부·지침·미구현·적용 제외를 구분해 보고한다. 원본 스킬 통째 설치 수를 목표나 완성률로 삼지 않는다.','four_categories':[{'name':'분석 신뢰성·근거·기록','state':'일부 구현·실제 내용 보완 중','exit_result':'실제 기록의 잘못된 식별·속성 누락·시간 범위를 확인하고, 이미 본 자료와 새 자료를 구분한 검증 결과'},{'name':'사례 검색·패턴 재사용','state':'등록·번호·스냅샷·관계 연결, 단순 키워드 검색까지 일부','exit_result':'조건에 맞는 후보를 찾고 현재 장면의 근거·차이·미확정을 기록한 반복 사례'},{'name':'전문가 판단·기획','state':'지침·인계 형식 중심','exit_result':'목적·제약에서 복수 대안을 만들고 선택 근거·비평·수정 후 재평가를 남긴 기획 사례'},{'name':'역설계·제작 검증','state':'이번 후보에서 미구현','exit_result':'관측 명세에 연결한 편집 가능한 결과물·렌더 대조·내용 변경 재사용 결과'}],'next_category':'사용자가 이미 선택한 분석 정확도·근거 기록 우선 유지. 전체 반영이나 기본 승격으로 보고하지 않음.'}
save(WORK/'implementation-audit-20261019/current-progress.json',progress)
print(json.dumps(result,ensure_ascii=False))
