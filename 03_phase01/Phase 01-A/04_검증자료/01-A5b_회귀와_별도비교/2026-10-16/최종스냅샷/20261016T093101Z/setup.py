from pathlib import Path
import sys,json,hashlib,shutil,datetime
B=Path(__file__).resolve().parent;W=B.parent;A=W/'phase01a-a5a'
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for v in iter(lambda:f.read(1024*1024),b''):h.update(v)
 return h.hexdigest()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
pins=json.loads((A/'candidate-pins.json').read_text(encoding='utf-8'))
for f in pins['snapshot_files']:
 assert sha(A/'candidate/company-video-grammar-analyzer'/f['relative'])==f['sha256']==sha(ROOT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'/f['relative'])
shutil.copytree(A/'candidate/company-video-grammar-analyzer',B/'candidate/company-video-grammar-analyzer')
for name in ['contract-v1.json','candidate-pins.json','common-task.md','common-output-format.md','windows.json','run-matrix.json','legacy-regression-plan.json','exposure.json','materials-metadata.json']:
 shutil.copy2(A/name,B/name)
plan=json.loads((W/'phase01a-a4/case-plan.json').read_text(encoding='utf-8'))['cases']
for cid,aid,phases in [('V05','A4-G',['V05','V05_retest_more','V05_with_more']),('V06S','A4-S',['V06S','V06S_retest_more','V06S_retest_extra']),('V06W','A4-W',['V06W','V06W_retest_more','V06W_retest_extra'])]:
 case=next(x for x in plan if x['case_id']==cid)
 case['raw_extraction_logs']=[str(W/'phase01a-a4/cases'/aid/ph/'실행기록.json') for ph in phases]
 for p in case['raw_extraction_logs']:assert Path(p).is_file()
 case['output_dir']=str(B/'legacy'/cid/'outputs');case['skill']=str(B/'candidate/company-video-grammar-analyzer/SKILL.md')
 case['run_wall_limit_minutes']=10;case['crop_limit']=40
 write(B/'legacy'/cid/'input.json',case)
write(B/'execution-start.json',{'started_at':datetime.datetime.now().astimezone().isoformat(),'user_authorization':'이 설계대로 A5b 진행. 기존3구간 회귀부터 확인하고 통과하면 별도16회 비교','stage':'legacy_regression','skill_version':'0.1.0-draft.3','primary_runs_started':0,'new_material_pixels_opened':False,'model_configuration':'inherit parent settings; no override or mid-trial switch','model_checkpoint':'host not exposed','user_model_context':'6.1-sol high suitability question; not proof of exact host model','separate_paid_API_calls':0})
print('candidate pins matched; three neutral regression inputs ready; no new-source decode')
