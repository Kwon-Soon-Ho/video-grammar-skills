"""Phase 00 기본 검사: v0.2 통합 기록 / v0.1 접수·이관 대기. 읽기만으로 이관하지 않는다."""
from pathlib import Path
import argparse,json,importlib.util,hashlib
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
BASE=Path(__file__).resolve().parents[1]
def load(name):
 p=BASE/'07_실행도구'/name;s=importlib.util.spec_from_file_location('phase00_entry_dep',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(rel):
 p=(BASE/rel).resolve()
 if not p.is_relative_to(BASE):raise ValueError('Phase 00 외부 참조 금지')
 return load('기록접수.py').strict_json(p.read_bytes())
def schema_errors(instance,filename):
 schema=read('04_기록규격/'+filename)
 canonical=read('04_기록규격/통합최소기록_스키마_v0.2.json')
 registry=Registry().with_resource(canonical['$id'],Resource.from_contents(canonical))
 Draft202012Validator.check_schema(schema)
 return [str(list(e.path))+': '+e.message[:400] for e in Draft202012Validator(schema,registry=registry,format_checker=FormatChecker()).iter_errors(instance)]
def validate_catalogs():return load('구형기록_보존검사.py').validate_catalogs()
def catalogs():return load('구형기록_보존검사.py').catalogs()
def inspect_record(data):
 flags={'fact_verified':False,'human_identity_verified':False,'company_approved':False,'operational_release':False}
 if not isinstance(data,dict):return {'valid':False,'status':'invalid','errors':['기록 객체 필요'],'unresolved':[],**flags}
 version=data.get('schema_version')
 if version=='0.1.0':
  intake=load('기록접수.py');legacy=load('구형기록_보존검사.py')
  try:prior_errors=legacy.validate_record(data)
  except Exception as e:prior_errors=['보존 진단 예외: '+type(e).__name__]
  return {'valid':False,'status':'needs_migration','schema_version':version,'errors':['구형 v0.1.0은 새 통합 기록으로 통과시키지 않음. 기록접수.py로 원문·누락 보존 후 명시 이관 필요.'],'unresolved':[],'legacy_shape_errors':prior_errors,'missing_or_review_items':intake.diagnose(data),'analysis_search_allowed':False,'company_rule_search_allowed':False,**flags}
 if version!='0.2.0':return {'valid':False,'status':'unsupported_version','errors':['지원하지 않는 기록 버전'],'unresolved':[],**flags}
 result=load('통합기록_규격검사.py').validate(data)
 catalog_errors=validate_catalogs();result['errors'].extend('catalog: '+e for e in catalog_errors);result['valid']=not result['errors']
 result.update({'status':'invalid' if not result['valid'] else 'draft_with_unresolved' if result['unresolved'] else 'draft_structure_pass','schema_version':version,'scope':'기록 계약의 구조/연결 검사. 실제 영상·사람 검수·회사 승인·운영 반영 아님.'})
 return result
def validate_record(data):
 """기존 list API 호환: 구조 오류만 반환. 빈 목록은 내용/회사/운영 승인이 아니다."""
 return inspect_record(data)['errors']
def inspect_file(path):
 try:
  path=Path(path).resolve();raw=path.read_bytes();data=load('기록접수.py').strict_json(raw);result=inspect_record(data)
  result['source_json_sha256']=hashlib.sha256(raw).hexdigest();return result
 except (ValueError,UnicodeError,OSError,RecursionError) as e:return {'valid':False,'status':'invalid_json_or_input','errors':['지원 파서 깊이 초과' if isinstance(e,RecursionError) else str(e)],'unresolved':[],'fact_verified':False,'human_identity_verified':False,'company_approved':False,'operational_release':False}
def save_result(output,result):
 output=Path(output).resolve();allowed=(BASE/'08_검증결과').resolve()
 if not output.is_relative_to(allowed):raise ValueError('검사 출력은 Phase 00/08_검증결과 안에 저장')
 raw=(json.dumps(result,ensure_ascii=True,indent=2,allow_nan=False)+'\n').encode('utf-8')
 if output.exists() and output.read_bytes()!=raw:output=output.with_name(output.stem+'_'+hashlib.sha256(raw).hexdigest()[:12]+output.suffix)
 load('기록접수.py').atomic_new(output,raw,BASE);return output
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--record',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 result=inspect_file(a.record or BASE/'04_기록규격/통합최소기록_설명용_v0.2.json')
 if a.output:result['saved_result_path']=str(save_result(a.output,result))
 print(json.dumps(result,ensure_ascii=True,indent=2));return 0 if result['valid'] else 2 if result['status']=='needs_migration' else 1
if __name__=='__main__':raise SystemExit(main())
