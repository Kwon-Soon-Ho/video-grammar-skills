import json,hashlib,re,sys,importlib.util
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
docs=['09_다음단계인계/'+n for n in ['R7_00_현재인계안내.md','R7_R8_스킬재구성_인계.md','R7_01-A_구현전_인계.md','R7_사람판단과_남은준비.md']];a,b,c,d=[(B/r).read_text(encoding='utf-8') for r in docs]
regpath='00_운영계약/정본과표시_연결목록.json';verpath='05_출처와검토/버전목록.json';reportpath='08_검증결과/R7_04_03_등록확인.json';source=read(B/'08_검증결과/R7_04_01_입력보존.json')['source_hashes'];backup=B/'backup/2026-10-15_R7_04_1_현행대조/입력정본';reg=read(B/regpath);ver=read(B/verpath);oldreg=read(backup/regpath);oldver=read(backup/verpath);w=read(B/reportpath);added=w['added_entries'];rels=set(docs+[regpath,verpath,reportpath,'08_검증결과/R7_04_01_02_단계보고.md'])|set(source)|{e['path'] for e in added}|{'07_실행도구/R7_연결확인.py','13_품질검수/연결과인계/現在연결_입력고정.json'.replace('現在','현재'),'13_품질검수/연결과인계/품질검수_작성양식.json'};status_paths={'00_시작안내.md','01_진행현황.md','09_다음단계인계/00_인계안내.md','13_품질검수/연결과인계/00_R7-4_진행안내.md'};rels|=status_paths;before={r:sha(B/r) for r in rels}
originals=[{'path':r,'expected_sha256':h,'backup_same':sha(backup/r)==h,'current_same':sha(B/r)==h,'current_sha256':sha(B/r)} for r,h in source.items()];changed={x['path'] for x in originals if not x['current_same']}
registration_checks=[]
for item in added:
 obj=read(B/item['path']);r=[x for x in reg['canonical_entries'] if (x['id'],x['version'])==(item['id'],item['version'])];v=[x for x in ver['entries'] if (x['id'],x['version'])==(item['id'],item['version'])]
 registration_checks.append({'id':item['id'],'version':item['version'],'path':item['path'],'file_identity_same':(obj['id'],obj['version'])==(item['id'],item['version']),'hash_same':sha(B/item['path'])==item['sha256'],'one_reg_and_version':len(r)==len(v)==1,'reg_same':len(r)==1 and all(r[0][k]==item[k] for k in item),'version_same':len(v)==1 and all(v[0][k]==item[k] for k in item),'planning_reference_not_company_approval':len(v)==1 and v[0]['company_approved'] is False and 'not_actual_quality_approval' in v[0]['state']})
all_entries=[]
for collection in [reg['canonical_entries'],ver['entries']]:
 for item in collection:all_entries.append({'id':item['id'],'version':item['version'],'path':item['path'],'sha_matches':sha(B/item['path'])==item['sha256']})
links=[]
for rel,t in zip(docs,[a,b,c,d]):
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if not link.startswith(('http:','https:','#')):links.append({'source':rel,'link':link,'exists':((B/rel).parent/link).resolve().is_file()})
plan=read(B/'13_품질검수/평가계획/평가설계_정본.json');form=read(B/'13_품질검수/연결과인계/품질검수_작성양식.json');manifest=read(B/'13_품질검수/연결과인계/현재연결_입력고정.json')
checks={
 '130_original_bytes_in_backup':len(originals)==130 and all(x['backup_same'] for x in originals),
 'only_two_registries_changed_of_original130':changed=={regpath,verpath},
 '128_current_originals_unchanged':sum(x['current_same'] for x in originals)==128,
 'future_status_update_paths_hashes_tracked':status_paths<=set(before),
 'registration_envelope_versions':reg['version']=='0.3.15' and ver['version']=='0.1.11',
 'prior_canonical_entries_order_and_content_exact':reg['canonical_entries'][:len(oldreg['canonical_entries'])]==oldreg['canonical_entries'],
 'prior_version_entries_order_and_content_exact':ver['entries'][:len(oldver['entries'])]==oldver['entries'],
 'exact_13_entries_added_both':len(added)==13 and len(reg['canonical_entries'])-len(oldreg['canonical_entries'])==13 and len(ver['entries'])-len(oldver['entries'])==13,
 'all_13_id_version_path_hash_real_files_match':all(all(x[k] for k in ['file_identity_same','hash_same','one_reg_and_version','reg_same','version_same','planning_reference_not_company_approval']) for x in registration_checks),
 'all_current_and_historical_registration_hashes_match':all(x['sha_matches'] for x in all_entries),
 'registration_identity_version_pairs_unique':all(len(x)==len({(e['id'],e['version']) for e in x}) for x in [reg['canonical_entries'],ver['entries']]),
 'manual_guide_order_history_preserved':reg['manual_guides'][:len(oldreg['manual_guides'])]==oldreg['manual_guides'],
 'new_R7_guides_manual_not_generated':all(r in reg['manual_guides'] for r in docs) and reg['display_groups']==oldreg['display_groups'],
 'local_handoff_links_exist':all(x['exists'] for x in links),
 'current_vs_historical_reading_order':'시작 안내/진행 현황을 우선' in a and '과거 단계 보고서는 그 시점의 이력' in a,
 '26_conditional_no_total':'26항목은 목적에 따라 적용' in a and '단일 품질 총점은 없다' in a,
 'registration_not_company_approval':'등록이 회사 승인은 아님' in a,
 'R8_plan_not_performed_and_three_skills':'스킬 수정·재평가는 아직 하지 않았다' in b and all(x in b for x in ['video-knowledge-curator','video-record-steward','video-guidance-reviewer']),
 'existing_A_draft_pilot_authority_preserved':'소량 시범 승인 A안은 유지' in b and '같은 사항을 재승인받지 않는다' in d,
 'Anthropic_creator_current_instruction_separate_copy':'Anthropic Skill Creator의 현행 지침을 읽고 별도 작업 사본' in b,
 'source_license_dependencies_review_before_transfer':'코드·의존성·라이선스' in b and '정적 검토/다운로드는 코드 실행이나 효과 검증이 아니다' in b,
 'intermediate_review_and_new_judgment_four_options':'초안→중간 목적 검토→테스트→레드팀→보완' in b and '최소4지선다와 추천안' in b,
 'R8_write_scope_backups_failure_recovery_tests':'허용 파일 외 변경, 로그/backup/diff·복구, 검사 실패 후 중단' in b,
 'no_past_scores_as_new_effect':'11/12 동률' in b and '새 R4/R6/R7 호환' in b,
 '01A_not_started_and_Phase00_first':'01-A 구현·모델/API 호출·실제 영상 분석은 미실시' in c and '남은 R8과 최종 정리를 먼저' in c,
 'first_small_sample_not_statistically_sufficient':'성능 검증에 충분한 표본 수나 잠금 묶음 확보를 뜻하지 않는다' in c,
 'scenario_unknown_not_fabricated':'시나리오가 없거나 불일치하면' in c and '의도·시간표를 새로 꾸미지 않는다' in c,
 'external_model_handling_conditions_and_no_manual_PTS_required':'자료별 외부 모델 처리 가능 여부' in c and 'PTS·해시·OCR·좌표를 수작업으로 만들 필요는 없다' in c,
 'current_R4_R5_R6_and_unit_contracts_preserved':'픽셀 경계 원점' in c and '지원 범위를 넘는 공간 주장의 보류 유지' in c and '선택형UI' in c,
 'gold_leakage_both_candidates_and_solo_limits':'미노출 검증 자료라고 부르지 않는다' in c and '후보 양쪽을 같은 새 정답으로 재채점' in c and '단독 검토' in c,
 'actual_counts_zero_and_numeric_null':all(v==0 for v in plan['actual_counts'].values()) and all(v is None for v in plan['numeric_decisions'].values()) and plan['actual_scores'] is None,
 '01B_company_grammar_02_creation_separate':'회사 공통 문법 추출·승인은01-B' in c and '새 기획/창작은02' in c,
 'new_R7_requests_zero_vs_CI_reply1':'실제 검수 요청을 접수한 대장이 아니라' in d and '기존 R6 CI 최신성 실제 회신1건과 구분' in d,
 'human_questions_conditional_not_global_block':'안 쓰는 자산 때문에 전체 일괄 차단하지 않음' in d and '실제 내용 담당자' in d,
 'content_free_response_and_policy_four_choices':'자유 서술과 근거' in d and '운영 방식의 판단에는 최소4지선다·추천안' in d,
 'unknown_partial_retraction_and_no_fake_intake':'부분 확인/모름/기권·정정/철회' in d and 'R6 새 접수/회신이나 회사 승인이 생기지 않는다' in d,
 'three_skills_common14files_preserved':len([r for r in source if r.startswith('06_맞춤스킬/')])==14 and all(sha(B/r)==h for r,h in source.items() if r.startswith('06_맞춤스킬/')),
 'stage2_frozen_code_manifest_form_unchanged':all(sha(B/r)==h for r,h in read(O/'R7_04_02_최종판정.json')['after_hashes'].items() if r in ['07_실행도구/R7_연결확인.py','13_품질검수/연결과인계/현재연결_입력고정.json','13_품질검수/연결과인계/품질검수_작성양식.json']),
 'new_registration_report_no_actual_activity':all(w[k] is False for k in ['actual_media_analysis','actual_human_content_review','R8_skills_rebuilt','phase01a_started']),
}
sys.path.insert(0,str(B/'07_실행도구'));import R7_연결확인 as r7;import R6_통합조회 as r6
q7=r7.inspect(B);q6=r6.inspect(B);checks['R7_current_check_valid']=q7['valid'];checks['R6_separate_current_query_valid']=q6['valid'];checks['actual_CI8_latest_guide8_unresolved_not_approval']=q6['recorded_answer_count']==1 and len(q6['companies'])==8 and all(x['latest_materials']=='user_statement_recorded' and x['additional_ci_guide']=='unresolved' and x['official_screen_color_or_usage_approval'] is False for x in q6['companies']);after={r:sha(B/r) for r in before};checks['review_sources_unchanged']=after==before
snap=O/'R7_04_03_검토시점원문'
for r in docs+[regpath,verpath,reportpath]+sorted(status_paths):
 dest=snap/r;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((B/r).read_bytes())
result={'scope':'R7-4-3 인계/등록 정적독립검토.기존원문바이트/선택참조와사람경계확인; 실제영상/스킬/모델실행아님','static_conditions':len(checks),'static_passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'registration_rows':registration_checks,'all_current_historical_registration_rows':all_entries,'original130':originals,'links':links,'R7_readonly_current':q7,'R6_separate_current_query':q6,'before_hashes':before,'after_hashes':after}
(O/'R7_04_03_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'all_registry_rows':len(all_entries),'hashcount':len(after)}))


