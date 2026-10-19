"""R4-4 copy-only 기록 접수. 구형을 분석 사실로 자동 변환하지 않는다."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,copy,importlib.util,math
BASE=Path(__file__).resolve().parents[1]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def strict_json(raw):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('중복 JSON key: '+k.encode('utf-8','backslashreplace').decode('utf-8'))
   d[k]=v
  return d
 def bad(x):raise ValueError('NaN/Infinity 금지: '+x)
 data=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=bad)
 def walk(v):
  if isinstance(v,str):v.encode('utf-8')
  elif isinstance(v,float) and not math.isfinite(v):raise ValueError('비유한 수 금지')
  elif isinstance(v,dict):
   for k,x in v.items():walk(k);walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(data);return data
def load(p):
 s=importlib.util.spec_from_file_location('intake_dependency',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def pathin(p,root=BASE):
 p=p.resolve();root=root.resolve()
 if not p.is_relative_to(root):raise ValueError('지정 Phase 00 경계 밖 경로: '+str(p))
 return p
def source_path(source_rel,base):
 if not isinstance(source_rel,str) or not source_rel:raise ValueError('출처의 정규 상대경로 필요')
 p=Path(source_rel)
 if p.anchor or p.drive or any(v in ['.','..'] for v in source_rel.replace('\\','/').split('/')) or p.as_posix()!=source_rel:raise ValueError('출처 경로는 정규 상대경로로 보존')
 result=pathin(base/p,base);rel=result.relative_to(base.resolve())
 if any(v.casefold() in ['backup','.환경','11_기록접수함','12_통합기록','__pycache__','.git'] for v in rel.parts):raise ValueError('백업/환경/보존 폴더를 출처로 재귀 접수 금지')
 return result
def atomic_new(p,raw,base=BASE):
 p=pathin(p,base);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  if p.read_bytes()!=raw:raise ValueError('원문 보존 파일 충돌: '+str(p))
  return
 # 파일을 열기 전 재확인하고 원자적 배타 생성한다. 기존 원문 덮어쓰기 없음.
 with p.open('xb') as f:f.write(raw)
def diagnose(data):
 missing=[]
 def add(pointer,reason):missing.append({'pointer':pointer,'reason':reason,'automatic_fill_allowed':False})
 if not isinstance(data,dict):add('','기록 객체가 아님');return missing
 if data.get('schema_version')!='0.1.0':add('/schema_version','지원하는 구형 v0.1.0이 아님');return missing
 asset=data.get('asset')
 if not isinstance(asset,dict):add('/asset','원본 영상 식별 자료 없음');return missing
 for k in ['id','version','sha256']:
  if not asset.get(k):add('/asset/'+k,'원본 영상 identity 미확인. JSON/파일명에서 추정 금지')
 if asset.get('duration_s') is None:add('/asset/duration_s','재생 길이와 확인 근거 미확인')
 add('/time_contract','원점·PTS·구간/프레임·근거를 새 시간 계약에 명시 연결해야 함')
 add('/targets','원본/설명 구간/화면 상태/동작·대상의 범위와 버전 연결 필요')
 add('/evidence','자료 pin·선택 부분·주장 범위/근거 역할 연결 필요')
 add('/segments/*/classification','구형 태그는 출처와 범위를 검토할 후보. 상태/관측 사실 자동 생성 금지')
 if data.get('run') is None:add('/run','실제 수행 기록 미작성. 미실행과 구분해 보존')
 add('/review','구형 검수/승인 상태는 새 통합 context로 자동 이전하지 않음')
 return missing
def proposal(raw,source_rel,role):
 source_sha=digest(raw);error=None
 try:data=strict_json(raw)
 except RecursionError:data=None;error='JSON 입력이 지원하는 파서/재귀 깊이를 초과함'
 except (ValueError,UnicodeError) as e:data=None;error=str(e).encode('utf-8','backslashreplace').decode('utf-8')
 version=data.get('schema_version') if isinstance(data,dict) else None
 missing=diagnose(data) if not error else [{'pointer':'','reason':'JSON 파싱 오류: '+error,'automatic_fill_allowed':False}]
 return {'entry_version':'0.1.0','entry_id':'INTAKE-'+digest((source_rel+'\0'+source_sha).encode('utf-8'))[:24],'source':{'path':source_rel,'sha256':source_sha,'byte_length':len(raw),'role':role,'schema_version':version if isinstance(version,str) else None,'record_id':data.get('record_id') if isinstance(data,dict) and isinstance(data.get('record_id'),str) else None,'record_version':data.get('version') if isinstance(data,dict) and isinstance(data.get('version'),str) else None},'status':'invalid_json' if error else 'legacy_requires_mapping' if version=='0.1.0' else 'requires_version_review','missing_or_review_items':missing,'snapshot':None,'source_unchanged':True,'history':[],'analysis_search_allowed':False,'company_rule_search_allowed':False,'fact_verified':False,'company_approved':False,'operational_release':False}
def receive(source,role='사용자 지정 기록',base=None):
 base=Path(base or BASE).resolve();source=pathin(Path(source),base)
 if not isinstance(role,str) or not role.strip():raise ValueError('접수 역할은 비어 있지 않은 문자열 필요')
 role.encode('utf-8')
 if not source.is_file() or source.suffix.lower()!='.json':raise ValueError('접수할 단일 JSON 파일 필요')
 rel=source.relative_to(base)
 source_path(rel.as_posix(),base)
 raw=source.read_bytes();entry=proposal(raw,rel.as_posix(),role)
 slug=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',source.stem).strip(' .')[:60] or '이름없음'
 folder=pathin(base/'11_기록접수함'/(slug+'_'+entry['entry_id'][-12:]),base)
 snapshot=folder/'원문.json';entry_path=folder/'접수기록.json'
 atomic_new(snapshot,raw,base)
 entry['snapshot']={'path':snapshot.relative_to(base).as_posix(),'sha256':digest(snapshot.read_bytes())}
 if entry['source']['sha256']!=entry['snapshot']['sha256']:raise ValueError('원문 보존 hash 불일치')
 if source.read_bytes()!=raw:raise ValueError('접수 중 원본 변경 — 판정 저장 중단')
 if entry_path.exists():
  old=strict_json(entry_path.read_bytes())
  checked=inspect_entry(old,base)
  if not checked['valid']:raise ValueError('저장 접수기록 검증 실패 — 원문을 덮어쓰지 않음: '+'; '.join(checked['errors']))
  # 동일 입력의 재실행은 불변. 이미 저장한 메타도 임의 덮어쓰지 않음.
  if old['entry_id']!=entry['entry_id'] or old['snapshot']!=entry['snapshot'] or old['source']!=entry['source']:raise ValueError('접수 메타 충돌')
  return old
 entry['history']=[{'event':'copy_only_received','at_utc':datetime.now(timezone.utc).isoformat(),'note':'원문 bytes 보존. 분석/회사 승인 이관 미수행.'}]
 checked=inspect_entry(entry,base)
 if not checked['valid']:raise ValueError('새 접수기록 검증 실패: '+'; '.join(checked['errors']))
 atomic_new(entry_path,(json.dumps(entry,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),base)
 return entry
def inspect_entry(entry,base=None):
 base=Path(base or BASE).resolve();errors=[]
 if not isinstance(entry,dict):return {'valid':False,'errors':['접수 기록 객체 필요'],'fact_verified':False,'operational_release':False}
 schema_path=base/'04_기록규격/기록접수_스키마.json'
 if not schema_path.exists():return {'valid':False,'errors':['접수 스키마가 없어 검증 보류'],'fact_verified':False,'operational_release':False}
 if schema_path.exists():
  from jsonschema import Draft202012Validator,FormatChecker
  from jsonschema.exceptions import SchemaError
  try:
   schema=json.loads(schema_path.read_text(encoding='utf-8'));Draft202012Validator.check_schema(schema)
   errors.extend('schema: '+e.message[:300] for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(entry))
  except (ValueError,UnicodeError,OSError,SchemaError,RecursionError) as e:errors.append('접수 스키마 검증 불가: '+str(e).encode('utf-8','backslashreplace').decode('utf-8'))
  if errors:return {'valid':False,'errors':errors,'fact_verified':False,'operational_release':False}
 for k in ['analysis_search_allowed','company_rule_search_allowed','fact_verified','company_approved','operational_release']:
  if entry.get(k) is not False:errors.append('접수함의 검색/승인 승격 금지: '+k)
 try:
  source_path(entry['source']['path'],base)
  path=pathin(base/entry['snapshot']['path'],base)
  if not path.is_relative_to(base/'11_기록접수함'):errors.append('접수 snapshot 위치 불일치')
  raw=path.read_bytes()
  if digest(raw)!=entry['source']['sha256'] or digest(raw)!=entry['snapshot']['sha256'] or len(raw)!=entry['source']['byte_length']:errors.append('원문 snapshot bytes/hash 불일치')
  regenerated=proposal(raw,entry['source']['path'],entry['source']['role'])
  for k in ['entry_id','source','status','missing_or_review_items']:
   if regenerated[k]!=entry[k]:errors.append('접수 판정/원문 메타 불일치: '+k)
 except (KeyError,ValueError,OSError,TypeError,UnicodeError) as e:errors.append('접수 기록 검증 실패: '+str(e).encode('utf-8','backslashreplace').decode('utf-8'))
 return {'valid':not errors,'errors':errors,'fact_verified':False,'operational_release':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--role',default='사용자 지정 기록');a=p.parse_args()
 entry=receive(a.source,a.role);print(json.dumps({'entry_id':entry['entry_id'],'status':entry['status'],'snapshot':entry['snapshot'],'missing_or_review_items':entry['missing_or_review_items'],'analysis_search_allowed':False},ensure_ascii=False,indent=2))
