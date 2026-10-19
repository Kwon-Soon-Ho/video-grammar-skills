from pathlib import Path
import json,hashlib,base64
from html.parser import HTMLParser
C=Path(r'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기')
W=C/'phase00-build/R8_시험/video-guidance-reviewer-workspace';IT=W/'iteration-1';A=C/'phase00-build/R8_03_독립검토'
CREATOR=Path(r'C:\Users\User\.codex\skills\anthropic-skill-creator')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def embedded(text):
    marker='const EMBEDDED_DATA = '
    start=text.index(marker)+len(marker)
    data,end=json.JSONDecoder().raw_decode(text[start:])
    return data,text[start:start+end]
class Inventory(HTMLParser):
    def __init__(self):super().__init__();self.external=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in {'link','script','iframe','img','source'}:
            for key in ['src','href']:
                if d.get(key,'').startswith(('http:','https:','//')):self.external.append([tag,key,d[key]])

criteria=read(W/'평가항목.json');summary=read(W/'비교결과_정본.json');bench=read(IT/'benchmark.json')
totals={'new_skill':0,'old_skill':0};grading_errors=[]
for case in summary['comparisons']:
    ed=next(p for p in IT.glob('eval-*') if read(p/'eval_metadata.json')['eval_id']==case['case'])
    for arm in ['new_skill','old_skill']:
        grade=read(ed/arm/'run-1/grading.json');copy=case['configurations'][arm]
        assert grade['expectations']==copy['expectations']
        assert [x['text'] for x in grade['expectations']]==criteria['cases'][str(case['case'])]['expectations']
        assert all(type(x['passed']) is bool and isinstance(x['evidence'],str) and x['evidence'].strip() for x in grade['expectations'])
        n=sum(x['passed'] for x in grade['expectations']);assert n==copy['passed']==grade['summary']['passed']
        assert copy['grading_sha256']==sha(ed/arm/'run-1/grading.json')
        match=[r for r in bench['runs'] if r['eval_id']==case['case'] and r['configuration']==arm];assert len(match)==1
        assert match[0]['expectations']==grade['expectations'] and match[0]['result']['passed']==n
        assert all(match[0]['result'][k] is None for k in ['time_seconds','tokens','tool_calls','errors'])
        totals[arm]+=n
viewer_log=read(W/'공식뷰어_실행기록.json')
raw_path=Path(viewer_log['args'][viewer_log['args'].index('--static')+1]);display_path=W/'적용성검토자_출력검토.html'
raw=raw_path.read_text(encoding='utf-8');display=display_path.read_text(encoding='utf-8');raw_data,raw_literal=embedded(raw);data,literal=embedded(display)
assert data==raw_data
inv=Inventory();inv.feed(display);rawinv=Inventory();rawinv.feed(raw)
assert not inv.external and len(rawinv.external)==4
assert '</script' not in literal.casefold() and '<' not in literal
expected={p.parent.relative_to(IT).as_posix().replace('/','-'):p for p in IT.glob('eval-*/*/run-1/outputs')}
assert len(expected)==len(data['runs'])==6 and {r['id'] for r in data['runs']}==set(expected)
output_count=0;grading_key_presence=[];prompt_mismatches=[]
for run in data['runs']:
    out=expected[run['id']];names=set()
    for f in run['outputs']:
        assert f['name'] not in names;names.add(f['name']);p=out/f['name']
        if f['type']=='text':assert p.read_text(encoding='utf-8')==f['content']
        elif f['type']=='binary':assert p.read_bytes()==base64.b64decode(f['data_uri'].split(';base64,',1)[1])
        else:raise ValueError('unexpected output type')
        output_count+=1
    assert names=={p.name for p in out.iterdir() if p.is_file()}
    grade=read(out.parent/'grading.json')
    gkeys=[k for k,v in run.items() if v==grade]
    grading_key_presence.append({'run':run['id'],'full_grading_equal_keys':gkeys,'run_keys':list(run)})
    assert gkeys,'full grading data absent/mismatched'
    meta=read(out.parent.parent.parent/'eval_metadata.json')
    if run.get('prompt')!=meta['prompt']:prompt_mismatches.append({'run':run['id'],'actual_prompt':run.get('prompt'),'expected_prompt':meta['prompt']})
assert output_count==12
first_raw_path=W/'뷰어보완이력/첫생성본/원문보존/공식뷰어_생성원본.html'
assert sha(first_raw_path)=='1021a5a149519fa1c95b22730ad58b5ef9e26a2173a9361829770b4e5e7a61ee'
first_data,_=embedded(first_raw_path.read_text(encoding='utf-8'))
first_runs={r['id']:r for r in first_data['runs']}
for run in data['runs']:
    original=first_runs[run['id']]
    assert run['outputs']==original['outputs'] and run['grading']==original['grading']
assert first_data['benchmark']==data['benchmark']
log=read(W/'공식뷰어_실행기록.json');shown=read(W/'뷰어_표시검증.json')
for record in log['post_execution_display_metadata_copies']:
    source=read(W/record['source']);destination=read(W/record['display_only_destination'])
    assert set(destination)=={'eval_id','eval_name','prompt'}
    assert destination=={key:source[key] for key in record['selected_keys']}
    assert sha(W/record['source'])==record['source_sha256'] and sha(W/record['display_only_destination'])==record['sha256']
    assert record['assertions_not_copied'] and record['created_after_all_six_executor_and_grader_completions']
assert len(log['post_execution_display_metadata_copies'])==6
assert log['returncode']==0 and log['stderr']=='' and '--static' in log['args']
assert sha(CREATOR/'eval-viewer/generate_review.py')==log['creator_script_sha256']
assert sha(CREATOR/'eval-viewer/viewer.html')==log['template_sha256']
assert sha(C/'phase00-build/R8_01_뷰어작성.py')==log['display_adapter_sha256']
assert sha(CREATOR/'LICENSE.txt')==sha(W/'원문보존/LICENSE.txt')
assert sha(raw_path)==shown['official_raw_sha256'] and sha(display_path)==shown['display_sha256']
assert data.get('benchmark')==bench,('benchmark differs',data.keys())
assert bench['run_summary']=={'new_skill':{},'old_skill':{},'delta':{}}
assert all(summary[k] is False for k in ['human_feedback_received','candidate_adopted','actual_video_analysis','automatic_trigger_tested','statistical_superiority_claimed','full_R6_R7_context_validated'])
assert summary['actual_attempts']=={'executor_trials_total':6,'cases':3,'runs_per_case_per_configuration':1,'infrastructure_invalid_model_trials':0}
result={'kind':'independent_static_aggregate_viewer_data_audit','totals':totals,'cases':3,'model_runs':6,'output_files_equal':output_count,'grading_data_equal':grading_key_presence,'prompt_mismatches':prompt_mismatches,'embedded_raw_display_data_equal':True,'display_external_resource_tags':inv.external,'raw_external_tags_removed':rawinv.external,'embedded_script_boundary_escaped':True,'benchmark_equals_file':True,'benchmark_uncollected_summary_statistics_empty':True,'official_script_template_and_adapter_current_hashes_match_log':True,'official_license_bytes_equal':True,'raw_display_hashes_match_record':True,'publisher_sha256':sha(C/'phase00-build/R8_03_결과정리.py'),'human_output_feedback_received':False,'browser_render_or_click_tested':False,'limits':['static source/data comparison, not rendered UI verification','no official viewer or aggregate script rerun','tie does not establish independent skill effect or general equivalence']}
result.update(first_viewer_preserved_and_output_grading_benchmark_payload_unchanged=True,post_execution_display_metadata_minimal_keys_verified_count=6)
(A/'07_집계와뷰어_독립대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['grading_data_equal','prompt_mismatches']},ensure_ascii=True))
print(json.dumps({'prompt_mismatches_count':len(prompt_mismatches),'actual_prompt_values':sorted(set(p['actual_prompt'] for p in prompt_mismatches))},ensure_ascii=True))
