"""Reuse prior behavior tests against the new candidate in isolated output folders."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'skill-pattern-linking-20261019'
core=(OLD/'validate_core.py').read_text(encoding='utf-8')
core=core.replace("OUT=HERE/'validation-core-retry1'","OUT=HERE/'validation-core'")
core=core.replace("value.update(schema_version='video-observation-0.3',skill_version='0.1.0-draft.5',reuse_map=None);return render_impl(value)","value.update(schema_version='video-observation-0.4',skill_version='0.1.0-draft.7',reuse_map=None)\n    for claim in value['claims']:claim.setdefault('dimension',claim['id'])\n    return render_impl(value)")
composition=(OLD/'validate_composition.py').read_text(encoding='utf-8')
composition=composition.replace("d=load(HERE/'development/H02/observations-linked.json')","d=load(WORK/'skill-pattern-linking-20261019/development/H02/observations-linked.json')\nd.update(schema_version='video-observation-0.4',skill_version='0.1.0-draft.7')\nfor claim in d['claims']:claim.setdefault('dimension',claim['id'])")
composition=composition.replace("HERE/'knowledge/pattern-library.json'","WORK/'skill-pattern-linking-20261019/knowledge/pattern-library.json'")
composition=composition.replace("HERE/'development/H02/input-detail.json'","WORK/'skill-pattern-linking-20261019/development/H02/input-detail.json'")
for name,source in [('core',core),('composition',composition)]:
    path=HERE/('regression-'+name+'.py');path.write_text(source,encoding='utf-8')
    subprocess.run([sys.executable,str(path)],check=True)
(HERE/'regression-adaptations.json').write_text(json.dumps({'new_candidate':'draft.7','prior_suites':['38 core','34 composition'],'adaptation':'isolated output folders; preserved historical sources; composition fixture uses current schema/version and per-claim field dimensions; core renderer fixture also normalized; expected behaviors retained','independent_visual_test':False},ensure_ascii=False,indent=2),encoding='utf-8')
