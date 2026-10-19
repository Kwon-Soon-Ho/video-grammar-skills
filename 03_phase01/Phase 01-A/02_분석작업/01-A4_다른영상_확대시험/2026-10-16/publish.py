"""Publish completed A4 snapshot and verified project-local skill; no source-media mutation."""
from pathlib import Path
import json,shutil,datetime
from prepare import ROOT,sha,write
B=Path(__file__).resolve().parent
stage=ROOT/'Phase 01-A'
dest=stage/'02_분석작업/01-A4_다른영상_확대시험/2026-10-16'
current=stage/'03_분석스킬/company-video-grammar-analyzer'
state_path=stage/'00_진행안내/01-A_계획상태.json'
plan_path=ROOT/'00기획/07_Phase01-A_진행계획.md'
report_rel='Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md'
notice_rel='Phase 01-A/00_진행안내/21_01-A4_확대시험_현재안내.json'
result_rel='Phase 01-A/02_분석작업/01-A4_다른영상_확대시험/2026-10-16/result.json'
r=json.loads((B/'result.json').read_text(encoding='utf-8'))
assert r['status']=='A4_completed_with_targeted_retests'
assert r['content_issues_open']==0 and len(r['selected_results'])==7
validation=json.loads((B/'output-validation.json').read_text(encoding='utf-8'))
assert len(validation)==17 and all(not v['errors'] for v in validation)
audit=json.loads((B/'final-audit.json').read_text(encoding='utf-8'))
assert len(audit['sealed_outputs'])==17 and audit['source_hashes_unchanged']
assert not dest.exists(),'Use a new explicit snapshot rather than overwrite an existing A4 publication'
for p in (B/'skill-draft2').rglob('*'):
 if p.is_file():assert sha(p)==sha(current/p.relative_to(B/'skill-draft2')),'canonical skill changed since baseline'
backups=B/'publication-backup';backups.mkdir(exist_ok=False)
shutil.copy2(state_path,backups/'01-A_계획상태.before.json')
shutil.copy2(plan_path,backups/'07_Phase01-A_진행계획.before.md')
shutil.copytree(current,backups/'company-video-grammar-analyzer-draft2')
state=json.loads(state_path.read_text(encoding='utf-8'))
state.update(version='1.2',date='2026-10-16',state='A4_other_video_tests_and_targeted_improvements_completed',current_stage='01-A4',approved_execution_scope='A4 additional video tests, skill/no-skill comparison, fixes and affected-case retests; A5 not started',A4_started=True,stage_A4_authorized=True,stage_A4_status=r['status'],stage_A4_report=report_rel,stage_A4_current_notice=notice_rel,stage_A4_result=result_rel,stage_A4_skill_version='0.1.0-draft.3',current_skill_version='0.1.0-draft.3',company_media_opened_this_stage=5,stage_A4_registered_bundles=4,stage_A4_tasks=6,stage_A4_source_windows=7,stage_A4_initial_runs=14,stage_A4_retest_runs=3,stage_A4_content_issue_types=3,stage_A4_content_issues_open=0,stage_A4_helper_regression_tests=23,stage_A4_selected_png_count=audit['selected_png_count'],stage_A4_unique_source_times=audit['unique_source_times'],A5_started=False,numeric_thresholds=None,actual_scores=None,next_decision='Review A4 result; choose A5a numeric criteria and separate sample plan if continuing',human_content_reviews_pending=0,implementation_scope='Project-local analyzer draft3 with evidence provenance helpers; bounded A4 adapter for five registered videos',actual_media_analysis_runs_legacy_note='existing value is historical route count; A3/A4 per-case executions are recorded in stage-specific fields')
notice={'stage':'01-A4','status':r['status'],'skill_version':'0.1.0-draft.3','report':report_rel,'result':result_rel,'human_reconfirmation_required':False,'new_AI_observations_are_human_approved':False,'next_stage':'01-A5a not started','numeric_thresholds':None,'authorization_quote':'그럼 이제 다른 영상에도 이 스킬 적용해서 테스트해보자. A4로 넘어가서 누락이나 잘못 분석한 부분이 있는지 확인하고, 문제 있으면 보완해줘.','scope':'5 MP4 / 4 registered bundles / 6 tasks / 7 source windows; visual selected-frame audit, not whole-video/audio validation'}
write(B/'plan-state.after.json',state);write(B/'current-notice.json',notice)
plan='> 최신 2026-10-16: 사용자 지시로 01-A4 다른 영상 확대시험과 보완·영향 구간 재시험을 완료했습니다. 현재 스킬은 0.1.0-draft.3입니다. [A4 결과 보고](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>)와 21번 현재안내를 우선 적용합니다. A5는 미착수이며 아래 이전 상태는 이력입니다.\n\n'+plan_path.read_text(encoding='utf-8')
(B/'plan.after.md').write_text(plan,encoding='utf-8')
shutil.copytree(B,dest,ignore=shutil.ignore_patterns('__pycache__'))
copied=[]
for p in sorted(B.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts:continue
 q=dest/p.relative_to(B);expected=sha(p)
 assert sha(q)==expected,'snapshot copy mismatch'
 copied.append({'path':str(p.relative_to(B)),'sha256':expected,'size':p.stat().st_size})
for p in (B/'skill-draft3').rglob('*'):
 if p.is_file():
  q=current/p.relative_to(B/'skill-draft3');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(p)==sha(q)
shutil.copy2(B/'A4-결과보고.md',ROOT/report_rel)
write(ROOT/notice_rel,notice);write(state_path,state);plan_path.write_text(plan,encoding='utf-8')
publication={'at':datetime.datetime.now().astimezone().isoformat(),'snapshot':str(dest),'files':len(copied),'bytes':sum(x['size'] for x in copied),'snapshot_files':copied,'canonical_skill':str(current),'report':str(ROOT/report_rel),'state':str(state_path),'verified':'all copied files SHA256 matched; current skill matched draft3; prior state/plan/skill preserved','path_policy':'immutable observations retain original C workspace evidence paths; snapshot contains the same relative tree and hashes for recovery'}
write(B/'publication.json',publication);write(dest/'publication.json',publication)
print(json.dumps({k:v for k,v in publication.items() if k!='snapshot_files'},ensure_ascii=False))
