"""Prepare bounded full-length overview requests and focused unresolved-property probes."""
from pathlib import Path
from fractions import Fraction as F
import json,shutil
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OLD=WORK/'analysis-reliability-20261019/fresh';OUT=HERE/'source-overview';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((OLD/'manifest.json').read_text(encoding='utf-8'))
for name in ('manifest.json','adapter-scope.json'):shutil.copyfile(OLD/name,OUT/name)
tools=OUT/'tools';tools.mkdir(exist_ok=True)
(tools/'prepare.py').write_text((OLD/'tools/prepare.py').read_text(encoding='utf-8').replace(str(OLD).replace('\\','\\\\'),str(OUT).replace('\\','\\\\')),encoding='utf-8')
shutil.copyfile(OLD/'tools/extract.py',tools/'extract.py')
tasks=[]
for m in manifest:
    duration=F(m['duration_seconds']);times=[F(i) for i in range(0,int(duration),5)]
    # Last target remains inside the movie; do not infer an unselected endpoint.
    last=F(int(duration*10)-1,10)
    if last>times[-1]:times.append(last)
    for i,start in enumerate(range(0,len(times),30),1):
        phase='overview'+str(i);path=OUT/'requests'/(m['id']+'-'+phase+'.json');path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps([str(t) for t in times[start:start+30]]),encoding='utf-8')
        tasks.append({'id':m['id'],'phase':phase,'targets':len(times[start:start+30])})
(HERE/'overview-plan.json').write_text(json.dumps({'purpose':'두 원본 전체의 내용·표현 구간 목록과 상세 미검수 범위 파악. 5초 개요 표본은 컷 경계 정밀 검수나 전체 내용 분석 완료가 아님.','tasks':tasks,'frame_count':sum(t['targets'] for t in tasks),'whole_video_analysis_complete':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(tasks,ensure_ascii=False))
