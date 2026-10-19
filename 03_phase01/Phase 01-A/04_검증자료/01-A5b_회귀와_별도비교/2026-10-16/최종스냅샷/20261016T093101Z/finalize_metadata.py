from pathlib import Path
import json,datetime
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
save(B/'blind/H02-r1/timing-supplement.json',{'source':'independent grader reported clock end of metadata save 09:28:39 UTC; first grading saved 09:28:13','first_content_saved_seconds':239,'metadata_completion_utc':'2026-10-16T09:28:39Z','total_review_seconds_including_metadata':265,'operational_180_second_overrun':85,'first_grading_unchanged':True,'new_content_exploration_after_09_25_25':False})
save(B/'critical-confirmation.json',{'reviewer':'root AI after blind alert; unblinded; not human approval','start_clock_utc':'2026-10-16T09:24:47Z','end_clock_utc':'2026-10-16T09:25:05Z','elapsed_seconds':18,'source':'recorded tools.clock UTC before native evidence reinspection and STOP creation','file_read':str(B/'blind/H02-r1/sample-A/evidence/evidence-001.png'),'finding':'Giant glyph A, not numeral4; definite wrong target identity changes reconstruction object','critical_contract_basis':'target confusion','action':'STOP.json then notify both active analyses; preserve first observations','original_grade_unchanged':True})
d=read(B/'execution-ledger.json');d.update(primary_completed=6,primary_graded=6,primary_interrupted=['H02-r2-with_skill','H02-r2-without_skill'],primary_not_started=8,status='stopped_on_critical_error',stop_record='STOP.json',finalized_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save(B/'execution-ledger.json',d)
