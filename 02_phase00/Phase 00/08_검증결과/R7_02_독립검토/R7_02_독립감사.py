import json,hashlib,re,sys,collections
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/';d=read(BASE/f/'품질항목_정본.json');human=read(BASE/f/'사람검수_준비목록.json');research=read(BASE/'05_출처와검토/R7_02_품질항목_조사기록.json');pres=read(BASE/'08_검증결과/R7_02_입력보존.json');written=read(BASE/'08_검증결과/R7_02_작성확인.json')
rels=list(written['output_hashes'])+['08_검증결과/R7_02_입력보존.json','08_검증결과/R7_02_작성확인.json'];before={r:sha(BASE/r) for r in rels+list(pres['protected_inputs'])};byid={r['id']:r for r in d['cards']};source={s['id']:s for s in research['sources']};mds={p.relative_to(BASE).as_posix():p.read_text(encoding='utf-8') for p in (BASE/f/'항목별기준').glob('*.md')};texts={r:(BASE/r).read_text(encoding='utf-8-sig') for r in rels if r.endswith(('.md','.json'))}
backup=BASE/'backup/2026-10-15_R7_02_초안/입력정본';protected=[{'path':r,'declared':h,'current':sha(BASE/r),'backup':sha(backup/r),'same':h==sha(BASE/r)==sha(backup/r)} for r,h in pres['protected_inputs'].items()]
checks={};checks['26_unique_cards']=len(d['cards'])==len(byid)==26;checks['7_groups_7_documents']=len({r['group'] for r in d['cards']})==len(mds)==7
required=['id','group','title','question','applies_when','required_evidence','review_method','positive_example','counterexample','valid_exception','hold_when','human_review','impact','source_refs','knowledge_refs','interpretation_origin','example_kind','company_mandatory','universal_numeric_default']
checks['all_card_fields_nonblank']=all(set(required)==set(r) and all(isinstance(r[k],str) and r[k].strip() for k in required if k not in ['human_review','source_refs','knowledge_refs','company_mandatory','universal_numeric_default']) for r in d['cards'])
checks['no_company_or_numeric_default_promotion']=all(r['company_mandatory'] is False and r['universal_numeric_default'] is None for r in d['cards']) and d['company_approved'] is False
checks['no_actual_media_or_01A']=d['actual_media_review'] is False and d['phase01a_started'] is False and written['actual_media_review'] is False and written['criteria_effectiveness_proven'] is False
checks['24_unique_sources_15external_9existing']=len(source)==24 and len([s for s in source.values() if s['kind']=='external_primary_author_or_publisher'])==15 and len([s for s in source.values() if s['kind']=='existing_project_record_not_new_external_research'])==9
checks['all_source_refs_resolve']=all(r['source_refs'] and len(set(r['source_refs']))==len(r['source_refs']) and set(r['source_refs'])<=set(source) for r in d['cards'])
local=[]
for s in research['sources']:
 if 'path' in s:local.append({'id':s['id'],'path':s['path'],'expected':s['sha256'],'actual':sha(BASE/s['path']),'same':s['sha256']==sha(BASE/s['path'])})
checks['9local_pins_match']=len(local)==9 and all(s['same'] for s in local)
checks['policy_operation_research_pin_match']=all(sha(BASE/d[k]['path'])==d[k]['sha256'] for k in ['outcome_policy_ref','operation_ref','source_catalog_ref'])
# Compare every canonical core field with the corresponding complete rendered Markdown block.
fields=['question','applies_when','required_evidence','review_method','positive_example','counterexample','valid_exception','hold_when','impact']
render=[]
for r in d['cards']:
 containing=[(path,t) for path,t in mds.items() if '## '+r['id']+' ·' in t]
 row={'id':r['id'],'exactly_one_document':len(containing)==1,'core_fields_match':False,'human_role_match':False}
 if len(containing)==1:
  path,t=containing[0];block=t.split('## '+r['id']+' ·',1)[1].split('\n## ',1)[0];row.update(path=path,core_fields_match=all(r[k] in block for k in fields),human_role_match=r['human_review']['role'] in block,source_urls_match=all(source[s].get('url',source[s].get('path','').split('/')[-1]) in block for s in r['source_refs']))
 render.append(row)
checks['all26_MD_core_fields_human_roles_match']=all(r['exactly_one_document'] and r['core_fields_match'] and r['human_role_match'] and r.get('source_urls_match') for r in render)
# Knowledge IDs are checked by identifier only; this is not a fresh full semantic review of R3.
ids=set()
def collect(v):
 if isinstance(v,dict):
  if isinstance(v.get('id'),str):ids.add(v['id'])
  for x in v.values():collect(x)
 elif isinstance(v,list):
  for x in v:collect(x)
for p in (BASE/'02_원칙과레이아웃').glob('*.json'):collect(read(p))
checks['knowledge_IDs_exist']=all(set(r['knowledge_refs'])<=ids for r in d['cards'])
checks['templates7_actual0']=len(human['templates'])==7 and human['actual_review_count']==0 and all(t['state']=='template_not_issued_no_actual_target' and t['actual_target'] is None and t['actual_answer'] is None and t['review_performed'] is False for t in human['templates'])
flat=[r for t in human['templates'] for r in t['required_input']]
checks['templates_cover26_once']=len(flat)==26 and len({x['criterion_ref'] for x in flat})==26 and {x['criterion_ref'] for x in flat}==set(byid)
checks['template_questions_evidence_hold_roles_match']=all((r['evidence'],r['role'],r['question'],r['hold'])==(byid[r['criterion_ref']]['required_evidence'],byid[r['criterion_ref']]['human_review']['role'],byid[r['criterion_ref']]['human_review']['question'],byid[r['criterion_ref']]['hold_when']) for r in flat)
checks['no_new_materials_or_reapproval_request_now']=human['new_user_answer_needed_now'] is False
checks['all94_original_and_backup_pins_match']=len(protected)==94 and all(r['same'] for r in protected)
checks['written_output_hashes_match']=all(sha(BASE/r)==h for r,h in written['output_hashes'].items())
links=[]
for r,t in texts.items():
 if not r.endswith('.md'):continue
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if not link.startswith(('https://','http://','#')):links.append({'file':r,'link':link,'exists':(BASE/r).parent.joinpath(link.split('#')[0]).resolve().is_file()})
checks['local_links_exist']=all(x['exists'] for x in links)
# Targeted semantic guards on the corrected canonical cards. This asserts wording/ranges, not measured effects.
checks['contrast_calculation_not_video_pass']='계산값·방법·가정만 기록 가능' in byid['Q-SCREEN-03']['hold_when'] and '색 계산 통과' not in byid['Q-SCREEN-03']['hold_when']
flash=byid['Q-MOTION-04'];checks['flash_loop_HDR_conditions_explicit']=all(w in flash['required_evidence'] for w in ['전 구간','최대 재생 크기','색공간/전달특성','SDR/HDR','끝→시작']) and '단회 SDR 결과를 HDR/반복본으로 승계하지 않는다' in flash['review_method'] and '후보 미검출을 비적용 이유로 쓰지 않음' in flash['hold_when']
trust=byid['Q-TRUST-01'];checks['nonspatial_exception_and_spatial_nonbypass']='spaces=[]' in trust['valid_exception'] and '공간 주장 누락을 비공간 예외로 우회하지 않음' in trust['hold_when']
checks['caption_time_precision_scope_nonbypass']='그 정밀도/범위' in byid['Q-CAP-02']['hold_when'] and 'R4 필수값/검사 우회는 금지' in byid['Q-CAP-02']['hold_when']
checks['missing_caption_requirement_not_NA']='자막이 없다는 이유만으로 비적용 처리하지 않음' in byid['Q-CAP-01']['hold_when']
checks['unsupported_intent_absence_not_generalized']='부분 표본의 부재를 전 구간 부재로' in byid['Q-TRUST-02']['review_method']
checks['source_transcription_vs_correction_separate']='원문 전사와 제작용 수정 제안' in byid['Q-INFO-02']['review_method']
checks['units_value_and_punctuation_ambiguity_hold']='소수 구분이 모호' in byid['Q-TEXT-02']['hold_when'] and 'SI식으로 자동 덮어쓰지 않음' in byid['Q-TEXT-02']['valid_exception']
checks['no_card_or_linear_motion_blanket_ban']='카드·대칭·표·정형 구도도 내용에 맞으면 가능' in byid['Q-SCREEN-02']['valid_exception'] and '등속·정지·절제된 모션' in byid['Q-MOTION-03']['valid_exception']
checks['CI_latest_not_usage_approval']='최신성 확인은 배포·세부가이드 승인 아님' in byid['Q-BRAND-01']['impact'] and '공식CI색으로 복사' in byid['Q-BRAND-02']['counterexample']
sys.path.insert(0,str(BASE/'07_실행도구'));import R6_통합조회 as q
r6=q.inspect(BASE);checks['current_R6_query_valid']=r6['valid'] is True
skills={p.relative_to(BASE).as_posix():sha(p) for p in (BASE/'06_맞춤스킬').rglob('*') if p.is_file()};baseline=json.loads((OUT.parent/'R6_독립검토/R6_04_최종판정.json').read_text(encoding='utf-8'))['after_hashes'];checks['existing14_skill_files_preserved']=len(skills)==14 and all(baseline.get(r)==h for r,h in skills.items())
after={r:sha(BASE/r) for r in before};checks['source_unchanged_during_audit']=before==after
result={'scope':'R7-2 static canonical/render/template/source-pin/current-reference checks. Counts are audit conditions, not video trials or efficacy metrics.','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'protected_files':protected,'local_source_pins':local,'MD_card_comparison':render,'template_item_count':len(flat),'current_R6_query':r6,'links':links,'skill_hashes':skills,'actual_video_analyzed':False,'actual_human_content_review_performed':False,'criteria_effectiveness_proven':False,'before_hashes':before,'after_hashes':after}
(OUT/'R7_02_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failures':[k for k,v in checks.items() if not v],'after_hash_count':len(after)},ensure_ascii=True))
