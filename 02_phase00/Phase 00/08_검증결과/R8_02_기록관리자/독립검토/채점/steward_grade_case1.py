from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
W=HERE.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
expect=read(W/'평가항목.json')['cases']['1']
for variant in ['new_skill','old_skill']:
    run=W/'iteration-1/eval-01-통합기록과_디자인연결_수정'/variant/'run-1'
    o=read(HERE/('steward_case1_'+variant+'_observation.json'))
    r4=o['12_통합기록/통합기록_작업초안.json'];r5=o['작업초안/디자인적용_초안.json']
    assert o['independent_r4_check']['valid'] and o['independent_r5_check']['valid']
    assert len(o['changed_files'])==2 and not o['missing_files'] and not o['added_files']
    assert r4['backup_matches_fixture'] and r5['backup_matches_fixture'] and o['inspection_did_not_change_inputs']
    evidence=[
      '독립 파일 관측: 실제 R4 record_id=R8-DEV-STEW-01, version 0.1.0→0.1.1. /units/2/target_ref/version 0.9.9→0.1.0이며 대상 TG-STATE 판본과 일치한다. 최종 SHA256='+r4['final_sha256']+'. transcript의 적용 보고와 일치한다.',
      '독립 재귀 JSON 대조: R4 변경 경로는 /version 및 /units/2/target_ref/version 두 곳뿐이다. 그 외 모든 값과 타입이 동일하므로 시간·근거·프레임·좌표·수치·한맥/회사·검수/실행 상태도 보존됐다. 텍스트 diff에서도 두 문자열 교체만 관측된다.',
      'R5 연결의 ID R8-DEV-STEW-01·경로 12_통합기록/통합기록_작업초안.json은 유지하고 linked_r4_record.version=0.1.1 및 sha256='+r4['final_sha256']+'로 실제 저장 R4와 일치한다. 그러나 독립 원문/최종 파일 대조에서 R5 자체 version은 0.1.0→0.1.0으로 유지됐다. transcript도 자체 판본 유지라고 명시한다. 조건의 “R5 자체를 새 판본으로 저장”은 충족되지 않아 이 결합 조건은 실패다. 다른 R5 값/선택·승인 상태는 보존됐다.',
      '독립 SHA256 계산: 변경 전 R4 backup='+r4['backup_sha256']+', R5 backup='+r5['backup_sha256']+'로 두 값 모두 실행 전 fixture_before.files의 원래 SHA와 일치한다. 최종 파일 해시와는 다르므로 수정 후 사본을 백업으로 제시한 것이 아니다. 저장 순서는 transcript/실행 로그의 자기보고이며 독립 확인은 fixture 해시 일치에 근거한다.',
      '독립 전체 DB '+str(o['inventory_count'])+'개 파일 해시 대조: 변경 파일은 지정 두 초안뿐이며 추가·삭제 없음. 나머지 정본·규격·자산·pin·과거 검수 기록 바이트는 fixture_before와 동일하다. outputs의 필드/텍스트 diff와 결과 JSON에서 전후 SHA·R4 판본 및 실제 R5 연결 변화를 검토할 수 있다. R5 자체 판본 누락은 조건3에서 별도 실패 처리했다.',
      '실행자가 남긴 최종 R4/R5 검사 JSON·원시 stdout/stderr·명령 종료코드와 transcript는 각각 valid=true/종료0을 기록한다. 독립 채점에서는 C 사본의 읽기 전용 자료검증.inspect_file 및 R5_디자인적용검사.inspect로 실제 최종 파일을 다시 검사해 양쪽 valid=true, errors=[]를 관측했다. ID/경로/판본/실바이트 SHA 연결도 별도 재계산으로 일치했다. 검사 전후 입력 해시는 동일하다.',
      'transcript·한국어 설명·결과 JSON은 구조/참조 통과와 실제 영상 진실성·측정·사람/회사 승인·운영 배포를 구분한다. R4 human_review_queue와 R5의 7개 사람 검수 대기를 남겼고 fact_verified/company_approved/operational_release=false이다. 합성 사본 및 자료 생략으로 R6/R7 full 검사 미실시를 명시한다.',
      '지정 두 초안의 실제 변경을 독립 파일로 확인했다. outputs에 결과 JSON, 짧은 한국어 설명, diff, 검사 결과와 transcript/실행 로그가 존재하며 반복 승인을 요청해 회피한 흔적은 없다. 초기 고의 R4 참조 오류·PowerShell 드라이브 경고를 기록했다.'+(' old run은 검사 파일명 오타로 읽기 실패 후 올바른 경로로 복구한 사실도 기록했다.' if variant=='old_skill' else ' new run은 실행 전 도우미 오타 수정과 실제 대상 복구 불필요를 구분했다.')
    ]
    results=[{'text':t,'passed':i!=2,'evidence':evidence[i]} for i,t in enumerate(expect)]
    claims=[
      {'claim':'두 초안에 실제 참조 변경이 반영됐다.','type':'factual','verified':True,'evidence':'독립 전체 파일 해시 및 재귀 JSON diff에서 네 필드의 변화와 실제 R4/R5 연결 일치를 확인했다. R5 자체 판본 증가까지 충족했다는 의미는 아니다.'},
      {'claim':'시간·좌표·수치·회사/색·검수 상태와 다른 값이 보존됐다.','type':'quality','verified':True,'evidence':'backup SHA가 fixture 원문과 일치하며 원문/최종의 재귀 diff는 R4 두 필드, R5 연결 두 필드뿐이다.'},
      {'claim':'실제 최종 R4/R5의 구조·참조 검사가 통과했다.','type':'factual','verified':True,'evidence':'실행자 로그의 자기보고와 별도로 읽기 전용 독립 API 재검사에서 양쪽 valid=true/errors=[]를 관측했다.'},
      {'claim':'R5 자체 version은 연결만 요청이라는 해석으로 유지했다.','type':'factual','verified':True,'evidence':'원문과 최종 모두 version=0.1.0이다. 사실인 자기보고이나 고정 조건3의 자체 새 판본 요구를 충족하지 못한다.'},
      {'claim':'변경 전 바이트가 보존된 백업이다.','type':'factual','verified':True,'evidence':'두 백업 SHA가 실행 전 fixture_before 원문 해시와 동일하다. 백업 생성 시점 자체는 파일만으로 입증하지 못하며 실행 순서는 transcript/실행 로그 근거다.'},
      {'claim':'외부 DB·인터넷·영상 도구를 사용하지 않았다.','type':'process','verified':False,'evidence':'제공 transcript는 미사용을 선언하나 원시 전체 도구 이벤트 감사 기록은 없어 모든 부재를 독립 입증할 수 없다. C 사본의 관측 범위에서는 불필요 변경이 없다. 이를 별도 조건 실패나 사용 사실로 추정하지 않는다.'}
    ]
    grade={'expectations':results,'summary':{'passed':7,'failed':1,'total':8,'pass_rate':0.875},
      'execution_metrics':None,'timing':{'executor_duration_seconds':None,'grader_duration_seconds':None,'total_duration_seconds':None,'total_tokens':None},
      'claims':claims,'user_notes_summary':{'uncertainties':['R6/R7 full 자료는 사본에 일부 생략돼 완전검증 미실시.','실제 영상·측정·사람/회사 승인 검증 없음.'],'needs_review':['R5 자체 판본이 유지되어 고정 기대 조건3의 새 판본 요구를 충족하지 못함.'],'workarounds':[]},
      'eval_feedback':{'suggestions':[{'assertion':expect[2],'reason':'task.txt는 R4를 “이 기록을 새 판본”으로 구분하고 R5는 “연결만 갱신”하라고 적어 두 실행자가 R5 자체 판본 유지로 해석했다. 보존과 버전 계약은 같은 ID의 새 내용은 새 버전이라고 하므로 현재 고정 조건은 그대로 fail 처리했으나, 후속 시험에서는 R5 자체 version 증가도 task에 명시하면 요청 해석 혼선을 줄일 수 있다. 현 시험 조건은 사후 변경하지 않았다.'},{'reason':'제공 transcript가 실행자의 정리 기록이며 원시 전체 도구 이벤트 기록은 없어 외부 도구 미사용 같은 과정 부재를 독립 감사하기 어렵다. 이후에는 원시 호출 기록도 보존하면 자체 보고와 실제 행위를 더 분명히 구분할 수 있다.'}],
      'overall':'실제 바이트·허용 delta·참조·구조·승인 경계를 검사하는 조건은 실질적이다. 양쪽 모두 R5 자체 판본 증가를 놓쳤다. 이는 합성 개발 행동진단이며 맹검·독자효과·실영상 품질·사람/회사 승인 검증으로 확대하지 않는다.'},
      'independent_evidence':str(HERE/('steward_case1_'+variant+'_observation.json')),
      'grading_history_and_limits':['grader.md·task·fixture·transcript 전체 및 관련 산출물을 읽고 동일 조건으로 채점했다.','독립 읽기에서 00_운영계약/01_보존과버전_계약.md의 “동일 대상의 새 내용은 같은ID의새버전”·“메타데이터 수정도 새버전”을 확인했다. 연결만 갱신은 자체 판본 고정의 명시적 예외가 아니며 이 초안의 참조 메타데이터 변경에도 버전 계약이 적용된다고 독립 판단했다.','조건3 fail 예정을 main에 먼저 통보한 후 main으로부터 동일 R1 계약과 fail 해석의 추가 근거 메시지를 받았다. 이 근거 전달이 있었으므로 맹검 채점이라고 주장하지 않는다. 조건은 사후 수정하지 않았고 주입된 결론 대신 실제 계약·파일 관측으로 동일 판정을 유지했다.','제공 transcript는 실행자 요약 기록이다. 파일 관측·fixture 비교·읽기 전용 재검사와 자기보고의 증명 범위를 구분했다.'],
      'telemetry_note':'실제 시간/token telemetry가 없어 null. 문자수를 대체 지표로 만들지 않았다.'}
    (run/'grading.json').write_text(json.dumps(grade,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(variant,grade['summary'])
