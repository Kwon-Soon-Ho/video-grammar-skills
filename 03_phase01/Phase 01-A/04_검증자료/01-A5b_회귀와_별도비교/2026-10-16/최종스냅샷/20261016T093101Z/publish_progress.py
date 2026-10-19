from pathlib import Path
import json,shutil,datetime
B=Path(__file__).resolve().parent;R=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');P=R/'Phase 01-A';N=P/'00_진행안내';A=P/'04_검증자료/01-A5b_회귀와_별도비교/2026-10-16'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');backup=A/'업데이트전'/stamp
paths=[N/'01-A_계획상태.json',N/'26_01-A5b_회귀와비교_현재안내.json']
for p in paths:
 if p.exists():backup.mkdir(parents=True,exist_ok=True);shutil.copy2(p,backup/p.name)
d=read(paths[0]);d.update(version='1.5',state='A5b_comparison_running_after_3_regression_pass',current_stage='01-A5b',A5b_started=True,A5b_authorized=True,A5_experiment_started=True,approved_execution_scope='User authorized A5b: three known-case regressions, if passed 16 frozen skill/no-skill comparisons; stop policy and resource caps unchanged',current_execution_stage_note='A5b legacy3 passed;57-atom AI reference independently audited and sealed before first primary answer; comparison running',next_decision='Review A5b actual results; no A6/default promotion yet',stage_A5b_current_notice='Phase 01-A/00_진행안내/26_01-A5b_회귀와비교_현재안내.json',stage_A5b_artifacts='Phase 01-A/04_검증자료/01-A5b_회귀와_별도비교/2026-10-16',stage_A5b_skill_version='0.1.0-draft.3',stage_A5b_legacy_completed=3,stage_A5b_legacy_passed=3,stage_A5b_primary_planned=16,stage_A5b_primary_dispatched=2,stage_A5b_primary_completed=0,stage_A5b_reference_atoms=57,stage_A5b_reference_human_gold=False,stage_A5b_report=None,default_skill_promotion=False)
notice={'date':'2026-10-16','stage':'01-A5b','status':'running','authorization':'latest user A5b instruction','contract_unchanged':'25_01-A5a_평가실행계약.md','legacy_passed':3,'legacy_total':3,'legacy_non_gating_residual_detail_omissions':1,'primary_planned':16,'primary_dispatched_at_snapshot':2,'primary_completed_at_snapshot':0,'reference_sealed':True,'reference_atoms':57,'reference_human_gold':False,'local_live_workspace':str(B),'later_outputs_are_AI_observations_not_user_approvals':True,'model_settings':'parent inherited; exact host ID unavailable; no switch','A6_or_01B_or_02_authorized':False,'snapshot_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
save(paths[0],d);save(paths[1],notice)
for name in ['execution-start.json','execution-ledger.json','legacy-decision.json','legacy-criteria.json','candidate-pins.json','preservation-check.json']:
 A.mkdir(parents=True,exist_ok=True);shutil.copy2(B/name,A/name)
for name in ['reference.json','seal.json','audit.json','audit.md']:
 (A/'reference').mkdir(exist_ok=True);shutil.copy2(B/'reference'/name,A/'reference'/name)
print('A5b progress and state published; historical A5a/A1-A4 untouched')
