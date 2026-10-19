from pathlib import Path
import json,re,urllib.parse,hashlib
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).resolve().parent
paths=['00_시작안내.md','01_진행현황.md','14_스킬재구성/R8_현재사용안내.md']
paths += [f'08_검증결과/{s}/01_회신이후_현재안내.md' for s in ['R8_01_큐레이터','R8_02_기록관리자','R8_03_적용성검토자']]
paths += [f'06_맞춤스킬/재구성후보/{s}/SKILL.md' for s in ['video-knowledge-curator','video-record-steward','video-guidance-reviewer']]
rows=[]
for rel in paths:
 p=D/rel
 for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',line):
   u=urllib.parse.urlsplit(match[1]);
   if u.scheme or not u.path:continue
   q=(p.parent/urllib.parse.unquote(u.path)).resolve();rows.append({'source':rel,'line':n,'target':str(q),'exists':q.exists()})
context=json.loads((O/'isolated/baseline/Phase00/14_스킬재구성/현재후보_입력고정.json').read_text(encoding='utf-8'))
candidate=[]
for rel,h in context['files'].items():
 if rel.startswith('06_맞춤스킬/재구성후보/'):
  candidate.append({'path':rel,'current_D_equals_audited_C':hashlib.sha256((D/rel).read_bytes()).hexdigest()==h})
(O/'05_신규동선_실재검사.json').write_text(json.dumps({'documents':len(paths),'links':rows,'missing':[r for r in rows if not r['exists']],'candidate_inputs':candidate},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'documents':len(paths),'links':len(rows),'missing':sum(not r['exists'] for r in rows),'candidate_files':len(candidate),'candidate_match':all(r['current_D_equals_audited_C'] for r in candidate)},ensure_ascii=False))
