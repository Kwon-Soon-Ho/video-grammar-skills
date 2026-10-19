"""Read-only R8 candidate/errata reference check. Not video, content, rights or adoption approval."""
from pathlib import Path
import json,hashlib,re,argparse

CONTEXT='14_스킬재구성/현재후보_입력고정.json'
FOUNDATION={
 '05_출처와검토/검수와사용범위/통합검수_입력고정.json':'257971f59f01c3e834acb4b25ee789e78872dfc7ce29960801551f3052f46a57',
 '13_품질검수/연결과인계/현재연결_입력고정.json':'99cfb91c11ef43d57f5ffc1eb5dc35f67bc4e889e75f9dd515aee3222ceda855'}
SKILLS={
 'video-knowledge-curator':['SKILL.md','references/작업기준.md','references/출력지침.md'],
 'video-record-steward':['SKILL.md','references/기록연결기준.md','references/수정과복구.md','references/보고지침.md','scripts/판본대조.py'],
 'video-guidance-reviewer':['SKILL.md','references/근거찾기와적용조건.md','references/판정과사람검수.md']}
EXTRA=['14_스킬재구성/현재상태_정정표.json','14_스킬재구성/R8_현재사용안내.md','14_스킬재구성/제한소스_보관과활용_미정.json','14_스킬재구성/검증문맥/기존문맥구조조회_영수증.json','07_실행도구/R8_후보연결확인.py','14_스킬재구성/검증문맥/구조조회_파일목록.json']
def raw(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def pairs(v):
 d={}
 for k,x in v:
  if k in d:raise ValueError('duplicate JSON key: '+k)
  d[k]=x
 return d
def read(p):return json.loads(raw(p).decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite '+x)))
def inspect(base):
 base=Path(base).resolve();errors=[];checked=[]
 def path(rel):
  if not isinstance(rel,str) or not rel or Path(rel).is_absolute():raise ValueError('relative path required')
  p=(base/rel).resolve()
  if not p.is_relative_to(base):raise ValueError('outside base: '+rel)
  return p
 def pin(rel,h):
  if not isinstance(h,str) or re.fullmatch(r'[0-9a-f]{64}',h) is None:raise ValueError('invalid SHA for '+rel)
  p=path(rel)
  if not p.is_file():errors.append('missing: '+rel);return
  got=sha(p);checked.append({'path':rel,'sha256':got,'match':got==h})
  if got!=h:errors.append('hash mismatch: '+rel)
 try:
  c=read(path(CONTEXT))
  if c.get('id')!='r8-candidate-link-context' or c.get('scope')!='R8_candidate_references_and_errata_only':raise ValueError('wrong context identity/scope')
  if not isinstance(c.get('version'),str) or re.fullmatch(r'\d+\.\d+\.\d+',c['version']) is None:raise ValueError('invalid context version')
  for k,v in {'candidate_only':True,'company_approved':False,'operational_release':False,'candidate_adopted':False}.items():
   if c.get(k) is not v:errors.append('unsupported approval/adoption flag: '+k)
  expected=set(FOUNDATION)|set(EXTRA)|{f'06_맞춤스킬/재구성후보/{name}/{rel}' for name,rels in SKILLS.items() for rel in rels}
  files=c.get('files')
  if not isinstance(files,dict) or set(files)!=expected:raise ValueError('context file set mismatch')
  for rel,h in files.items():pin(rel,h)
  if sha(Path(__file__))!=files[EXTRA[4]]:errors.append('executing checker hash mismatch')
  for rel,h in FOUNDATION.items():
   if files[rel]!=h:errors.append('historical foundation pin replacement: '+rel)
  versions=c.get('candidate_versions',{})
  if set(versions)!=set(SKILLS):errors.append('candidate version set mismatch')
  for name in SKILLS:
   txt=raw(path(f'06_맞춤스킬/재구성후보/{name}/SKILL.md')).decode('utf-8');m=re.search(r'(?m)^  version: "([^"]+)"',txt)
   if not m or versions.get(name)!=m.group(1):errors.append('candidate version mismatch: '+name)
   folder=path(f'06_맞춤스킬/재구성후보/{name}');actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
   if actual!=set(SKILLS[name]):errors.append('unexpected candidate file set: '+name)
  errata=read(path(EXTRA[0]));ids=[]
  if errata.get('id')!='r8-current-stage-errata':raise ValueError('wrong errata identity')
  if not isinstance(errata.get('records'),list) or not errata['records']:raise ValueError('missing errata records')
  for k in ['company_approved','operational_release']:
   if errata.get(k) is not False:errors.append('unsupported errata approval flag: '+k)
  for row in errata['records']:
   if not isinstance(row.get('id'),str) or not row['id']:raise ValueError('missing errata id')
   if not isinstance(row.get('basis'),list) or not row['basis']:raise ValueError('missing errata decision basis: '+row['id'])
   ids.append(row['id'])
   if row.get('semantic_contract_changed') is not False:errors.append('errata expands semantic contract: '+row['id'])
   for ref in [row['source']]+row['basis']:pin(ref['path'],ref['sha256'])
  if len(ids)!=len(set(ids)):errors.append('duplicate errata id')
  if not {'ST-R4','ST-R2','ST-R2-JSON','ST-HANDOFF','ST-R7-R8'}.issubset(set(ids)):errors.append('missing required current-stage correction')
  hold=read(path(EXTRA[2]))
  if hold.get('permission_granted') is not False or hold.get('status')!='custody_permission_unknown':errors.append('unsupported restricted-source permission claim')
  receipt=read(path(EXTRA[3]))
  if receipt.get('scope')!='unchanged_R6_R7_full_copy_structure_query_only' or receipt.get('behavior_performer_read_full_copy') is not False:errors.append('full-query receipt scope mismatch')
  checks=receipt.get('read_checks',[])
  if not isinstance(checks,list) or len(checks)!=4:errors.append('historical query receipt incomplete')
  elif {x.get('tool') for x in checks}!={'R6_출처사용검사.py','R6_사람검수.py','R6_통합조회.py','R7_연결확인.py'}:errors.append('historical query receipt duplicated or wrong tool set')
  if any(type(x.get('exit_code')) is not int or x['exit_code']!=0 or x.get('valid') is not True for x in checks):errors.append('historical query receipt invalid result/type')
  for key in ['candidate_behavior_evaluated','actual_video_analyzed','content_verified','company_approved','permission_granted','operational_release']:
   if receipt.get(key) is not False:errors.append('unsupported historical receipt claim: '+key)
  foundation_hashes=list(FOUNDATION.values())
  for key,h in [('source_R6_manifest_sha256',foundation_hashes[0]),('copy_R6_manifest_sha256',foundation_hashes[0]),('source_R7_manifest_sha256',foundation_hashes[1]),('copy_R7_manifest_sha256',foundation_hashes[1])]:
   if receipt.get(key)!=h:errors.append('receipt foundation binding mismatch: '+key)
  if receipt.get('inventory_sha256')!=files[EXTRA[5]]:errors.append('receipt inventory binding mismatch')
 except (OSError,ValueError,KeyError,TypeError,AttributeError) as e:errors.append(type(e).__name__+': '+str(e))
 return {'valid':not errors,'errors':errors,'checked':checked,'scope':'R8 candidate file/version, historical manifest hash, errata source/basis and declared prior receipt references only','R6_live_query':False,'R7_live_query':False,'behavior_or_content_verified':False,'actual_video_analyzed':False,'permission_granted':False,'company_approved':False,'candidate_adopted':False,'operational_release':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',required=True);a=p.parse_args();r=inspect(a.base);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['valid'] else 1)
