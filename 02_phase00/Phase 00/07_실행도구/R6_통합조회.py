"""R6-4 자료·검수 선언의 현재 연결 조회. 기존 R4/R5 계약은 변경하지 않는다."""
from pathlib import Path
import json,copy,re
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable
import R6_출처사용검사 as src
import R6_사람검수 as human

FOLDER=src.FOLDER
MANIFEST=FOLDER+'통합검수_입력고정.json'
SCHEMA=FOLDER+'통합검수_입력규격.json'
R4_REFS=['04_기록규격/'+x for x in ['통합최소기록_스키마_v0.2.json','좌표변환_스키마.json','근거주장_스키마.json','시간프레임_스키마.json']]+['07_실행도구/'+x for x in ['통합기록_규격검사.py','좌표변환_규격검사.py','근거주장_규격검사.py','시간프레임_규격검사.py']]+['01_공통용어/분류운영규칙.json']
R5_REFS=['03_한맥디자인/'+x for x in ['디자인적용_기록규격.json','회사별_디자인연결_현황.json','영상적용_예와반례.json','영상전용_미정항목.json','R5_표시_입력목록.json']]+['07_실행도구/R5_디자인적용검사.py']
OWN_REFS=[src.INDEX,src.SCHEMA,human.LEDGER,human.SCHEMA,human.CATALOG,SCHEMA,'07_실행도구/R6_출처사용검사.py','07_실행도구/R6_사람검수.py','07_실행도구/R6_통합조회.py']
def expected_paths(base):
 paths=set(src.INPUTS.values())|set(human.FIXED_INPUTS.values())|set(R4_REFS+R5_REFS+OWN_REFS)
 policies=src.read(src.local(base,human.FIXED_INPUTS['workflow_policy_links']))
 paths.update(p['source']['path'] for p in policies['entries'])
 ledger=src.read(src.local(base,human.LEDGER))
 for event in ledger['events']:
  if event['reply_evidence_pin'] is not None:
   receipt=event['reply_evidence_pin'];paths.add(receipt['path'])
   evidence=src.read(src.local(base,receipt['path']));paths.add(evidence['presented_request_snapshot']['path'])
 return sorted(paths)
def build(base):
 return {'id':'r6-integrated-review-context','version':'0.1.0','scope':'reference_and_declared_review_context_only',
         'pins':[{'path':p,'sha256':src.digest(src.local(base,p))} for p in expected_paths(base)],
         'spatial_supported_unlocked':False,'company_approved':False,'permission_granted':False,'operational_release':False}
def basic_manifest_shape(value):
 keys={'id','version','scope','pins','spatial_supported_unlocked','company_approved','permission_granted','operational_release'}
 if not isinstance(value,dict) or set(value)!=keys:raise ValueError('invalid manifest object')
 if value['id']!='r6-integrated-review-context' or value['version']!='0.1.0' or value['scope']!='reference_and_declared_review_context_only':raise ValueError('invalid manifest identity/scope')
 if any(value[k] is not False for k in ['spatial_supported_unlocked','company_approved','permission_granted','operational_release']):raise ValueError('manifest cannot create approval')
 if not isinstance(value['pins'],list) or not value['pins']:raise ValueError('invalid manifest pins')
 for p in value['pins']:
  if not isinstance(p,dict) or set(p)!=set(['path','sha256']) or not isinstance(p['path'],str) or not p['path'].strip() or not isinstance(p['sha256'],str) or re.fullmatch('[0-9a-f]{64}',p['sha256']) is None:raise ValueError('invalid file pin')
def local_schema_references_only(value):
 if isinstance(value,dict):
  for k,v in value.items():
   if k in ['$ref','$dynamicRef','$recursiveRef'] and (not isinstance(v,str) or not v.startswith('#')):raise ValueError('external schema references are not allowed')
   local_schema_references_only(v)
 elif isinstance(value,list):
  for v in value:local_schema_references_only(v)
def inspect(base):
 base=Path(base).resolve();errors=[]
 out={'valid':False,'errors':errors,'human_queue':[],'companies':[],'r4_r5_contract_references_current':False,'actual_r4_r5_records_validated':False,'actual_video_analyzed':False,'spatial_supported_unlocked':False,'identity_authenticated':False,'content_verified':False,'company_approved':False,'permission_granted':False,'operational_release':False}
 try:
  manifest,manifest_hash=src.read_snapshot(src.local(base,MANIFEST))
  basic_manifest_shape(manifest)
  if [p['path'] for p in manifest['pins']]!=expected_paths(base):errors.append('context_path_set_differs');return out
  def verify_pins():
   for p in manifest['pins']:
    if src.digest(src.local(base,p['path']))!=p['sha256']:errors.append('stale_context: '+p['path'])
  verify_pins()
  if errors:return out
  schema,schema_hash=src.read_snapshot(src.local(base,SCHEMA))
  if next(p['sha256'] for p in manifest['pins'] if p['path']==SCHEMA)!=schema_hash:errors.append('schema_changed_before_parse');return out
  if not isinstance(schema,dict):raise ValueError('schema root must be object')
  local_schema_references_only(schema);Draft202012Validator.check_schema(schema)
  # 명시적 비네트워크 registry: 외부 자원을 자동 검색/다운로드하지 않는다.
  errors.extend('schema: '+e.message for e in Draft202012Validator(schema,registry=Registry()).iter_errors(manifest))
  if errors:return out
  # 검증한 사람 대장의 동일 반환값을 사용한다. 새로 읽은 미검증 대장으로 판단하지 않는다.
  hr=human.inspect(base)
  if not hr['structural_valid']:errors.extend('human: '+e for e in hr['errors']);return out
  companies=src.read(src.local(base,human.FIXED_INPUTS['companies']))['companies']
  profile=src.read(src.local(base,human.FIXED_INPUTS['hanmac_profile']))
  rows=[r for r in hr['queue'] if r['request_id']=='R6-REQ-CI-STATUS']
  if len(rows)!=1:raise ValueError('human result requires exactly one CI status row')
  row=rows[0]
  for key in ['covered_scope_ids','unresolved_scope_ids']:
   if not isinstance(row[key],list) or not all(isinstance(v,str) and v.strip() for v in row[key]) or len(set(row[key]))!=len(row[key]):raise ValueError('invalid human scope ID list')
  if set(row['covered_scope_ids'])&set(row['unresolved_scope_ids']):raise ValueError('conflicting human scope ID lists')
  for key in ['recorded_answer_count','active_declared_answer_count']:
   if type(hr[key]) is not int or hr[key]<0:raise ValueError('invalid human answer count')
  if hr['active_declared_answer_count']>hr['recorded_answer_count']:raise ValueError('active answer count exceeds recorded count')
  current=[]
  for c in companies:
   current.append({'company_id':c['company_id'],'name_ko':c['name_ko'],
    'latest_materials':'user_statement_recorded' if c['company_id']+':latest_material' in row['covered_scope_ids'] else 'unresolved',
    'additional_ci_guide':'unresolved' if c['company_id']+':usage_guide' in row['unresolved_scope_ids'] else 'declared_response_or_non_applicability',
    'official_screen_color_or_usage_approval':False})
  # 현재 문맥과 실제 파일 확인을 반환 직전에 다시 수행한다. 원자 snapshot 보장은 아니다.
  end_source=src.inspect(base)
  if not end_source['structural_valid']:errors.extend('source_final: '+e for e in end_source['errors'])
  verify_pins()
  if src.digest(src.local(base,MANIFEST))!=manifest_hash:errors.append('manifest_changed_during_query')
  if errors:return out
  out.update(valid=True,human_queue=copy.deepcopy(hr['queue']),companies=current,r4_r5_contract_references_current=True,
   current_context_sha256=manifest_hash,recorded_answer_count=hr['recorded_answer_count'],active_declared_answer_count=hr['active_declared_answer_count'],
   hanmac_design={'profile_id':profile['profile_id'],'version':profile['version'],'source_selection':profile['source_selection'],'scope':'기존 웹 정제본. 전역 컬러 라이브러리·UI 선택 참고. 현재 웹 새 검토/모든CI규정 승인 아님.'})
 except (OSError,ValueError,TypeError,KeyError,IndexError,AttributeError,RecursionError,SchemaError,Unresolvable) as e:errors.append(type(e).__name__+': '+str(e))
 return out

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();r=inspect(args.base)
 print(json.dumps(r,ensure_ascii=True,indent=2));raise SystemExit(0 if r['valid'] else 1)
