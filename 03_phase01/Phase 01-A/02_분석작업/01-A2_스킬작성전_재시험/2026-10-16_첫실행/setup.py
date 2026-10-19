from pathlib import Path
from fractions import Fraction as F
from datetime import datetime
from zoneinfo import ZoneInfo
import json,sys,shutil
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
public=ROOT/'Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/분석입력/중립과제.json'
contract=ROOT/'Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/01_착수판정기준.json'
DATA=HERE/'analysis_input';DATA.mkdir(exist_ok=True)
packet=json.loads(public.read_text(encoding='utf-8'));write(DATA/'cases.json',packet)
write(HERE/'실행시작_고정.json',{'started_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'input_packet_sha256':sha(public),'acceptance_criteria_sha256':sha(contract),'source':'new extracts from allowlisted originals; no copied old observations','new_skill_available':False,'baseline_procedure':'A2 generic object/time/region inspection v0.2; case-specific answers withheld','initial_case_outputs':{},'media_scope':'existing six current-window cases only','A3_started':False})
for case in packet['cases']:
    aid='자료005' if '장헌' in case['media_path'] else '자료013';case['asset_id']=aid
    assert sha(Path(case['media_path']))==case['media_sha256']
write(DATA/'cases.json',packet)
shutil.copy2(HERE.parent/'phase01a-a2/extract.py',DATA/'bounded_base.py')
step={'T01':F('0.1'),'T02':F('0.05'),'T03':F('0.1'),'T04':F(1,3),'T05':F(1,30),'T06':F('0.14')}
groups={}
for c in packet['cases']:
    lo,hi=map(lambda x:F(str(x)),c['allowed_window_seconds']);ts=[];t=lo
    while t<=hi:ts.append(t);t+=step[c['case_id']]
    if ts[-1]!=hi:ts.append(hi)
    assert len(ts)<=40
    groups[c['case_id']]={'id':c['asset_id'],'times':[str(t) for t in ts],'width':3840 if c['asset_id']=='자료013' else 1920}
write(DATA/'groups.json',groups)
src=(HERE.parent/'phase01a-a2/extract.py').read_text(encoding='utf-8')
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',"sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent/'phase01a-a2'))\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent\nGROUPS=json.loads((OUT/'groups.json').read_text(encoding='utf-8'))")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'","OUT.parent.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'")
src=src.replace("OUT.parent/'phase01a-a1/후보런타임'","OUT.parent.parent/'phase01a-a1/후보런타임'")
line=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(line,"    group=GROUPS[phase]\n    if aid!=group['id']:raise ValueError('wrong_case_asset')\n    targets=[Fraction(t) for t in group['times']]")
src=src.replace('width=1920;height=',"width=group['width'];height=")
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:","if phase not in GROUPS:")
src=src.replace("for aid in ([sys.argv[2]] if len(sys.argv)>2 else ['자료005','자료013']):","for aid in [GROUPS[phase]['id']]:")
(DATA/'extract.py').write_text(src,encoding='utf-8')
(DATA/'PROCEDURE.md').write_text('''# Neutral A2 procedure, no new analysis skill

Analyze only the assigned media case and its allowed time window. Read cases.json and your assigned extraction logs/frames. Do not search or read other project reports, previous observations, answer files, or chat histories. Existing generic animation knowledge may help naming but cannot replace visible evidence. Never use an entrance/exit rule as proof of the curve.

Inventory observable subjects across the whole image: primary objects, supporting details, text, borders, lines, light, internal content, and content within displayed screens. Separate an object's overall movement from changes inside it. Inspect temporal order forward and trace settled objects backward. Compare native crops where overview sheets are too small. Investigate changes in apparently held areas before declaring them static. No fixed object count is expected.

Record position, size, shape/orientation, visibility/reveal, color/brightness, internal changes, overlap/occlusion, appearance order, and observable acceleration/deceleration. Not every field needs a numeric estimate. Separate what changes from what cannot be identified. Do not infer actual AE layers, handles, presets or intentions from the rendering. Record positive observations even if an exact curve remains uncertain. If more evidence is needed, use the bounded inspect_more.py helper in your own output folder or make crops of supplied PNGs; no source modification or external API.

Save first-pass observations per case before any grading feedback. Include evidence paths/times, uncertain aspects, extra evidence you requested, and all files read. Do not grade yourself against hidden expected answers. No A3 skill creation or AE/CU operation.
''',encoding='utf-8')
print(json.dumps({k:len(v['times']) for k,v in groups.items()}))
