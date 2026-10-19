"""Update source-to-current-code traceability without promoting partial adoption."""
from pathlib import Path
import json,hashlib,collections
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
def load(p):return json.loads(Path(p).read_text('utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
audit=load(WORK/'implementation-audit-20261019/implementation-audit.json')
sources=load(WORK/'research/ponytail-rea-20261019/source-audit.json');by_id={x['id']:x for x in sources['records']}
skill=WORK/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer'
updates={
 'P2':'이후 번호/스냅샷/조합에 단순 키워드 AND 검색 추가. 의미·조건 적합성 검색과 재사용 성공 판단은 아직 없음.',
 'P7':'자체 구조·참조·집계 오류 주입 및 회귀 검사. 독립 AI·새 조건 A/B·품질/공수 효과 검증은 여전히 없음.',
 'R2':'지적→변경 주장→근거 연결 review_ledger 추가. revision 필드는 있으나 동시 갱신 충돌 제어·상충 최신 판정 선택기는 없음.',
 'R3':'수정 검수 장부가 요구 대상/속성/차원/근거 유형을 확인. 원본 REA의 expected_revision 충돌 제어는 이식하지 않음.',
 'R7':'선언한 범위 검사를 보완하고 원본 전체/기록 창 집계 추가. 미발견 요소를 자동으로 찾거나 정밀 검수 완전성을 입증하지 않음.',
 'R9':'상충 판정 보존·최신 유효 판정 선택 실행기는 여전히 없음. 기존 기록 보존/기각 표시는 그 전체 기능의 대체가 아님.',
 'R10':'편집 가능한 재제작→렌더→원본 비교→내용 변경 검증은 여전히 미구현.',
 'R14':'프로젝트 D: 개발 작업본은 draft.8로 반영·백업·해시 확인. 전역 자동 설치·검증 완료 판본 승격은 없음.',
 'T2':'이번 자료에 한정한 제한 추출 보조 어댑터는 존재. 원본 전문 분석 배치/예산/실패 필터링 실행 흐름을 이식한 것은 아님.',
 'S1':'실제 사내 영상에서 대상·속성·중간 상태를 보완 중. 같은 AI가 반복 확인하는 개발 사례이며 독립 개선 효과 입증은 없음.',
 'S2':'draft.8 구조 검사와 시각 내용 판단을 계속 구분. 검사 95개는 영상 품질 95건 평가가 아님.',
 'I1':'목적/조건 인계 형식 수준. 목적별 설계 대안 생성→선택→결과 검증은 여전히 미구현.',
 'I2':'내용 검수 상태 필드와 AI 관찰은 있음. 독립 시각 비평·기계 검출을 격리한 실행기는 없음.',
 'G1':'대안/반례/선택 이유 형식 수준. 시니어 디자인 비평의 실제 결과물 비교 과정은 미구현.',
 'M1':'사용자 선택과 분류 ID는 기록. 전체 파이프라인의 공통 용어집·별칭·규칙 개정 연결은 아직 부분적.',
 'E1':'draft 상태와 사례 축적. 수정 피드백에서 작은 규칙을 자동 추출·반례 검증하는 학습 루프는 없음.'}
reason={
 'P':'관측을 충분히 축적한 뒤 기존 지식 재사용을 우선하는 판단을 참고. 적게 기록하기를 목표로 삼지 않음.',
 'R':'렌더 영상의 관측·근거·미해결·판정 범위를 분리하는 데 적용. 소프트웨어 역설계 전체 도메인 모델을 통째로 복제하지 않음.',
 'T':'증거를 이해하는 과정과 평가 결론을 혼동하지 않기 위해 참고. 보안 도메인의 위험 분류를 영상 정답으로 쓰지 않음.',
 'S':'실제 실패를 바탕으로 수정·재검증하는 원칙을 적용. 지침 추가만으로 행동 개선이 입증됐다고 하지 않음.',
 'I':'장면 목적과 표현의 적합성을 판단할 구조로 참고. UI 기본 시간 수치나 웹 상태를 영상 기본값으로 이식하지 않음.',
 'G':'시각적 결함→대안→재평가를 향후 판단 기능에 적용할 후보. 장문의 원문 전체를 매번 강제 호출하지 않음.',
 'A':'평가 분모·미실행 상태·평가기 검토를 참고. 구조 검사 수를 품질 점수로 바꾸지 않음.',
 'M':'용어·구분·중요한 결정 이유의 일관성에 활용. 모든 사소한 선택마다 사용자 승인을 요구하지 않음.',
 'E':'검증한 피드백에서 규칙 후보를 축적하는 방향만 채택. 빈도/점수만으로 회사 규칙 승격 금지.',
 'V':'조건·영향·예/반례를 함께 적는 형식을 참고. React용 규칙과 원본 검증기를 영상에 그대로 실행하지 않음.'}
rows=[]
for r in audit['records']:
    s=by_id[r['id']];assert sha(s['local_path'])==s['sha256'],s['local_path']
    current=[]
    if r['current_evidence']:
        old=Path(r['current_evidence']['path']);assert sha(old)==r['current_evidence']['sha256']
        parts=old.parts;relative=Path(*parts[parts.index('company-video-grammar-analyzer')+1:]);p=skill/relative
        assert p.is_file();current.append({'path':str(p),'sha256':sha(p)})
    if r['id'] in ('R2','R3','R5','R8'):current.append({'path':str(skill/'scripts/review_ledger.py'),'sha256':sha(skill/'scripts/review_ledger.py')})
    if r['id']=='R7':current.append({'path':str(skill/'scripts/source_coverage.py'),'sha256':sha(skill/'scripts/source_coverage.py')})
    rows.append({'id':r['id'],'repository':r['repository'],'upstream':{'commit':s['commit'],'path':s['path'],'local_path':s['local_path'],'sha256':s['sha256'],'review_scope':s['review_scope'],'url':s['url']},'finding':r['finding'],'historical_draft5_status':r['implementation_status'],'current_classification':r['implementation_status'],'adoption_rationale':reason[r['id'][0]],'current_evidence':current,'remaining_or_exclusion':updates.get(r['id'],r['remaining_or_exclusion']),'decision_state':'first_selection_with_partial_implementation_not_final_quality_acceptance','full_upstream_function_implemented':False,'independent_video_effect_proven':False})
result={'schema_version':'source-adoption-trace-0.1','current_skill_version':'0.1.0-draft.8','initial_survey_method':sources['method'],'review_scope_counts':dict(collections.Counter(r['review_scope'] for r in sources['records'])),'record_count':len(rows),'classification_counts':dict(collections.Counter(r['current_classification'] for r in rows)),'counts_are_not_completion_percentages':True,'third_party_test_execution':False,'whole_original_candidate_list_exhaustively_reviewed':False,'candidate_coverage_note':'41개는 선별한 10개 저장소의 소스 검토 항목. 이전 11개 조사와 합산한 19개 이력은 최초 대화의 모든 후보·내부 스킬을 전수 분해했다는 뜻이 아님. Agency Agents/wshobson/Awesome Copilot/Claude Skills 등 소개 후보 전체의 직접 소스 재감사는 이 41개 목록에 포함되지 않음.','records':rows}
(HERE/'adoption-trace-draft8.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 조사·선별·구현·검증의 현재 범위','', '현재는 스킬 제작·실제 사례 보완 중이다. 외부 스킬 전체 적용 완료 후 최종 테스트 단계가 아니다.','', '이번 추가 조사 41개 항목: 17개 full, 24개 selected. full도 해당 파일의 정적 검토 범위이며 전체 저장소 감사나 원본 테스트 실행을 뜻하지 않는다. 과거 원본과 최신 작업본을 SHA로 연결했다.','', '1차 선별 이유는 있으나 모든 채택 판단의 옳음을 영상 결과로 검증한 것은 아니다. 이 표는 기능별 완료율이 아니다.','', '| ID | 구조 | 현재 반영 | 이유와 변형 | 남은 범위·제외 |','|---|---|---|---|---|']
for r in rows:md.append('| '+' | '.join([r['id'],r['finding'],r['current_classification'],r['adoption_rationale'],r['remaining_or_exclusion']])+' |')
md+=['','검증 결과는 세 종류로 구분한다: ① 구조·참조·시간·출처 검사 ② 실제 영상에서 AI가 발견/정정한 사실 ③ 독립적인 설계 품질·정보 전달·공수 개선 비교. 현재는 주로 ①과 일부 ②이며, ③은 미실행이다.','', '이번 두 장면 보완은 분석 신뢰성에 관한 실제 사례 검증이다. 전문가 대안·선택·비평이나 재제작 실행기의 완성을 뜻하지 않는다.']
(HERE/'01_외부스킬_반영과_보류_추적.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['record_count','review_scope_counts','classification_counts','whole_original_candidate_list_exhaustively_reviewed']},ensure_ascii=False))
