from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent/'phase01a-a2'
groups={
 'jh_detail':{'id':'자료005','times':['0','2','4','6','181/30','91/15','6.1','6.2','6.4','6.6','7.9','8.1','8.3','8.5','8.7','9','9.3','21','21.2','21.4','21.6','21.8','22','22.2','22.5','23','24']},
 'eg_title':{'id':'자료013','times':['0','.25','.5','.75','1','1.25','1.5','1.75','1.9','2','2.05','2.1','2.15','2.2','2.25','2.3','2.4','2.5','2.8','3','3.1','3.2','3.3','3.4','3.5','3.6','3.8','4']},
 'eg_screens':{'id':'자료013','times':['6.7','6.8','6.9','7','7.1','7.2','7.3','7.4','7.5','7.6','7.8','8','8.2','8.5','10.4','10.6','10.8','11','11.1','11.2','11.3','11.4','11.5','11.6','11.7','11.8','12','12.2','12.5']},
 'eg_model':{'id':'자료013','times':['12.8','12.9','13','13.1','13.2','13.3','13.4','13.5','13.6','13.8','14','14.1','14.2','14.3','14.4','14.5','14.6','14.7','14.8','14.9','15','15.1','15.2','15.3','15.4','15.5']}}
(HERE/'상세구간_선택.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
src=(BASE/'extract.py').read_text(encoding='utf-8')
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',"sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase01a-a2'))\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent\nGROUPS=json.loads((OUT/'상세구간_선택.json').read_text(encoding='utf-8'))")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'","OUT.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'")
line=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(line,"    group=GROUPS[phase.removesuffix('_retest')]\n    if aid!=group['id']:raise ValueError('wrong_group_asset')\n    targets=[Fraction(t) for t in group['times']]")
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:","if phase.removesuffix('_retest') not in GROUPS:")
src=src.replace("for aid in ([sys.argv[2]] if len(sys.argv)>2 else ['자료005','자료013']):","for aid in [GROUPS[phase.removesuffix('_retest')]['id']]:")
(HERE/'detail.py').write_text(src,encoding='utf-8')
print('prepared',list(groups))
