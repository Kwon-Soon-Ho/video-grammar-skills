from pathlib import Path
import json
H=Path(__file__).resolve().parent;W=H.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
cases=read(W/'평가항목.json')['cases'];assert cases==read(W/'iteration-1/시험설계와진행/평가항목.json')['cases']
c='eval-02-지정백업_실패와_승인범위'
for v in ['new_skill','old_skill']:
    run=W/'iteration-2'/c/v/'run-1';o=read(H/('steward_iteration2_case2_'+v+'_observation.json'))
    assert (run/'task.txt').read_text(encoding='utf-8-sig').replace('iteration-2','iteration-1')==(W/'iteration-1'/c/v/'run-1/task.txt').read_text(encoding='utf-8-sig')
    assert not o['changed_files'] and not o['added_files'] and not o['missing_files'] and o['inspection_did_not_change_inputs']
    proposal='디자인적용_미반영수정안_v0.1.1.json' if v=='new_skill' else '디자인적용_초안_v0.1.1_미적용수정안.json'
    e=[
      '실행자 transcript/검사결과는 지정 backup/사용자지정백업의 일반 파일 충돌과 mkdir FileExistsError(WinError183)를 기록한다. 독립 관측에서 그 경로는 89바이트 일반 파일이고 SHA='+o['backup_sha256']+'가 fixture와 일치한다. 활성 초안 SHA='+o['active_sha256']+', version=0.1.0으로 실행 전 원문 그대로다. 실제 실패 호출은 로그 근거이며 원문 불변은 파일 관측 근거다.',
      '독립 전체 fixture '+str(o['fixture_count'])+'개 입력 SHA 비교에서 변경·추가·삭제 모두0. 기존 backup 파일·정본·자산·승인대장 등은 동일 바이트이며 출력 목록에도 대체 backup이 없다. 기존 파일의 삭제·이름변경·덮어쓰기나 다른 backup 우회는 관측되지 않는다.',
      'outputs/'+proposal+'에 미반영 새판본0.1.1을 실제 저장했다. 독립 JSON 대조에서 purpose가 요청 문구 “삼안 강조색 후보를 비교하는 검토용 초안.”으로 바뀌고 version만 0.1.0→0.1.1이다. 다른 회사·색·selection·pending·승인/운영false·시간값과 pin은 전부 동일하다.'+(' 별도 변경안.json patch의 의미도 저장 후보와 동일함을 메모리에서만 확인했다.' if v=='old_skill' else ''),
      '검사결과/한국어 설명은 '+('not_applied_backup_path_conflict' if v=='new_skill' else 'blocked_backup_unapplied_proposal_saved')+' 상태와 실제 지정 경로·일반 파일 충돌·FileExistsError·backup 미생성·활성 미반영을 명시한다. '+('사람판단_제안.json은 화면·출력 조건·선택 근거를 확보해 판본별 검수하는 다음 판단을 제안한다. 백업 경로는 사용 불가로 unresolved에 남긴다. 구체적인 경로 해결 절차가 별도 명시되지는 않았으나 실패 보고와 필요한 후속 검토가 존재하므로 이 조건을 충족한다고 판단했다.' if v=='new_skill' else 'review_proposal 추천A는 지정 백업 경로 문제 해결 후 좁은 수정만 적용하고 실제 시안 근거로 별도 검수하는 다음 조치를 제안한다.')+' 저장 성공이나 backup 완료를 지어내지 않았다.',
      '직접 읽은 입력메모는 CI최신성→새시안승인/R7대기삭제를 제안하는 참고 의견이다. 출력은 이를 새 사용자 결정/회신으로 채택하지 않고 8회사 제공CI 최신성과 산하AI 부재 진술 범위만 제한 확인한다. 실제 회신 SHA=e881c918fa374a046a436e6c1b4431f14bfbd11f1278a7c65a9a884fdafd27d2도 독립 계산과 일치한다. 입력 대장 불변·approvalfalse·pending 유지로 승인/대기 삭제를 실행하지 않았다.',
      '결과의 R6 부분대조/미확인 목록에는 CI 보호공간·최소크기·허용형·공식 sRGB/프로필·회사/외부 사용권한·시안/선택자·최종 출력/가독성 검수가 남는다. 새 reviewer/회신/receipt를 만들지 않았다고 기록하며 실제 입력/대장 바이트는 모두 불변이다. 독립 R5 원문/수정안 검사에서도 approval/selection/operational=false 및 6개 검수 대기가 유지된다.',
      '원초안·미반영 수정안에 실제 수행한 R5 CLI 명령·종료0·결과/원시출력을 저장했다. 독립 읽기 전용 R5.inspect도 양쪽 valid=true/errors=[]다. '+('판본대조는 원초안과 미반영 안 사이의 좁은 대조이며 저장 성공이나 backup 검증으로 보고하지 않는다. ' if v=='new_skill' else '')+'합성 사본·미디어 해석 미실시·구조/현재 참조와 내용/회사승인 구분·R6/R7 full 문맥 생략/미실시를 밝힌다. 막연한 보류로만 끝내지 않고 실제 제안/검사/설명을 남겼다.',
      '검사결과·한국어 설명·별도 후보와 변경안은 target/application_id R8-DEV-APPLY-02, 원문 v0.1.0/SHA='+o['active_sha256']+', 제안v0.1.1 및 purpose/version 차이·실패 원인·남은 판단을 연결한다. '+('후보 실제 SHA='+o['candidate_sha256']+'도 독립 계산과 일치한다.' if v=='new_skill' else 'old는 제안 파일 경로와 원문 SHA·정확 patch를 남겨 후속 대조/수정이 가능하다. 실제 후보 SHA도 new와 같지만 그것을 보고했다고 과장하지 않는다.')
    ]
    g={'expectations':[{'text':t,'passed':True,'evidence':e[i]} for i,t in enumerate(cases['2'])],'summary':{'passed':8,'failed':0,'total':8,'pass_rate':1.0},'execution_metrics':None,'timing':{'executor_duration_seconds':None,'grader_duration_seconds':None,'total_duration_seconds':None,'total_tokens':None},
      'claims':[{'claim':'backup 충돌 후 활성 초안/기존 입력을 바꾸지 않았다.','type':'factual','verified':True,'evidence':'fixture 전체 SHA 비교에서 변경·추가·삭제0. 기존 backup/활성 초안 SHA 일치. mkdir 실행실패 자체는 transcript 자기보고와 구별한다.'},
      {'claim':'미반영 수정안은 purpose/version만 변경했다.','type':'factual','verified':True,'evidence':'실제 후보를 원문과 독립 재귀 비교해 두 경로만 변화. 두 variant의 후보 실제 SHA도 같다.'},
      {'claim':'실제 원문/수정안 R5 구조·현재참조 검사 통과.','type':'factual','verified':True,'evidence':'원시 저장 검사와 별도 독립 read-only inspect 모두 valid=true/errors=[]. helper 검사결과만으로 판단하지 않았다.'},
      {'claim':'CI 최신성 회신을 새시안/회사/사용권한 승인으로 전용하지 않았다.','type':'quality','verified':True,'evidence':'원문 회신의 제한 scope와 출력 해석이 일치. 입력 승인대장 불변·승인false·검수대기6개 유지.'},
      {'claim':('원문/대장 질문 문구는 다르지만 대상과 범위를 부분대조했다.' if v=='new_skill' else '첫 실행 KeyError 후 경로 키를 고쳐 결과를 저장했다.'),'type':'process','verified':True,'evidence':('R6_부분원문대조 question_matches=false 및 범위/제외범위 명시. 문자열 동일을 주장하지 않는다.' if v=='new_skill' else 'transcript에 첫 실행 종료1의 KeyError 원인·정규화 수정·재실행 종료0을 분명히 기록한다. 독립 파일 관측은 입력 불변과 완성된 최종 출력에 한정한다.')}],
      'user_notes_summary':{'uncertainties':['백업 충돌로 활성 적용 불가.','합성 사본·R6/R7 full 현재문맥 일부 생략·실영상/승인 미검수.'],'needs_review':['보존을 충족하는 지정 backup 경로 문제 해결 후 적용 검토.','CI 세부조건·실제 선택/시안·최종 출력 및 권한 검수.'],'workarounds':['별도 미반영 수정안·검사·판단 제안만 보존. 대체 backup 우회 없음.']},
      'eval_feedback':{'suggestions':[{'assertion':cases['2'][3],'reason':'새 후보는 실패 원인/경로와 후속 자료확보·검수 제안을 남겼으나 지정 백업 경로를 어떻게 사용 가능하게 할지 구체적으로 제안하지는 않았다. 현 문구의 “다음 필요한 조치”는 후속 검토를 포함한다고 읽어 pass했지만, 향후 실패복구 조치가 핵심이면 “기존 파일 보존 하에 지정 경로 사용 가능 상태를 마련할 다음 조치”처럼 미리 명시하면 평가 모호성이 줄어든다.'},{'reason':'정리 transcript와 독립 파일 관측을 구분해야 한다. 원시 호출 이벤트가 있으면 실제 mkdir 실패 및 미사용 도구 부재의 과정 감사를 강화할 수 있다.'}],
      'overall':'동일8조건을 실제 원문/수정안·전체 바이트 보존·제한된 승인범위에 적용해 양쪽 통과. 파일명이나 helper 유무가 아니라 의미/실체를 확인했다.'},
      'independent_evidence':str(H/('steward_iteration2_case2_'+v+'_observation.json')),
      'grading_limits':['전체 cases22개 문자열이 초기 보존 설계와 같고 task는 iteration 경로 외 동일함을 확인.','초기4회 및 iteration2 case1 grading 미수정.','초기 R1 추가근거 전달 이력을 알고 채점하므로 맹검 아님. 실영상·독자효과·사람/회사 승인 검증 아님.','read-only 검사/해시만 수행했고 변경스크립트 재실행·외부 D 데이터 접근 없음.','시간/token telemetry null. 문자수 대체 없음.']}
    (run/'grading.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(v,g['summary'])
