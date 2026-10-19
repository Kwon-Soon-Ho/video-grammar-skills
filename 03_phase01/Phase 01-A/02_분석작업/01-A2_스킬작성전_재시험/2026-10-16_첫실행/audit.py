from pathlib import Path
from fractions import Fraction as F
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
PRE=ROOT/'Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
start=read(HERE/'실행시작_고정.json')
assert sha(PRE/'분석입력/중립과제.json')==start['input_packet_sha256']
assert sha(PRE/'01_착수판정기준.json')==start['acceptance_criteria_sha256']
packet=read(HERE/'analysis_input/cases.json');refs=read(PRE/'채점전용/실패사례와_내용대조기준.json')
for ref in refs['required_known_failure_cases']:assert sha(ROOT/ref['reference_receipt'])==ref['reference_sha256']
for c in packet['cases']:assert sha(Path(c['media_path']))==c['media_sha256']
logs=[];unique=set();counts={};sizes={}
for p in sorted(HERE.rglob('실행기록.json')):
    if 'evaluation' in p.parts:continue
    r=read(p);assert r['complete_target_selection'];assert r['input_sha256']==r['input_sha256_after'];assert r['timing_status']=='all_decoded_frame_pts_match_reconstructed_sample_tables_in_this_window'
    lo=1e6;hi=-1
    for f in r['frames']:
        assert sha(Path(f['path']))==f['sha256']
        t=float(F(f['actual_playback_seconds']));lo=min(lo,t);hi=max(hi,t)
        unique.add((r['input_sha256'],str(F(f['actual_playback_seconds']))))
        size='x'.join(map(str,f['derived_size']));sizes[size]=sizes.get(size,0)+1
    logs.append({'path':str(p),'sha256':sha(p),'frames':len(r['frames']),'min_seconds':lo,'max_seconds':hi,'input_sha256':r['input_sha256']})
    counts['base' if 'analysis_input' in p.parts else 'adaptive']=counts.get('base' if 'analysis_input' in p.parts else 'adaptive',0)+len(r['frames'])
cases=[]
for c in packet['cases']:
    cid=c['case_id'];seal=read(HERE/'seals'/(cid+'.json'));nseal=read(HERE/'seals'/(cid+'_narrative.json'))
    for s in [seal,nseal]:assert sha(Path(s['source_path']))==s['source_sha256']==sha(Path(s['sealed_copy']))
    grading=read(HERE/'evaluation/iteration-1'/('eval-'+cid)/'without_skill/grading.json')
    assert grading['raw_output_sha256']==seal['source_sha256'];assert grading['graded_at']>=seal['sealed_at'];assert grading['graded_at']>=nseal['sealed_at']
    raw=read(Path(seal['sealed_copy']));assert raw['case_id']==cid
    cases.append({'case_id':cid,'window':c['allowed_window_seconds'],'case_status':grading['case_status'],'requirements':grading['summary'],'raw_output_sha256':seal['source_sha256'],'first_output_unchanged':True})
report={'audited_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'frozen_input_criteria_and_human_reference_hashes_unchanged':True,'original_media_hashes_unchanged':True,'frame_logs':logs,'fresh_selected_PNG_counts':counts,'total_selected_PNGs':sum(counts.values()),'unique_source_times_within_this_run':len(unique),'raster_counts':sizes,'unique_times_not_additive_with_previous_runs':True,'case_results':cases,'first_analysis_outputs_preserved_before_grading':True,'content_analysis_retries_after_grader_feedback':0,'technical_extraction_retry':'T03 directory creation failure before decoding; later succeeded, first error retained','known_tool_issue':'retest_b first SciPy import unavailable; local NumPy replacement; original exploration files retained','new_human_confirmation_requested':False,'new_human_confirmation_count':0,'audio_analyzed':False,'A3_started':False,'skill_created':False,'independent_unseen_source_evaluation':False,'audit_limit':'Access lists are executor-reported; separate contexts/workflow paths are not an OS security boundary. Full executor token/duration telemetry unavailable.'}
(HERE/'실행감사.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['fresh_selected_PNG_counts','total_selected_PNGs','unique_source_times_within_this_run','raster_counts','first_analysis_outputs_preserved_before_grading']},ensure_ascii=False))
