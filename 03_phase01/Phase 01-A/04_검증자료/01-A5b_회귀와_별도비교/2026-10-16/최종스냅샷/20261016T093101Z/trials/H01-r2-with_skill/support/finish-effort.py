import json,datetime,hashlib
from pathlib import Path
R=Path('phase01a-a5b/trials/H01-r2-with_skill').resolve();S=R/'support'
start=datetime.datetime(2026,10,16,9,1,6,tzinfo=datetime.timezone.utc)
read=json.loads((S/'read-files.json').read_text(encoding='utf-8'))
validation=json.loads((R/'validation.json').read_text(encoding='utf-8'));seal=json.loads((R/'seal.json').read_text(encoding='utf-8'))
assert validation['structure_passed'] and validation['evidence_provenance_checked']
for n,h in seal['files'].items(): assert hashlib.sha256((R/'outputs'/n).read_bytes()).hexdigest()==h
extra_read=[R/'outputs/observations.json',R/'outputs/observations.md',R/'validation.json',R/'seal.json',S/'crops.json',S/'rows.json',S/'read-files.json',S/'prepare.py',S/'more-crops.py',S/'paragraph-crops.py',S/'measure.py',S/'write-report.py',S/'request-1.json',S/'request-2.json']
end=datetime.datetime.now(datetime.timezone.utc)
d={'run_id':'H01-r2-with_skill','case_id':'H01','condition':'with_skill','start_utc':start.isoformat(),'end_utc':end.isoformat(),'ai_elapsed_seconds':round((end-start).total_seconds(),3),'elapsed_includes_validation':True,'wall_limit_seconds':900,'model':'parent inherited exact host ID unavailable','tokens':None,'human_intervention':False,'human_reading_time_estimated':False,'files_read':sorted(set(read['files_read']+[str(p) for p in extra_read])),'boards':{'visual_opened':6,'created_this_run':4,'base_preprovided':2},'direct_png':{'visual_opened':23,'unique_paths':read['direct_png_visual_paths'],'programmatically_opened_unique':len(read['programmatic_png_paths']),'programmatic_paths':read['programmatic_png_paths']},'native_rgb_crops':{'created':28,'visual_opened':28,'manifest_path':str(S/'crops.json'),'max_allowed':40},'additional_extraction':{'rounds':2,'round_image_counts':[24,16],'selected_total':40,'max_allowed_total':48,'technical_failures':[]},'required_items_incomplete':[],'unresolved_observation_items':['정확한AE구현·가속함수·원본키프레임','배경 띠의이동/리빌 구분 및 개별가감속','Value of형태곡선·O/V/A개별속도곡선','국문 첫줄 최초시작·리빌과 밝기구현분리','지도내부의 독립줌/이동 여부'],'validation':{'structure_passed':True,'evidence_provenance_checked':True,'content_verified_by_common_tool':False,'sealed_outputs_sha256_rechecked':True,'seal_utc':seal['utc']},'stop_file_present_at_last_check':(R.parent.parent/'STOP.json').exists(),'completion_status':'complete_with_stated_observation_limits'}
assert d['ai_elapsed_seconds']<900
(R/'run-effort.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
assert json.loads((R/'run-effort.json').read_text(encoding='utf-8'))['additional_extraction']['selected_total']==40
print(json.dumps({'run_id':d['run_id'],'start_utc':d['start_utc'],'end_utc':d['end_utc'],'ai_elapsed_seconds':d['ai_elapsed_seconds'],'sealed_outputs_unchanged':True,'run_effort_saved':True},ensure_ascii=False))
