import json,hashlib,re,base64
from pathlib import Path
from html.parser import HTMLParser
O=Path(__file__).parent;C=O.parent.parent;W=O.parent/'R8_시험/video-knowledge-curator-workspace';I=W/'iteration-2'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def embedded(p):
 t=p.read_text(encoding='utf-8');m='const EMBEDDED_DATA = ';s=t.index(m)+len(m);d,n=json.JSONDecoder().raw_decode(t[s:]);return t,d,t[s:s+n]
class Inventory(HTMLParser):
 def __init__(self):super().__init__();self.external=[]
 def handle_starttag(self,tag,attrs):
  if tag in ['link','script','iframe','img','source']:
   for k,v in attrs:
    if k in ['src','href'] and v and v.startswith(('http:','https:','//')):self.external.append([tag,k,v])
behavior=read(O/'R8_01_최종행동_대조.json');static=read(O/'R8_01_정적판정.json');source=read(D/'08_검증결과/R8_00_입력보존.json')['source_hashes']
D_hashes={r:sha(D/r) for r in static['after_hashes']}
expected=read(W/'평가항목.json')['cases'];summary=read(W/'비교결과_정본.json');benchmark=read(I/'benchmark.json');completion=read(W/'실행완료_기록.json');displaycheck=read(W/'뷰어_표시검증.json')
rt,rd,rj=embedded(W/'원문보존/공식뷰어_생성원본.html');vt,vd,vj=embedded(W/'큐레이터_출력검토.html');inventory=Inventory();inventory.feed(vt)
grades=[];content_errors=[];completion_errors=[]
for case in sorted(I.glob('eval-*')):
 meta=read(case/'eval_metadata.json');cid=str(meta['eval_id'])
 for arm in ['new_skill','old_skill']:
  run=case/arm/'run-1';g=read(run/'grading.json');items=g['expectations'];passed=sum(x['passed'] for x in items)
  valid_types=all(type(x['passed']) is bool and isinstance(x['evidence'],str) and bool(x['evidence'].strip()) for x in items)
  cal={'passed':passed,'failed':len(items)-passed,'total':len(items),'pass_rate':passed/len(items)}
  entry=next(x for x in benchmark['runs'] if str(x['eval_id'])==cid and x['configuration']==arm)
  compare=next(x for x in summary['comparisons'] if str(x['case'])==cid)['configurations'][arm]
  grades.append({'case':cid,'arm':arm,'texts_and_count_match':[x['text'] for x in items]==expected[cid],'schema_valid':valid_types,'summary_exact':g['summary']==cal,'benchmark_expectations_match':entry['expectations']==items,'benchmark_result_match':all(entry['result'][k]==v for k,v in cal.items()),'comparison_match':compare['expectations']==items and compare['grading_sha256']==sha(run/'grading.json') and compare['passed']==passed and compare['total']==len(items),'resource_metrics_null':all(entry['result'][k] is None for k in ['time_seconds','tokens','tool_calls']),'total':len(items),'passed':passed})
  viewer_id=run.relative_to(I).as_posix().replace('/','-');v=next(x for x in vd['runs'] if x['id']==viewer_id)
  grades[-1]['viewer_grade_matches']=v['grading']==g
  for f in v['outputs']:
   p=run/'outputs'/f['name']
   if f['type']=='text':same=p.is_file() and p.read_text(encoding='utf-8')==f['content']
   elif f['type']=='binary':same=p.is_file() and p.read_bytes()==base64.b64decode(f['data_uri'].split(';base64,',1)[1])
   else:same=False
   if not same:content_errors.append({'run':viewer_id,'file':f['name']})
for row in completion['attempts']:
 run=W/row['run']
 if row['transcript_sha256']!=sha(run/'transcript.md'):completion_errors.append(row['run']+'/transcript')
 for r,h in row['output_hashes'].items():
  if sha(run/r)!=h:completion_errors.append(row['run']+'/'+r)
checks={**behavior['checks'],
 'all163_static_D_sources_still_unchanged':D_hashes==static['after_hashes'],
 'old14_skill_files_in_152_unchanged':sum(r.startswith('06_맞춤스킬/') for r in source)==14 and all(sha(D/r)==h for r,h in source.items() if r.startswith('06_맞춤스킬/')),
 'six_grades_exact_expectation_schema_and_8_8_6':len(grades)==6 and all(g['schema_valid'] and g['texts_and_count_match'] and g['summary_exact'] for g in grades),
 '44_total_AI_behavior_judgments_not_video_quality':sum(g['total'] for g in grades)==44 and sum(len(x) for x in expected.values())==22 and summary['kind']=='synthetic_development_skill_comparison_not_R7_quality_total',
 'aggregate_from_all_six_grades_exact':all(g['benchmark_expectations_match'] and g['benchmark_result_match'] and g['comparison_match'] for g in grades),
 'all_resource_metrics_null':all(g['resource_metrics_null'] for g in grades) and all(all(r['timing'][k] is None for k in ['total_tokens','duration_ms','total_duration_seconds']) for r in behavior['runs']),
 'attempt8_eligible6_invalid2_and_prepared4':completion['executor_attempt_count']==8 and completion['comparison_eligible_count']==6 and completion['infrastructure_invalid_count']==2 and len(completion['prepared_but_not_executed'])==4,
 'completion_transcripts_and_output_hashes_match':not completion_errors,
 'excluded_iteration1_not_aggregated':len(benchmark['runs'])==6 and len(summary['comparisons'])==3,
 'summary_no_adoption_human_trigger_statistical_claims':all(summary[k] is False for k in ['actual_video_analysis','human_feedback_received','candidate_adopted','automatic_trigger_rate_tested','statistical_superiority_claimed']),
 'official_static_raw_and_display_same_decoded_data':rd==vd,
 'viewer_embedded_benchmark_and_grades_match_actual':vd['benchmark']==benchmark and all(g['viewer_grade_matches'] for g in grades),
 'six_viewer_runs_output_contents_match':len(vd['runs'])==6 and not content_errors,
 'display_no_external_resource_tags':not inventory.external,
 'display_embedded_script_boundaries_escaped':'</script' not in vj.casefold() and '<' not in vj,
 'viewer_verification_hashes_match_actual':displaycheck['official_raw_sha256']==sha(W/'원문보존/공식뷰어_생성원본.html') and displaycheck['display_sha256']==sha(W/'큐레이터_출력검토.html'),
 'viewer_not_claiming_human_or_browser_render_review':displaycheck['human_review_performed'] is False and 'no rendered browser/CU screenshot verification' in displaycheck['limitations'],
}
files=[p for p in W.glob('*') if p.is_file()]+[I/'benchmark.json',I/'benchmark.md',W/'원문보존/공식뷰어_생성원본.html',W/'원문보존/LICENSE.txt']
for case in sorted(I.glob('eval-*')):
 files.append(case/'eval_metadata.json')
 for arm in ['new_skill','old_skill']:
  run=case/arm/'run-1';files.extend(p for p in run.glob('*') if p.is_file());files.extend(p for p in (run/'outputs').rglob('*') if p.is_file());files.extend(p for p in (run/'backup').rglob('*') if p.is_file())
  if case.name.startswith('eval-02'):files.append(run/'inputs/Phase00/작업초안/레이아웃지식_초안.json')
files.extend(O/n for n in ['R8_01_정적판정.json','R8_01_시험기반_판정.json','R8_01_최종행동_대조.json','R8_01_최종행동감사.py','R8_01_최종집계감사.py'])
C_hashes={p.relative_to(C).as_posix():sha(p) for p in sorted(set(files)) if p.is_file()}
result={'scope':'independent AI final artifact/aggregation/viewer structural red-team; no browser/CU human approval','checks':checks,'condition_count':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'grading_summaries':grades,'viewer_output_content_errors':content_errors,'completion_hash_errors':completion_errors,'D_source_hashes':D_hashes,'C_result_hashes':C_hashes}
(O/'R8_01_최종集계_대조.json'.replace('集','집')) .write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'conditions':len(checks),'passed':sum(checks.values()),'failed':result['failed'],'D_sources':len(D_hashes),'C_results':len(C_hashes),'grade_summaries':[{k:g[k] for k in ['case','arm','passed','total']} for g in grades]},ensure_ascii=True,indent=2))
