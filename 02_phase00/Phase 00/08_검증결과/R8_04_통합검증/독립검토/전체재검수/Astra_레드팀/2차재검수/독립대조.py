from pathlib import Path
import json, hashlib, re, difflib
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
O=Path(__file__).parent
A=O.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=read(B/'08_검증결과/R8_04_통합검증/1차보완_확인.json')
prior={str(Path(x['path'])).lower():x['sha256'].lower() for x in read(A/'감사시작_해시.json')}
pin=read(A/'R7_기존고정입력_130건_바이트대조.json')
tech=read(A.parent/'기술과사용성/07_R8게시영수증_현재성감사.json')
checks={}
watched={}
def check(p,expected):
 actual=sha(p);watched[str(p)]=actual
 return {'path':str(p),'expected':expected,'actual':actual,'match':actual==expected}
checks['declared_changes']=[check(B/x['path'],x['after']) for x in m['changes']]
checks['change_backups']=[check(B/'backup/2026-10-15_R8_04_1차보완/변경전/Phase 00'/x['path'],x['before']) for x in m['changes'] if x['before']]
checks['sealed_reports']=[check(B/x['report'],x['expected_and_restored_sha256']) for x in m['sealed_reports']]
checks['receipts_unchanged']=[check(B/x['receipt_path'],x['current_receipt_sha256']) for x in tech]
checks['append_backups']=[check(B/x['append_version_preserved'],t['current_report_sha256']) for x,t in zip(m['sealed_reports'],tech)]
checks['original_R7_130']=[check(B/x['path'],x['expected']) for x in pin]
checks['errata_source_basis']=[]
for r in read(B/'14_스킬재구성/현재상태_정정표.json')['records']:
 for x in [r['source']]+r['basis']:
  checks['errata_source_basis'].append({'record':r['id'],**check(B/x['path'],x['sha256'])})
checks['candidate_files']=[]
changed={str((B/x['path'])).lower():x for x in m['changes']}
diffs=[]
for p in sorted((B/'06_맞춤스킬/재구성후보').rglob('*')):
 if not p.is_file(): continue
 old=prior.get(str(p).lower()); row=changed.get(str(p).lower())
 checks['candidate_files'].append({'original_sha':old,'declared_changed':bool(row),**check(p,row['after'] if row else old)})
 if row:
  bak=B/'backup/2026-10-15_R8_04_1차보완/변경전/Phase 00'/row['path']
  diffs.extend(difflib.unified_diff(bak.read_text(encoding='utf-8').splitlines(True),p.read_text(encoding='utf-8').splitlines(True),fromfile=str(bak),tofile=str(p)))
checks['links']=[]
for x in m['changes']:
 p=B/x['path']
 if p.suffix!='.md': continue
 for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if target.startswith(('http:','https:','#')): continue
  q=(p.parent/target.split('#')[0]).resolve()
  checks['links'].append({'file':x['path'],'target':target,'exists':q.exists()})
checks['scope']={'test_inputs_expected_outputs_read':False,'actual_behavior_verified':False,'whole_phase_complete':False,'D_mutations_by_this_audit':False,'all_files_read_claim':False}
checks['summary']={k:{'count':len(v),'failed':sum(not x.get('match',x.get('exists',False)) for x in v)} for k,v in checks.items() if isinstance(v,list)}
dump(O/'기계대조.json',checks)
dump(O/'재검수_관찰해시.json',watched)
(O/'후보스킬_실제변경.diff').write_text(''.join(diffs),encoding='utf-8')
print(json.dumps(checks['summary'],ensure_ascii=False))
