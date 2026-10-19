import json,hashlib
from pathlib import Path
O=Path(__file__).parent;C=O.parent.parent;W=O.parent/'R8_시험/video-knowledge-curator-workspace'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(O/'R8_01_최종집계_대조.json');assert a['passed']==a['condition_count']==26 and not a['failed']
text='''# R8-1 큐레이터 최종 독립 레드팀 판정

**후보 작성·소량 개발 비교·사람 검토용 결과 정리의 한정 완료를 지지한다. 이 범위의 열린 차단 결함은 없다.** 후보 채택·기본 전환과 R8 전체 완료는 지지하지 않으며 사람의 실제 출력 피드백은 아직 없다.

이번 최종 감사의 파일·집계·뷰어 구조 조건은 26/26이다. 앞선 정적 41조건과 시험기반 23조건은 각자의 범위 판정으로 남기며 성능 표본 수에 더하지 않는다. 행동진단은 3과제의 22개 서로 다른 조건에 대해 old/new 각각 1회씩 채점한 44개 AI 판단이다. 두 버전 모두 과제별 8/8·8/8·6/6으로 동률이다. 실영상 품질 총점이나 스킬 독자 효과·일반화·통계적 우위를 입증하지 않는다.

실행 기록은 전체 완료 시도8·비교적격6·자료누락 무효2를 구분하고 준비만 한4폴더를 시행 수에서 뺀다. iteration1의 무효 출력·로그와 사전 코드 실패 이력을 보존했다. 이 제외는 사후 인프라 보완이며 사전 고정 정책이었다고 주장하지 않는다. 시간/token은 전부 null이다.

검토 시점 D 기존152입력과 후보3파일, 계획·현황·작성확인을 포함한163근거파일의 SHA가 이전 검토와 모두 같다. 기존06_맞춤스킬 아래14파일도 그대로다. C 수행 사본6개의 시험 전 manifest와 최종 바이트를 독립 대조했다.

- 사례1은 두 버전 모두 기존 입력을 변경하지 않았다. 실제 JSON/한국어 설명은 지식 정리·적용 조건·예와 반례를 남기며 회사 규칙·최신 CI 역할·효과를 임의 확정하지 않는다.
- 사례2는 지정 `작업초안/레이아웃지식_초안.json`만 바뀌었다. 객체 차이는 `/layouts/0/limits`, `/layouts/0/version`, `/version` 세 곳이며 요청 문구가 정확하고 나머지13항목과 다른 필드는 같다. 양측 변경 전 백업 SHA는 `0225b8ff97c7ab9441cbe6d1fd7539da8d97ce90bf2e9003d63f4f4ae6175306`이다.
- 사례3은 실행 전 주입한 현재 SHA `b83fcc5cbb62d4fea94784c596b85287564da1e5fc04d6353305b5796b2ef9a2`를 유지했다. 등록 SHA와 고정목록을 재기준화하지 않았다. “회사 최신/반드시 중앙”은 충돌 증거로 남기고 미등록 안전 초안과 운영 반영 보류를 구분했다.

6 grading.json의 text/passed/evidence와 8/8/6조건 수·재계산 요약, 정본의 grading hash 및 benchmark의 모든 기대항목을 대조했다. 공식 생성 뷰어 원본과 표시 사본의 디코딩 데이터가 같고 표시된6회 결과 파일·채점·benchmark는 실제 파일과 일치한다. 표시 사본의 외부 리소스 태그는0이며 내장 JSON의 닫는 script 경계는 이스케이프됐다. 공식 원본과 라이선스를 보존했다. 이는 HTML/데이터 구조 감사로서 브라우저 렌더·픽셀·클릭 동작의 시각 검증은 아니다.

열린 한계는 남아 있다. 신 스킬 사례1에서 지정 참조의 R8 평가설계 문단이 노출됐고, 공통DB가 과제의 답을 구체적으로 제공하며 기대항목은 최초 실행 시작 뒤 작성했다. 채점자는 구성명을 알았다. 무노출·사전고정·맹검 시험이 아니다. 요약·정본·benchmark가 이를 공개하며, R8-4의 참조/평가설계 분리·사전 기준 고정·답 없는 개념/오인용·부분충돌·쓰기/백업 실패의 미사용 사례 확인은 미완료로 남겼다. 이는 제한된 관찰을 보존할 수 있게 하는 한계 고지이며 해당 후속 작업을 대신하지 않는다.

명령·실행 시점은 실행자 transcript·코드·보존 로그와 최종 파일의 일관성 근거다. 독립 이벤트 로그로 원 실행을 인증하지 않았고 최종 SHA만으로 중간 일시 변경 후 원복을 배제할 수 없다. 초기 준비 builder의 바이트 사본 부재, 채점자의 최초 PowerShell 읽기 절차 편차도 삭제하지 않았다. 검토자는 수행자의 변경 스크립트를 재실행하지 않았다.

사람의 내용 검수·CI/회사 승인·실영상 분석·전체 R6 원문/자산 검사·자동 트리거 시험·후보 채택/기본 전환·R8-2/3/4·01-A는 완료하지 않았다. AI 채점이나 이 판정을 사람 승인으로 쓰지 않는다. D 출판 예정 스크립트의 두 루트 안내와 R8 상태 갱신은 이 검토 시점 이후 별도 작업이며, 본 검토의 불변 주장에는 포함되지 않는다. 출판 전 아래 JSON의 D/C SHA를 대조하고 출판 후 의도한 안내 변경과 나머지 입력 보존을 따로 기록해야 한다.

실제 조건·전체 체크·파일별 SHA는 [최종 집계 대조](R8_01_최종집계_대조.json), [행동 대조](R8_01_최종행동_대조.json), [기계 판정](R8_01_최종판정.json)에 있다. 검토자는 C 검토폴더만 작성했고 운영D·후보·시험출력·채점파일을 수정하지 않았다. CU·외부앱·웹과 새 수행agent 호출은 하지 않았다.
'''
(O/'R8_01_최종판정.md').write_text(text,encoding='utf-8')
extra=[O/'R8_01_최종집계_대조.json',O/'R8_01_최종판정.md',O/'R8_01_최종판정저장.py',O.parent/'R8_01_결과정리.py',O.parent/'R8_01_뷰어작성.py',O.parent/'R8_01_집계.py']
ch=dict(a['C_result_hashes']);ch.update({p.relative_to(C).as_posix():sha(p) for p in extra})
verdict={
 'stage':'R8-1 큐레이터 최종 행동·집계·뷰어 독립 레드팀',
 'candidate_version':'0.2.0-draft.1',
 'limited_completion_supported':True,
 'supported_completion':'후보 작성·소량 개발 비교·사람 출력검토 자료 준비의 한정 완료',
 'unresolved_blocking_findings':[],
 'open_nonblocking_findings':[
  {'id':'evaluation_independence','severity':'limitation','status':'open_for_R8_4','detail':'new case1에 지정 참조의 평가설계 문단 노출, 풍부한DB가 답 제공, 최초dispatch후 expectation 작성, 구성명 비맹검. 무노출/사전고정/스킬 독자효과 시험 아님.'},
  {'id':'coverage_and_tie','severity':'limitation','status':'open_for_R8_4','detail':'세 개발과제·각구성1회이며 모든22조건 양측통과로 스킬 효과를 구별하지 못함. 답없는개념/오인용부분충돌/쓰기·backup실패 미사용사례는 아직 없음.'},
  {'id':'execution_authentication','severity':'limitation','status':'not_authenticated','detail':'원 실행과 읽기 과정은 자기보고 transcript/로그·코드의 일관성 근거. 독립 이벤트 기록 없음. 최종 hash는 일시변경후원복을 배제하지 않음.'},
  {'id':'visual_browser_review','severity':'scope_limit','status':'not_performed','detail':'뷰어 데이터·script 경계/리소스태그 구조검사 수행; 브라우저 렌더/클릭 시각검사는 CU금지 범위로 미수행.'},
  {'id':'human_output_feedback','severity':'next_required_stage','status':'pending','detail':'실제 사용자 출력 피드백·후보 채택/운영 기본전환은 미완료. AI검토를 사람승인으로 전용 금지.'}
 ],
 'verification':{'final_audit_conditions':a['condition_count'],'final_audit_passed':a['passed'],'checks':a['checks'],'prior_static_conditions':41,'prior_infrastructure_conditions':23,'behavior_distinct_conditions':22,'behavior_AI_judgments':44,'development_cases':3,'eligible_executor_runs':6,'executor_attempts_total':8,'infrastructure_invalid_runs':2,'prepared_only_runs':4,'runs_per_case_per_configuration':1,'new_passed_by_case':[8,8,6],'old_passed_by_case':[8,8,6],'D_preserved_input_count_at_review':152,'D_reviewed_source_count':len(a['D_source_hashes']),'old_skill_file_count':14,'candidate_file_count':3,'C_hashed_result_count':len(ch)},
 'scope':{'actual_video_trials':0,'automatic_trigger_tested':False,'unseen_holdout':False,'statistical_superiority_claimed':False,'time_tokens_collected':False,'total_tokens':None,'duration_ms':None,'R6_full_original_artifact_check':False,'human_content_review':False,'candidate_adopted':False,'default_changed':False,'R8_1_complete':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'R8_2':'not_started','R8_3':'not_started','R8_4':'not_started'},
 'reviewer_actions':{'C_review_directory_writes_only':True,'D_modified':False,'outputs_modified':False,'grading_modified':False,'candidate_modified':False,'executor_write_scripts_reexecuted':False,'CU_web_external_app_calls':False,'new_agents_spawned':False},
 'publication_review':{'planned_script':'phase00-build/R8_01_결과정리.py','script_executed_by_reviewer':False,'planned_root_navigation_changes':['00_시작안내.md','01_진행현황.md'],'requires_prewrite_all_review_hash_match':True,'requires_postwrite_intended_navigation_changes_and_other150_preserved_receipt':True,'publication_not_included_in_current_unchanged_claim':True},
 'D_source_hashes':a['D_source_hashes'],'C_result_hashes':ch
}
(O/'R8_01_최종판정.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'limited_completion_supported':True,'conditions':a['condition_count'],'passed':a['passed'],'D_sources':len(a['D_source_hashes']),'C_results':len(ch),'verdict_sha256':sha(O/'R8_01_최종판정.json'),'md_sha256':sha(O/'R8_01_최종판정.md')},ensure_ascii=True))
