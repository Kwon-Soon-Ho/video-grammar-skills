from 공통지원 import BASE,save as base_save,safe,sha,check_links
from pathlib import Path
import json,shutil,sys,importlib.util
L=Path(__file__).parent.resolve();CR=L.parent;W=L/'R8_시험/video-guidance-reviewer-workspace';RV=L/'R8_03_독립검토'
S='2026-10-15_R8_03_시험정리';D='08_검증결과/R8_03_적용성검토자/';F='14_스킬재구성/'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
io=lambda p:Path('\\\\?\\'+str(p.resolve()))
CONTEXT={};OWNED={}
def save(rel,value,stage):
    base_save(rel,value,stage)
    OWNED[rel]=sha(BASE/rel)
def record_publication_failure(exc):
    if not CONTEXT.get('started'):return
    actual={p:{'last_owned_sha256':h,'current_sha256':sha(BASE/p) if (BASE/p).is_file() else None} for p,h in OWNED.items()}
    status=F+'진행상태.json';report=D+'00_결과안내.md'
    if status in OWNED and (BASE/status).is_file() and sha(BASE/status)==OWNED[status]:
        data=read(BASE/status);data['stages']['R8-3']='publication_failed_not_complete'
        data['publication_error']=str(exc);base_save(status,data,S)
    if report in OWNED and (BASE/report).is_file() and sha(BASE/report)==OWNED[report]:
        raw=(BASE/report).read_text(encoding='utf-8')
        base_save(report,'# 게시 실패 — 완료가 아님\n\n게시상태.json과 오류/부분 반영 기록을 먼저 확인한다.\n\n'+raw,S)
    base_save(D+'게시상태.json',{'publication_state':'failed','completion_receipt_valid_for_publication':False,'receipt_file_present':(BASE/D/'보존과최종연결_확인.json').is_file(),'error_type':type(exc).__name__,'error':str(exc),'partial_saved_files':actual,'archive_files_completed_and_hashed':len(CONTEXT.get('archive_manifest',{})),'candidate_adopted':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'limits':'only matching owned report/status are relabeled; failure marker written separately; not atomic rollback or complete concurrency protection'},S)

def main():
    review=read(RV/'R8_03_최종판정.json')
    assert review['limited_completion_supported'] and not review['unresolved_blocking_findings']
    assert all(sha(BASE/p)==h for p,h in review['D_source_hashes'].items())
    assert all(sha(CR/p)==h for p,h in review['C_result_hashes'].items())
    initial=read(BASE/'08_검증결과/R8_03_입력보존.json')['source_hashes']
    prior={'00_시작안내.md','01_진행현황.md',F+'진행상태.json','08_검증결과/R8_02_기록관리자/00_결과안내.md'}
    assert len(initial)==174 and {p for p,h in initial.items() if sha(BASE/p)!=h}==prior
    summary=read(W/'비교결과_정본.json');assert summary['candidate_instruction_version']=='0.2.0-draft.2'
    CONTEXT['started']=True
    save(D+'게시상태.json',{'publication_state':'in_progress','completion_receipt_written':False},S)
    archived={};CONTEXT['archive_manifest']=archived
    def exact(src,dst):
     dst=safe(dst);q=io(dst);s=io(src);h=sha(s);q.parent.mkdir(parents=True,exist_ok=True)
     if q.exists():assert sha(q)==h,str(dst)
     else:shutil.copy2(s,q)
     assert sha(q)==h and sha(s)==h,'archive source/destination changed or mismatched: '+str(dst)
     archived[dst.relative_to(BASE).as_posix()]=h
    for source,label in [(W,'video-guidance-reviewer-workspace'),(W.parent/'video-guidance-reviewer','video-guidance-reviewer')]:
     for p in sorted(source.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:exact(p,BASE/'backup'/S/'실행원문'/label/p.relative_to(source))
    for p in L.glob('R8_03_*.py'):exact(p,BASE/'backup'/S/'작성도구'/p.name)
    for n in ['R8_01_뷰어작성.py','공통지원.py']:exact(L/n,BASE/'backup'/S/'작성도구'/n)
    for p in RV.rglob('*'):
     if p.is_file() and '__pycache__' not in p.parts:exact(p,BASE/D/'독립검토'/p.relative_to(RV))
    for n in ['비교결과_정본.json','비교결과_요약.md','실행결과_사실검사.json','실행완료_기록.json','평가항목.json','평가기준_고정기록.json','수행자료_포함과분리.json','동등조건_확인.json','진행계획.md','적용성검토자_출력검토.html','뷰어_표시검증.json','공식뷰어_실행기록.json']:
     exact(W/n,BASE/D/n)
    for p in (W/'원문보존').rglob('*'):
     if p.is_file():exact(p,BASE/D/'원문보존'/p.relative_to(W/'원문보존'))
    for run in (W/'iteration-1').glob('eval-*/*/run-1'):
     for p in [run/'grading.json',run/'transcript.md']+list((run/'outputs').rglob('*')):
        if p.is_file():exact(p,BASE/D/'사례별출력'/run.relative_to(W/'iteration-1')/p.relative_to(run))
    table=['| 개발 과제 | 후보 | 기존 |','|---|---|---|']
    for c in summary['comparisons']:
     a,b=c['configurations']['new_skill'],c['configurations']['old_skill']
     table.append(f'| {c["eval_name"]} | {a["passed"]}/{a["total"]}조건 | {b["passed"]}/{b["total"]}조건 |')
    report='''# R8-3 적용성 검토자 — 결과와 사람 검토
    
    2026-10-15 · **후보 재구성·정적 보완·합성 개발 비교·독립 채점/레드팀을 정리했다. 이번 출력 피드백은 대기 중이다.** 후보 채택·기본 전환·R8/Phase00 완료는 아니다. R8-4와01-A 구현은 시작하지 않았다. 자료 게시 완료는 [게시상태](게시상태.json)의 complete 및 연결된 최종 확인서 해시로 확인한다.
    
    ## 무슨 일을 맡기는가
    
    원칙·레이아웃·외부 지침을 이 상황에 써도 되는지 검토한다. 목적에 맞는 반복·정지·대칭·텍스트는 유지할 수 있고, 근거로 확인된 오류는 수정 제안한다. 자료 없는 판단만 국소적으로 보류하고 필요한 사람 질문을 남긴다. 새 화면 제작·영상 분석/측정·사람 내용 승인 대행은 아니다.
    
    [후보 v0.2.0-draft.2](../../06_맞춤스킬/재구성후보/video-guidance-reviewer/SKILL.md)는 본문과 참조2개로 구성했다. 참조는 근거 찾기/적용 조건과 항목별 판정/사람 검수다. 이 역할에는 새 실행 코드나 외부 패키지를 넣지 않았다. 기존 스킬·고정 정본/목록은 유지했다.
    
    ## 무엇을 보완했나
    
    - R7의 적용/필수 선정·네 항목 판정과 미검수·핵심 오류 비상쇄·부분 결과/사람 질문을 연결했다. 26개를 전부 의무화하거나 총점을 만들지 않는다.
    - 문서의 수치/부정어 불일치는 확인하면서 실제 영상의 읽기/동기화 검수를 대신하지 않도록 했다.
    - 한맥 웹 관측 라이브러리·회사 CI·프로젝트 역할과 실제 R6 회신의 확인 범위를 분리했다. 웹 지침의 수량·px/ms·취향을 회사 의무로 옮기지 않는다.
    - 정적 레드팀 후 이미 유효하게 접수된 R6 회신을 재요청해야 한다는 오독을 막고, 저장 실패의 실제 상태 확인/내 쓰기 일치 시 복구/외부 변경 보호를 명확히 했다. 변경 전 draft.1과 근거를 보존했다. 이 쓰기 실패 분기를 실행 시험했다는 뜻은 아니다.
    
    ## 같은 요청·자료로 비교한 결과
    
    '''+'\n'.join(table)+'''
    
    이번 세 사례는 구·신 모두 각7/7조건으로 동률이다. 이 표본에서 개정효과를 변별하지 못했으므로 후보의 일반 우위·효율 향상을 주장하지 않는다.

    사례1은 한국어/단위·의미 오류와 무음 전달·적합한 반복 비교를 함께 검토했다. 사례2는 삼안 초안에 관한 회사색/웹 라이브러리·최신성 회신의 범위를 검토했다. 사례3은 등속 예외·숙련도 근거·UX 연결 후보·외부 수량 강제·인용 SHA/주장 범위를 검토했다. 실제 결과의 근거/누락·동률과 구분 조건은 [독립 채점](독립검토/채점/독립채점_종합.md)과 [비교 상세](비교결과_요약.md)를 함께 본다. 각 run의 dispatch.json은 실행 전 준비 사본이며 실제 시작·완료 알림/출력 해시는 실행완료_기록.json으로 대조한다.
    
    [실제 출력 뷰어](적용성검토자_출력검토.html)에서 과제·출력·항목별 채점 근거를 볼 수 있다. 채점 조건 수는 영상 품질 총점이 아니다. 각 과제/구성1회, 구/신3쌍 총6회이며 실패도 보존한다. 실행 전 고정한21조건과 평가자료는 수행 사본 밖에 뒀다. 일반적인 단계/오류 집계 지식 문장까지 전부 제거했다고 하지는 않는다.
    
    ## 무엇을 조사·검토했나
    
    기존 R3의 모션/정보 전달·14레이아웃과 조건/반례, 외부 지침 선별 기록, R5 회사 CI 연결, R6 실제 회신 범위, R7의7묶음26항목과 원문 조사 깊이/운영 계약을 대조했다. 외부 지침은 Taste 외 Impeccable·LottieFiles·발표/PPT·visual QA의 기존 분야별 선별 기록을 사용했다. R3 원문 전체가 아니라5절 발췌인 수행 자료와 원본의 SHA/변환 목록을 보존했다.
    
    이번에는 원격 원문을 새로 열거나 최신 버전·학술 장 전문·외부 스킬 코드를 전수 재검증하지 않았다. R7 WEB 원문은 DB의 locator/요약/이식 한계 기록이며 전문 보관/원격 hash가 없다. 이를 새로운 원문 열람·실영상 효과의 증거로 쓰지 않는다. 원문/코드·의존성/라이선스의 기존 이식 한계도 유지한다.
    
    Anthropic Skill Creator의 초안·구버전 비교·독립 채점·공식 정적 뷰어 절차를 Codex 실행 환경에서 사용했다. Claude CLI/API·전역 설치·자동 트리거 시험을 하지 않았다. 공식 뷰어 원본과 Apache-2.0 LICENSE를 보존하고 표시 사본의 외부 리소스4개 제거/script 경계 이스케이프 후 실제 출력과 대조했다. 이는 HTML/데이터 구조 검사이며 브라우저 렌더·클릭/시각 검수는 아니다. CU/AE 연결을 사용하거나 변경하지 않았다.
    
    ## 검증 범위와 남은 일
    
    수행 사본의 모든 입력은 읽기 전용이고 결과 보고만 작성했다. 해시 대조·JSON 검사·독립 내용 채점과 [레드팀](독립검토/R8_03_최종판정.md)은 사람 출력 피드백을 대신하지 않는다. 시간/token은 미수집이며 가짜 반복/분산·문자수 대체 통계를 넣지 않았다. 각 과제1회/풍부한 공통DB로 일반 우위·효율·스킬 독자효과를 입증하지 않는다.
    
    로고 실물/실제 영상·전체 R6 현재 선언/원문·전체 R7 고정 문맥과 검사도구는 수행 사본에 없다. D 운영의 별도 R6/R7 정상 조회를 이 사본의 full 통과로 전용하지 않는다. 지식 draft 실제 수정과 저장 실패 복구도 이번 행동시험의 완료 범위가 아니다.
    
    R8-4에서 새 미사용 사례·정상 유지/부분보류·실제 인용 지지/판본 변경·스킬 간 전달·허용 쓰기/실패·현재 문맥/전환을 별도로 확인해야 한다. [R8-4 필수 보완 계획](../../14_스킬재구성/R8-4_독립확인_보완계획.md)을 유지한다. 기존 R8-1·R8-2 구성 유지 회신이 이번 스킬의 출력 평가나 전체 완료 회신은 아니다.
    
    이번에는 검토 결론·근거·보류/사람 질문·설명 분량이 실무에 맞는지 피드백을 받는다. 기존 목적/draft 권한을 다시 묻는 것이 아니다.
    '''
    report=report.replace('\n    ','\n')
    save(D+'00_결과안내.md','# 게시 검사 중 — 아직 완료 확인 전\n\n'+report,S)
    edited=[F+'진행상태.json',F+'R8-3_적용성검토자_구성안내.md','00_시작안내.md','01_진행현황.md',F+'R8-4_독립확인_보완계획.md']
    navigation_before={p:sha(BASE/p) for p in edited}
    state=read(BASE/edited[0]);state['version']='0.1.6';state['stages']['R8-3']='guidance_reviewer_development_comparison_and_redteam_complete_human_feedback_pending'
    state['reviewer_candidate_version']='0.2.0-draft.2';state['reviewer_trials']={'actual_executor_attempts':6,'cases':3,'runs_per_case_per_configuration':1,'actual_video_trials':0,'input_files_read_only':True}
    save(edited[1],(BASE/edited[1]).read_text(encoding='utf-8')+'\n\n## 현재 결과\n\n후보 draft.2의 정적 보완·3종 구/신 개발 비교·독립 채점/레드팀을 정리했다. [결과와 사람 검토](../08_검증결과/R8_03_적용성검토자/00_결과안내.md). 이번 출력 피드백 대기이며 R8-4/기본 전환·전체 완료·01-A는 아직이다.\n',S)
    for p in edited[2:4]:
     t=(BASE/p).read_text(encoding='utf-8');marker='\n\n현재 R8-1·R8-2의 구성·분량 유지 회신을 보존했고'
     if marker in t:t=t[:t.index(marker)]
     t=t.replace('세 번째 스킬 후보 검토','세 번째 스킬 출력 피드백 대기').replace('R8-3 적용성 검토자 후보 검토 중.','R8-3 개발 비교/레드팀 정리, 출력 피드백 대기.').replace('적용성 검토자 후보를 검토 중이다.','적용성 검토자의 출력 피드백을 기다린다.')
     t+='\n\n현재 R8-1·R8-2의 회신을 보존했고 [R8-3 결과와 출력 검토](08_검증결과/R8_03_적용성검토자/00_결과안내.md)를 정리했다. R8-3 출력 피드백 대기이며 R8-4·기본 전환·전체 Phase00 완료·01-A 구현은 아직이다.\n';save(p,t,S)
    save(edited[4],(BASE/edited[4]).read_text(encoding='utf-8')+'\n\n## R8-3에서 남긴 확인 범위\n\n적용성 검토자는 이번에 입력 읽기와 검토 보고만 수행했다. 새 미사용 정상 후보/국소 보류, hash가 일치해도 인용문이 주장을 지지하지 않는 경우, 대상/판본이 달라진 회신 재사용을 추가 확인한다. 지식 draft 실제 수정/저장 실패 복구 기능을 채택 범위에 둘 때에는 그 실제 쓰기·실패 분기도 별도 실행 검증한다. 전체 R6/R7 현재 문맥·스킬 간 전달·기본 전환 검토는 여전히 남아 있다.\n\n이는 계획 추가이며 R8-4 실행/통과가 아니다. [R8-3 보고](../08_검증결과/R8_03_적용성검토자/00_결과안내.md)의 개발 사례를 새 미사용 자료로 부르지 않는다.\n',S)
    assert {p for p,h in initial.items() if sha(BASE/p)!=h}==prior|{edited[4]}
    for p,h in initial.items():assert sha(io(BASE/'backup/2026-10-15_R8_03_착수/입력정본'/p))==h
    sys.path.insert(0,str(BASE/'07_실행도구'));checks={}
    for n in ['R7_연결확인.py','R6_통합조회.py']:
     sp=importlib.util.spec_from_file_location('publish803_'+n,BASE/'07_실행도구'/n);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);checks[n]=m.inspect(BASE);assert checks[n]['valid']
    assert not check_links([BASE/D/'00_결과안내.md']+[BASE/p for p in edited if p.endswith('.md')])
    save(D+'00_결과안내.md',report,S)
    save(edited[0],state,S)
    review_changes={p:{'before':h,'after':sha(BASE/p)} for p,h in review['D_source_hashes'].items() if sha(BASE/p)!=h};assert set(review_changes)<=set(edited)
    save(D+'보존과최종연결_확인.json',{'version':'0.1.0','redteam_verdict_sha256':sha(RV/'R8_03_최종판정.json'),'review_inputs_matched_before_publication':True,'reviewed_D_file_changes_after_publication':review_changes,'navigation_and_status_changes':{p:{'before':h,'after':sha(BASE/p)} for p,h in navigation_before.items()},'initial174_backup_unchanged':True,'initial174_changed_only_reported_paths':sorted(prior|{edited[4]}),'other169_initial_inputs_unchanged':True,'D_R6_current_query_valid':checks['R6_통합조회.py']['valid'],'D_R7_current_query_valid':checks['R7_연결확인.py']['valid'],'fixture_full_R6_R7_validation_claimed':False,'R8_2_feedback_received':True,'R8_3_feedback_received':False,'candidate_adopted':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'archived_hashes':archived,'report_sha256':sha(BASE/D/'00_결과안내.md')},S)
    save(D+'게시상태.json',{'publication_state':'complete','completion_receipt_written':True,'receipt_path':D+'보존과최종연결_확인.json','receipt_sha256':sha(BASE/D/'보존과최종연결_확인.json'),'limitations':'single last marker; not a multi-file atomic transaction'},S)
    print(json.dumps({'published':D,'archived_files':len(archived),'R6_R7_valid':True,'R8_3_human_feedback_pending':True,'R8_4_not_started':True},ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        try:record_publication_failure(exc)
        except Exception as report_error:print('failure report could not be saved:',type(report_error).__name__,str(report_error),file=sys.stderr)
        raise
