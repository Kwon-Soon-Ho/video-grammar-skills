import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=read(O/'R7_04_02_최종_독립반례결과.json');s=read(O/'R7_04_02_최종_정적대조.json');allhash=dict(e['after_hashes']);allhash.update(s['after_hashes']);same=all(e['after_hashes'][r]==s['after_hashes'][r] for r in set(e['after_hashes'])&set(s['after_hashes']))
artifacts=['R7_04_02_초기_독립반례코드.py','R7_04_02_초기_독립반례결과.json','R7_04_02_추가반례.py','R7_04_02_추가초기_독립반례결과.json','R7_04_02_초기_발견사항.json','R7_04_02_초기원문_복구.py','R7_04_02_초기원문_복구증거.json','R7_04_02_추가_발견사항.json','R7_04_02_CLI_인코딩반례.py','R7_04_02_CLI_인코딩_초기반례.json','R7_04_02_최종_독립반례코드.py','R7_04_02_최종_독립반례결과.json','R7_04_02_정적감사.py','R7_04_02_최종_정적대조.json']
findings=[{'id':'F1','fixed':True,'area':'빈양식 구조계약','initial':'필수inventory키/전체blank키 삭제·정책빈값/필수검수누락허용·회사승인outcome·bool건수가 메모리구조검사에 통과','fix':'29blank키 정확집합·목록4개[]/나머지null·규칙키/True/판정진행목록 고정·건수 strict int0','boundary':'실제파일변경은초기에도고정해시에서차단; 메모리parse반환결함은해시우회가아님'}, {'id':'F2','fixed':True,'area':'연결표 종류/예시범위/필드목록','initial':'map.kind/소스data_scope 승격·22binding전부제거·bool건수 통과','fix':'kind/source별scope 고정·22bindingID집합·중복/빈후보 차단·strict int0','boundary':'필드경로존재확인은실제관측내용·의미·권한검수가아님'}, {'id':'F3','fixed':True,'area':'R7-1최소기록과양식연결','initial':'판단방법/담당역할 기록칸 없음','fix':'양식v0.1.1 review_method/reviewer_role null추가·사용안내에역할선언≠신원인증 명시'}, {'id':'F4','fixed':True,'area':'Windows CLI 진단출력','initial':'cp949+없는emoji경로→UnicodeEncodeError/JSON미출력','fix':'ensure_ascii=True·현재exit1/구조화JSON오류확인; 입력원문정규화없음'}]
j={'stage':'R7-4-2 별도연결표/빈양식/읽기전용기반확인도구','limited_completion_supported':e['passed']==e['conditions'] and s['all_static_checks_passed'] and same,'unresolved_blocking_findings':[],'findings_fixed':findings,
 'scope':{'included':['현재입력문맥v0.1.3/130pins·22binding/26항목·양식v0.1.1/29필드·03규칙/04안내','D정상읽기·C바이트사본원문/manifest변경거절·메모리구조분기반례·CLI/parser/시작끝변경감지','기존필드/스키마구조와현재canon항목/최소판정기록의의미경계대조'],
 'excluded':['R6livequery와선언문맥검사·실제R4/R5/R7기록구조/참조/의미검사','실제영상분석·품질/성능평가·사람내용검수·신원/회사/권한인증','3단계정본등록/인계문서·R8스킬재구성/평가·01-A·전체Phase00완료']},
 'verification':{'independent_conditions':e['conditions'],'independent_passed':e['passed'],'runtime_exceptions':e['runtime_exceptions'],'static_document_conditions':s['static_conditions'],'static_document_passed':s['static_passed'],'existing130_inputs_unchanged':s['checks']['existing130_inputs_unchanged'],'D_before_after_in_independent_test_same':e['D_sources_unchanged'],'D_static_before_after_same':s['checks']['review_sources_unchanged'],'overlapping_test_and_static_hashes_same':same,'after_hash_count':len(allhash),'no_performance_or_actual_media_trial_counts':True},
 'method_limits':{'C_copies_no_manifest_rebaseline':True,'D_input_writes':False,'memory_fault_method':'parse返値だけに改変JSONを差し込む'.replace('parse返値だけに改変JSONを差し込む','parse返却値だけ'.replace('parse返却値だけ','parseの返却値のみ')).replace('parseの返却値のみ','元バイト/ハッシュはそのままのparse戻り値だけを差し替える').replace('元バイト/ハッシュはそのままのparse戻り値だけを差し替える','원문bytes/해시는그대로두고parse반환객체만결함주입해구조검사분기를검증'),'memory_fault_not_real_hash_bypass':True,'start_end_change_detection_checked':True,'atomic_snapshot_or_signature_guaranteed':False,'actual_content_correctness_tested':False},
 'initial_evidence':{'initial_conditions':45,'initial_passed':39,'additional_initial_structure_cases':4,'additional_initial_passed':0,'initial_structure_misses_preserved':10,'v012_65_of_65_history_preserved':True,'minimum_method_role_gap_and_CLI_encoding_failure_preserved':True,'exact_initial_code_manifest_recovered_from_matching_backup':True,'mixed_snapshot_kept_with_hash_mismatch_annotations':'R7_04_02_초기후보원문은보완중간본2개가혼합되어원문복구증거에따라정확초기후보2개를별도보존. 초기성적/혼합본을조용히수정하지않음'},
 'human_boundary':{'actual_new_R7_content_reviews':0,'actual_human_content_review_performed':False,'reviewer_role_is_declaration_not_identity_authentication':True,'CI_reply_reused_as_R7_approval':False,'R4_spatial_supported_unlocked':False,'actual_video_analyzed':False,'company_approved':False,'permission_granted':False},
 'source_depth':'03/04안내전문·양식/도구전문과22실제key_path/26정본문구대조.130보존은hash검사이며130파일전체의새의미정독/내용진실성확인이아님.이번외부이론조사없음.',
 'remaining_gates':['실제검수기록은빈템플릿사본을작성한뒤대상/버전·기존기록검사·구체사람내용검수를별도로거쳐야함','현재R6선언/회신문맥은R6통합조회로별도확인;R7도구valid로대체금지','등록/현재읽는순서/R8/01-A/사람준비인계는3단계에서별도검토'],
 'archive_guidance':{'must_keep':'초기/추가실패·v01265이력·정확초기원문복구증거·최종코드/68결과/정적26결과/판정·최종후보원문6개.혼합보존본은hash불일치주석과함께유지.','temporary_whole_foundation_copies':'TemporaryDirectory로만든130파일실행사본은자동삭제되어아카이브할잔여임시폴더없음.','unnecessary_to_archive_for_reproduction':['R7_04_02_최종코드작성.py','R7_04_02_68조건_코드작성.py','R7_04_02_발견저장.py','R7_04_02_추가발견저장.py','R7_04_02_판정저장.py'],'note':'생성보조코드는선택제외가능하나실제로실행한반례/정적감사코드와그결과는제외하지않음.무관한workspace전체/임시실행캐시를포괄복사하지않음.'},
 'R7_4_complete':False,'R7_complete':False,'Phase00_complete':False,'evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in artifacts],'after_hashes':allhash}
(O/'R7_04_02_최종판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-4 2단계 독립 판정

**연결 설계·빈 양식·읽기전용 기반 확인 범위에 한정해 완료를 지지한다. 차단 결함은 보완됐으며 남은 차단사항은 없다.**

최종 문맥은v0.1.3, 고정파일130개·필드22개·품질항목26개, 빈 양식은v0.1.1의29필드다. 독립 구조·고정파일·파서·CLI·변경시점 조건68/68, 문서/의미경계 정적 조건26/26이며 예외0이다. 두 검사 숫자는 영상/모델 성능으로 합산하지 않는다. 기존130파일과3개 맞춤스킬/공통자료14파일은 그대로이고 검토 동안 D파일도 바뀌지 않았다.

초기에45조건 중39개와 추가4조건에서 구조 미검출10개를 확인했다. 고정해시를 유지한 실제 C사본의 변조는 모두 차단됐다. 미검출10개는 원문bytes/해시를 바꾸지 않고 parse반환값에만 결함을 넣은 별도구조검사이므로 해시 우회 공격으로 과장하지 않는다. 보완판은 필수양식키·정책상수·판정목록·strict건수, 연결표kind/source범위·22binding집합을 확인한다.

그 뒤 R7-1이 요구하는 판단방법/담당역할 빈칸 누락과 cp949콘솔의emoji오류경로 JSON출력 실패를 추가 확인했다. review_method/reviewer_role을 추가하고 역할선언은 신원인증이 아님을 명시했다. CLI는 입력을 정규화하지 않고 JSON escape출력으로 오류를 보존한다. 최종68조건은 이 보완과 정상입력/순서변경/emoji설명 양성대조까지 재검사했다.

22개 경로는 기존 R4/R5합성예와 R6실제대장에 존재하고, 26개 항목의 근거·보류·사람역할은 정본과 일치한다. 필드후보를 모든 검수의 필수목록으로 강제하지 않는다. 미검수/보류/비적용·필수선정·부분범위·동일원인과항목영향/지표분모·변경후재검토가 분리돼 있다. 기존 CI회신을 새 R7품질승인에 옮기거나 R4spatial supported보류를 우회하지 않는다.

이 도구는 R6live선언문맥, 실제R4/R5/R7기록, 영상, 사람내용·신원·회사/사용권한을 검사하지 않는다. 시작/종료 읽기비교는 확인했지만 원자적snapshot·전자서명·악의적인코드/manifest동시교체 인증은 아니다. 저장JSON은 생성시점사본으로만 읽는다. 실제내용검수는0건이며 후속 담당 검수를 완료로 넘기지 않았다.

초기10미검출·추가내용/CLI실패·v0.1.2의65통과이력과 정확한초기코드/manifest를 보존했다. 초기원문보존시점에 보완중간본2개가 섞였던 사실도 SHA로 남기고 변경전backup에서 초기성적hash와 같은2개를 별도로 보존했다. 최종판정JSON에 원문/코드/결과hash가 있다.

3단계의 등록/읽는순서·R8/01-A/사람준비 인계는 아직 별도검수 대상이다. 실행용130파일 C임시사본은 자동삭제되어 보존할잔여폴더가 없다. 아카이브에는 실제검사코드·실패/최종결과·원문/복구증거를 남기고 생성보조스크립트/무관한workspace·임시캐시는 제외해도 된다.
'''
(O/'R7_04_02_최종판정.md').write_text(md,encoding='utf-8')
for n in ['R7_04_02_최종판정.json','R7_04_02_최종판정.md','R7_04_02_최종_독립반례결과.json','R7_04_02_최종_독립반례코드.py','R7_04_02_최종_정적대조.json','R7_04_02_정적감사.py']:print(n.encode('unicode_escape').decode(),sha(O/n))
print('after_hash_count',len(allhash))
