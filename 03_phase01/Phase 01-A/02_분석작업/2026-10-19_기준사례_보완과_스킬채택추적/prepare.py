from pathlib import Path
import json,shutil
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OLD=WORK/'internal-video-audit-20261019/source-overview';OUT=HERE/'extraction'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'tools').mkdir(exist_ok=True);(OUT/'requests').mkdir(exist_ok=True)
for name in ('manifest.json','adapter-scope.json'):shutil.copyfile(OLD/name,OUT/name)
s=(OLD/'tools/prepare.py').read_text('utf-8').replace(str(OLD).replace('\\','\\\\'),str(OUT).replace('\\','\\\\'))
(OUT/'tools/prepare.py').write_text(s,encoding='utf-8');shutil.copyfile(OLD/'tools/extract.py',OUT/'tools/extract.py')
requests={'NEW-N':{'scout':['164','165','349/2','175','176','177','178','179','180','181','182']},'NEW-P':{'scout':['38','39','97/2','49','50','51','52','53','54','55','79','80','81','82']}}
for aid,phases in requests.items():
 for phase,times in phases.items():(OUT/'requests'/f'{aid}-{phase}.json').write_text(json.dumps(times),encoding='utf-8')
(HERE/'decision.json').write_text(json.dumps({'user_choice':'① 현재 두 장면을 기준 사례로 보완 (추천)','scope':'기존 미해결 5개와 인접 문맥을 먼저 조사. 전체 디자인·흐름·독립 세부 기록 연결. 원본 전체 정밀 완료·재제작은 이 묶음 범위 밖.','reviewer':'same_agent_context','reuse_existing_evidence':True,'original_records_preserved':True,'next_batch_requires_user_choice':True},ensure_ascii=False,indent=2),encoding='utf-8')
print(str(OUT))
