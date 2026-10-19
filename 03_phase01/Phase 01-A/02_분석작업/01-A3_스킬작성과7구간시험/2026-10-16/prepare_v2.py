from pathlib import Path
import shutil
B=Path(__file__).resolve().parent
S=B/'company-video-grammar-analyzer'
D=B/'company-video-grammar-analyzer-workspace/skill-candidate-v2'
shutil.copytree(S,D)
p=D/'scripts/check_observations.py';s=p.read_text(encoding='utf-8')
s=s.replace("    for o in objects:\n", "    parents={o['id']:o.get('parent') for o in objects}\n    for oid in ids:\n        visited=set();current=oid\n        while current in parents and current is not None:\n            if current in visited:\n                errors.append('parent cycle');break\n            visited.add(current);current=parents[current]\n    for o in objects:\n")
s=s.replace("            if not lo<=a<=b<=hi:errors.append('event outside window')", "            if not lo<=a<=b<=hi:errors.append('event outside window')\n            if ev['status']=='observed' and times and not any(a<=t<=b for t in times):errors.append('no evidence in event range')")
p.write_text(s,encoding='utf-8')
p=D/'SKILL.md';s=p.read_text(encoding='utf-8').replace('0.1.0-draft.1','0.1.0-draft.2');p.write_text(s,encoding='utf-8')
print('candidate v2 corrects event-reference time gap and parent cycles; v1 preserved')
