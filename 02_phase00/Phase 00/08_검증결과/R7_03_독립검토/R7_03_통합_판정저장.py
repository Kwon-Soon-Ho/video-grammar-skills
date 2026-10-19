import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
e=read(O/'R7_03_통합_최종_원문대조.json')
s1=read(O/'R7_03_1_공개원문_독립대조.json')['sources'];s2=read(O/'R7_03_2_공개원문_독립대조.json')['sources'];s3=read(O/'R7_03_3_최종판정.json')['independent_primary_reading'][0]
primary=s1+s2+[s3]
evidencefiles=['R7_03_통합_독립감사.py','R7_03_통합_최종_원문대조.json','R7_03_1_最종판정.json'.replace('最','최'),'R7_03_2_최종판정.json','R7_03_3_최종판정.json','R7_03_1_공개원문_독립대조.json','R7_03_2_공개원문_독립대조.json']
j={
 'stage':'R7-3 평가계획 통합 연결 독립 검토','limited_completion_supported':e['all_static_checks_passed'],'unresolved_blocking_findings':[],
 'findings_fixed_in_this_integration':[],
 'scope':{'included':['통합5파일 전문/데이터 비교, 계획9문서·정책2종·지표·26항목 준비행 연결','출처7개 지정부분의 앞소단계 직접 대조 기록과 기존7참조의 정확한 구분','가상 판정예12개 의미 검토·총점 비상쇄·실제0/null·해시/경로 정합성','이전 소단계 최종 독립판정3건과 연결한 R7-3 문서설계 범위 한정 완료'],
 'excluded':['평가 도구/채점기/harness 구현·01-A·미디어 추출/업로드·스킬 실행/재구성','실제 표본/정답/잠금/사람 초기답·중재·모델시행·alpha/효과 검증','표본수·허용오차·반복수·통계법·합격선 확정·회사 승인/권한 인증','최종 state/진행안내/보고 갱신 뒤의 미래 파일상태 인증·R7-4/R8/전체 Phase00 완료']},
 'verification':{'static_conditions':e['total'],'static_passed':e['passed'],'all_static_checks_passed':e['all_static_checks_passed'],'reference_entries_checked':len(e['reference_comparisons']),'criterion_plan_rows':26,'hypothetical_examples':12,'protected_files_current_and_backup_at_this_snapshot':110,'source_hashes_during_review':len(e['after_hashes']),'R6_current_query_valid':e['current_R6_query']['valid'],'source_unchanged':e['before_hashes']==e['after_hashes'],'not_video_model_or_human_performance':True},
 'source_depth':{'unique_external_sources_partially_directly_checked_across_R7_3':7,'new_full_reads_during_final_cross_reference_check':0,'existing_local_contexts':7,'independent_primary_reading':primary,'whole_public_documents_or_cited_literature_certified':False,'authors_reading_authenticated':False,'raw_public_fulltext_archived':False,'remote_content_sha256':None,'limits':'해당 지정부분의 개념 대조만. 계산·실험·라이브러리·논문 증명 전체를 재현하지 않음. 기존7참조/동일출처 재열람은 신규7연구/실험이 아님.'},
 'skill_preservation':{'custom_skills':3,'files_in_protected_list_under_custom_skill_folder':len([x for x in e['protected_files'] if x['path'].startswith('06_맞춤스킬/')]),'meaning':'3개 스킬과 공통 평가자료에 속한14파일. 14개 스킬이라는 뜻 아님.','unchanged_at_review_time':all(x['current_same'] and x['backup_same'] for x in e['protected_files'] if x['path'].startswith('06_맞춤스킬/'))},
 'actual_media_samples':0,'actual_gold_items':0,'actual_locked_groups':0,'actual_human_annotations':0,'actual_adjudications':0,'actual_model_trials':0,'actual_scores':None,'actual_alpha':None,'actual_human_content_review_performed':False,
 'remaining_gates':['적합한 실제 자료·출처/사용범위 및 사람 역할을 확보한 뒤 예비 자료와 기준답안 작성/검수','예비 관찰 뒤 표본수·오차·반복·통계법/합격선의 목적과 근거를 사용자에게 구체적 선택지+추천으로 검토','미해결 기준답안/실제 사람 의견차이/필요 내용검수를 완료로 넘기지 않음','실제 잠금 자료/운영통제·평가 구현과 실행은 후속 범위로 별도 진행'],
 'snapshot_boundary':{'current_verdict_is_pre_final_metadata_update':True,'protected_110_current_matches_at_this_snapshot':True,'announced_future_change':'부모가13_품질검수/00_R7_단계별진행안내.md를 최종현황으로 갱신할 계획. 변경전원문/old-new해시와 다른109개 불변을 별도 확인해야 하며 이 판정은 미래110개 현재불변 보증이 아님.','future_state_hash_changes':'계획/지표/조사state변경과종속ref갱신은별도시점검사필요. 과거판정/입력보존의초기해시는이력으로유지.'},
 'company_approved':False,'permission_granted':False,'R7_3_design_review_limited_complete':True,'R7_complete':False,'Phase00_complete':False,
 'evidence':[{'path':str(O/x),'sha256':sha(O/x)} for x in evidencefiles],
 'after_hashes':e['after_hashes']}
(O/'R7_03_통합_독립판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-3 평가계획 통합 독립 판정

판정: **문서설계·참조 연결 범위의 한정 완료를 지지한다. 미해결 차단 결함은 없다.**

통합5파일을 읽고 26개 준비행을 기존 품질항목과 각각 비교했다. 질문·그룹·필요근거·사람역할이 정확히 대응하고 실제 사례/정답은 모두 비어 있다. 26개 준비행과 각5개 계획조건은 실제 과제나130건 시험이 아니다. 12개 판정예도 실행하지 않은 가상 설명이며 성능 통과 건수로 세지 않는다.

정적 조건35/35, 경로·해시 참조22개 일치, 검토 시점 보호원문110개 및 backup 일치, R6 현재조회 valid, 검토 중125개 파일 해시 불변을 확인했다. 이는 문서 정합성 결과다. 앞소단계의 정적 조건과 산술 설명 검사를 합쳐 영상·모델·사람 성능으로 표시하면 안 된다.

공개7원문은 R7-3의 앞소단계에서 지정부분만 직접 대조했다. 마지막 연결검토에서 전체를 새로 읽은 것으로 계수하지 않는다. 기존7참조도 신규7개 연구나 실험이 아니다. 원문 전체·인용문헌·증명/계산·모델효과는 인증하지 않았다. 자세한 읽기범위와 URL은 JSON에 기록했다.

R7-1의 적용 필수 핵심오류·사람보류 비상쇄 정책과 R7-3의 사용자A 예비보정→다른 원본묶음 잠금확인 순서는 분리해 연결되어 있다. 누출/미해결정답/올바른보류/추출중복/모순결론/중재후초기답변조작/최고재시도선별/양측재채점/CI권한승격 반례는 앞서 검토한 정의와 충돌하지 않는다. 표본수·오차·반복수·합격선·통계법은 null로 남고 예비 뒤 근거와 사용자 검토가 필요하다.

실제 영상표본·기준답안·잠금묶음·사람초기답·중재·모델시행은 각각0이다. 실제 점수/alpha는 null이고 회사승인·권한인증·실제내용검수는 하지 않았다. 3개 맞춤 스킬과 공통자료의14파일은 검토시점 그대로다. 14개 스킬이 아니다.

이 판정은 최종 메타데이터/진행안내 갱신 전 스냅샷이다. 예정된13/00 안내1개 변경은 변경전원문 보존과 old/new해시·나머지109개 현재불변을 별도로 기록해야 한다. 이후 계획/지표/조사state 및 종속해시 변경도 별도시점 정합성 검사가 필요하다. 지금의110개 일치를 갱신 뒤의 실시간 보증으로 읽지 않는다.

R7-4 연결, R8 스킬 재평가, 01-A 구현과 전체 Phase00 완료는 이번 판정 밖이다. 실제 사람이 필요한 검수는 자료와 담당 응답을 받을 때까지 후속 대기로 유지한다.
'''
(O/'R7_03_통합_독립판정.md').write_text(md,encoding='utf-8')
for name in ['R7_03_통합_독립판정.json','R7_03_통합_독립판정.md','R7_03_통합_최종_원문대조.json','R7_03_통합_독립감사.py']:
 print(name,sha(O/name))
print('skill_file_count',j['skill_preservation']['files_in_protected_list_under_custom_skill_folder'])
