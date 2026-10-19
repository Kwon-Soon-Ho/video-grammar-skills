from pathlib import Path
import json,shutil,datetime
B=Path(__file__).resolve().parent
R=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');P=R/'Phase 01-A';N=P/'00_진행안내';A=P/'04_검증자료/01-A5b_회귀와_별도비교/2026-10-16'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
r=read(B/'result.json');i=read(B/'final-integrity.json');e=read(B/'effort-rollup.json')
assert r['stopped'] and i['primary_sealed_completed']==r['primary_completed'] and r['primary_graded']==r['primary_completed'] and not r['grading_integrity_flags']
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');snapshot=A/'최종스냅샷'/stamp
assert not snapshot.exists();snapshot.mkdir(parents=True)
for p in B.rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.json','.md','.py','.html']:
  q=snapshot/p.relative_to(B);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
report=P/'05_결과보고/17_01-A5b_고정판본_회귀와_비교시험_결과.md'
backup=A/'업데이트전'/stamp;backup.mkdir(parents=True)
for p in [N/'01-A_계획상태.json',N/'26_01-A5b_회귀와비교_현재안내.json',report]:
 if p.exists():shutil.copy2(p,backup/p.name)
report.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(B/'A5b-result-report.md',report)
d=read(N/'01-A_계획상태.json');d.update(version='1.6',state='A5b_stopped_on_with_skill_critical_error',current_stage='01-A5b',A5b_authorized=True,A5b_started=True,current_execution_stage_note='Legacy3 passed; primary6/16 completed,2 interrupted,8 not started; with-skill H02-r1 giant A misidentified as number4 triggers fixed stop policy',stage_A5b_legacy_completed=3,stage_A5b_legacy_passed=3,stage_A5b_primary_planned=16,stage_A5b_primary_dispatched=i['primary_started'],stage_A5b_primary_completed=r['primary_completed'],stage_A5b_primary_graded=r['primary_graded'],stage_A5b_primary_interrupted=len(i['primary_interrupted']),stage_A5b_primary_not_started=len(i['primary_not_started']),stage_A5b_status='stopped_failed_critical_gate',stage_A5b_report=str(report),stage_A5b_final_snapshot=str(snapshot),stage_A5b_quality_passed=False,stage_A5b_review_benefit_proved=False,default_skill_promotion=False,next_decision='User reviews A5b failure and incomplete assertion audit; no A6/01-B/02 advancement or candidate rewrite in this batch')
save(N/'01-A_계획상태.json',d)
notice=dict(stage='01-A5b',status='stopped_failed_critical_gate',date='2026-10-16',authorization='latest user A5b instruction; prospective contract stop policy applied',legacy_completed=3,legacy_passed=3,primary_planned=16,primary_started=i['primary_started'],primary_completed=r['primary_completed'],primary_graded=r['primary_graded'],primary_interrupted=i['primary_interrupted'],primary_not_started=i['primary_not_started'],stop=r['stop'],quality_passed=False,AI_review_cost_benefit_proved=False,human_review_cost_benefit_proved=False,human_gold=False,report=str(report),snapshot=str(snapshot),local_evidence_root=str(B),evidence_storage_note='Raw PNG/crops stay in the live local workspace referenced by absolute paths; JSON/Markdown/code/review viewer snapshot is archived here',measured_AI_seconds=e['measured_seconds'],human_reading_seconds=None,exact_tokens=None,exact_host_model_id=None,skill_version='0.1.0-draft.3 unchanged',promotion=False,next_stage_authorized=False,snapshot_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
save(N/'26_01-A5b_회귀와비교_현재안내.json',notice)
save(A/'최종스냅샷_현재.json',{'snapshot':str(snapshot),'report':str(report),'local_evidence_root':str(B)})
save(B/'published.json',{'report':str(report),'snapshot':str(snapshot),'state':str(N/'01-A_계획상태.json'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'report':str(report),'snapshot':str(snapshot)},ensure_ascii=False))
