import json,hashlib,re,importlib.util
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f='13_품질검수/연결과인계/';rels=['07_실행도구/R7_연결확인.py']+[f+n for n in ['기존기록_연결표.json','품질검수_작성양식.json','03_검수와보류_연결규칙.md','현재연결_입력고정.json','04_연결확인_사용안내.md']];source=read(B/'08_검증결과/R7_04_01_입력보존.json')['source_hashes'];before={r:sha(B/r) for r in set(rels)|set(source)}
fm=read(B/rels[1]);form=read(B/rels[2]);rule=(B/rels[3]).read_text(encoding='utf-8');m=read(B/rels[4]);guide=(B/rels[5]).read_text(encoding='utf-8');code=(B/rels[0]).read_text(encoding='utf-8');criteria=read(B/'13_품질검수/품질항목_정본.json');cards={c['id']:c for c in criteria['cards']};cr=[];fields=[]
for x in fm['criteria_links']:
 c=cards[x['criterion_ref']];cr.append({'id':x['criterion_ref'],'same_evidence_and_hold_and_role':(x['group'],x['required_evidence'],x['hold_when'],x['human_role'])==(c['group'],c['required_evidence'],c['hold_when'],c['human_review']['role'])})
for x in fm['bindings']:
 value=read(B/x['structure_reference'])
 for k in x['key_path']:value=value[k]
 fields.append({'id':x['id'],'path':x['structure_reference'],'key_path':x['key_path'],'value_type':type(value).__name__,'hash_same':sha(B/x['structure_reference'])==x['structure_reference_sha256'],'not_actual_evidence':x['actual_evidence'] is False})
links=[]
for r,t in [(rels[3],rule),(rels[5],guide)]:
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if not link.startswith(('http:','https:','#')):links.append({'source':r,'link':link,'exists':((B/r).parent/link).resolve().is_file()})
checks={
 'existing130_inputs_unchanged':len(source)==130 and all(sha(B/r)==h for r,h in source.items()),
 'three_custom_skills_common14files_unchanged':len([r for r in source if r.startswith('06_맞춤스킬/')])==14 and all(sha(B/r)==h for r,h in source.items() if r.startswith('06_맞춤스킬/')),
 'manifest_v013_130pins_current':m['version']=='0.1.3' and len(m['pins'])==130 and all(sha(B/x['path'])==x['sha256'] for x in m['pins']),
 '22_actual_field_paths_exist_but_not_actual_evidence':len(fields)==22 and all(x['hash_same'] and x['not_actual_evidence'] for x in fields),
 '26_criteria_exact_canonical_text_connection':len(cr)==26 and all(x['same_evidence_and_hold_and_role'] for x in cr),
 'all_actual_mapping_fields_empty':all(x['actual_target_ref'] is None and x['actual_evidence_refs']==[] and x['actual_review_result'] is None for x in fm['criteria_links']),
 'form_v011_and29_keys':form['version']=='0.1.1' and len(form['blank_fields'])==29,
 'R71_method_role_minimum_now_in_template':form['blank_fields']['review_method'] is None and form['blank_fields']['reviewer_role'] is None,
 'role_declaration_not_identity_authentication':'개인신원' in guide.replace(' ','') and 'review_method' in guide and 'reviewer_role' in guide,
 'required_inventory_before_results_and_partial_scope':'필수 항목 목록을 결과를 보기 전에' in rule and '부분 결과로 표시' in rule,
 'conditional_time_coordinates_not_universal':'문서 전사·비공간 주장의 비적용과 실제 공간 주장 누락을 구분' in rule,
 'CI_reply_not_new_R7_review':'기존 CI 질문으로 대신하지 않음' in json.dumps(fm,ensure_ascii=False) and '자동 이식하지 않는다' in rule,
 'human_partial_correction_withdrawal_preserved':'미확인/기권·부분확인/정정/철회' in rule,
 'spatial_hold_not_bypassed_by_human_reply':'사람 답변으로 우회 해제하지 않는다' in rule,
 'mandatory_unreviewed_hold_and_no_total_offset':'목적의 필수 오류/미검수/사람 대기' in rule and '단일 품질 총점·핵심 오류 상쇄' in rule,
 'irrelevant_unknowns_not_global_block':'관계없는 미정을 전체 차단으로 확대하지 않는다' in rule,
 'same_cause_impact_not_merged_automatically':'원인 불명확 시 자동 병합하지 않는다' in rule and '각 위치/항목의 영향은 유지' in rule,
 'metric_denominators_not_changed_by_cause_group':'분모를 사후에 원인 그룹으로 바꿔 점수를 높이지 않는다' in rule,
 'changes_stale_not_silent_reuse_or_repin':'옛 참조는 재검토 대상' in rule and 'manifest를 다시 만들어 어긋남을 숨기지 않는다' in rule,
 'four_scopes_separate_no_R6_live_or_actual_inspection':'이 네 범위를 하나의 valid나 승인으로 합치지 않는다' in rule and 'r6_live_query_executed' in guide,
 'storage_snapshot_not_current_and_no_signature_claim':'작성 시점의 기록' in guide and '전자서명이나 외부 신뢰 기준이 아니다' in guide,
 'bounded_read_nonatomic_documented':'8 MiB' in guide and '100' in guide and '원자적 파일 묶음 읽기를 보장하지는 않는다' in guide,
 'no_future_actual_record_validator_claim':'실제 검수 결과를 검사하는 기능은 없다' in guide,
 'local_links_exist':all(x['exists'] for x in links),
 'CLI_escaped_output_no_source_normalization':'ensure_ascii=True' in code,
}
after={r:sha(B/r) for r in before};checks['review_sources_unchanged']=before==after
snapshot=O/'R7_04_02_최종후보원문'
for r in rels:
 d=snapshot/r;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes((B/r).read_bytes())
result={'scope':'R7-4-2 문서/의미경계·구조위치 정적대조, 전체파일 의미정독 인증아님','static_conditions':len(checks),'static_passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'field_paths':fields,'criterion_links':cr,'links':links,'before_hashes':before,'after_hashes':after}
(O/'R7_04_02_최종_정적대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'hashes':len(after)}))
