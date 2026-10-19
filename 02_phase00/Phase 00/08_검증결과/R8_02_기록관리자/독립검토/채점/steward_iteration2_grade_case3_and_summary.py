from pathlib import Path
import json
H=Path(__file__).resolve().parent;W=H.parents[1]/'R8_시험/video-record-steward-workspace'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
cases=read(W/'평가항목.json')['cases'];assert cases==read(W/'iteration-1/시험설계와진행/평가항목.json')['cases']
c='eval-03-정확한_체크포인트_복구'
for v in ['new_skill','old_skill']:
    run=W/'iteration-2'/c/v/'run-1';o=read(H/('steward_iteration2_case3_'+v+'_observation.json'));r=o['recovery_request']
    assert o['active_bytes_equal_checkpoint'] and o['checkpoint_matches_request'] and o['failed_backup_matches_fixture_and_request']
    assert o['independent_restored_check']['valid'] and o['independent_legacy_check']['status']=='needs_migration'
    e=[
      '복구요청.json의 target_path='+r['target_path']+', failed_current_sha256='+r['failed_current_sha256']+', checkpoint_path='+r['checkpoint_path']+', checkpoint_sha256='+r['checkpoint_sha256']+'를 실제 파일/fixture와 독립 대조했다. 최종 활성 파일 전체 바이트가 checkpoint와 정확히 같고 SHA='+o['active_sha256']+'다. ID=R8-DEV-STEW-03도 일치한다.',
      '독립 전체 '+str(o['fixture_count'])+'개 원래 입력 해시 비교에서 기존 변경은 지정 활성 R4 한 개, 새 추가는 '+o['added_files'][0]+' 한 개, 삭제0이다. 새 보존 사본의 실제 SHA='+o['failed_backup_sha256']+'가 실행 전 fixture 활성파일 SHA 및 복구요청 failed_current_sha256과 일치한다. 기존 checkpoint/복구요청/legacy·원문·타 입력은 동일 바이트다.',
      '최종 파일을 정상 checkpoint와 전체 바이트로 비교해 정확 일치 확인했다. final/checkpoint version=0.1.0이다. 실패본→복원본 JSON 변화는 잘못 저장된 x.num 301→checkpoint300 및 version0.1.1→checkpoint0.1.0뿐이며 새 판본상승/임의 직렬화·추가개선이 없다. 결과/설명/로그는 실패 SHA f9480485...에서 정상 SHA4f309bf8...로 복구 및 exact restored 상태를 기록한다. 이는 좌표 재측정이나 임의 수치 보정이 아니라 요청된 원바이트 복원이다.',
      '실행자는 복구 후 실제 자료검증 명령·종료0·원시 stdout/stderr·결과 JSON을 남겼다. 독립 C 읽기 전용 inspect_file로 실제 복원 R4를 검사해 valid=true/status=draft_structure_pass/errors=[]와 최종 source SHA를 확인했다. 정상 구조와 실제 내용/측정/사람·회사/운영 승인을 구분하며 승인 플래그false·사람검수 대기27개를 유지한다.',
      '실제 legacy 파일 SHA='+o['legacy_sha256']+'가 fixture와 동일하다. 저장된 읽기 검사와 독립 inspect_file 모두 schema0.1.0/status=needs_migration/valid=false이며 원본 version·SHA·duration, time_contract, targets, evidence, 분류 범위, run, review의 9개 누락/검토항목을 남긴다. JSON/설명에도 접수·이관·수정 미실시를 명시하고 입력/대장 불변·추가파일이 실패본backup뿐이므로 가짜identity/시간 채움·접수/이관 출력은 관측되지 않는다.',
      'outputs에 '+('result.json·설명.md·개별 검사 JSON/원시출력·전후hash/diff/scope_audit' if v=='new_skill' else '검사결과.json·결과설명.md·개별 복구전/후·legacy검사 JSON/원시출력·보존_검증')+' 및 transcript를 남겼다. 고의 실패본의 core MAP-ONE 오류와 복구 후 해소를 구분하고 legacy needs_migration/사람검수 대기·합성 구조검사 한계·R6/R7 full 미실시를 명시한다. 내용/회사 승인이나 운영 완료로 승격하지 않는다.'
    ]
    g={'expectations':[{'text':t,'passed':True,'evidence':e[i]} for i,t in enumerate(cases['3'])],'summary':{'passed':6,'failed':0,'total':6,'pass_rate':1.0},'execution_metrics':None,
      'timing':{'executor_duration_seconds':None,'grader_duration_seconds':None,'total_duration_seconds':None,'total_tokens':None},
      'claims':[{'claim':'정상 checkpoint 바이트 그대로 실제 복원했다.','type':'factual','verified':True,'evidence':'독립 전체 바이트 직접 비교 및 SHA=4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2 일치. JSON 재직렬화로 기대값을 재구성하지 않았다.'},
      {'claim':'실패본은 새 backup으로 보존하고 다른 기존 입력은 바꾸지 않았다.','type':'factual','verified':True,'evidence':'새 backup SHA=f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9가 실행 전 fixture·요청과 일치. 원래 입력 중 활성1개 외 전부 불변.'},
      {'claim':'복원된 R4 구조/참조는 유효하다.','type':'factual','verified':True,'evidence':'실행자 결과와 별도 독립 read-only inspect_file valid=true/errors=[]; 사실/회사 승인은false.'},
      {'claim':'구형자료는 검사만 했고 needs_migration 및 누락을 남겼다.','type':'factual','verified':True,'evidence':'실제legacy bytes 불변, 독립 needs_migration/valid=false/누락9개·automatic_fill_allowed=false와 저장결과 일치.'},
      {'claim':'R6/R7 full 검증과 실제 영상/회사 승인 검사는 수행하지 않았다.','type':'process','verified':True,'evidence':'transcript/결과의 미실시 범위 명시 및 full 통과 주장 없음. 모든 외부 호출 부재의 원시 감사 인증을 뜻하지 않는다.'}],
      'user_notes_summary':{'uncertainties':['legacy 원본identity/시간계약/대상/근거/run/review 누락.','실영상·내용·사람/회사승인 미검수, R6/R7 full 자료 일부 생략.'],'needs_review':['실제 자료가 확보된 후 필요한 내용/사람 검수. legacy 접수/이관은 별도 명시 요청이 필요함.'],'workarounds':[]},
      'eval_feedback':{'suggestions':[{'reason':'원시 전체 호출 이벤트 없이 요약 transcript를 제공하므로 접수/이관 CLI 미실시 등 과정 부재는 파일불변 관측과 구별해야 한다. 이후 원시 호출기록 보존으로 강화 가능하다.'}],
      'overall':'6조건은 exact restore와 새 내용수정의 차이·실패본 원바이트 보존·구형 검사only를 실질적으로 구별한다. 양쪽 모두 충족. helper의 존재/좁은 unit검사로 pass를 대체하지 않았다.'},
      'independent_evidence':str(H/('steward_iteration2_case3_'+v+'_observation.json')),
      'grading_history_and_limits':['초기 보존설계와 현재 cases22개 문자열이 같음을 직접확인. 두 run 실제 task/fixture/transcript/결과·입력 파일에 근거.','초기 R1 계약 추가근거 전달 이력이 있어 맹검 채점이 아님. 실영상·스킬 독자효과·사람/회사승인 검증 아님.','main의 별도 사실검사 코드가 case1 baseline 재구성 assert에서 중단됐다는 통보를 받았다. 이는 모델 시행의 결함으로 세지 않았으며 이 채점은 fixture 원문SHA·실제backup/checkpoint 직접대조에 근거한다. 본 채점 시점 main의 최종 사실검사 파일은 아직 제공되지 않았고 이를 근거로 사용하지 않았다.','초기4회 및 iteration2 case1/2 판정을 수정하지 않음. 변경스크립트 재실행 없이 읽기전용 API/해시/파싱만 수행.','실제 시간/token telemetry null, 문자수 대체없음.']}
    (run/'grading.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(v,g['summary'])

rows=[]
cs=['eval-01-통합기록과_디자인연결_수정','eval-02-지정백업_실패와_승인범위',c]
for it,n in [('iteration-1',2),('iteration-2',3)]:
    for ci in cs[:n]:
        for v in ['new_skill','old_skill']:
            p=W/it/ci/v/'run-1/grading.json';g=read(p)
            assert [x['text'] for x in g['expectations']]==cases[str(cs.index(ci)+1)]
            count=sum(x['passed'] for x in g['expectations']);assert count==g['summary']['passed'] and len(g['expectations'])==g['summary']['total'] and g['summary']['pass_rate']==count/len(g['expectations'])
            rows.append({'iteration':it,'case':ci,'variant':v,'grading':str(p),'summary':g['summary'],'failed_expectations':[x['text'] for x in g['expectations'] if not x['passed']]})
def agg(rr):
    p=sum(x['summary']['passed'] for x in rr);t=sum(x['summary']['total'] for x in rr)
    return {'runs':len(rr),'passed':p,'failed':t-p,'total':t,'pass_rate':p/t}
summary={'scope':'합성 개발 행동진단: 초기draft.2 4회 + 보완draft.3/기준fresh 최종6회','runs':rows,
      'initial4':{v:agg([x for x in rows if x['iteration']=='iteration-1' and x['variant']==v]) for v in ['new_skill','old_skill']},
      'final6':{v:agg([x for x in rows if x['iteration']=='iteration-2' and x['variant']==v]) for v in ['new_skill','old_skill']},
      'all10_descriptive_only':agg(rows),'unexecuted_initial_case3_excluded':True,'time_seconds':None,'tokens':None,
      'limits':['초기후보와보완후보는 다른판본이므로 합산값은 10회 기록의 기술적 집계일 뿐 동일후보 성공률이 아님.','초기case3 두run미실행으로 분모 제외.','매조건 매run 같은고정문자열, 사후기준변경/실패제외없음.','보완에 사용한 같은 과제 재시험이므로 일반화/독자효과/맹검 근거 아님.','초기 R1 추가근거 전달 이력/요청 해석 한계 유지.','main의 별도최종사실검사 파일은 본 요약 시점 미제공이며 근거로 사용하지 않음. main 코드실패는 모델시행 실패로 세지 않음.','실영상/회사승인/운영완료검증 아님, R6/R7 full 생략한계 유지.']}
(H/'steward_iteration2_최종6회와초기4회_전체진단요약.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# video-record-steward 초기 4회와 보완 후 6회 진단

| 시행 | 과제 | 후보 new_skill | 기준 old_skill | 실패 |
|---|---|---:|---:|---|
| 초기 iteration-1, draft.2 | 1. 통합기록/디자인 연결 | 7/8 | 7/8 | 양쪽 R5 자체 판본 누락 |
| 초기 iteration-1, draft.2 | 2. 백업 충돌/승인 범위 | 8/8 | 8/8 | 없음 |
| 보완 iteration-2, draft.3 | 1. 통합기록/디자인 연결 | 8/8 | 7/8 | 기준 R5 자체 판본 누락 |
| 보완 iteration-2, draft.3 | 2. 백업 충돌/승인 범위 | 8/8 | 8/8 | 없음 |
| 보완 iteration-2, draft.3 | 3. 정확 checkpoint 복구 | 6/6 | 6/6 | 없음 |

초기 4회는 후보·기준 각각 15/16(93.75%)이었다. 보완 후 최종 6회는 후보 22/22(100%), 기준 21/22(95.45%)이다. 전체 10회 기록의 판정 집계는 73/76(96.05%)이며 서로 다른 후보 판본을 섞은 기술적 집계다. 동일 후보의 성공률이나 스킬 효과 크기로 읽을 수 없다. 초기 과제3 두 폴더는 미실행으로 보존하고 분모에서 제외했다.

확인된 보완 결과는 과제1의 R5 소유 판본이다. 새 후보의 실제 최종 R5 version은 0.1.1로 증가했으며 실제 R4 ID/새판본/저장파일 SHA도 일치한다. 기준 fresh는 다시 R5 자체 version을 0.1.0으로 유지해 같은 조건3이 실패했다. R1 계약의 동일 대상 새 내용·메타데이터도 새 판본 원칙을 적용했다. task의 ‘연결만’ 문구 해석 여지와 main의 R1 추가 근거 전달 이력은 각 grading에 남겼다. 초기 판정·고정 조건은 바꾸지 않았다.

과제2는 두 run 모두 기존 일반 파일 충돌 때문에 활성 초안과 전체 입력을 보존하고 purpose/version만 바꾼 별도 미반영 수정안을 남겼다. 원문과 실제 후보의 R5 구조/참조를 독립 검사했고 CI 최신성 회신을 새 시안·회사·사용권한 승인으로 확대하지 않았음을 확인했다. 새 후보의 후속 제안은 자료 확보/판본별 검수 중심이어서 구체적인 backup 경로 해결 절차를 더 명확히 할 여지는 eval_feedback에 남겼다. 현 조건의 후속 조치를 의미로 평가해 pass했다.

과제3은 양쪽 모두 지정 checkpoint 전체 바이트와 정확히 같은 활성 R4를 복원했다. SHA는 4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2다. 실패본 backup SHA는 f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9로 실행 전 fixture/요청과 일치했다. 기존 변경은 대상 R4 한 개, 추가는 실패본 backup 한 개뿐이었다. legacy는 바이트 그대로이고 독립 검사도 needs_migration/valid=false·누락9개였다. 복원된 R4의 독립 구조검사는 true였으며 실제 내용·회사 승인과 구분했다.

판정 근거는 실제 task·fixture_before/preflight·transcript 전체·입력/backup/checkpoint·outputs와 전체 파일 SHA, 재귀 JSON 차이 및 읽기 전용 개별 검사다. helper unit12/정적 통과는 행동 pass의 대체 근거가 아니다. 제안/patch·파일명·접미사 차이는 의미로 확인했다. 변경스크립트는 재실행하지 않았고 초기 산출물·후보·입력·metadata는 수정하지 않았다.

main의 별도 사실검사 코드가 case1 baseline 재구성 assert에서 중단됐다는 통보를 받았다. 이는 모델 시행의 실패가 아니며 본 채점은 기대 JSON을 재직렬화해 만들지 않고 fixture 원문 SHA와 실제 backup/checkpoint 바이트를 직접 대조했다. 이 요약 시점 main의 최종 사실검사 파일은 아직 제공되지 않아 근거로 쓰지 않았다. main의 검사 보완 결과는 별도 증거로 후속 연결할 수 있다.

이것은 합성 개발 행동진단이다. 같은 과제에 대한 보완 재시험·각 조건 1회 표본·초기 추가 근거 전달 때문에 맹검/독자효과/일반 성능을 입증하지 않는다. 실영상 품질·측정·사람/회사 승인·운영 완료와 무관하며 R6/R7 full 문맥 부재는 허용된 한계로 유지했다. 실행자의 정리 로그와 독립 파일 관측 범위도 구분했다. 실제 시간/token telemetry는 null이고 문자수로 대체하지 않았다.
'''
(H/'steward_iteration2_최종6회와초기4회_전체진단요약.md').write_text(md,encoding='utf-8')
print('all10',summary['all10_descriptive_only'])
