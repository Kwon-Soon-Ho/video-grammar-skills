from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
groups={
 'eg_intro':{'id':'자료013','times':[str(i/5) for i in range(33)]},
 'eg_late':{'id':'자료013','times':[str(round(6.5+i*.3,3)) for i in range(31)]},
 'eg_model':{'id':'자료013','times':[str(round(12.8+i*.05,3)) for i in range(35)]},
 'jh_all':{'id':'자료005','times':[str(6+i*.5) for i in range(37)]},
 'eg_fine':{'id':'자료013','times':['0','.1','.2','.3','.4','.5','.6','.8','1','1.2','1.4','2.9','3.1','3.3','4.2','4.6','5','5.5','6','6.5','7','7.5','8','9','10','11','12','12.9','13','13.1','13.2','13.4','13.6','13.8','14','14.5','15','15.5']}}
(HERE/'groups.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
src=(HERE.parent/'phase01a-a2/extract.py').read_text(encoding='utf-8')
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',"sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase01a-a2'))\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent\nGROUPS=json.loads((OUT/'groups.json').read_text(encoding='utf-8'))")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'","OUT.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'")
line=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(line,"    group=GROUPS[phase.removesuffix('_retest')]\n    if aid!=group['id']:raise ValueError('wrong_asset_group')\n    targets=[Fraction(t) for t in group['times']]")
src=src.replace('width=1920;height=',"width=3840 if phase.startswith('eg_fine') else 1920;height=")
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:","if phase.removesuffix('_retest') not in GROUPS:")
src=src.replace("for aid in ([sys.argv[2]] if len(sys.argv)>2 else ['자료005','자료013']):","for aid in [GROUPS[phase.removesuffix('_retest')]['id']]:")
(HERE/'extract.py').write_text(src,encoding='utf-8')
print('5 bounded groups prepared; native pixels only for thin-line/detail checks')
