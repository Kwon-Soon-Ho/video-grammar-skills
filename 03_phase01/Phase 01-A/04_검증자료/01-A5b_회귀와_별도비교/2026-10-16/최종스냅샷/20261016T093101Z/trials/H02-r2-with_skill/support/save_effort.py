from pathlib import Path
import json,datetime
from fractions import Fraction
B=Path.cwd()/'phase01a-a5b'
D=B/'trials/H02-r2-with_skill'
start=datetime.datetime(2026,10,16,9,18,50,tzinfo=datetime.timezone.utc)
end=datetime.datetime.now(datetime.timezone.utc)
base_direct=[12,12.4,12.8,13.2,13.6,14.4,15.2,16.4,16.8,17.2,17.6,18,18.4,18.8,19.2,19.6,20]
extra1_direct=[12.1,12.2,12.3,12.5,12.6,12.7,12.9,13,17.8,17.9,18.1,18.2,18.3,18.5,18.6,18.7]
extra2_direct=[17.7,17.75,18.05,18.15,18.25,18.35,18.45]
direct=[]; logs=[]
for name,ts in [('H02',base_direct),('H02-r2-with_skill-extra1',extra1_direct),('H02-r2-with_skill-extra2',extra2_direct)]:
 p=B/'cases/A5-A'/name/'실행기록.json'; logs.append(str(p))
 log=json.loads(p.read_text(encoding='utf-8'))
 direct += [f['path'] for f in log['frames'] if float(Fraction(f['actual_playback_seconds'])) in ts]
crops=json.loads((D/'support/crops.json').read_text(encoding='utf-8'))
boards=[str(B/'cases/A5-A'/folder/f'board-{i}.jpg') for folder in ['H02','H02-r2-with_skill-extra1'] for i in [1,2]]
text_files=[B/'trial-instructions.md',B/'common-task.md',B/'common-output-format.md',D/'input.json',B/'candidate/company-video-grammar-analyzer/SKILL.md',*[B/'candidate/company-video-grammar-analyzer/references'/n for n in ['evidence-and-records.md','motion-review.md','output-contract.md']],B/'trial_tools.py',B/'common-tools/check_observations.py',B/'common-tools/evidence_catalog.py']
data={'run_id':'H02-r2-with_skill','start_utc':start.isoformat(),'end_utc':end.isoformat(),'ai_elapsed_seconds_including_validation':(end-start).total_seconds(),'complete':False,'stopped':True,'stop_reason':'STOP.json 존재 확인 및 주 실행자의 전체 배치 중단 지시. 별도 선행 실행의 중대 오류에 따른 중단으로 이 실행의 내용 평가 결과는 아님. 새 분석·추출·관측 본문 작성·finish 검증을 중지함.','observations_json_saved':False,'observations_md_saved':False,'validation_attempted':False,'finish_attempted':False,'sealed':False,'files_read':[str(p) for p in text_files]+logs+boards+direct+[r['path'] for r in crops], 'direct_png_viewed_count':len(direct),'board_viewed_count':len(boards),'native_crop_unique_generated_count':len(crops),'native_crop_unique_viewed_count':len(crops),'native_crop_write_operations':53,'native_crop_write_operations_note':'make_crops.py로 19개 생성 후 more_crops.py가 같은 19 경로를 동일 좌표로 재생성하고 15개 고유 경로 추가. 고유 crop은 34개.','additional_extraction_rounds':2,'additional_extraction_images':[24,18],'additional_extraction_total_images':42,'extraction_failures':[],'unfinished':['observations.json 및 observations.md 미작성','저장 전 최종 주장-근거 역대조 미완료','공통 finish 구조·근거 검증 미실행','출력 동결 미실행'],'preserved_support':['request1.json','request2.json','crops.json','measurements.json','34 native PNG crops','make_crops.py','more_crops.py','measure.py'],'user_participation':'없음','tokens':None,'model':'parent inherited exact host ID unavailable','human_reading_time_estimated':False}
(D/'run-effort.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:data[k] for k in ['run_id','end_utc','ai_elapsed_seconds_including_validation','complete','direct_png_viewed_count','board_viewed_count','native_crop_unique_generated_count','additional_extraction_total_images']},ensure_ascii=False))
