"""Assemble reviewed results, preserving original runs and their grades."""
from pathlib import Path
import json,shutil
from prepare import write,ROOT
B=Path(__file__).resolve().parent
W=B/'company-video-grammar-analyzer-workspace'
review=json.loads((B/'root-audit/retest-review.json').read_text(encoding='utf-8'))
assert set(review)=={'V05','V06S','V06W'} and all(v['content_issue_resolved'] for v in review.values())
for path,count,field in [('helper-tests-A4-draft3.json',12,'passed'),('root-audit/draft3-provenance-tests.json',6,'correct'),('root-audit/crop-tests.json',5,'correct')]:
 tests=json.loads((B/path).read_text(encoding='utf-8'))
 assert len(tests)==count and all(t[field] for t in tests)
for cid,r in review.items():
 original=W/f'iteration-1/eval-{cid}'
 dest=W/f'iteration-2/eval-{cid}'
 meta=json.loads((original/'eval_metadata.json').read_text(encoding='utf-8'));meta['iteration']='targeted draft3 rerun'
 write(dest/'eval_metadata.json',meta)
 initial=json.loads((original/'with_skill/grading.json').read_text(encoding='utf-8'))
 assert len(r['criterion_notes'])==len(initial['expectations'])
 expectations=[dict(text=e['text'],passed=True,evidence=n,post_hoc=e.get('post_hoc',False)) for e,n in zip(initial['expectations'],r['criterion_notes'])]
 write(dest/'with_skill/grading.json',{'grader':'root inline source/ROI comparison','human_approved':False,'expectations':expectations,'summary':{'passed':len(expectations),'failed':0,'total':len(expectations),'pass_rate':1},'interpretation':'targeted reanalysis only; known development cases, not held-out accuracy','remaining_limits':r['remaining_limits']})
 write(dest/'with_skill/timing.json',{'total_tokens':None,'duration_ms':None,'total_duration_seconds':None,'reason':'host telemetry not exposed'})
selected=[]
for cid in ['V01','V02','V03','V04','V05','V06S','V06W']:
 iteration=2 if cid in review else 1
 src=W/f'iteration-{iteration}/eval-{cid}'
 output=B/'selected-review'/f'eval-{cid}'
 assert not output.exists(),'do not overwrite a completed presentation'
 output.mkdir(parents=True)
 shutil.copy2(src/'eval_metadata.json',output/'eval_metadata.json')
 display=output/'with_skill';(display/'outputs').mkdir(parents=True)
 for name in ['observations.json','observations.md','variant-comparison.md']:
  p=src/'with_skill/outputs'/name
  if p.exists():shutil.copy2(p,display/'outputs'/name)
 for name in ['grading.json','timing.json']:
  p=src/'with_skill'/name
  if p.exists():shutil.copy2(p,display/name)
 selected.append({'case_id':cid,'iteration':iteration,'skill_version':'0.1.0-draft.3' if iteration==2 else '0.1.0-draft.2','observations':str((src/'with_skill/outputs/observations.json').relative_to(B)),'status':'listed criteria satisfied; remaining limits retained'})
result={'stage':'01-A4','status':'A4_completed_with_targeted_retests','skill_version':'0.1.0-draft.3','new_video_files':5,'registered_bundles':4,'task_count':6,'source_window_count':7,'initial_source_window_runs':14,'targeted_retest_runs':3,'selected_results':selected,'content_issue_types':3,'affected_with_skill_source_windows':3,'content_issues_open':0,'remaining_uncertainties_preserved':True,'helper_issue_types':1,'helper_tests':{'prior_regression':12,'source_time_provenance':6,'native_crop_provenance':5,'all_passed':True},'human_approval':False,'general_accuracy':None,'A5_started':False,'reserved_sources_not_opened':['자료011','자료014'],'no_repeat_user_review_required':True}
write(B/'result.json',result)
audit=json.loads((B/'final-audit.json').read_text(encoding='utf-8'))
report=(B/'A4-결과보고.md').read_text(encoding='utf-8')
report=report.replace('{{RETEST_OUTCOME}}','영향을 받은 G·싱글·듀얼 3구간을 새 문맥에서 다시 시험했고, 발견한 두 내용 문제는 재시험 결과에서 해소됐습니다. 나머지4구간의 최초 결과와 함께 선택한7개 결과가 이번 명시 기준을 충족합니다. **전체 영상에 더 이상 누락이 없다는 판정은 아닙니다.**')
report=report.replace('{{VARIANT_RETEST}}',review['V06S']['report_summary']+' '+review['V06W']['report_summary'])
report=report.replace('{{FINAL_COUNTS}}',f"입력 원본5개와 최초 출력의 해시 보존을 확인했습니다. A4의 성공 추출 PNG는{audit['selected_png_count']}장, 원본별 고유 시각은{audit['unique_source_times']}개입니다. 개요·기본·추가·추출기 진단을 모두 합한 수이며 크롭/보드와 별도이고, 전부 연속 열람했다는 뜻이 아닙니다. 모든17개 관측 기록의 구조·원본/시각 연결 검사를 통과했습니다.")
snapshot=ROOT/'Phase 01-A/02_분석작업/01-A4_다른영상_확대시험/2026-10-16'
links='## 결과 위치\n\n'+ '\n'.join(f'- [{label}](<{str(path).replace(chr(92),"/")}>)' for label,path in [('스킬 본문',ROOT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer/SKILL.md'),('선택 결과 검토 화면',snapshot/'A4-선택결과-검토.html'),('최초 사용/미사용 결과 검토 화면',snapshot/'A4-최초시험-검토.html'),('재시험 원본 결과',snapshot/'company-video-grammar-analyzer-workspace/iteration-2'),('실행·판정 요약',snapshot/'result.json')])
report=report.replace('{{LINKS}}',links)
assert '{{' not in report
(B/'A4-결과보고.md').write_text(report,encoding='utf-8')
print('selected seven results assembled; original versions explicitly retained')
