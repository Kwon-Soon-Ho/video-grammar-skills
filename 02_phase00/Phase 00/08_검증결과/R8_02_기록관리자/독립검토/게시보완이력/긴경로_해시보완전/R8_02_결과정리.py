from 공통지원 import BASE,save,safe,sha,check_links
from pathlib import Path
import json,shutil,importlib.util,sys
LOCAL=Path(__file__).parent.resolve();CROOT=LOCAL.parent;W=LOCAL/'R8_시험/video-record-steward-workspace';REVIEW=LOCAL/'R8_02_독립검토'
S='2026-10-15_R8_02_시험정리';D='08_검증결과/R8_02_기록관리자/';CAND='06_맞춤스킬/재구성후보/video-record-steward/'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
review=read(REVIEW/'R8_02_최종판정.json');assert review['limited_completion_supported'] and not review['unresolved_blocking_findings']
assert all(sha(safe(BASE/p))==h for p,h in review['D_source_hashes'].items())
assert all(sha(CROOT/p)==h for p,h in review['C_result_hashes'].items())
comparison=read(W/'비교결과_정본.json');assert comparison['candidate_instruction_version']=='0.2.0-draft.3'
assert len(comparison['comparisons'])==3 and all(c['configurations']['new_skill']['failed']==0 for c in comparison['comparisons'])
initial=read(BASE/'08_검증결과/R8_02_입력보존.json')['source_hashes'];assert len(initial)==164
allowed_prior={'00_시작안내.md','01_진행현황.md','14_스킬재구성/진행상태.json','08_검증결과/R8_01_큐레이터/00_결과안내.md'}
assert {p for p,h in initial.items() if sha(BASE/p)!=h}==allowed_prior
archived={}
def exact(src,dst):
    dst=safe(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert sha(dst)==sha(src),str(dst)
    else:shutil.copy2(src,'\\\\?\\'+str(dst))
    archived[dst.relative_to(BASE).as_posix()]=sha(dst)
# Retain all real trials, failures, preparation histories, version snapshots and evaluation source package.
for source,label in [(W,'video-record-steward-workspace'),(LOCAL/'R8_시험/video-record-steward','video-record-steward')]:
    for p in sorted(source.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:exact(p,BASE/'backup'/S/'실행원문'/label/p.relative_to(source))
for p in LOCAL.glob('R8_02_*.py'):exact(p,BASE/'backup'/S/'작성도구'/p.name)
for name in ['R8_01_뷰어작성.py','공통지원.py']:exact(LOCAL/name,BASE/'backup'/S/'작성도구'/name)
for p in REVIEW.rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:exact(p,BASE/D/'독립검토'/p.relative_to(REVIEW))
for name in ['비교결과_정본.json','비교결과_요약.md','실행결과_사실검사.json','실행완료_기록.json','평가항목.json','평가기준_고정기록.json','수행자료_포함과분리.json','동등조건_확인.json','판본대조_단위검사.json','검사도구_실패와보완.json','기록관리자_출력검토.html','뷰어_표시검증.json','공식뷰어_실행기록.json']:
    exact(W/name,BASE/D/name)
for folder in ['원문보존','초기후보검토']:
    for p in (W/folder).rglob('*'):
        if p.is_file():exact(p,BASE/D/folder/p.relative_to(W/folder))
for iteration in ['iteration-1','iteration-2']:
    for ed in sorted((W/iteration).glob('eval-*')):
        for arm in ['new_skill','old_skill']:
            run=ed/arm/'run-1'
            for p in [run/'grading.json',run/'transcript.md']+list((run/'outputs').rglob('*')):
                if p.is_file():exact(p,BASE/D/'사례별출력'/iteration/ed.name/arm/p.relative_to(run))
table=['| 과제 | 보완 후보 | 기존 |','|---|---|---|']
for c in comparison['comparisons']:
    n,o=c['configurations']['new_skill'],c['configurations']['old_skill'];table.append(f'| {c["eval_name"]} | {n["passed"]}/{n["total"]}조건 | {o["passed"]}/{o["total"]}조건 |')
report='''# R8-2 기록·한맥 연결 관리자 — 결과와 사람 검토

2026-10-15 · **초안·실제 수정/백업 실패/복구 개발시험·보완·재시험과 레드팀까지 정리했다. 이번 출력의 사람 피드백은 대기 중이다.** 후보 채택·기본 전환·R8/Phase00 완료는 아니다. R8-3/R8-4·01-A 구현은 시작하지 않았다. 큐레이터 유지/R8-2 진행 회신은 별도 범위로 보존했다.

## 무엇을 맡기는 스킬인가

기록의 ID·판본·시간·근거·좌표·회사/CI 참조를 확인하고 요청한 초안만 고친다. 변경 전 사본과 차이·검사 결과를 남기고 실패하거나 복구할 때의 실제 상태를 보고한다. 새로 영상·프레임·좌표를 알아내거나 디자인을 만들지는 않는다.

[후보 v0.2.0-draft.3](../../06_맞춤스킬/재구성후보/video-record-steward/SKILL.md)은 본문, 기록 연결/수정·복구/보고 지침 3개, 읽기 전용 판본 대조 도구로 구성했다. 기존 세 스킬과 고정 정본/목록은 유지했다. R4는 관측 기록, R5는 별도 디자인 선택 초안, R6는 실제 질문/답변 문맥, R7은 별도 품질 검수 연결로 구분한다.

## 발견해서 고친 것

1. 정적 레드팀은 일부 파일을 저장한 뒤 검사에 실패했을 때 복구 의무가 모호하다고 지적했다. 내 쓰기와 현재 bytes가 같으면 작업 전 backup으로 복구하고, 외부 변경/복구 실패는 덮어쓰지 않고 미복구·사용 중단으로 남기도록 보완했다.
2. 수행 자료의 출처 연결 목록에도 R8 평가 설계 문단 사본이 있었다. 실제 실행 전에 발견해 이전 준비본을 보존하고 CI 질문·답변에 필요한 자료만 좁혀 다시 만들었다. 준비만 한 폴더를 모델 시행으로 세지 않았다.
3. 초기 draft.2와 기존 스킬 모두 정상 수정 과제에서 R5 연결을 바꾸고도 R5 자체 판본은 유지했다. 두 버전 모두 해당 과제7/8, backup 실패 과제8/8이었다. 기본 R4/R5 검사는 통과했지만 ‘메타데이터 변경도 새 소유 판본’이라는 기존 R1 계약을 놓친 것이다. 초기 결과·실패·독립 채점·공식 뷰어를 보존했다.
4. 새 판단 정책을 만든 것이 아니라 R1의 기존 규칙을 지침에 명확히 연결하고 [판본 대조 도구](../../06_맞춤스킬/재구성후보/video-record-steward/scripts/판본대조.py)를 추가했다. 표준 라이브러리만 쓰고 파일을 수정하지 않는다. 내용 수정과 정확 checkpoint 복원을 구분하며, 좁은 단위검사12조건을 통과했다. 이는 스킬 시행 수나 실영상 성능이 아니다.

## 같은 요청·조건으로 재시험한 결과

'''+'\n'.join(table)+'''

정상 수정에서는 R4 참조와 해당 기록의 새 판본, R5의 연결 ID/판본/저장 SHA 및 자체 판본을 확인했다. 시간·좌표·수치·회사/색/검수 상태와 다른 필드는 보존해야 한다. backup 충돌에서는 활성 원문과 기존 파일을 보존하고 미반영 제안을 남겨야 한다. 복구에서는 실패본을 보존하고 지정 checkpoint의 bytes와 정확히 같아야 하며, 구형 자료는 needs_migration으로 검사만 하고 이관하지 않아야 한다.

[비교 상세](비교결과_요약.md) · [최종 출력 뷰어](기록관리자_출력검토.html) · [초기 실패 출력 뷰어](초기후보검토/기록관리자_출력검토.html). 최종 뷰어에는 이전4회 출력도 함께 연결했다. 원문과 전체 입력/로그는 backup에, 읽기용 결과는 사례별출력 폴더에 보존했다.

## 숫자와 검토 범위

실제 모델 시행은 초기4회+최종6회=10회다. 초기 과제3 미실행2폴더와 간접 평가문단 수정 전 준비6폴더는 시행 수가 아니다. 초기 실패를 삭제하거나 인프라 무효로 바꾸지 않았다. 최초의 기대항목22개는 실행 전에 고정했고 재시험에서도 문구를 바꾸지 않았다. 초기 채점에 main이 실제 R1 조항을 추가 전달한 사실, 요청의 ‘연결만’ 문구 해석 한계와 비맹검 이력도 채점 원문에 남겼다.

등록 자산135개를 수행 사본에 포함해 R4/R5 실제 기록 검사를 할 수 있게 했다. R6 full 원문/현재 문맥·R7 전체 고정목록은 이 사본의 범위 밖이다. D 운영의 별도 정상 확인을 수행 사본 통과로 전용하지 않았다. 구조 valid·backup SHA는 내용·실제 선택자/사람·회사/사용권한·운영 승인과 다르다.

Anthropic Skill Creator의 비교·채점·공식 정적 뷰어 절차를 Codex 실행 환경에서 사용했다. Claude 모델 성능을 시험하지 않았다. 공식 뷰어 원본과 Apache-2.0 LICENSE를 보존했고 표시 사본만 외부 리소스4개 제거/script 경계 이스케이프 후 실제 결과와 대조했다. 이는 HTML·데이터 구조 검사이며 브라우저 렌더/클릭의 시각 검수는 아니다.

[독립 최종 레드팀](독립검토/R8_02_최종판정.md)을 함께 본다. AI 채점·레드팀은 사람 내용 검수를 대신하지 않는다. 전체 시간/token은 미수집이며 출력 글자 수나 가짜 반복/분산으로 채우지 않았다. 소량 개발 과제로 일반적인 품질/속도·비용 우위를 주장하지 않는다.

자체 사실검사 코드에서 줄바꿈 방식 때문에 원문 재직렬화 SHA가 달라진 오류도 [보완 이력](검사도구_실패와보완.json)에 남겼다. 실제 byte-pinned backup으로 대조하도록 고쳤으며 모델 시행 실패·제외로 세거나 실행 결과를 수정하지 않았다.

최종 기존 스킬의 backup 실패 과제에서는 수행 코드의 키 해석 오류(KeyError)를 같은 시행 안에서 고쳐 다시 실행한 이력도 transcript에 보존했다. 이는 별도 모델 시행이나 무효 시행이 아니며, 위 사실검사 도구의 줄바꿈 오류와도 구분한다.

결과를 D 폴더에 정리할 때 긴 Windows 경로로 원문 backup 복사가 중단된 이력도 독립검토/게시보완이력에 보존했다. 이미 복사된 3,644파일은 원문 SHA와 같았고 보고서/진행 현황은 변경 전이었다. 이름을 줄이거나 결과를 바꾸지 않고 긴 경로 지정으로 복사 도구만 보완했다. 모델 시행 수에는 포함하지 않는다.

## 지금 검토할 부분과 남은 일

기록을 정리·검사·복구하는 방식과 설명 분량이 실무에 맞는지 실제 출력 피드백이 필요하다. 기존 목적·draft 권한을 다시 묻는 것이 아니다. R8-3 적용성 검토자는 아직 시작하지 않았다.

R8-4에서 새 미사용 사례와 실제 저장 후 실패 자동복구·복수 파일 부분 실패·외부 변경 분기를 더 확인해야 한다. 이번 정상 수정/backup 실패/명시 checkpoint 복구로 그 분기를 완료 처리하지 않는다. 전체 R6/R7 현재 문맥·스킬 간 전달/기본 전환 검토도 남아 있다. 실제 영상 분석·회사 공통 문법·납품 품질과 01-A는 별도다.

[단계별 진행 안내](../../14_스킬재구성/00_R8_진행안내.md) · [R8-2 구성](../../14_스킬재구성/R8-2_기록관리자_구성안내.md) · [필수 독립 확인 계획](../../14_스킬재구성/R8-4_독립확인_보완계획.md).
'''
save(D+'00_결과안내.md',report,S)
edited=['14_스킬재구성/진행상태.json','14_스킬재구성/R8-2_기록관리자_구성안내.md','00_시작안내.md','01_진행현황.md','14_스킬재구성/R8-4_독립확인_보완계획.md'];navigation_before={p:sha(BASE/p) for p in edited}
p=edited[0];state=read(BASE/p);state['version']='0.1.4';state['stages']['R8-2']='record_steward_draft3_comparison_and_redteam_complete_human_feedback_pending';state['steward_candidate_version']='0.2.0-draft.3';state['steward_trials']={'actual_executor_attempts':10,'initial_draft2':4,'final_draft3_comparison':6,'infrastructure_invalid_model_trials':0,'helper_unit_conditions_not_model_trials':12};save(p,state,S)
p=edited[1];save(p,(BASE/p).read_text(encoding='utf-8')+'\n\n## 현재 결과\n\n후보는 실제 판본 누락을 보완한 v0.2.0-draft.3이며 읽기 전용 판본 대조 도구를 추가했다. [결과/초기 실패·재시험·사람 검토](../08_검증결과/R8_02_기록관리자/00_결과안내.md)를 확인한다. 이번 사람 피드백 대기이고 R8-3/4·기본 전환·01-A는 아직이다.\n',S)
for p in edited[2:4]:
    t=(BASE/p).read_text(encoding='utf-8');start=t.find('\n\n현재 R8-1 큐레이터의 구성·분량 유지/R8-2 진행 A 피드백을 받았다.')
    if start>=0:t=t[:start]
    t+='\n\n현재 R8-1 구성·분량 유지 회신을 보존했고 R8-2 기록관리자의 후보 보완·재시험·레드팀 결과를 정리했다. [R8-2 결과와 사람 검토](08_검증결과/R8_02_기록관리자/00_결과안내.md). 이번 출력 피드백 대기이며 R8-3·R8-4/운영 기본 전환·전체 Phase00 완료·01-A 구현은 아직이다.\n'
    if p=='01_진행현황.md':t=t.replace('진행 중 / 두 번째 스킬 검토','진행 중 / 두 번째 스킬 출력 피드백 대기').replace('R8-1 구성·분량 유지 회신 접수. R8-2 기록관리자 후보 검토 중. R8-3/4·운영 전환과 최종 인계 미진행.','R8-1 구성·분량 유지 회신 접수. R8-2 후보 보완/재시험·레드팀 완료, 출력 피드백 대기. R8-3/4·운영 전환과 최종 인계 미진행.').replace('기록관리자 후보 검토 중이며 적용성 검토자·통합 검증/전환은 남아 있다.','기록관리자 보완 후보의 출력 피드백을 기다리며 적용성 검토자·통합 검증/전환은 남아 있다.')
    save(p,t,S)
p=edited[4];save(p,(BASE/p).read_text(encoding='utf-8')+'\n\n## R8-2에서 추가로 확인할 잔여\n\n기록·한맥 연결 관리자의 개발시험에서는 정상 수정, 지정 backup 경로 충돌, 명시 checkpoint 복구와 구형 읽기검사를 확인했다. 실제 저장 후 검사 실패가 난 자동 rollback, 여러 파일 중 일부만 저장된 실패, backup 뒤 외부 변경과 복구 실패 분기는 아직 실행 검증하지 않았다. R8-4의 별도 미사용 사례에 포함한다. R6/R7 완전 현재 문맥·스킬 간 전달도 수행 자료와 평가 설계를 분리한 경계에서 별도로 확인해야 한다.\n\n연결 메타데이터 변경도 각 소유 기록의 새 판본이 필요하다는 R1 규칙을 반례에 포함한다. 초기 판본 누락과 보완 후 결과는 [R8-2 보고](../08_검증결과/R8_02_기록관리자/00_결과안내.md)에 보존했다. 이 항목은 계획 추가이며 R8-4 완료가 아니다.\n',S)
assert {p for p,h in initial.items() if sha(BASE/p)!=h}==allowed_prior|{edited[4]}
for p,h in initial.items():assert sha(BASE/'backup/2026-10-15_R8_02_착수/입력정본'/p)==h
review_changes={p:{'before':h,'after':sha(BASE/p)} for p,h in review['D_source_hashes'].items() if sha(BASE/p)!=h};assert set(review_changes)<=set(edited)
sys.path.insert(0,str(BASE/'07_실행도구'));checks={}
for name in ['R7_연결확인.py','R6_통합조회.py']:
    spec=importlib.util.spec_from_file_location('r8_02_publish_'+name,BASE/'07_실행도구'/name);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);checks[name]=m.inspect(BASE);assert checks[name]['valid'],checks[name]
docs=[BASE/D/'00_결과안내.md']+[BASE/p for p in edited if p.endswith('.md')];assert not check_links(docs),check_links(docs)
save(D+'보존과최종연결_확인.json',{'version':'0.1.0','redteam_verdict_sha256':sha(REVIEW/'R8_02_최종판정.json'),'review_inputs_matched_before_publication':True,'reviewed_D_file_changes_after_publication':review_changes,'navigation_and_status_changes':{p:{'before':h,'after':sha(BASE/p)} for p,h in navigation_before.items()},'initial164_backup_unchanged':True,'initial164_changed_only_reported_paths':sorted(allowed_prior|{edited[4]}),'other159_initial_inputs_unchanged':True,'D_R7_current_query_valid':checks['R7_연결확인.py']['valid'],'D_R6_current_query_valid':checks['R6_통합조회.py']['valid'],'fixture_full_R6_R7_validation_claimed':False,'R8_1_feedback_received':True,'R8_2_feedback_received':False,'candidate_adopted':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'archived_hashes':archived,'report_sha256':sha(BASE/D/'00_결과안내.md')},S)
print(json.dumps({'published':D,'archived_files':len(archived),'D_R6_R7_valid':True,'R8_2_human_feedback_pending':True,'R8_3_4_not_started':True},ensure_ascii=False))
