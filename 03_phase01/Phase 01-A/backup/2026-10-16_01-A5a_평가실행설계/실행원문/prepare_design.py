from pathlib import Path
import json,sys,shutil,hashlib,datetime,platform
from fractions import Fraction
B=Path(__file__).resolve().parent
W=B.parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
STAGE=ROOT/'Phase 01-A'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def snapshot(source,dest):
 assert not dest.exists()
 shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__'))
 return [{'relative':str(p.relative_to(dest)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()]
skill=STAGE/'03_분석스킬/company-video-grammar-analyzer'
skill_files=snapshot(skill,B/'candidate/company-video-grammar-analyzer')
(B/'candidate/tool').mkdir(parents=True)
for name in ['extract.py','prepare.py','boards.py']:
 shutil.copy2(W/'phase01a-a4'/name,B/'candidate/tool'/name)
shutil.copy2(W/'phase01a-a4/output-format.md',B/'common-output-format.md')
sys.path.insert(0,str(W/'phase01a-a1/후보런타임'))
import av,PIL,numpy
runtime={'python':sys.version,'python_executable':sys.executable,'python_exe_sha256':sha(sys.executable),'platform':platform.platform(),'av':av.__version__,'av_libraries':av.library_versions,'Pillow':PIL.__version__,'numpy':numpy.__version__,'AI_model_id':None,'AI_model_reason':'exact checkpoint/version not exposed by current host tools; record visible setting at execution','runtime_binary_pins':[]}
for folder in [Path(av.__file__).parent,Path(PIL.__file__).parent]:
 for p in sorted(folder.rglob('*')):
  if p.is_file() and p.suffix.lower() in ['.pyd','.dll']:
   runtime['runtime_binary_pins'].append({'path':str(p),'sha256':sha(p)})
write(B/'candidate-pins.json',{'version':'0.1.0-draft.3','snapshot_files':skill_files,'tool_files':[{'path':str(p.relative_to(B)),'sha256':sha(p)} for p in sorted((B/'candidate/tool').glob('*.py'))],'runtime':runtime,'tool_scope':'A4 code snapshot; A5b uses separate allowlist/requests configuration. Unsupported media gate fails rather than silently changing code. No A5 decoder run in A5a.'})
materials=json.loads((B/'materials-metadata.json').read_text(encoding='utf-8'))
videos=[m for m in materials if m.get('kind')!='planning_document']
k,t,a=videos
cases=[('H01','자료014',t,0,8),('H02','자료014',a,12,20),('H03','자료011',k,25,35),('H04','자료011',k,66,76)]
windows=[]
for cid,group,m,lo,hi in cases:
 assert 0<=lo<hi<m['container_duration_seconds']
 windows.append({'case_id':cid,'project_group':group,'path':m['path'],'sha256':m['sha256'],'window_seconds':[lo,hi],'document_id':'DOC064' if group=='자료011' else None,'base_targets_seconds':[str(Fraction(lo)+Fraction(2,5)*i) for i in range(int(Fraction(hi-lo)/Fraction(2,5))+1)],'base_step_seconds':0.4,'end_frame_role':'context_after','selection':'A5a duration/registration-based selection before opening any video pixels; no failure-dependent replacement','within_seconds':hi-lo})
write(B/'windows.json',windows)
runs=[]
for c in windows:
 for rep in [1,2]:
  modes=['with_skill','without_skill'] if (int(c['case_id'][1:])+rep)%2==0 else ['without_skill','with_skill']
  for mode in modes:
   runs.append({'run_id':f"{c['case_id']}-r{rep}-{mode}",'case_id':c['case_id'],'repeat':rep,'configuration':mode,'isolated_context':True,'prior_answers_or_criteria_visible':False,'status':'not_started'})
write(B/'run-matrix.json',runs)
write(B/'legacy-regression-plan.json',{'status':'not_started_requires_A5b_authorization','purpose':'final unified draft3 regression, not held-out performance','runs':[{'case_id':cid,'A4_iteration_source':2,'configuration':'with_skill','repeats':1,'wall_cap_minutes':10} for cid in ['V05','V06S','V06W']],'total_runs':3,'stop_on_failure':True,'new_source_frames_opened_before_pass':False})
doclog=json.loads((W/'phase01a-docreview/문서목록과_읽기결과.json').read_text(encoding='utf-8'))['documents']
doc=next(x for x in doclog if x['id']=='DOC064')
exposure={'scope':'current thread, referenced direction thread, accessible A1–A4 logs and input document-review records; no claim of exhaustive all-account history','source_records':['reference-thread.json','phase01a-a4/result.json','phase01a-a4/adapter-scope.json','phase01a-docreview/문서목록과_읽기결과.json','자료011/03_기획서검토_근거.json'],'projects':[{'id':'자료014','visual_used_in_A1_A4':False,'document_status':'none, user-confirmed','current_stage_inspection':'selected two MP4 hashes and headers only','independence_limit':'same homepage genre as earlier EG-BIM, asset/template independence unverified','reserve_clips':['02_(O).mp4','03_(V).mp4'],'reserve_use':'not silently substituted after failure; unused same-project clips are not new independent projects'},{'id':'자료011','visual_used_in_A1_A4':False,'document_status':'DOC064 text previously extracted/reviewed','prior_document_record':{k:doc[k] for k in ['id','path','sha256','status','chunk_count','chars','detail']},'current_stage_inspection':'MP4 header/hash and PPTX hash; no new body or pixel read','independence_limit':'video-new/document-exposed, not fully unseen multimodal input'}],'unverified_other_context_exposure':'If later confirmed before execution, revise label/report scope; do not relabel as unseen merely because evaluator context is fresh.'}
write(B/'exposure.json',exposure)
# Preserve relevant old reports, criteria and result records without rewriting them.
protected=[]
for folder in [STAGE/'05_결과보고',skill,STAGE/'04_검증자료']:
 for p in folder.rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.md','.json','.py','.yaml']:
   protected.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
for name in ['01-A3_스킬작성과7구간시험','01-A4_다른영상_확대시험']:
 folder=STAGE/'02_분석작업'/name
 for p in folder.rglob('*'):
  if p.is_file() and (p.name in ['observations.json','observations.md','grading.json','output-seal.json','result.json','criteria-frozen.json','retest-review.json','final-review-changes.json']):
   protected.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
write(B/'protected-records.before.json',protected)
write(B/'A5-run-record-template.json',{'run_id':None,'analysis_profile':'grammar-structure-and-time','skill_and_tool_pins':'candidate-pins.json','exposure_group':None,'criterion_version':None,'actual_resource_use':{'start_utc':None,'end_utc':None,'elapsed_seconds':None,'tool_wait_seconds':None,'base_pngs':None,'adaptive_pngs':None,'ROI_count':None,'token_count':None,'separate_API_cost':None},'review_effort':{'actor':'human_or_AI','active_human_seconds':None,'AI_review_elapsed_seconds':None,'waiting_for_user_seconds':None,'correction_seconds':None,'reason_if_unavailable':None},'unresolved_questions':[],'handoff_refs':[],'status':'template_not_an_actual_run'})
print(json.dumps({'candidate_files':len(skill_files),'runtime_binary_pins':len(runtime['runtime_binary_pins']),'projects':2,'windows':len(windows),'unique_visual_seconds':sum(c['within_seconds'] for c in windows),'trial_runs':len(runs),'legacy_runs':3,'protected_records':len(protected),'video_frames_decoded':0},ensure_ascii=False))
