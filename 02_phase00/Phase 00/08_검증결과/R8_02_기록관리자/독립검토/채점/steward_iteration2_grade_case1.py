from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent;W=HERE.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
criteria=read(W/'평가항목.json')['cases'];prior=read(W/'iteration-1/시험설계와진행/평가항목.json')['cases'];assert criteria==prior
case='eval-01-통합기록과_디자인연결_수정'
for variant in ['new_skill','old_skill']:
    run=W/'iteration-2'/case/variant/'run-1';o=read(HERE/('steward_iteration2_case1_'+variant+'_observation.json'))
    initial=W/'iteration-1'/case/variant/'run-1'
    assert run.joinpath('task.txt').read_text(encoding='utf-8-sig').replace('iteration-2','iteration-1')==initial.joinpath('task.txt').read_text(encoding='utf-8-sig')
    r4=o['12_통합기록/통합기록_작업초안.json'];r5=o['작업초안/디자인적용_초안.json'];own_new=r5['after_version']!=r5['before_version']
    assert len(r4['json_diff'])==2 and len(r5['json_diff'])==(3 if own_new else 2)
    assert o['independent_r4_check']['valid'] and o['independent_r5_check']['valid'] and o['inspection_did_not_change_inputs']
    assert o['link_check']['sha_matches'] and r4['backup_matches_fixture'] and r5['backup_matches_fixture']
    ev=[
      '독립 실제 파일 관측: R4 record_id=R8-DEV-STEW-01 유지, 자체 version 0.1.0→0.1.1; /units/2/target_ref/version 0.9.9→대상 TG-STATE의 실제 판본0.1.0. 실제 저장 SHA='+r4['final_sha256']+'.',
      'fixture 원문 SHA와 일치하는 backup 및 실제 최종 R4를 재귀 JSON 대조했다. 변경은 /version 및 /units/2/target_ref/version뿐이다. 다른 모든 값/타입과 시간·근거·프레임·좌표·수치·한맥/회사·검수/실행 상태는 보존됐다. R4.diff의 제한 문자열 변경과도 일치한다.',
      '독립 R5 관측: linked_r4_record의 ID R8-DEV-STEW-01·경로는 그대로이고 참조 version=0.1.1 및 SHA='+r4['final_sha256']+'가 실제 최종 R4와 일치한다. '+('R5 자체 version도 0.1.0→0.1.1로 실제 저장했다. R5 diff는 소유 version·연결 version·연결 SHA 세 곳뿐이며 나머지 선택/승인상태는 보존됐다.' if own_new else '그러나 R5 자체 version은 0.1.0→0.1.0으로 유지했다. transcript도 자체 판본 보존을 명시한다. 조건의 R5 자체 새 판본 요구를 충족하지 않아 fail. 실제 R1 계약의 같은 ID 새 내용/메타데이터도 새 버전 원칙에 연결만 갱신은 명시적 판본고정 예외가 아니라고 판단한다. 다른 R5 값/선택·승인 상태는 보존됐다.'),
      '독립 계산: R4 backup SHA='+r4['backup_sha256']+', R5 backup SHA='+r5['backup_sha256']+'로 각각 실행 전 fixture_before 원문 해시와 정확히 같다. 현재 변경 파일 SHA와는 다르므로 변경 후 사본을 백업으로 제시하지 않았다. 백업 선행 순서는 실행자 transcript/로그 근거이며 독립 관측은 fixture 해시 일치에 근거한다.',
      '독립 전체 입력 '+str(o['inventory_count'])+'개 파일 해시 대조: 지정 R4/R5 두 초안만 변경됐고 추가·삭제 없음. 나머지 정본·자산·규격·pin·과거 검수 이력 바이트는 fixture와 동일하다. outputs의 diff·결과 JSON·backup에 전후 SHA 및 판본/연결 변화가 남아 검토 가능하다.'+(' R5 자체 판본 누락은 조건3에서만 실패 처리했다.' if not own_new else ''),
      '실행자는 실제 저장 후 R4 자료검증 및 R5 디자인적용검사의 원시 stdout/stderr·결과·명령 종료0을 남겼다. 독립 채점에서 C 사본의 읽기 전용 inspect_file/inspect를 실제 최종 R4/R5에 수행해 양쪽 valid=true/errors=[]를 관측했다. ID·경로·참조판본·실제 SHA도 별도 대조로 유효하다. helper 단위검사/정적 통과를 행동 pass로 대체하지 않았다.',
      '한국어 설명·transcript·결과는 합성 사본의 구조/참조 valid와 실제 영상·측정·내용·사람/회사 승인·운영 배포를 구분한다. R4 27건/R5 7건 사람 검수 대기를 남겼고 company_approved/operational_release=false다. R6/R7 full 자료 생략으로 완전검증 미실시를 명시했다.',
      '독립 실제 두 초안 수정이 확인됐고 결과 JSON·짧은 한국어 설명·텍스트/필드 diff·개별 검사와 수행/실패 로그를 저장했다. 재승인을 반복 요청해 회피하지 않았다. 초기 고의 TG-STATE 오류의 전후 해소와 PowerShell 경고·'+('저장 실패/복구 불필요' if own_new else '사전 잘못된 검사기 파일명 탐색 실패 후 복구')+'를 기록한다.'
    ]
    verdicts=[True,True,own_new,True,True,True,True,True];passed=sum(verdicts)
    grade={'expectations':[{'text':t,'passed':verdicts[i],'evidence':ev[i]} for i,t in enumerate(criteria['1'])],
      'summary':{'passed':passed,'failed':8-passed,'total':8,'pass_rate':passed/8},'execution_metrics':None,
      'timing':{'executor_duration_seconds':None,'grader_duration_seconds':None,'total_duration_seconds':None,'total_tokens':None},
      'claims':[{'claim':'요청된 R4 수정 및 R5 연결 갱신이 실제 적용됐다.','type':'factual','verified':True,'evidence':'독립 actual SHA·재귀 diff·연결 일치 확인. R5 소유 판본 충족 여부는 별도로 평가했다.'},
      {'claim':('R4/R5 자체 판본을 모두 0.1.1로 구분했다.' if own_new else 'R5 자체 판본을 요청 범위에 따라 유지했다.'),'type':'factual','verified':True,'evidence':('독립 원문/최종 두 기록 모두 자체 version 0.1.0→0.1.1.' if own_new else '독립 R5 자체 version은 0.1.0 불변이다. 사실인 자기보고지만 고정 조건3 및 R1 버전 계약을 충족하지 못한다.')},
      {'claim':'다른 입력과 시간·좌표·수치·회사/색·검수 상태는 보존됐다.','type':'quality','verified':True,'evidence':'전체 fixture 해시 대조 및 허용 필드 외 모든 JSON 값/타입 동일 확인.'},
      {'claim':'최종 R4/R5 구조·참조 검사 통과.','type':'factual','verified':True,'evidence':'실행자 로그 외 독립 읽기 전용 재검사 valid=true/errors=[] 및 source SHA 일치.'},
      {'claim':'backup은 변경 전 바이트다.','type':'factual','verified':True,'evidence':'각 backup SHA가 실행 전 fixture_before 원문과 일치. 선행 생성 시점의 호출 감사와는 구분한다.'}],
      'user_notes_summary':{'uncertainties':['합성 사본·실영상 없음·R6/R7 full 자료 일부 생략.'],'needs_review':([] if own_new else ['R5 자체 새 판본 누락.']),'workarounds':[]},
      'eval_feedback':{'suggestions':[{'assertion':criteria['1'][2],'reason':'task의 연결만 갱신은 R5 자체 판본 고정으로 읽힐 여지가 있고 old fresh가 다시 그 해석을 했다. R1 계약은 메타데이터 변경도 새 버전이라고 규정하므로 동일 기준을 유지했으며, 향후 task에서는 두 소유 판본을 명확히 쓰면 혼선을 줄일 수 있다. 현재 고정 조건은 사후 수정하지 않았다.'},{'reason':'제공 transcript는 정리 로그여서 모든 도구 미사용·백업 생성 순서의 독립 감사에는 한계가 있다. 원시 호출 기록을 함께 남기면 과정 증거가 강화된다.'}],
      'overall':'보완 후보는 실제 R5 소유 판본도 갱신했고 기준 fresh는 이를 유지했다. 나머지 판정은 실제 파일·fixture·읽기 전용 검사에 근거한다. 표본 1회 차이를 스킬 독자효과나 일반 성능으로 확대할 수 없다.'},
      'independent_evidence':str(HERE/('steward_iteration2_case1_'+variant+'_observation.json')),
      'grading_history_and_limits':['iteration-1 보존 평가항목의 cases 전체22개 문자열과 현재 cases가 같음을 코드로 확인했다. 두 variant의 task도 iteration 경로를 제외하고 초기 task와 같다.','초기4회 grading은 수정하지 않았다.','초기 case1에서 main이 R1 계약 추가 근거를 보냈던 이력과 task 해석 한계를 알고 채점하므로 맹검이라고 주장하지 않는다. 실제 계약/파일에 근거해 같은 조건을 적용했다.','helper narrow unit/정적 통과 주장은 개별 행동판정 근거로 사용하지 않았다.','합성 행동진단이며 실영상·사람/회사 승인·독자효과 평가 아님.','실제 시간/token telemetry는 null. 문자수 대체 없음.']}
    (run/'grading.json').write_text(json.dumps(grade,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(variant,grade['summary'])
