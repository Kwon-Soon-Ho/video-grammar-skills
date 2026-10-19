from pathlib import Path
import json,shutil,hashlib,datetime
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['evidence_catalog.py','check_observations.py']:
 dest=B/'common-tools'/name;dest.parent.mkdir(exist_ok=True);shutil.copy2(B/'candidate/company-video-grammar-analyzer/scripts'/name,dest)
for r in read(B/'run-matrix.json'):
 c=read(B/'inputs'/f"{r['case_id']}.json");d=B/'trials'/r['run_id'];(d/'outputs').mkdir(parents=True,exist_ok=True);(d/'support').mkdir(exist_ok=True)
 c.update(run_id=r['run_id'],output_dir=str(d/'outputs'),wall_minutes_max=15,native_crop_max=40,adaptive_rounds_max=2,adaptive_selected_per_round_max=24,adaptive_selected_total_max=48)
 c['document_text']=str(B.parent/'phase01a-docreview/본문/DOC064.txt') if c['document_id'] else None
 c['document_mode']='provided_draft_script_production_status_unverified' if c['document_id'] else 'none'
 save(d/'input.json',c)
 save(d/'eval_metadata.json',{'eval_id':int(c['case_id'][1:]),'eval_name':r['run_id'],'prompt':(B/'common-task.md').read_text(encoding='utf-8'),'assertions':[]})
pins={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'trial_tools.py',B/'trial-instructions.md',B/'common-task.md',B/'common-output-format.md',*list((B/'common-tools').glob('*.py'))]}
save(B/'trial-harness-pins.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':pins,'before_any_primary_output':True,'both_conditions_same_IO_helpers':True})
print('16 empty trial folders configured; zero primary runs launched')
