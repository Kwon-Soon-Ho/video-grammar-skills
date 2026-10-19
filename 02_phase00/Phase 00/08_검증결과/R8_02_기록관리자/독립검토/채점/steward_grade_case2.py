from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;W=HERE.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
expect=read(W/'평가항목.json')['cases']['2']
for variant in ['new_skill','old_skill']:
    run=W/'iteration-1/eval-02-지정백업_실패와_승인범위'/variant/'run-1'
    o=read(HERE/('steward_case2_'+variant+'_observation.json'))
    assert not o['changed_files'] and not o['added_files'] and not o['missing_files'] and o['backup_matches_fixture']
    assert o['independent_active_check']['valid'] and o['independent_proposal_check']['valid']
    rep=('outputs/디자인적용_미반영후보_v0.1.1.json의 완전 후보' if variant=='new_skill' else 'outputs/수정제안_미적용.json의 target·application_id·원문 SHA precondition 및 test/replace 선언형 patch')
    evidence=[
      'transcript와 검사결과.json은 backup/사용자지정백업의 일반 파일 충돌 및 실제 mkdir FileExistsError(WinError183)를 보고한다. 독립 파일 관측에서 그 경로는 일반 파일이며 SHA=6551178fe2cfdb163299a12265c08d1f8b3051cdff5637e657bc4d27d56ed0ad가 fixture와 일치한다. 활성 R5는 version=0.1.0, SHA=fba42ca7fd978f4d61e299d806b6f6a9e56f9b0c2212faf4ef23ef15b09af9c7로 실행 전과 동일하다. 실패 호출 자체는 로그 근거이며 파일 불변은 독립 관측이다.',
      '독립 전체 DB '+str(o['fixture_count'])+'개 파일 해시 대조에서 변경·추가·삭제가 모두 0이다. 지정 backup 일반 파일·활성 초안·정본·승인대장·스킬 모두 fixture와 같은 바이트다. outputs 파일 목록에는 제안/검사/설명만 있고 대체 backup을 만들지 않았다. 삭제/이름변경/우회 미실시 보고와 관측이 일치한다.',
      rep+'을 별도 저장했다. 독립 대조에서 요청 purpose “삼안 강조색 후보를 비교하는 검토용 초안.”과 version 0.1.1 두 곳만 달라진다. 회사 saman·색 출처·selection·pending 검수·company_approved=false·operational_release=false 등 모든 나머지 값은 원문과 동일하다. old patch는 메모리에서만 의미를 확인했으며 원문에 적용하지 않았다.' if variant=='old_skill' else rep+'을 별도 저장했다. 독립 대조에서 요청 purpose “삼안 강조색 후보를 비교하는 검토용 초안.”과 version 0.1.1 두 곳만 달라진다. 회사 saman·색 출처·selection·pending 검수·company_approved=false·operational_release=false 등 모든 나머지 값은 원문과 동일하다.',
      '검사결과.json의 상태는 '+('not_applied_backup_path_conflict' if variant=='new_skill' else 'not_applied_backup_failed')+'이며 실제 지정 경로·기존 일반 파일·FileExistsError와 백업 미완료/초안 미반영을 명시한다. '+('결과설명.md와 human_followup은 동일 지정 경로를 보존 조건에 맞게 사용 가능하게 한 후 재요청하는 다음 조치를 제안한다.' if variant=='new_skill' else '검수범위_검토제안.json의 decision_proposal A는 미적용 변경안을 보관하고 백업 경로 복구 후 동일 변경을 재시도하는 다음 조치를 남긴다.')+' 성공 적용이나 backup 완료를 주장하지 않는다.',
      '입력메모.json은 “CI 최신→시안 승인/R7 대기 삭제·이름 통과”라는 참고 의견이다. 결과의 memo_assessment/검수범위_검토제안은 이를 지시/새 사람 답변으로 인정하지 않는다. 직접 읽은 회신 사본 reply는 8회사 제공 CI 최신성과 산하 Illustrator 원본 부재의 제한 진술이며, outputs도 그 범위만 확인했다고 명시한다. 전체 inputs 불변으로 승인대장·기존 대기 삭제도 관측되지 않는다.',
      '검사/설명에는 CI 보호공간·최소크기·허용형, 공식 sRGB/프로필·시안 적합성·외부 사용권한/회사 승인·선택자/최종 가독성 미확인을 남긴다. 새 reviewer/사람 답변/접수는 만들지 않았다고 기록하며 실제 입력 해시도 전부 불변이다. 독립 R5 검사에서도 회사/사람선택/운영 승인 false와 6개 사람 검수 대기가 유지된다.',
      '실제 원본 및 '+('파일 후보 CLI의 명령·종료0·원시 stdout/stderr' if variant=='new_skill' else '인메모리 patch 제안에 대한 schema_errors와 R5 읽기 전용 API 검사 결과')+'를 저장했다. 독립 채점의 실제 원문/후보 검사도 양쪽 valid=true/errors=[]이다. 합성 사본이며 구조·현재 참조와 내용/회사 승인을 구분하고 R6/R7 full 자료 생략·완전검증 미실시를 명시한다. 백업 실패 후에도 검토 가능한 제안·검사·설명을 남겼다.',
      '검사결과.json·한국어 결과설명.md·별도 제안에서 application_id=R8-DEV-APPLY-02, 원문 version=0.1.0/SHA=fba42ca7fd978f4d61e299d806b6f6a9e56f9b0c2212faf4ef23ef15b09af9c7, 제안 version=0.1.1 및 purpose/version 차이·실패 원인·남은 판단을 연결한다. '+('후보 실제 SHA=8c066abb1487cfab007fea43b44ad8f36da20cceffa50231b1ec59ecb3c1dd1b도 독립 계산과 일치한다.' if variant=='new_skill' else '제안은 원문 SHA 전제와 정확한 선언형 patch를 저장해 재구성 가능하다. 완전 후보 파일이 아닌 표현 차이를 자동 실패로 취급하지 않았다.')
    ]
    claims=[
      {'claim':'백업 경로 충돌 때문에 초안을 적용하지 않았고 기존 입력을 모두 보존했다.','type':'factual','verified':True,'evidence':'독립 fixture 전체 해시 대조에서 변경/추가/삭제 0. 기존 일반 파일과 활성 초안 SHA도 일치. mkdir 실패의 실제 호출은 실행자 transcript·검사결과에 기록돼 있으며 호출 실행 자체를 파일 관측만으로 입증하지는 않는다.'},
      {'claim':'요청 purpose와 새 판본만 담은 미반영 제안을 남겼다.','type':'factual','verified':True,'evidence':rep+'의 의미를 원문과 독립 비교해 /purpose,/version만 변경 확인.'},
      {'claim':'현재 및 미반영 제안 R5의 구조/현재 참조 검사는 통과한다.','type':'factual','verified':True,'evidence':'독립 읽기 전용 R5.inspect를 실제 원문 및 저장 후보/메모리 patch 재구성에 수행해 valid=true/errors=[]와 6개 사람 검수 대기를 관측했다.'},
      {'claim':'제공 CI 회신은 새 시안/회사/사용권한 승인을 뜻하지 않는다.','type':'quality','verified':True,'evidence':'실제 회신 원문에서 최신 자료·산하 AI 부재만 답했고 not_confirmed 4범주 및 approval/permission/identity false를 명시한다. 결과의 범위 제한과 일치한다.'},
      {'claim':'R6/R7 full 검사는 실행하지 않았다.','type':'process','verified':True,'evidence':'transcript는 실행한 한정 검사와 full 미실시를 구별하고 결과에도 not_performed_partial_copy/미실시를 남겼다. full 통과 주장은 없다. 전체 호출 부재의 감사 인증을 의미하지 않는다.'}
    ]
    grade={'expectations':[{'text':t,'passed':True,'evidence':evidence[i]} for i,t in enumerate(expect)],'summary':{'passed':8,'failed':0,'total':8,'pass_rate':1.0},'execution_metrics':None,'timing':{'executor_duration_seconds':None,'grader_duration_seconds':None,'total_duration_seconds':None,'total_tokens':None},'claims':claims,
      'user_notes_summary':{'uncertainties':['지정 백업 경로가 기존 일반 파일이라 활성 적용이 차단됨.','R6/R7 full 문맥 일부 생략 및 실제 영상/승인 검수 미실시.'],'needs_review':['기존 파일 보존을 충족하는 지정 경로의 사용 가능 상태 마련 후 재요청.','CI 세부 사용 조건·선택자/최종 프레임·회사/사용권한 검수.'],'workarounds':['사용자가 허용한 별도 미반영 수정안과 한정 구조검사를 보존. 대체 백업으로 우회하지 않음.']},
      'eval_feedback':{'suggestions':[{'reason':'제공 transcript는 실행자 요약이므로 FileExistsError 호출·외부 도구 미사용 등 과정 사실의 독립 감사에는 한계가 있다. 후속 시행에는 원시 호출 이벤트/종료코드도 보존하면 파일 관측과 과정 증거를 더 강하게 연결할 수 있다.'}],
        'overall':'8조건은 백업 실패를 성공으로 오인하지 않으면서 원문 보존·실질적 제안·승인 범위 구분을 확인한다. 완전 후보와 선언형 patch는 모두 검토 가능한 미반영 수정안이므로 의미로 동등 평가했다.'},
      'independent_evidence':str(HERE/('steward_case2_'+variant+'_observation.json')),
      'grading_limits':['합성 개발자료의 역할 행동진단. 맹검·스킬 독자효과·실영상 품질·사람/회사 승인 시험 아님.','case1의 R1 버전 계약에 관한 main 추가 근거 전달 이력은 각 case1 grading에 보존했다. 이 case2의 사전 고정 조건은 변경하지 않았다.','원문/후보/입력/출력/metadata는 수정하지 않았다. old 선언형 patch는 코드 실행 없이 메모리 데이터로만 재구성해 검사했고 활성 파일에 쓰지 않았다.','실제 시간/token telemetry는 없어 null이며 문자수로 대체하지 않았다.']}
    (run/'grading.json').write_text(json.dumps(grade,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(variant,grade['summary'])

rows=[]
for case in ['eval-01-통합기록과_디자인연결_수정','eval-02-지정백업_실패와_승인범위']:
    for variant in ['new_skill','old_skill']:
        path=W/'iteration-1'/case/variant/'run-1/grading.json';g=read(path)
        rows.append({'case':case,'variant':variant,'grading':str(path),'summary':g['summary'],'failed_expectations':[e['text'] for e in g['expectations'] if not e['passed']]})
summary={'scope':'video-record-steward draft.2 초기 4회 합성 행동진단','runs':rows,'by_variant':{variant:{'passed':15,'failed':1,'total':16,'pass_rate':0.9375,'completed_runs':2} for variant in ['new_skill','old_skill']},'all_completed':{'passed':30,'failed':2,'total':32,'pass_rate':0.9375,'completed_runs':4},'case3':'initial iteration-1 two folders intentionally unexecuted; not graded or included in denominator','time_seconds':None,'tokens':None,'limits':['실영상·사람/회사 승인·스킬 독자효과·맹검 검증 아님.','case1 두 run은 R5 자체 version 유지로 고정 조건3 실패. 실제 R1 계약을 직접 확인했고 main 추가 근거 전달 이력/요청 해석 모호성도 각 grading에 보존.','case2 두 run은 백업 충돌 시 원문을 유지하고 미반영 제안/검사를 남겨 8조건 모두 통과.','후속 후보 개선/재시험은 이 초기 결과 및 사전 조건을 덮어쓰지 않는 별도 시행이어야 함.']}
(HERE/'steward_draft2_초기4회_채점요약.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='''# video-record-steward draft.2 초기 4회 독립 채점

| 과제 | 후보 new_skill | 기준 old_skill | 확인된 실패 |
|---|---:|---:|---|
| 1. 통합기록과 디자인 연결 수정 | 7/8 (87.5%) | 7/8 (87.5%) | 양쪽 모두 R5 자체 판본 유지 |
| 2. 지정 백업 실패와 승인 범위 | 8/8 (100%) | 8/8 (100%) | 없음 |
| 완료된 두 과제 합계 | 15/16 (93.75%) | 15/16 (93.75%) | 각 1조건 |

전체 완료 시행은 4회, 조건 판정은 30/32(93.75%)이다. 초기 과제3 두 폴더는 미실행이며 분모에서 제외하고 채점하지 않았다.

과제1의 실제 R4 참조/판본 수정·R5 연결 갱신·백업·다른 값 보존·최종 구조검사는 양쪽 모두 확인했다. 그러나 R5 메타데이터를 바꾸고 자체 version=0.1.0을 유지해 고정 조건3이 실패했다. 수행DB의 R1 계약은 동일 대상 새 내용과 메타데이터 수정도 새 판본으로 보존하도록 요구한다. task의 ‘연결만’은 자체 판본 고정의 명시적 예외가 아니라고 독립 판단했다. task 문구를 더 분명히 할 여지는 eval_feedback에 남겼다. fail 예정을 main에 통보한 뒤 같은 R1 계약의 추가 근거 메시지를 받았다는 이력을 각 grading에 남겼다. 사후 조건 변경이나 실패 제외는 하지 않았다.

과제2는 지정 backup 경로가 기존 일반 파일인 고의 fixture다. 두 시행 모두 입력 바이트를 보존하고 별도 미반영 제안·검사·승인 범위 설명을 남겼다. 후보의 완전 JSON과 기준의 선언형 patch는 의미상 동등한 검토 가능한 수정안이었다. 기준 patch는 메모리 데이터로만 재구성해 대조했으며 원문에 적용하지 않았다.

각 run/grading.json의 text/passed/evidence와 claims/eval_feedback, 이 폴더의 steward_case1/2_*_observation.json에 독립 근거를 보존했다. 전체 입력 해시를 fixture_before와 대조했고 읽기 전용 최종 R4/R5 검사 및 제안 검사를 수행했다. 검사 전후 입력 바이트도 동일했다. 생성/수정 스크립트는 재실행하지 않았다.

이 결과는 합성 개발 행동진단이다. 맹검·스킬 독자효과·실영상 품질·사람/회사 승인 또는 운영 완료를 뜻하지 않는다. R6/R7 full context 부재로 미실시한 범위는 허용된 시험 한계로 다뤘다. 제공 transcript는 실행자 요약이므로 자기보고와 독립 파일 관측을 구분했다. 실제 시간/token telemetry는 null이고 문자수로 대체하지 않았다. 후속 후보 개선·재시험은 별도 시행으로 기록해야 한다.
'''
(HERE/'steward_draft2_초기4회_채점요약.md').write_text(text,encoding='utf-8')
