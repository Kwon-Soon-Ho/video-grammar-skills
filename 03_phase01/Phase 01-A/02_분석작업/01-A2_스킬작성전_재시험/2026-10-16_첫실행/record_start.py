from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import sha,write
packet=json.loads((HERE/'analysis_input/cases.json').read_text(encoding='utf-8'))
dispatch={'recorded_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'skill_used_for_eval_workflow':'anthropic-skill-creator; baseline-only adaptation because A3 skill not yet exists','new_analysis_skill_available':False,'agent_input_history':'fork_turns none; neutral prompt/procedure/current raw frames only','input_separation':'instructions and separate input paths; no filesystem security boundary asserted','analysts':{'retest_a':['T01','T04'],'retest_b':['T02','T05'],'retest_c':['T03','T06']},'model':'inherited configured model; exact backend model revision not exposed by spawn tool','independence_scope':'separate analysis contexts, no prior user corrections supplied; same known source videos, not unseen-source generalization','allowed_additional_evidence':'only assigned time windows, bounded local extraction helper, no answer feedback','grading_status':'not started; wait until per-case raw output hashes sealed','A3_started':False}
write(HERE/'분석실행_배포기록.json',dispatch)
runs=[]
for c in packet['cases']:
    log=HERE/'analysis_input/cases'/c['asset_id']/c['case_id']/'실행기록.json';r=json.loads(log.read_text(encoding='utf-8'))
    assert r['complete_target_selection'] and r['input_sha256']==r['input_sha256_after']==c['media_sha256']
    assert r['timing_status']=='all_decoded_frame_pts_match_reconstructed_sample_tables_in_this_window'
    for f in r['frames']:assert sha(Path(f['path']))==f['sha256']
    runs.append({'case_id':c['case_id'],'log_path':str(log),'log_sha256':sha(log),'frames':len(r['frames']),'input_sha256':r['input_sha256'],'sample_table_times_match':True,'min_seconds':r['frames'][0]['actual_playback_seconds'],'max_seconds':r['frames'][-1]['actual_playback_seconds'],'raster':r['frames'][0]['derived_size']})
write(HERE/'원본추출_고정.json',{'cases':runs,'selected_frames_total':sum(r['frames'] for r in runs),'fresh_extraction_this_run':True,'technical_retry':'T03 first attempt parent-directory creation error before decode, saved; retry succeeded','content_analysis_retries':0})
print('neutral inputs and fresh frame extraction pinned; grading not started')
