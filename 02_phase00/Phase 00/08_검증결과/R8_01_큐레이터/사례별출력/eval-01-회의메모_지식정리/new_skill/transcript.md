# 실행 기록

## 범위
- 지정 task.txt와 이 run의 inputs/Phase00만 자료로 사용. 지정 실행스킬과 그 references만 실행스킬로 로드.
- 쓰기 위치: 이 run 내부의 outputs, build_and_check.py, transcript.md.
- Python: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe 만 실행. -B 및 sys.dont_write_bytecode로 입력 실행도구의 __pycache__ 생성을 막음.
- 외부 네트워크/API/AE/CU/설치 미사용. 다른 실행·부모 폴더·실제 D 프로젝트 자료 미열람. D 실행파일만 실행.
- 입력 DB의 06/08 과거평가 직접 열람 없음. 별도 R6/R7 검사를 실행하지 않음.
- 자기채점/총점 없음. 전체 작업 시간·토큰 사용량은 측정하지 않아 null. catalog_validation.json의 elapsed_seconds는 해당 함수 호출 범위에서 실제 측정한 값뿐임.

## 초기 읽기 명령과 실제 결과

### 작업 지시 확인
```powershell
Get-Content -LiteralPath 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\task.txt'
```
exit_code=0. DB 루트·입력·출력·실행스킬·지정 Python과 시험 범위 확인.

### 실행스킬 확인
```powershell
Get-Content -LiteralPath 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00\실행스킬\video-knowledge-curator\SKILL.md'
```
exit_code=0. v0.2.0-draft.1 전체 읽음.

### 스킬 참조와 입력 확인
```powershell
Get-Content -LiteralPath 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00\실행스킬\video-knowledge-curator\references\작업기준.md','C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00\실행스킬\video-knowledge-curator\references\출력지침.md','C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00\입력메모.json'
```
exit_code=0. 참조 두 파일과 합성 회의 메모 v0.1.0 5개 전체 읽음.

### 허용 디렉터리 파일 목록
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; @('01_공통용어','02_원칙과레이아웃','03_한맥디자인','04_영상분석','05_출처와검토','07_실행도구','09_다음단계인계','13_품질검수') | ForEach-Object { $p = Join-Path $db $_; if (Test-Path -LiteralPath $p) { rg --files $p } }
```
exit_code=0. 파일 목록 출력이 길어 일부 잘림. 04_영상분석은 존재하지 않아 조회 없음. 평가계획 등 파일명은 목록에 나왔으나 해당 내용은 열지 않음. 입력 06/08은 나열/열람하지 않음.

### 첫 정본 배치 읽기
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; @('01_공통용어\공통용어사전.json','01_공통용어\분류운영규칙.json','02_원칙과레이아웃\모션과정보전달원칙.json','02_원칙과레이아웃\화면설계원칙.json','02_원칙과레이아웃\레이아웃_확장후보.json') | ForEach-Object { Write-Output $_; Get-Content -LiteralPath (Join-Path $db $_) }
```
exit_code=0. 배치 출력이 잘렸으므로 전체를 확인했다고 취급하지 않음. 뒤에 필요한 항목을 선택 재조회함.

## 이후 명령과 실제 반환
아래는 실제 exec_command의 명령·종료 코드·반환 출력이다. 일부 긴 읽기 결과는 도구에서 잘린 그대로이며 전체 본문 검토로 계산하지 않았다.

### 실행 1
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; @('01_공통용어\분류운영규칙.json','02_원칙과레이아웃\모션과정보전달원칙.json','02_원칙과레이아웃\레이아웃지식.json','02_원칙과레이아웃\레이아웃_심화지식.json','03_한맥디자인\한맥디자인정본.json','05_출처와검토\출처목록.json','05_출처와검토\R3_모션_조사기록.json') | ForEach-Object { $j = Get-Content -Raw -LiteralPath (Join-Path $db $_) | ConvertFrom-Json; [PSCustomObject]@{path=$_; keys=@($j.PSObject.Properties.Name);version=$j.version} | ConvertTo-Json -Compress -Depth 5 }; Get-Content -LiteralPath (Join-Path $db '07_실행도구\지식조회.py') -TotalCount 180; Get-Content -LiteralPath (Join-Path $db '07_실행도구\자료검증.py') -TotalCount 180
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
{"path":"01_공통용어\\분류운영규칙.json","keys":["version","status","decision","taxonomy_ref","taxonomy_sha256","units","axis_units","cross_unit_policy","states","reason_codes","unclassified_policy","mapping_boundary","company_approval","claim_status_policy","evidence_rules"],"version":"0.1.1"}
{"path":"02_원칙과레이아웃\\모션과정보전달원칙.json","keys":["version","principles","default_company_requirement","overlap_policy"],"version":"0.1.2"}
{"path":"02_원칙과레이아웃\\레이아웃지식.json","keys":["version","layouts"],"version":"0.1.1"}
{"path":"02_원칙과레이아웃\\레이아웃_심화지식.json","keys":["id","version","authority","company_approved","actual_video_test","core_refs","design_reference","layout_cards","screen_cards","universal_numeric_defaults","automatic_selection","text_edit_policy"],"version":"0.1.2"}
{"path":"03_한맥디자인\\한맥디자인정본.json","keys":["schema_version","profile_id","version","retrieved_on","timezone","status","description","source_selection","sources","color_tokens","gradients","references","rules","issues","semantic_roles","loading_policy","not_defined","provenance_limit","db_contract"],"version":"0.1.0"}
{"path":"05_출처와검토\\출처목록.json","keys":["version","sources"],"version":"0.1.1"}
{"path":"05_출처와검토\\R3_모션_조사기록.json","keys":["id","version","read_on","sources","original_core_changed","decision_pending","scope","approved_change"],"version":"0.1.1"}
"""Phase 00 지식 조회. 관측·창작·자동 승인 수행하지 않음."""
from 자료검증 import catalogs, BASE
import argparse,json
def lookup(query,axis=None,include_pending=False):
    t,s,p,q,l,d=catalogs();query=query.casefold().strip();out=[]
    if not query:return out
    for r in t['terms']:
        if r['status']=='deprecated' or (axis and r['axis']!=axis):continue
        keys=[r['id'],r['name_ko'],r['name_en'],*r['aliases']]
        if any(query in x.casefold() for x in keys):
            directions={'페이드인':'enter','fade in':'enter','페이드아웃':'exit','fade out':'exit','확대':'increase','축소':'decrease'}
            out.append({'kind':'term','matched_query':query,'qualifiers':{'direction':directions.get(query,'unknown')},'data':r})
    if axis:return out
    for r in p['principles']+q['principles']+l['layouts']:
        if r['status']=='deprecated' or (not include_pending and r['status']=='needs_primary_definition_review'):continue
        if query in (r['id']+' '+r['name_ko']+' '+r['definition']).casefold():out.append({'kind':'reference_knowledge','data':r})
    return out
def palette(include_optional=False):
    d=catalogs()[-1]
    return {'profile_ref':d['profile_id']+'@'+d['version'],'colors':[x for x in d['color_tokens'] if include_optional or x['scope']=='global_color_library'],'optional_styles':d['references']+d['gradients'] if include_optional else [],'authority':'출처 선택 확인·사용 가능 컬러. 회사 문법 승인과 별개.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('query',nargs='?');p.add_argument('--axis');p.add_argument('--palette',action='store_true');p.add_argument('--include-optional',action='store_true');p.add_argument('--include-pending',action='store_true');a=p.parse_args()
    result=palette(a.include_optional) if a.palette else lookup(a.query or '',a.axis,a.include_pending)
    print(json.dumps(result,ensure_ascii=False,indent=2))
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

```

### 실행 2
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; $j=Get-Content -Raw -LiteralPath (Join-Path $db '02_원칙과레이아웃\모션과정보전달원칙.json')|ConvertFrom-Json; $j.principles|Where-Object {($_ | ConvertTo-Json -Compress -Depth 8) -match '이징|선형|전문|분절|신호|중복|초보|단계'}|ConvertTo-Json -Depth 10; $j=Get-Content -Raw -LiteralPath (Join-Path $db '01_공통용어\공통용어사전.json')|ConvertFrom-Json; $j.terms|Where-Object {$_.id -match 'LAYOUT|TIMING' -or $_.name_ko -match '선형|이징'}|Select-Object id,name_ko,definition,include_when,exclude_or_limit,status,version,source_refs|ConvertTo-Json -Depth 6; Get-Content -LiteralPath (Join-Path $db '01_공통용어\분류운영규칙.json'); Get-Content -LiteralPath (Join-Path $db '07_실행도구\구형기록_보존검사.py') -TotalCount 130
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
[
  {
    "id": "AP-02",
    "family": "animation12",
    "name_ko": "Anticipation · 예비 동작",
    "definition": "본 동작 전 준비 신호",
    "consider_when": "큰 변화의 예고로 후보. 모든 등장에 반대 움직임을 넣지 않음. 이해에 도움인가 지연인가?",
    "avoid_or_adjust_when": "정보 정확성·읽기 시간·원본 형태를 해치거나 해당맥락에무관한효과는제외",
    "analysis_observables": "본 동작 전 반대 움직임·정지·표식 등 예고 상태의 존재와 순서.",
    "planning_decisions": "큰 변화의 예고로 후보. 모든 등장에 반대 움직임을 넣지 않음. 이해에 도움인가 지연인가?를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "준비 동작이 다음 변화를 이해하게 하는가, 불필요하게 지연하는가?"
    ],
    "source_refs": [
      "SRC-ADOBE-12"
    ],
    "related_ids": [
      "MP-04"
    ],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "AP-06",
    "family": "animation12",
    "name_ko": "Slow In / Slow Out · 가속과 감속",
    "definition": "시간에 따른 이동 간격 변화",
    "consider_when": "도착·이동의 속도 성격을 관찰. 등속 전달·기계 시뮬레이션은 선형도 적합. 목적에 맞는 속도 변화인가?",
    "avoid_or_adjust_when": "정보 정확성·읽기 시간·원본 형태를 해치거나 해당맥락에무관한효과는제외",
    "analysis_observables": "추적 가능한 대상의 시간별 위치·간격 변화. 관측 부족이면 곡선 미확정.",
    "planning_decisions": "도착·이동의 속도 성격을 관찰. 등속 전달·기계 시뮬레이션은 선형도 적합. 목적에 맞는 속도 변화인가?를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "속도 변화가 전달 목적에 맞는가? 등속이 필요한 상황을 배제하지 않았는가?"
    ],
    "source_refs": [
      "SRC-ADOBE-12"
    ],
    "related_ids": [
      "MP-02"
    ],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "MP-02",
    "family": "motion10",
    "name_ko": "Eases · 이징",
    "definition": "속도 변화의 설계",
    "consider_when": "가속/감속을 목적과 연결. Bézier 피팅 결과를 원본 AE 핸들로 단정하지 않음. 출발·도착의 성격이 맞는가?",
    "avoid_or_adjust_when": "정보 정확성·읽기 시간·원본 형태를 해치거나 해당맥락에무관한효과는제외",
    "analysis_observables": "관측 변화율의 가속·감속·정착. 추적 오차와 피팅 근거.",
    "planning_decisions": "가속/감속을 목적과 연결. Bézier 피팅 결과를 원본 AE 핸들로 단정하지 않음. 출발·도착의 성격이 맞는가?를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "이징 성격이 동작 역할에 맞는가? 원본 핸들값을 복원한 것처럼 쓰지 않았는가?"
    ],
    "source_refs": [
      "SRC-JORGE-10"
    ],
    "related_ids": [
      "AP-06"
    ],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "MP-04",
    "family": "motion10",
    "name_ko": "Anticipation · 예비 동작",
    "definition": "본 동작의 준비",
    "consider_when": "큰 변화 예고에 후보. 과한 준비 동작이 시간을 소모하지 않는가?",
    "avoid_or_adjust_when": "정보 정확성·읽기 시간·원본 형태를 해치거나 해당맥락에무관한효과는제외",
    "analysis_observables": "주요 변화 앞의 준비 신호와 시간 범위.",
    "planning_decisions": "큰 변화 예고에 후보. 과한 준비 동작이 시간을 소모하지 않는가?를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "예고가 이해를 돕는가? 모든 동작에 불필요한 반동을 넣지 않았는가?"
    ],
    "source_refs": [
      "SRC-JORGE-10"
    ],
    "related_ids": [
      "AP-02"
    ],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-02",
    "family": "information",
    "name_ko": "정보 표식",
    "definition": "핵심과 구조를 식별하도록 돕는다",
    "consider_when": "강조·표식·단계번호의대상과순서",
    "avoid_or_adjust_when": "전부강조하면위계소실",
    "analysis_observables": "강조색·단계 번호·표식의 대상과 공개 순서.",
    "planning_decisions": "강조·표식·단계번호의대상과순서를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "중요한 정보와 구조를 구분하게 하는가? 모든 항목을 강조하지 않았는가?"
    ],
    "source_refs": [
      "SRC-CAM-EXTRANEOUS"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-03",
    "family": "information",
    "name_ko": "중복 조절",
    "definition": "같은 설명의 경쟁 경로를 조절한다",
    "consider_when": "화면본문·음성·그림설명의역할분담",
    "avoid_or_adjust_when": "접근성자막·무음시청·기술용어는삭제의무아님",
    "analysis_observables": "내레이션·본문·자막·도표 설명의 중복과 읽기 경쟁.",
    "planning_decisions": "화면본문·음성·그림설명의역할분담를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "경로가 역할을 분담하는가? 무음·접근성·기술 용어를 위한 문구를 지우지 않았는가?"
    ],
    "source_refs": [
      "SRC-CAM-EXTRANEOUS"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-06",
    "family": "information",
    "name_ko": "분절",
    "definition": "설명을 처리 가능한 단위로 나눈다",
    "consider_when": "단계경계·휴지·챕터·재생제어",
    "avoid_or_adjust_when": "고정MP4장면분할은학습자속도제어와같지않음",
    "analysis_observables": "장면·단계·휴지와 챕터·재생 제어의 존재를 별도 기록.",
    "planning_decisions": "단계경계·휴지·챕터·재생제어를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "복잡한 설명을 나눠 처리할 수 있는가? MP4 분할을 학습자 제어와 혼동하지 않는가?"
    ],
    "source_refs": [
      "SRC-CAM-ESSENTIAL"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-07",
    "family": "information",
    "name_ko": "사전 개념 소개",
    "definition": "본 설명 전 핵심 명칭·역할을 소개한다",
    "consider_when": "낯선기술·구조의짧은전체도·범례",
    "avoid_or_adjust_when": "전문가에게불필요한반복은줄임",
    "analysis_observables": "핵심 명칭·구성 요소·역할이 본 설명 전에 소개되는지.",
    "planning_decisions": "낯선기술·구조의짧은전체도·범례를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "시청자가 모를 개념을 준비하는가? 전문가에게 불필요한 반복은 없는가?"
    ],
    "source_refs": [
      "SRC-CAM-ESSENTIAL"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-09",
    "family": "information",
    "name_ko": "일시 정보 보완",
    "definition": "사라지는 정보를 다시 참조하도록 돕는다",
    "consider_when": "다단계도표·요약·유지·재생제어",
    "avoid_or_adjust_when": "모든동작을정지로대체하지않음",
    "analysis_observables": "앞 정보가 다음 설명에 필요한데 사라지는지, 다시 볼 수 있는 표식·누적·요약이 있는지.",
    "planning_decisions": "다단계도표·요약·유지·재생제어를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "앞 정보를 기억만 해야 하는 부담을 줄이는가? 모든 정보를 계속 남겨 과밀하게 하지 않는가?"
    ],
    "source_refs": [
      "SRC-CAM-TRANSIENT"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "IP-10",
    "family": "information",
    "name_ko": "숙련도별 설명 조정",
    "definition": "시청자의 지식에 따라 지원을 조정한다",
    "consider_when": "입력·인터뷰·검토 자료 등으로 시청자의 해당 주제 사전 지식이 확인될 때 설명 지원의 깊이를 비교한다.",
    "avoid_or_adjust_when": "직급·부서명만으로 숙련도를 결정하지 않는다. 정보 정확성·필수 고지·접근성 정보를 숙련도 이유로 삭제하지 않는다.",
    "analysis_observables": "시청자의 사전 지식은 제공 근거가 있을 때만 기록. 화면에는 개념 소개·요약의 분량과 순서를 관측하며 학습 효과는 별도 평가한다.",
    "planning_decisions": "초보자 개념 소개와 숙련자 요약을 조건부 후보로 비교한다. 숙련도 근거가 없으면 조정 판단을 보류한다.",
    "review_questions": [
      "시청자의 해당 주제 사전 지식 근거가 있는가? 공식 요약 수준의 참고를 효과 보장·회사 의무 규칙으로 확장하지 않았는가?"
    ],
    "source_refs": [
      "SRC-R3-EXPERTISE-SUMMARY"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "공개 학술 Summary에 근거한 조건부 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.2",
    "numeric_defaults": null,
    "interpretation_origin": "2021 공식 Summary 정의를 짧게 확인하고 프로젝트 적용·기권 조건을 자체 작성. 학술 장 전체·진단도구·회사 영상 효과 미검토.",
    "unknown_policy": "해당 주제 사전 지식 근거가 없으면 숙련도 unknown과 설명 조정 보류를 기록한다. 직무만으로 낮거나 높다고 단정하지 않는다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  },
  {
    "id": "MR-04",
    "family": "motion_relationship",
    "name_ko": "순차·동시 등장 선택",
    "definition": "시간으로 관계와 읽는 순서를 드러낸다",
    "consider_when": "단계공개·동시비교",
    "avoid_or_adjust_when": "항상stagger나UI시간값을강제하지않음",
    "analysis_observables": "사건별 시작·완료, 그룹·순서·중첩·누적 상태.",
    "planning_decisions": "단계공개·동시비교를 검토하되 사실·회사 필수조건을 우선.",
    "review_questions": [
      "순차 공개와 동시 비교 중 정보 관계에 맞는 방식을 골랐는가?"
    ],
    "source_refs": [
      "SRC-CARBON-CHOREO"
    ],
    "related_ids": [],
    "case_refs": [],
    "scope": "범용 참고 / 프로젝트 적용 해석",
    "status": "reference",
    "version": "0.1.1",
    "numeric_defaults": null,
    "interpretation_origin": "짧은 개념 정의와 프로젝트용 적용/제외를 자체 정리",
    "unknown_policy": "대상·시점·효과·의도 근거가 부족하면 확인 불가 또는 추론으로 기록한다.",
    "interpretation_source_refs": [
      "SRC-PROJECT-GUIDANCE"
    ]
  }
]
[
  {
    "id": "LAYOUT-SINGLE-FOCUS",
    "name_ko": "단일 초점",
    "definition": "핵심 대상·문장 중심의 구성",
    "include_when": "핵심 하나",
    "exclude_or_limit": "반드시 중앙 배치 아님",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-SPLIT-COMPARE",
    "name_ko": "분할 비교",
    "definition": "둘 이상의 대상을 공통 기준으로 나눈 구성",
    "include_when": "동등 비교",
    "exclude_or_limit": "분할이 항상 비교는 아님",
    "status": "draft",
    "version": "0.1.1",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-BEFORE-AFTER",
    "name_ko": "전후 대응",
    "definition": "같은 대상의 전후 상태를 대응한 구성",
    "include_when": "변화 설명",
    "exclude_or_limit": "서로 다른 대상의 비교와 구분",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-PROCESS-LINE",
    "name_ko": "선형 프로세스",
    "definition": "단계를 선·방향으로 연결한 구성",
    "include_when": "순서 있는 단계",
    "exclude_or_limit": "행태별 방향 속성은 별도",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-TIMELINE",
    "name_ko": "시간축",
    "definition": "실제 시간·기간에 대응한 배치",
    "include_when": "사건/기간",
    "exclude_or_limit": "영상 편집기 timeline과 문맥 구분",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-HIERARCHY",
    "name_ko": "계층 구성",
    "definition": "상하·종속 관계를 배치로 표현",
    "include_when": "계층 관계",
    "exclude_or_limit": "UI 컴포넌트 분류와 별개",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-NETWORK",
    "name_ko": "연결 구성",
    "definition": "연결·관계를 배치로 표현",
    "include_when": "관련·인과 관계",
    "exclude_or_limit": "선이 있다는 이유로 인과 확정 금지",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-OVERVIEW-DETAIL",
    "name_ko": "전체와 상세",
    "definition": "전체 맥락과 선택 부분 상세를 함께 표현",
    "include_when": "포커스 전환",
    "exclude_or_limit": "부분과 전체 관계는 따로 기록",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-SPACE-CALLOUT",
    "name_ko": "공간과 설명 표식",
    "definition": "지도·구조·공간 대상에 명칭·주석을 연결",
    "include_when": "위치·시설 설명",
    "exclude_or_limit": "이소메트릭은 투영 속성",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-DATA-CHART",
    "name_ko": "데이터 시각화",
    "definition": "데이터 관계를 차트로 구성",
    "include_when": "수치·분포·관계",
    "exclude_or_limit": "차트 유형·데이터 의미 별도",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-UI-ANNOTATION",
    "name_ko": "실제 UI와 설명",
    "definition": "제품 화면과 설명·초점·표식을 결합",
    "include_when": "SW 데모",
    "exclude_or_limit": "가상 UI를 실제 제품이라고 기록 금지",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-CARD-GROUP",
    "name_ko": "카드 그룹",
    "definition": "독립 항목들을 카드 형상으로 묶음",
    "include_when": "병렬·단계·비교",
    "exclude_or_limit": "카드와 다른 레이아웃 복합 가능",
    "status": "draft",
    "version": "0.1.0",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-SPLIT",
    "name_ko": "분할 구성",
    "definition": "서로 다른 역할의 화면 영역을 나눈 구성",
    "include_when": "영상+설명·주대상+지원 정보",
    "exclude_or_limit": "분할만으로 비교 의미를 확정하지 않음",
    "status": "draft",
    "version": "0.1.1",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  },
  {
    "id": "LAYOUT-PIP",
    "name_ko": "화면 속 화면",
    "definition": "주 화면 안에 별도 화면을 중첩",
    "include_when": "중첩 설명·데모",
    "exclude_or_limit": "정보 관계·주보조 역할 별도",
    "status": "draft",
    "version": "0.1.1",
    "source_refs": [
      "SRC-PROJECT-TAXONOMY"
    ]
  }
]
{
  "version": "0.1.1",
  "status": "project_draft",
  "decision": "사용자A안확정 2026-10-14",
  "taxonomy_ref": "company-video-taxonomy@0.1.1",
  "taxonomy_sha256": "c71ec597b924bd6da69fdfeb4635e290de75823186fbf7236b9615d613c6c7b2",
  "units": [
    {
      "id": "asset",
      "name_ko": "영상 전체",
      "meaning": "하나의제공영상·해당버전전체",
      "boundary": "파일/버전/편집본이달라지면R1자산참조로구분",
      "example": "한편의기술설명영상",
      "counterexample": "한장의대표이미지만보고전체유형확정",
      "existing_field": "asset; 현재classification은segments에있어전체분류필드는R4연결검토"
    },
    {
      "id": "segment",
      "name_ko": "설명 구간",
      "meaning": "하나의설명질문/정보주제를이루는시간범위",
      "boundary": "주요설명대상/질문/단계주제가바뀌면경계후보; 컷전환만으로강제분리하지않음",
      "example": "침투수발생원인설명구간; 그안에전체/확대화면포함",
      "counterexample": "아이콘이한번나타날때마다새장면으로분리",
      "existing_field": "segments; 논리구간이촬영scene/편집clip과같지않음"
    },
    {
      "id": "state",
      "name_ko": "화면 상태",
      "meaning": "식별가능한정보관계/구성요소배치가유지되는관측범위",
      "boundary": "새정보역할/비교패널/주석대상/구성이변하면후보. 배경입자움직임이나한프레임마다분리하지않음",
      "example": "제목만있는상태→제목과도표가있는상태",
      "counterexample": "움직임이있다는이유로화면상태를정의할수없다고처리",
      "existing_field": "현재명시필드없음. 프레임은표본일뿐화면상태와같지않음; R4에서구조연결"
    },
    {
      "id": "beat",
      "name_ko": "짧은 동작",
      "meaning": "대상/시간범위가분명한변화동작또는유지·정지등의미있는시간사건. 짧은동작이라는이름이고정최대길이를뜻하지않음.",
      "boundary": "같은대상의연관변화는묶을수있고다른대상의동작은동시/중첩허용. 화면상태의경계를가로지를수있음",
      "example": "도표공개와강조표시가겹쳐발생",
      "counterexample": "마지막정지이미지로등장방식/속도곡선확정",
      "existing_field": "segments[].beats; 상태참조/전역동작의필드연결은R4검토"
    }
  ],
  "axis_units": {
    "video_type": [
      "asset",
      "segment"
    ],
    "communication_purpose": [
      "segment",
      "state",
      "beat"
    ],
    "information_relation": [
      "segment",
      "state"
    ],
    "layout": [
      "state"
    ],
    "motion_function": [
      "beat"
    ],
    "motion_property": [
      "beat"
    ],
    "timing": [
      "beat"
    ],
    "art_direction": [
      "state",
      "segment"
    ]
  },
  "cross_unit_policy": "4단위는단순배타트리가아니다. 동작이화면상태를가로지를수있다. 서로다른범위의태그를자동합산/상속하지않는다. 컷표식은관측된보조정보. 겹친상태/분할영역은대상범위로구분.",
  "states": [
    "classified",
    "unknown",
    "not_applicable",
    "other_candidate",
    "not_assessed"
  ],
  "reason_codes": [
    "insufficient_temporal_evidence",
    "scope_unknown",
    "ambiguous_visual_evidence",
    "missing_context",
    "implementation_unknown",
    "outside_vocabulary",
    "not_applicable_to_scope",
    "not_assessed_yet"
  ],
  "unclassified_policy": "classified만현재유효용어ID를저장. 나머지는빈term_ids+이유. other_candidate는자유후보문구를별도로남기고즉시정본ID를발명하지않음.",
  "mapping_boundary": "R2연습기록은별도계약. 기존R4최소기록의classification배열/asset/segments/frames/beats필드를바꾸지않는다. null은의미상미판정이며배열자리에null을쓰는구현지시가아님.",
  "company_approval": false,
  "claim_status_policy": "판정상태는특정대상·범위·주장에대한것. 관측이충분하고구현만모르면관측태그는classified로유지하고구현주장을별도unknown으로남긴다. 관측대상/시간/량자체가부족하면unknown. 원본/출처가정의에필수인opacity/photo/실제UI는해당근거없으면기권.",
  "evidence_rules": {
    "whole_content_or_declared_context": {
      "requires": [
        "전체/해당구간의내용 또는 범위가확인된기획맥락"
      ],
      "limit": "일부프레임을전체유형으로자동상속하지않음. 기획맥락과실제완성영상의일치는별도."
    },
    "visible_scope_and_message_context": {
      "requires": [
        "대상화면/구간 또는 명시한시나리오범위",
        "표현된의미의근거"
      ],
      "limit": "계획/시나리오뿐이면계획된표현의후보. 실제렌더관측/제작자확인의도/현실사실로승격하지않음."
    },
    "temporal_change_plus_message_context": {
      "requires": [
        "대상과시간변화/유지의관측범위",
        "표현된기능의의미근거"
      ],
      "limit": "정지프레임/기획문장만으로실제모션기능을관측했다고판정하지않음."
    },
    "visible_scope": {
      "requires": [
        "대상/영역이확인된화면근거"
      ],
      "limit": "실제레이아웃관측에는화면이필요. 문장뿐이면계획/추론후보. 제작툴/원본지오메트리는별도."
    },
    "visible_ui_scope_and_verified_capture_source": {
      "requires": [
        "범위내UI화면",
        "확인가능한실제제품캡처출처"
      ],
      "limit": "UI처럼보이는모형이나기획문구는실제UI출처증거아님."
    },
    "visible_material_and_verified_photo_source": {
      "requires": [
        "범위내재료",
        "확인가능한촬영/사진출처"
      ],
      "limit": "사실적외관/합성조건/추정은촬영출처를대체하지않음."
    },
    "source_value_or_conditioned_opacity_estimate": {
      "requires": [
        "원본opacity속성 또는 합성조건/근거/불확실성을명시한수치추정"
      ],
      "limit": "보이는정도변화만으로정확한opacity값/알고리즘확정하지않음."
    },
    "quantity_and_temporal_samples": {
      "requires": [
        "같은대상과동일관측량",
        "시간표본과방향/속도크기구분"
      ],
      "limit": "개념적곡선후보이지원본키프레임/베지어값확정아님. 반전/시점/추적오차는한계로남김."
    },
    "tracked_target_and_temporal_scope": {
      "requires": [
        "대상/영역범위",
        "변화또는무변화를확인하는시간근거"
      ],
      "limit": "단일프레임에서등장/정지구간/순서/원본구현을확정하지않음."
    }
  }
}
"""구형 v0.1 보존 진단용. 현재 DB 통과/분석/승인에 사용하지 않음. 원문은 backup에 보존."""
from pathlib import Path
import argparse, json, hashlib, math
from jsonschema import Draft202012Validator, FormatChecker

BASE=Path(__file__).resolve().parents[1]
def read(rel): return json.loads((BASE/rel).read_text(encoding='utf-8'))
def schema_errors(instance, filename):
    schema=read('04_기록규격/'+('구형최소기록_스키마_v0.1.json' if filename=='최소기록_스키마.json' else filename))
    Draft202012Validator.check_schema(schema)
    return [('/'.join(map(str,e.path))+': '+('수치 추정 규격: ' if 'measurement' in e.path or (e.validator=='required' and 'measurement' in e.message) else '')+e.message) for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(instance)]
def catalogs():
    t=read('01_공통용어/공통용어사전.json')
    s=read('05_출처와검토/출처목록.json')
    p=read('02_원칙과레이아웃/모션과정보전달원칙.json')
    q=read('02_원칙과레이아웃/화면설계원칙.json')
    l=read('02_원칙과레이아웃/레이아웃지식.json')
    d=read('03_한맥디자인/한맥디자인정본.json')
    return t,s,p,q,l,d
def unique(items, label, errors):
    ids=[x['id'] for x in items]
    if len(set(ids))!=len(ids):errors.append(label+' ID 중복')
def finite(value, errors):
    if isinstance(value,float) and not math.isfinite(value):errors.append('NaN/Infinity는 기록 값이 아님')
    elif isinstance(value,dict):
        for v in value.values():finite(v,errors)
    elif isinstance(value,list):
        for v in value:finite(v,errors)
def validate_catalogs():
    t,s,p,q,l,d=catalogs();errors=[]
    for x,sch in [(t,'공통용어_스키마.json'),(s,'출처목록_스키마.json'),(p,'원칙지식_스키마.json'),(q,'원칙지식_스키마.json'),(l,'레이아웃지식_스키마.json')]:
        errors.extend(schema_errors(x,sch));finite(x,errors)
    if errors:return errors
    sources={x['id'] for x in s['sources']};axes={x['id'] for x in t['axes']};terms={x['id']:x for x in t['terms']}
    knowledge=p['principles']+q['principles']+l['layouts'];known={x['id'] for x in knowledge}
    for rows,label in [(t['terms'],'용어'),(s['sources'],'출처'),(knowledge,'지식')]:unique(rows,label,errors)
    for term in t['terms']:
        if term['axis'] not in axes:errors.append('없는 분류축: '+term['id'])
        for key in ['parent_id','replaced_by']:
            if term.get(key) and term[key] not in terms:errors.append('없는 용어 연결: '+term['id'])
        if term['parent_id'] and terms[term['parent_id']]['axis']!=term['axis']:errors.append('서로 다른 축의 상위 용어: '+term['id'])
        if term['status']=='deprecated' and not term['replaced_by']:errors.append('폐기 용어의 대체 없음: '+term['id'])
    for item in list(terms.values())+knowledge:
        for key in ['source_refs','interpretation_source_refs','application_reference_refs']:
            for ref in item.get(key,[]):
                if ref not in sources:errors.append('없는 출처: '+ref)
        for ref in item.get('related_ids',[]):
            if ref not in known and ref not in terms:errors.append('없는 관련 항목: '+ref)
    for item in l['layouts']:
        if item['term_id'] not in terms or terms[item['term_id']]['axis']!='layout':errors.append('레이아웃의 용어 연결 불일치')
    current_colors=[x for x in d['color_tokens'] if x['scope']=='global_color_library']
    if len(current_colors)!=30:errors.append('기존 한맥 전역 컬러 30개 불일치')
    tokenids={x['id'] for x in d['color_tokens']}
    for role in d['semantic_roles']:
        if role['token_id'] not in tokenids:errors.append('한맥 역할의 토큰 없음')
    if d['source_selection']['ui_mandatory'] is not False:errors.append('UI가 필수로 승격됨')
    return errors
def validate_record(r):
    errors=schema_errors(r,'최소기록_스키마.json');finite(r,errors)
    if errors:return errors
    t,s,p,q,l,d=catalogs();terms={x['id']:x for x in t['terms']};sources={x['id'] for x in s['sources']}
    scenarios={x['id'] for x in r['scenario_segments']};evidence={x['id']:x for x in r['evidence']}
    frames={x['id']:x for seg in r['segments'] for x in seg['frames']}
    ids=[r['asset']['id']]+[x['id'] for x in r['scenario_segments']]+[x['id'] for x in r['evidence']]+[x['id'] for x in r['claims']]+[x['id'] for x in r['segments']]+[x['id'] for seg in r['segments'] for x in seg['frames']]+[x['id'] for seg in r['segments'] for x in seg['beats']]
    if len(ids)!=len(set(ids)):errors.append('기록 내부 ID 중복')
    synthetic=r['asset']['source_type']=='synthetic_example'
    if r['taxonomy_ref']!=t['taxonomy_id']+'@'+t['version']:errors.append('분류 사전 버전 불일치')
    if r['design']['profile_ref']!=d['profile_id']+'@'+d['version']:errors.append('한맥 프로필 버전 불일치')
    tokens={x['id']:x for x in d['color_tokens']};styles={x['id'] for x in d['references']}|{x['id'] for x in d['gradients']}
    for role,token in r['design']['palette_role_bindings'].items():
        if token not in tokens:errors.append('없는 한맥 토큰: '+token)
        elif tokens[token]['scope']!='global_color_library':errors.append('선택 알파를 전역 단색처럼 연결: '+token)
    for ref in r['design']['optional_style_refs']:
        if ref not in styles:errors.append('없는 선택 스타일: '+ref)
    for override in r['design']['project_overrides']:
        if synthetic and override['review_state']=='approved':errors.append('설명용 예의 override 승인 금지')
    def time_check(period,label):
        start,end=period['start_s'],period['end_s']
        if start is not None and end is not None and end<start:errors.append(label+' 종료가 시작보다 빠름')
        if (start is None)!=(end is None):errors.append(label+' 시간 범위 반쪽만 입력')
        if start is not None and period['time_basis']=='unknown':errors.append(label+' 수치 시간의 기준 미기록')
        duration=r['asset']['duration_s']
        if end is not None and duration is not None and end>duration:errors.append(label+' 원본 길이 초과')
    def refs_check(refs):
        for ref in refs:
            if ref not in evidence:errors.append('없는 근거: '+ref)
    def measurement_check(item,label):
        v=item.get('measurement')
        if not isinstance(v,dict) or not all(k in v for k in ['method','quantity','unit','value','uncertainty','source_frame_refs','limitations','assumptions']):errors.append(label+' 수치 추정의 방법·단위·불확실성·근거 부족');return
        if not v['source_frame_refs'] or any(ref not in frames or frames[ref]['kind']!='extracted' for ref in v['source_frame_refs']):errors.append(label+' 수치 추정의 추출 프레임 근거 없음')
        if v['quantity']=='opacity_estimate' and not v['assumptions']:errors.append(label+' opacity 합성 조건 미기록')
    def supported(item,label):
        mode=item['support_mode'];refs_check(item['evidence_refs'])
        if mode in ['rendered_observation','numerical_estimate','scenario_supported','intent_confirmed'] and not item['evidence_refs']:errors.append(label+' 확인 주장에 근거 없음')
        if mode=='rendered_observation':
            if synthetic:errors.append('설명용 예는 원본 관측이 아님')
            valid=[]
            for ref in item['evidence_refs']:
                e=evidence.get(ref,{})
                if e.get('kind')=='frame':
                    f=frames.get(e.get('target_id'))
                    valid.append(bool(f and f['kind']=='extracted' and f['path'] and f['source_pts'] is not None and f['time_base']))
                elif e.get('kind')=='clip':
                    valid.append(bool(e.get('target_id') in {seg['id'] for seg in r['segments']} and e.get('sha256') and e.get('period',{}).get('start_s') is not None))
            if not any(valid):errors.append(label+' 렌더 관측에 실제 추출 프레임/클립 대상 연결 없음')
        if mode=='intent_confirmed' and not any(evidence.get(ref,{}).get('kind') in ['creator_confirmation','project_document'] for ref in item['evidence_refs']):errors.append(label+' 의도 확인의 제작자/기획 근거 없음')
        if mode=='scenario_supported':
            if not any(evidence.get(ref,{}).get('kind')=='script' and evidence.get(ref,{}).get('target_id') in scenarios and next(x for x in r['scenario_segments'] if x['id']==evidence[ref]['target_id'])['kind'] in ['original_scenario','transcript'] for ref in item['evidence_refs']):
                errors.append(label+' 시나리오 지원의 원문/전사 대상 근거 없음')
        if mode=='numerical_estimate':measurement_check(item,label)
    if not synthetic and (not r['asset']['path'] or not r['asset']['sha256']):errors.append('실제 자산 경로·해시 미기록')
    for x in r['scenario_segments']:
        time_check(x['period'],'시나리오')
        if x['source_ref'] not in sources:errors.append('시나리오 출처 없음')
    for e in evidence.values():
        if e['source_ref'] not in sources:errors.append('근거 출처 없음')
        if not synthetic and e['kind']=='example_description':errors.append('실제 사례에 설명용 근거 사용')
        if e['kind']=='frame' and (e.get('target_id') not in frames or frames.get(e.get('target_id'),{}).get('kind')!='extracted'):errors.append('프레임 근거의 원본 추출 대상 없음')
        if e['kind']=='clip' and e.get('target_id') not in {seg['id'] for seg in r['segments']}:errors.append('클립 근거의 구간 대상 없음')
        if e['kind']=='script' and e.get('target_id') not in scenarios:errors.append('시나리오 근거의 대상 없음')
    for seg in r['segments']:
        time_check(seg['period'],'구간')
        for ref in seg['scenario_refs']:
            if ref not in scenarios:errors.append('구간 시나리오 연결 없음')
        for axis,refs in seg['classification'].items():
            if axis not in {a['id'] for a in t['axes']}:errors.append('없는 분류축: '+axis)
            for ref in refs:
                if ref not in terms or terms[ref]['axis']!=axis:errors.append('분류 용어·축 불일치: '+ref)
                elif terms[ref]['status']=='deprecated':errors.append('폐기 용어 신규 사용: '+ref)
        if not any(seg['classification'].values()) and not seg['unclassified_reason']:errors.append('미분류 이유 없음')

```

### 실행 3
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; @('02_원칙과레이아웃\레이아웃지식.json','02_원칙과레이아웃\레이아웃_심화지식.json','03_한맥디자인\한맥디자인정본.json','05_출처와검토\R3_모션_조사기록.json') | ForEach-Object { $j=Get-Content -Raw -LiteralPath (Join-Path $db $_)|ConvertFrom-Json; Write-Output $_; if ($j.layouts) {$j.layouts|Where-Object {$_.term_id -match 'CARD|PROCESS|NETWORK|SPLIT-COMPARE'}|ConvertTo-Json -Depth 8 -Compress}; if ($j.layout_cards) {$j.layout_cards|Where-Object {($_|ConvertTo-Json -Depth 8 -Compress) -match 'CARD|PROCESS|NETWORK|番号|번호|반복'}|ConvertTo-Json -Depth 8 -Compress}; if ($j.profile_id) {$j|Select-Object profile_id,version,status,source_selection,rules,issues,semantic_roles,not_defined,provenance_limit|ConvertTo-Json -Depth 12 -Compress}; if ($j.read_on) {$j|ConvertTo-Json -Depth 10 -Compress} }; Get-Content -LiteralPath (Join-Path $db '09_다음단계인계\R5_디자인연결_인계.md'); Get-Content -LiteralPath (Join-Path $db '05_출처와검토\스킬심층검토\05_세스킬_이식설계안.md')
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
02_원칙과레이아웃\레이아웃지식.json
[{"id":"KNOW-LAYOUT-SPLIT-COMPARE","term_id":"LAYOUT-SPLIT-COMPARE","name_ko":"분할 비교","definition":"둘 이상의 대상을 공통 기준으로 나눈 구성","fit_conditions":"동등 비교","limits":"분할이 항상 비교는 아님","variant_dimensions":["요소 수","문구 길이","출력 비율","정보 관계","읽기·유지 시간"],"source_refs":["SRC-PROJECT-TAXONOMY"],"related_ids":["SCREEN-HIERARCHY","SCREEN-TYPE-KO","SCREEN-TIME-READ"],"company_examples":[],"status":"reference","version":"0.1.1","application_reference_refs":["SRC-IMPECCABLE"]},{"id":"KNOW-LAYOUT-PROCESS-LINE","term_id":"LAYOUT-PROCESS-LINE","name_ko":"선형 프로세스","definition":"단계를 선·방향으로 연결한 구성","fit_conditions":"순서 있는 단계","limits":"행태별 방향 속성은 별도","variant_dimensions":["요소 수","문구 길이","출력 비율","정보 관계","읽기·유지 시간"],"source_refs":["SRC-PROJECT-TAXONOMY"],"related_ids":["SCREEN-HIERARCHY","SCREEN-TYPE-KO","SCREEN-TIME-READ"],"company_examples":[],"status":"reference","version":"0.1.1","application_reference_refs":["SRC-IMPECCABLE"]},{"id":"KNOW-LAYOUT-NETWORK","term_id":"LAYOUT-NETWORK","name_ko":"연결 구성","definition":"연결·관계를 배치로 표현","fit_conditions":"관련·인과 관계","limits":"선이 있다는 이유로 인과 확정 금지","variant_dimensions":["요소 수","문구 길이","출력 비율","정보 관계","읽기·유지 시간"],"source_refs":["SRC-PROJECT-TAXONOMY"],"related_ids":["SCREEN-HIERARCHY","SCREEN-TYPE-KO","SCREEN-TIME-READ"],"company_examples":[],"status":"reference","version":"0.1.1","application_reference_refs":["SRC-IMPECCABLE"]},{"id":"KNOW-LAYOUT-CARD-GROUP","term_id":"LAYOUT-CARD-GROUP","name_ko":"카드 그룹","definition":"독립 항목들을 카드 형상으로 묶음","fit_conditions":"병렬·단계·비교","limits":"카드와 다른 레이아웃 복합 가능","variant_dimensions":["요소 수","문구 길이","출력 비율","정보 관계","읽기·유지 시간"],"source_refs":["SRC-PROJECT-TAXONOMY"],"related_ids":["SCREEN-HIERARCHY","SCREEN-TYPE-KO","SCREEN-TIME-READ"],"company_examples":[],"status":"reference","version":"0.1.1","application_reference_refs":["SRC-IMPECCABLE"]}]
02_원칙과레이아웃\레이아웃_심화지식.json
[{"id":"KNOW-LAYOUT-PROCESS-LINE","term_id":"LAYOUT-PROCESS-LINE","name_ko":"선형 프로세스","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"단계를 선·방향으로 연결한 구성","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":["REL-ORDER"],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"업무·공정 단계의 순서가 의미를 가지며 분기가 주요 내용이 아닐 때","reading_order":"시작 조건→단계와 연결 방향→종료·산출물","composition_decisions":"단계 이름과 화살표가 실제 절차를 표현하게 하고 현재 단계와 전체 진행 위치를 구분한다.","positive_example":"접수→검토→승인 흐름을 단계 이름·방향과 함께 표현한다.","counterexample":"자료 공개 순서만 보고 실제 업무가 그 순서라고 연결하거나 분기·회귀를 숨긴다.","acceptable_variation":"한 방향 선은 순서일 수 있으나 반드시 시간 길이를 나타내지는 않는다.","alternative_when":"실제 기간이면 시간축, 조건 분기가 중요하면 연결 구성·확장 후보를 검토한다.","korean_text_adjustment":"긴 단계명을 축약할 때 의미를 검토하고 작은 단위 설명은 현재 단계에 가까이 둔다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"수직 재배열 시 단계 번호·방향을 유지한다. 폭이 좁다고 순서를 뒤집지 않는다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"시나리오의 선후·분기 근거가 없으면 절차 순서를 확정하지 않는다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false},{"id":"KNOW-LAYOUT-HIERARCHY","term_id":"LAYOUT-HIERARCHY","name_ko":"계층 구성","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"상하·종속 관계를 배치로 표현","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":["REL-HIERARCHY"],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"상하·종속·구성의 위계가 자료로 확인됐을 때","reading_order":"최상위 의미→부모/자식 연결→필요한 하위 항목","composition_decisions":"같은 수준과 상하 수준을 배치·선·명칭으로 구분한다. 단순 중요도 위계와 실제 조직 위계를 나눈다.","positive_example":"문서에 확인된 부서와 팀의 상하 관계를 연결한다.","counterexample":"8개 가족사를 이름 확인만으로 모회사·자회사 조직도에 배치한다.","acceptable_variation":"같은 크기의 카드로 하위 항목을 표현할 수 있으나 카드 모양이 종속 관계의 근거는 아니다.","alternative_when":"다중 관계·회귀가 있으면 연결 구성, 단순 동등 항목이면 카드·분할을 검토한다.","korean_text_adjustment":"긴 법인명은 공식명을 보존하고 약칭은 확인 후 사용한다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"하위 그룹을 나누고 상위 위치 표식을 반복하되 실제 부모를 바꾸지 않는다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"실제 종속·소유·조직 관계 출처가 없으면 계층 주장과 배치 후보를 분리한다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false},{"id":"KNOW-LAYOUT-NETWORK","term_id":"LAYOUT-NETWORK","name_ko":"연결 구성","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"연결·관계를 배치로 표현","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":["REL-CORRELATION","REL-CAUSE","REL-SPACE"],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"여러 대상 사이의 관계·흐름·인과가 설명의 대상일 때","reading_order":"노드의 의미→선/방향 범례→핵심 연결→다른 관계","composition_decisions":"선 종류·방향·라벨로 관계를 표시한다. 겹침을 줄이되 위치가 실제 공간인지 개념 배치인지 나눈다.","positive_example":"시나리오가 설명하는 침투 경로와 압력 관계를 관계 라벨이 있는 연결도로 표현한다.","counterexample":"관련 선 하나를 그렸다는 이유로 과학적 인과가 증명됐다고 기록한다.","acceptable_variation":"관계를 강조한 개념 위치는 허용하지만 실제 시설 위치와 혼동되면 별도 공간도로 둔다.","alternative_when":"직선 순서가 중심이면 프로세스, 실제 위치가 중심이면 공간 표식을 검토한다.","korean_text_adjustment":"노드명·선의 관계명·단위를 분리하고 교차선의 설명이 어느 선에 붙는지 확인한다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"부분 연결을 나눌 때 전체 맥락·공유 노드 식별·돌아가는 연결을 유지한다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"관계 종류·방향·실제 인과 근거가 없으면 관련이라는 관측과 인과 주장을 구분한다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false},{"id":"KNOW-LAYOUT-SPACE-CALLOUT","term_id":"LAYOUT-SPACE-CALLOUT","name_ko":"공간과 설명 표식","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"지도·구조·공간 대상에 명칭·주석을 연결","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":["REL-SPACE","REL-PART"],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"위치·시설·부품과 명칭의 대응이 중요한 경우","reading_order":"기준 공간→대상 위치→라벨·주석→관계 설명","composition_decisions":"라벨을 대응 대상에 가깝게 두고 혼잡하면 리더라인을 사용한다. 실측 좌표·개념도·투영을 구분한다.","positive_example":"시설 도면의 대상에 번호와 명칭을 연결하고 중첩 라벨을 분산한다.","counterexample":"보기 좋게 하려고 실제 위치를 옮기거나 연결선이 다른 시설을 가리킨다.","acceptable_variation":"이소메트릭·정면·실사 위 주석은 표현 속성이며 그 자체로 새로운 레이아웃 이름은 아니다.","alternative_when":"세부 확대가 중심이면 전체/상세, 비공간 관계는 연결 구성을 검토한다.","korean_text_adjustment":"긴 기술명은 라벨 영역을 늘리거나 번호+범례로 분담하고 부위 이름을 임의 줄이지 않는다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"같은 공간을 유지할지 상세 뷰로 분절할지 선택하고 실제 위치 이동은 피한다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"위치·좌표·도면 버전·라벨 대응이 없으면 실측 공간 정확성을 주장하지 않는다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false},{"id":"KNOW-LAYOUT-CARD-GROUP","term_id":"LAYOUT-CARD-GROUP","name_ko":"카드 그룹","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"독립 항목들을 카드 형상으로 묶음","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":["REL-PARALLEL","REL-ORDER"],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"같은 역할의 독립 항목을 반복 구조로 묶으면 읽기에 도움이 될 때","reading_order":"그룹 제목→항목 명칭→공통 역할 정보→차이","composition_decisions":"카드의 경계가 그룹을 돕는지 확인한다. 같은 역할은 같은 정보 순서, 서로 다른 관계는 연결·배치로 표현한다.","positive_example":"동등한 사업 분야를 명칭·대표 이미지·짧은 설명이 같은 순서인 카드로 정리한다.","counterexample":"한 과정의 원인·결과를 독립 카드로 떼어 놓아 관계를 숨기거나 카드 자체를 항상 금지한다.","acceptable_variation":"카드 안에 차트·단계·비교가 있을 수 있다. 카드라는 모양과 관계를 분리한다.","alternative_when":"관계선이 핵심이면 연결 구성, 긴 정밀 비교는 표 후보, 핵심 하나면 단일 초점을 검토한다.","korean_text_adjustment":"긴 카드 제목은 영역·줄바꿈을 조절하고 한 카드만 작은 글자를 쓰지 않는다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"개수를 줄여 구간을 나눌 수 있으나 항목이 동등하다는 역할과 전체 개수를 잃지 않는다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"독립·동등한 항목인지 불분명하면 반복 모양만 관측하고 정보 관계는 보류한다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY","SRC-L2-NNG-REGION"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"},{"source_id":"SRC-L2-NNG-REGION","locator":"Definition / grouping by boundaries"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false},{"id":"KNOW-LAYOUT-SPLIT","term_id":"LAYOUT-SPLIT","name_ko":"분할 구성","status":"draft","company_approved":false,"definition_origin":"SRC-PROJECT-TAXONOMY","definition":"서로 다른 역할의 화면 영역을 나눈 구성","application_origin":"project_synthetic_transfer_not_source_example","fit_relation_ids":[],"relation_policy":"조건부 선택 후보. 모양만으로 정보 관계를 자동 부여하지 않음.","fit_when":"화면과 설명 등 서로 다른 역할을 나눠 동시에 참조할 필요가 있을 때","reading_order":"주 대상→연결된 설명→필요한 추가 맥락","composition_decisions":"영역의 읽는 역할과 대응을 명확히 한다. 같은 폭·다른 폭을 역할에 따라 후보로 둔다.","positive_example":"공법 단면도 옆에 해당 부위의 설명을 두고 색·번호로 대응한다.","counterexample":"왼쪽은 A 공법 사진, 오른쪽은 회사 소개문인데 비교 화면이라고 한다.","acceptable_variation":"반반 배치 자체가 비교는 아니다. 동등 비교 항목이 확인되면 비교 태그를 추가한다.","alternative_when":"전체/부분 동일성이 있으면 전체/상세, 작은 중첩이면 PIP를 검토한다.","korean_text_adjustment":"긴 본문은 요점·지원 정보를 나누되 사실과 필수 정보는 임의 삭제하지 않는다.","landscape_adjustment":"내용 역할을 나눈 영역의 폭을 조절한다. 화면 전체를 꽉 채울 의무는 없다. 핵심·단위·출처가 읽히는 완성 상태를 확인한다.","portrait_adjustment":"상하 재배열에서 그림과 설명의 대응을 유지하고 본문이 자막과 충돌하지 않게 둔다.","square_adjustment":"필수 내용·관계·비례를 잃는 중앙 크롭만으로 해결하지 않는다. 손실 없는 크롭·영역 재배치·구간 분절도 후보로 비교하고 실제 문구와 표시 조건을 확인한다.","temporal_conditions":"정보가 완성된 상태와 유지 시간을 별도로 확인한다. 읽기 가능한 대비·가림·배치가 유지되는 구간인지 보고 모션 자체의 길이로 대체하지 않는다.","abstain_when":"영역 역할과 대응 대상이 없으면 적합한 읽는 순서를 확정하지 않는다.","minimum_inputs":["설명 목적·핵심 주장","정보 항목·대응 관계와 출처","대상 시청자·시청 환경","출력 화면비·해상도·배포 UI","실제 문구·숫자·단위·자산"],"source_refs":["SRC-L2-CARBON-GRID","SRC-L2-NNG-VISUAL","SRC-L2-NNG-PROXIMITY"],"source_locator_refs":[{"source_id":"SRC-L2-CARBON-GRID","locator":"Contrast / Style models / Adaptive aspect ratios"},{"source_id":"SRC-L2-NNG-VISUAL","locator":"2. Visual Hierarchy / 3. Balance"},{"source_id":"SRC-L2-NNG-PROXIMITY","locator":"Place Related Elements near Each Other / Proximity May Shift in Responsive Designs"}],"numeric_default":null,"case_kind":"synthetic_not_company_video","auto_relation_assignment":false}]
03_한맥디자인\한맥디자인정본.json
{"profile_id":"hanmac-video","version":"0.1.0","status":"curated_seed","source_selection":{"brand_scales":"SB-COLOR","accent_and_neutral":"VC","authority":"USER","ui_mandatory":false},"rules":[{"id":"HM-RULE-SCOPE","version":"0.1.0","scope":"video","requirement":"required","source_refs":["USER"],"origin":"user_policy","text":"컬러 라이브러리는 전역 조회 가능. 모든 장면에서 모든 색을 쓰거나 특정 레이아웃을 강제한다는 뜻은 아니다.","review_status":"user_directed","case_refs":[],"reviewer":null},{"id":"HM-RULE-PRECEDENCE","version":"0.1.0","scope":"video","requirement":"required","source_refs":["USER"],"origin":"user_policy","text":"브랜드 기본색·명암 스케일은 Storybook, 강조색·중립색은 Vercel 값을 선택한다.","review_status":"user_directed","case_refs":[],"reviewer":null},{"id":"HM-RULE-UI-OPTIONAL","version":"0.1.0","scope":"video_system_policy","requirement":"required","source_refs":["USER"],"origin":"user_policy","text":"UI 규격은 참고 전용. UI를 사용하지 않았다는 이유로 영상 기획·검수에서 실패 처리하지 않는다.","review_status":"user_directed","case_refs":[],"reviewer":null},{"id":"HM-RULE-OBSERVATION","version":"0.1.0","scope":"video","requirement":"required","source_refs":[],"origin":"video_adaptation","text":"과거 영상의 관측 색을 선택된 팔레트 값으로 보정해서 기록하지 않는다. 공식 토큰 참조와 관측 픽셀을 분리한다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-ORANGE-ROLES","version":"0.1.0","scope":"video","requirement":"recommended","source_refs":["VC"],"origin":"source_interpretation","text":"기본 Orange #CC5200와 강조 액션 Orange #FF5C00를 서로 다른 역할로 관리한다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-YELLOW","version":"0.1.0","scope":"video","requirement":"recommended","source_refs":["VC"],"origin":"source_interpretation","text":"Yellow #FFC600는 Green 배경 강조 후보로 사용한다. 범용 차트 시리즈색으로 자동 지정하지 않는다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-NEUTRAL","version":"0.1.0","scope":"video","requirement":"recommended","source_refs":["VC"],"origin":"source_interpretation","text":"Green/Brown 테마의 주·보조 텍스트를 대응 중립색으로 선택한다. 최종 합성 배경에서 대비를 재확인한다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-TRANSITION","version":"0.1.0","scope":"video","requirement":"reference_only","source_refs":["VC"],"origin":"source_interpretation","text":"Green↔Brown 변경 시 Neutral 경유라는 원문이 있으나 웹 테마 변경인지 영상 시간 전환인지 불명확하다. 영상 컷·디졸브의 의무 규칙으로 확장하지 않는다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-GRADIENT","version":"0.1.0","scope":"video","requirement":"reference_only","source_refs":["VC"],"origin":"source_interpretation","text":"브랜드 표면의 transparent/rgba 금지는 해당 표면 레시피의 참고 제약으로 한정한다. 영상 페이드·알파 합성 전체 금지로 확장하지 않는다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-READABILITY","version":"0.1.0","scope":"video","requirement":"recommended","source_refs":["W3C-CONTRAST","W3C-COLOR"],"origin":"video_adaptation","text":"색 이외에 텍스트·번호·형태·위치로도 정보를 구분한다. 정지 색 대비는 보조 지표이며 최종 프레임·움직임·시청 조건을 검수한다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-TYPE","version":"0.1.0","scope":"video","requirement":"reference_only","source_refs":[],"origin":"video_adaptation","text":"폰트와 위계는 참고하되 웹 px·UI 행간을 영상 필수 수치로 사용하지 않는다.","review_status":"draft","case_refs":[],"reviewer":null},{"id":"HM-RULE-MOTION","version":"0.1.0","scope":"video","requirement":"reference_only","source_refs":[],"origin":"video_adaptation","text":"hover 120/150ms 등을 영상 등장·유지·퇴장 시간으로 사용하지 않는다. 영상 모션 수치는 사례·내레이션·읽기 시간에서 정한다.","review_status":"draft","case_refs":[],"reviewer":null}],"issues":[{"id":"HM-ISSUE-COLOR-6","status":"resolved_by_user","title":"6개 명암 단계값 차이","evidence":"Green 100; Brown 700; Orange 100~400","handling":"Storybook 선택. Vercel 값은 observations에 보존."},{"id":"HM-ISSUE-VERSION","status":"open_reference","title":"Vercel 버전 표기 불일치","evidence":"헤더/푸터 v2.2.0, 변경 이력 최신 v2.3.0","handling":"버전 단정 대신 조회일·메뉴 위치로 기록."},{"id":"HM-ISSUE-GRAD-COUNT","status":"open_reference","title":"그라데이션 개수 불일치","evidence":"설명 20개/엘리베이션 10개, 실제 CSS 고유 이름 18개/엘리베이션 8개","handling":"보이는 18개만 보관. 누락 2개를 추정 생성하지 않음."},{"id":"HM-ISSUE-GRAD-DIRECTION","status":"open_reference","title":"그라데이션 방향 불일치","evidence":"설명 90deg 수평, CSS 180deg","handling":"CSS 문자열을 관측값으로 보존. 시각 참고, 자동 강제 제외."},{"id":"HM-ISSUE-GRAD-ALIAS","status":"open_reference","title":"미정의 보더 예시 이름","evidence":"예시 --grad-border-green-1, 정의 --grad-border-green","handling":"서로 다른 원문 이름 기록. 유효 정의 이름만 참조."},{"id":"HM-ISSUE-TYPE-SCOPE","status":"resolved_by_scope","title":"타입 체계 차이","evidence":"Vercel 공통 9역할 vs Storybook 현재 구현 참고","handling":"필수 영상 타입 규격 미정. 출처별 UI 참고로 분리."},{"id":"HM-ISSUE-SPACE-SCOPE","status":"resolved_by_scope","title":"전역 간격 정의 차이","evidence":"Vercel 전역 4px 그리드 vs Storybook 전역 spacing/grid 미정","handling":"공식 공통 그리드로 합치지 않음."},{"id":"HM-ISSUE-UI-INTERNAL","status":"open_reference","title":"UI 설명과 CSS 값 차이","evidence":"radius 문서 버튼 8px vs 버튼/Variables 4px; 카드 설명 흰색/HM Brown hover vs CSS alpha white/accent orange","handling":"제품 재현은 실제 구현/캡처 우선, 영상 강제값 없음."},{"id":"HM-ISSUE-MOTION-UNKNOWN","status":"not_provided","title":"영상 전용 기준 미제공","evidence":"로고 원본·여백·최소 크기, 자막 규격, 영상 타입 크기·세이프존·이징·타이밍·데이터 시리즈 팔레트 미확인","handling":"null/후속 항목. 웹 수치로 채우지 않음."}],"semantic_roles":[{"role":"brand.green","token_id":"HM-COLOR-GREEN-500","origin":"source","requirement":"available"},{"role":"brand.brown","token_id":"HM-COLOR-BROWN-500","origin":"source","requirement":"available"},{"role":"brand.orange","token_id":"HM-COLOR-ORANGE-500","origin":"source","requirement":"available"},{"role":"emphasis.action","token_id":"HM-COLOR-ACCENT-ORANGE","origin":"source_interpretation","requirement":"recommended"},{"role":"emphasis.on_green","token_id":"HM-COLOR-YELLOW","origin":"source_interpretation","requirement":"recommended"},{"role":"text.on_green.primary","token_id":"HM-COLOR-NEUTRAL-GREEN-100","origin":"source_interpretation","requirement":"recommended"},{"role":"text.on_green.secondary","token_id":"HM-COLOR-NEUTRAL-GREEN-200","origin":"source_interpretation","requirement":"recommended"},{"role":"text.on_brown.primary","token_id":"HM-COLOR-NEUTRAL-BROWN-100","origin":"source_interpretation","requirement":"recommended"},{"role":"text.on_brown.secondary","token_id":"HM-COLOR-NEUTRAL-BROWN-200","origin":"source_interpretation","requirement":"recommended"}],"not_defined":{"video_font_sizes":null,"safe_area":null,"motion_durations":null,"easing":null,"logo_asset":null,"logo_clear_space":null,"data_series_palette":null},"provenance_limit":"수동 전사한 구조화 관측·정제 데이터. 원본 전체 HTML 스냅샷/배포 커밋은 확보하지 않았으며 라이브 페이지가 바뀔 수 있음."}
05_출처와검토\R3_모션_조사기록.json
{"id":"r3-motion-research","version":"0.1.1","read_on":"2026-10-14","sources":[{"id":"SRC-ADOBE-12","title":"Adobe 애니메이션 12원칙","url":"https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html","read_on":"2026-10-14","read_depth":"public_article_sections","sections":["History","1–12 principle headings and explanations"],"limits":["The Illusion of Life 책 전체 미검토","본문 삽입 영상 미시청"],"summary_ko":"12원칙의 공개 설명을 확인했다. 캐릭터 표현 지침을 정보 영상의 필수 조건으로 간주하지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-JORGE-10","title":"Jorge 모션 10원칙","url":"https://www.learnsquared.com/courses/motion-design","read_on":"2026-10-14","read_depth":"public_course_outline","sections":["Lesson 2: The 10 Principles of Motion Design / 10 chapter titles"],"limits":["유료 강의 상세 설명·예제·프로젝트 파일 미확보","공개 제목 확인을 이론 상세 정의 확인으로 확대하지 않음"],"summary_ko":"10개 항목과 순서를 확인했다. 항목별 프로젝트 해석과 강사의 설명은 별개다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-R3-POLYUM","title":"사용자 제공 한국어 해설","url":"https://polyum.tistory.com/9","read_on":"2026-10-14","read_depth":"secondary_article_sections","sections":["모션그래픽 10가지 원칙 목록·대조표","Mass & Weight","12원칙별 텍스트 설명·Timing"],"limits":["번역·해설 자료. 국제표준·원저자 강의로 취급하지 않음","GIF·임베드 영상 효과는 독립 검증하지 않음"],"summary_ko":"10개 항목명은 공식 강의 목록과 대응한다. 무게와 정지의 일반화, 재생속도와 출력 프레임레이트의 혼동은 DB 지침에 옮기지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-CAM-EXTRANEOUS","title":"Mayer·Fiorella 불필요 처리 감소","url":"https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning/F29A19FCD34C542806F736E0661C05F5","read_on":"2026-10-14","read_depth":"publisher_summary","sections":["Chapter 14 Summary"],"limits":["장 전체·세부 실험·효과크기·경계조건 전체 미검토","회사 영상에 대한 효과 검증 없음"],"summary_ko":"학습용 멀티미디어의 불필요 처리 감소 원칙 5개를 요약 수준에서 확인했다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-CAM-ESSENTIAL","title":"Mayer·Fiorella 필수 처리 관리","url":"https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning/A9E77D0172F905AC957689D1771E2888","read_on":"2026-10-14","read_depth":"publisher_summary","sections":["Chapter 19 Summary"],"limits":["장 전체·세부 실험·효과크기·경계조건 전체 미검토","회사 영상에 대한 효과 검증 없음"],"summary_ko":"필수 처리 부담을 관리하는 분절·사전 학습·양식 원칙을 공개 요약에서 확인했다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-CAM-TRANSIENT","title":"일시 정보 원칙","url":"https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/transient-information-principle-in-multimedia-learning/670D96C3B9520320CE558AA855A49EE9","read_on":"2026-10-14","read_depth":"publisher_summary","sections":["Chapter 21 Summary"],"limits":["장 전체·세부 실험·효과크기·경계조건 전체 미검토","회사 영상에 대한 효과 검증 없음"],"summary_ko":"사라지는 정보와 계속 참조 가능한 정보의 차이를 공개 요약에서 확인했다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-R3-EXPERTISE-SUMMARY","title":"Kalyuga 숙련도 역전 원칙 — 2021 공식 요약","url":"https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/expertise-reversal-principle-in-multimedia-learning/F6793786D8F79519A22E967FC2563839","read_on":"2026-10-14","read_depth":"publisher_summary","sections":["Chapter 13 Summary / DOI 10.1017/9781108894333.017"],"limits":["장 전체·숙련도 진단도구 미검토","직급·직무명으로 시청자 지식을 추정하지 않음"],"summary_ko":"초보자에게 유효한 설명이 지식이 많은 학습자에게는 유효하지 않거나 방해될 수 있다. 사전 지식에 맞춘 지원 조절이 시사점이다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-CARBON-CHOREO","title":"Carbon v10 모션 구성","url":"https://v10.carbondesignsystem.com/guidelines/motion/choreography/","read_on":"2026-10-14","read_depth":"archived_ui_guideline_sections","sections":["Paths","Composition: semantic/spatial/intentional consistency","Continuity","Sequence and stagger"],"limits":["v10 보관 UI 지침","격자 경로·대각선 회피·등장 순서·20ms/500ms를 회사 영상 기본값으로 복사하지 않음"],"summary_ko":"의미·공간 관계와 대상 연속성을 확인했다. 원문의 UI 구성 제약은 출처 맥락에 묶어 둔다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-CARBON-OVERVIEW","title":"Carbon v10 모션 역할","url":"https://v10.carbondesignsystem.com/guidelines/motion/overview/","read_on":"2026-10-14","read_depth":"archived_ui_guideline_sections","sections":["Style: Productive / Expressive","Easing"],"limits":["v10 브랜드 UI 규칙","선형 이동·바운스의 브랜드 제한과 곡선 수치를 영상 일반 법칙으로 채택하지 않음"],"summary_ko":"작업 지원과 표현적 순간을 구분하는 지침을 확인했다. 브랜드별 표현 규칙은 다를 수 있다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-FLUENT","title":"Fluent 2 Motion","url":"https://fluent2.microsoft.design/motion","read_on":"2026-10-14","read_depth":"ui_guideline_sections","sections":["Motion principles: Functional / Natural / Consistent / Appealing"],"limits":["Microsoft UI 지침","동작의 자연스러움이 실측 물리량의 정확성을 증명하지 않음"],"summary_ko":"기능·자연스러움·일관성·매력의 네 관점을 확인했다. 영상 적용은 별도 프로젝트 해석이다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-UX-MOTION","title":"Issara UX in Motion","url":"https://medium.com/ux-in-motion/creating-usability-with-motion-the-ux-in-motion-manifesto-a87a4584ddc","read_on":"2026-10-14","read_depth":"author_article_sections","sections":["Realtime vs non-realtime","Expectation / Continuity / Narrative / Relationship","Principles / Techniques / Properties / Values","Principles 1–12 textual explanations"],"limits":["2017 저자의 UI 설계론. 학습 효과 실험 결과로 취급하지 않음","임베드 움직임의 프레임별 검증 없음","항상 이징·값 변화로 agency/neurofeedback·fade 부족 주장을 영상 의무 규칙으로 복사하지 않음"],"summary_ko":"UI 움직임의 관계·연속성 관점 12개를 확인했다. 제작 구현과 화면 관측은 분리한다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-W3C-FLASH","title":"플래시 검토","url":"https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html","read_on":"2026-10-14","read_depth":"w3c_understanding_sections","sections":["SC 2.3.1 / Intent"],"limits":["Understanding은 해설 문서. WCAG 전체 적합 판정 아님","실제 영상·플레이어 검사 없음"],"summary_ko":"웹 콘텐츠의 플래시 횟수 또는 일반·적색 플래시 임계값 조건을 확인했다. 육안 확인만으로 안전 판정을 하지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-W3C-PAUSE","title":"재생중단 검토","url":"https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html","read_on":"2026-10-14","read_depth":"w3c_understanding_sections","sections":["SC 2.2.2 moving/blinking/scrolling and auto-updating conditions"],"limits":["Understanding은 해설 문서. WCAG 전체 적합 판정 아님","실제 영상·플레이어 검사 없음"],"summary_ko":"자동 시작·다른 콘텐츠와 병렬 제공 등 조건에 해당하는 웹 움직임의 제어를 확인했다. 업데이트 조건은 5초 조건과 다르다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-W3C-INTERACTION","title":"상호작용 모션 검토","url":"https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html","read_on":"2026-10-14","read_depth":"w3c_understanding_sections","sections":["SC 2.3.3 / essential / motion animation definition"],"limits":["Understanding은 해설 문서. WCAG 전체 적합 판정 아님","실제 영상·플레이어 검사 없음"],"summary_ko":"상호작용 유발 모션의 비활성화 조건을 확인했다. 일반 MP4 자체의 옵션으로 간주하지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-R3-MATERIAL2","title":"Material 2 Understanding motion","url":"https://m2.material.io/design/motion/understanding-motion/","read_on":"2026-10-14","read_depth":"search_extract_only","sections":["검색 추출: Principles / Hierarchy"],"limits":["직접 열기는 본문 1줄만 반환","검색 추출 확인. 원문 전체 검토 완료로 계산하지 않음"],"summary_ko":"정보 안내·초점·표현의 세 관점을 조사 후보로 남겼다. 기존 MR과 겹치므로 새 규칙은 만들지 않았다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-R3-APM","title":"Lowe·Schnotz 교육용 애니메이션 원칙","url":"https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/animation-principles-in-multimedia-learning/C32045ACB824BFD657DA6A702E8255DC","read_on":"2026-10-14","read_depth":"publisher_summary","sections":["2014 Chapter 22 Abstract / Summary"],"limits":["본문의 5원칙 명칭·세부 정의 미확보","APM의 인지 단계를 우리 R2 기록 단위로 치환하지 않음"],"summary_ko":"시간 변화를 직접 보여주는 이점과 처리 부담을 함께 다룬다. 다섯 원칙이 있다는 것만으로 이름·내용을 만들어 등록하지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."},{"id":"SRC-R3-CHANGE-STUDY","title":"Ploetzner·Berney·Bétrancourt 2021 변화 학습 연구","url":"https://link.springer.com/article/10.1007/s11251-021-09541-w","read_on":"2026-10-14","read_depth":"article_selected_sections","sections":["Abstract","Introduction","Theoretical background","Experimental study: research questions / learning task / pre-study design"],"limits":["본 실험 통계표·전체 결과·제한점의 독립 재분석 미수행","교육 실험을 사내 홍보영상의 성과로 일반화하지 않음"],"summary_ko":"88명 대학생의 기어 학습을 비교한 연구의 초록에서는 동작 식별은 애니메이션, 배치 식별은 정지 그림이 유리했다. 정지/동작 선택의 후보 근거이며 모든 영상에 대한 보장으로 쓰지 않는다.","verbatim_quote":null,"remote_content_sha256":null,"verification":"공개 웹 텍스트 확인. 원격 원문 전체 스냅샷·영상 시청 검증은 수행하지 않음."}],"original_core_changed":true,"decision_pending":[],"scope":"선택 원칙의 공개 본문·공개 요약·목록을 확인. 원문 전체·학술 실험 전체·유료강의·영상 시청까지 완료한 상태가 아님.","approved_change":"사용자 A에 따라 IP-10만 reference/공식 Summary 출처/기권 조건으로 개정. 다른42개 정의·분류ID는 유지."}
# R5 디자인 연결 후속 인계

- R6: 8회사 CI 공식성/최신성·사용 범위, 문서 선언 후보4개와 관측값의 상태, 실제 선택자·내용검수/승인 근거를 구분. 사용자 A는 역할 활용 정책으로만 보존.
- R7: 한국어/글자·숫자/단위·차트/자막/배경 변화·색 이외 구분·출력별 읽힘과 홀드아웃/실제 평가 계획. R5의24 설명 사례를 실제영상 성적으로 사용하지 않음.
- R8: 기존 세 스킬의 본문·참조·평가 입력 원문은 그대로 유지. Anthropic Skill Creator로 목적·권한을 유지하며 새 R4/R5 계약·미정/null·인용/선택자 선언·불충분근거 기권·사람검수 인계를 반영하고 재평가. 외부 스킬 실행/재라이선스/기존 점수 재사용은 하지 않음.
- 01-A: 관측 분석시 원본 픽셀/좌표/시간과 기획 토큰 선택을 분리. R4/R5의 구조 도구는 영상 추출/OCR/해석의 구현이 아님.
- 01-B: 실제 사내 영상 반복사례·반례와 검수로 영상 전용 규격을 검토. 현재 웹/CI 참고를 회사 영상 문법 승인으로 승격하지 않음.

[현재 R5 사용 안내](../07_실행도구/R5_조회와적용_사용안내.md) · [미정·필요자료](../03_한맥디자인/09_적용시_필요자료와_검수대기.md)
# 세 맞춤 스킬에 들어갈 기능 — A안 설계
이번 결과는 기능/권한/평가의 설계안이다. 기존SKILL을 아직 바꾸지 않았다. 사용자 승인한 draft 권한·소량시범 운영을 유지하며 R8에서 Anthropic Skill Creator를 활용해 재구성하고 단계별 사용자 검토를 받는다.

| 스킬 | 넣을 기능 | 입력/출력 | 하지 않는 일 |
|---|---|---|---|
| video-knowledge-curator | 용어/지식·적용조건·예/반례·출처 절/깊이·observed/inferred/unknown·원문/자체해석 구분; PPT/설명/도표/모션의 목적별 판단 카드 | 출처와 기존정본→draft지식카드·차이·미확정·검토 제안 | 의미병합·새taxonomyID·회사필수·승인 자동 생성, 실제 영상추출/새시나리오 |
| video-record-steward | 필수필드·버전/근거·회사/자산 참조·원본값과 파생/정규화값 구분·쓰기경계·diff/log/backup·허용delta·검사/기권 | 명시대상 draft+정본참조→검증된draft·검사결과·변경로그·되돌리기 안내 | 값/단위/정밀도 임의변경·dedupe승격·원본/정본덮어쓰기·회사승인; runtime분석 획득은01-A |
| video-guidance-reviewer | 목적/대상/숙련도·관계·레이아웃·한국어·숫자/단위·시간·무음/접근성·다중비율·CI보존; anti-generic을금지표보다적합성으로검토 | draft카드/설명용사례+근거→항목별수정/허용/보류·근거·영향·우선순위 | 무조건4사진/8움직임/1초점/3층/CTA/3항목/두줄·웹수치강제·주관점수승인·새화면창작 |

검토 단위는 목적→원문 강도→프로젝트 조건→관측 근거→예/반례→기권→권한→검증이다. 외부 취향의 완화는 의미를 감추는 번역이 아니라 프로젝트의 자체 해석임을 표시한다. 라이선스 보류 후보를 바꿔 쓰는 것으로 우회하지 않는다. 필요한 판단 절차는 기존 공개 원칙과 우리 업무 계약에서 자체 작성한다.

R8 평가는 정상양성/의미반례/권한위반/자료없음/쓰기실패를 포함한다. 정지·등속·동등비교·내용상반복·주제명제목·텍스트단독·긴한국어/소수/SI·결측·8회사 CI를 반드시 포함한다. baseline/with-skill은 같은 조건으로 비교하고 trigger/작업품질/쓰기안전/비용/infra_error를 구분한다. 선택용validation과최종test를분리한다.

각 스킬 초안 목적·참조·권한 변경 검토와 평가 후 운영 범위 검토는 최소4선택지+추천안으로 묻는다. 이미 승인한 목적·시범운영을 반복해서 승인받는 절차가 아니다.

편집분야추가: 큐레이터는격자유형/정보관계/원문과측정추정/스타일출처조건을draft지식으로, 기록관리자는좌표/값/브랜드 locks/원본과파생·검토깊이·변형이력을, 검토자는문구/그림/타입·편집성·데이터정확성·가독성/대칭과반복의반례를다룬다. 새사진/도표/판면제작과영상을읽는구현은이세Phase00스킬의기능에추가하지않는다.

```

### 실행 4
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; $j=Get-Content -Raw -LiteralPath (Join-Path $db '03_한맥디자인\한맥디자인정본.json')|ConvertFrom-Json; $j|Select-Object profile_id,version,status,source_selection,rules,issues,not_defined,provenance_limit|ConvertTo-Json -Depth 10; Get-Content -LiteralPath (Join-Path $db '03_한맥디자인\07_회사CI와_화면역할_연결규칙.md'); Get-Content -LiteralPath (Join-Path $db '13_품질검수\03_판정운영기준.md'); $j=Get-Content -Raw -LiteralPath (Join-Path $db '05_출처와검토\출처목록.json')|ConvertFrom-Json; $j.sources|Where-Object {$_.id -in @('SRC-IMPECCABLE','SRC-R3-EXPERTISE-SUMMARY','SRC-PROJECT-GUIDANCE','SRC-PROJECT-TAXONOMY','SRC-ADOBE-12','SRC-JORGE-10','SRC-CAM-ESSENTIAL','SRC-CAM-EXTRANEOUS')}|ConvertTo-Json -Depth 10
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
{
  "profile_id": "hanmac-video",
  "version": "0.1.0",
  "status": "curated_seed",
  "source_selection": {
    "brand_scales": "SB-COLOR",
    "accent_and_neutral": "VC",
    "authority": "USER",
    "ui_mandatory": false
  },
  "rules": [
    {
      "id": "HM-RULE-SCOPE",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "required",
      "source_refs": [
        "USER"
      ],
      "origin": "user_policy",
      "text": "컬러 라이브러리는 전역 조회 가능. 모든 장면에서 모든 색을 쓰거나 특정 레이아웃을 강제한다는 뜻은 아니다.",
      "review_status": "user_directed",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-PRECEDENCE",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "required",
      "source_refs": [
        "USER"
      ],
      "origin": "user_policy",
      "text": "브랜드 기본색·명암 스케일은 Storybook, 강조색·중립색은 Vercel 값을 선택한다.",
      "review_status": "user_directed",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-UI-OPTIONAL",
      "version": "0.1.0",
      "scope": "video_system_policy",
      "requirement": "required",
      "source_refs": [
        "USER"
      ],
      "origin": "user_policy",
      "text": "UI 규격은 참고 전용. UI를 사용하지 않았다는 이유로 영상 기획·검수에서 실패 처리하지 않는다.",
      "review_status": "user_directed",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-OBSERVATION",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "required",
      "source_refs": [],
      "origin": "video_adaptation",
      "text": "과거 영상의 관측 색을 선택된 팔레트 값으로 보정해서 기록하지 않는다. 공식 토큰 참조와 관측 픽셀을 분리한다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-ORANGE-ROLES",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "recommended",
      "source_refs": [
        "VC"
      ],
      "origin": "source_interpretation",
      "text": "기본 Orange #CC5200와 강조 액션 Orange #FF5C00를 서로 다른 역할로 관리한다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-YELLOW",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "recommended",
      "source_refs": [
        "VC"
      ],
      "origin": "source_interpretation",
      "text": "Yellow #FFC600는 Green 배경 강조 후보로 사용한다. 범용 차트 시리즈색으로 자동 지정하지 않는다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-NEUTRAL",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "recommended",
      "source_refs": [
        "VC"
      ],
      "origin": "source_interpretation",
      "text": "Green/Brown 테마의 주·보조 텍스트를 대응 중립색으로 선택한다. 최종 합성 배경에서 대비를 재확인한다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-TRANSITION",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "reference_only",
      "source_refs": [
        "VC"
      ],
      "origin": "source_interpretation",
      "text": "Green↔Brown 변경 시 Neutral 경유라는 원문이 있으나 웹 테마 변경인지 영상 시간 전환인지 불명확하다. 영상 컷·디졸브의 의무 규칙으로 확장하지 않는다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-GRADIENT",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "reference_only",
      "source_refs": [
        "VC"
      ],
      "origin": "source_interpretation",
      "text": "브랜드 표면의 transparent/rgba 금지는 해당 표면 레시피의 참고 제약으로 한정한다. 영상 페이드·알파 합성 전체 금지로 확장하지 않는다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-READABILITY",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "recommended",
      "source_refs": [
        "W3C-CONTRAST",
        "W3C-COLOR"
      ],
      "origin": "video_adaptation",
      "text": "색 이외에 텍스트·번호·형태·위치로도 정보를 구분한다. 정지 색 대비는 보조 지표이며 최종 프레임·움직임·시청 조건을 검수한다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-TYPE",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "reference_only",
      "source_refs": [],
      "origin": "video_adaptation",
      "text": "폰트와 위계는 참고하되 웹 px·UI 행간을 영상 필수 수치로 사용하지 않는다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    },
    {
      "id": "HM-RULE-MOTION",
      "version": "0.1.0",
      "scope": "video",
      "requirement": "reference_only",
      "source_refs": [],
      "origin": "video_adaptation",
      "text": "hover 120/150ms 등을 영상 등장·유지·퇴장 시간으로 사용하지 않는다. 영상 모션 수치는 사례·내레이션·읽기 시간에서 정한다.",
      "review_status": "draft",
      "case_refs": [],
      "reviewer": null
    }
  ],
  "issues": [
    {
      "id": "HM-ISSUE-COLOR-6",
      "status": "resolved_by_user",
      "title": "6개 명암 단계값 차이",
      "evidence": "Green 100; Brown 700; Orange 100~400",
      "handling": "Storybook 선택. Vercel 값은 observations에 보존."
    },
    {
      "id": "HM-ISSUE-VERSION",
      "status": "open_reference",
      "title": "Vercel 버전 표기 불일치",
      "evidence": "헤더/푸터 v2.2.0, 변경 이력 최신 v2.3.0",
      "handling": "버전 단정 대신 조회일·메뉴 위치로 기록."
    },
    {
      "id": "HM-ISSUE-GRAD-COUNT",
      "status": "open_reference",
      "title": "그라데이션 개수 불일치",
      "evidence": "설명 20개/엘리베이션 10개, 실제 CSS 고유 이름 18개/엘리베이션 8개",
      "handling": "보이는 18개만 보관. 누락 2개를 추정 생성하지 않음."
    },
    {
      "id": "HM-ISSUE-GRAD-DIRECTION",
      "status": "open_reference",
      "title": "그라데이션 방향 불일치",
      "evidence": "설명 90deg 수평, CSS 180deg",
      "handling": "CSS 문자열을 관측값으로 보존. 시각 참고, 자동 강제 제외."
    },
    {
      "id": "HM-ISSUE-GRAD-ALIAS",
      "status": "open_reference",
      "title": "미정의 보더 예시 이름",
      "evidence": "예시 --grad-border-green-1, 정의 --grad-border-green",
      "handling": "서로 다른 원문 이름 기록. 유효 정의 이름만 참조."
    },
    {
      "id": "HM-ISSUE-TYPE-SCOPE",
      "status": "resolved_by_scope",
      "title": "타입 체계 차이",
      "evidence": "Vercel 공통 9역할 vs Storybook 현재 구현 참고",
      "handling": "필수 영상 타입 규격 미정. 출처별 UI 참고로 분리."
    },
    {
      "id": "HM-ISSUE-SPACE-SCOPE",
      "status": "resolved_by_scope",
      "title": "전역 간격 정의 차이",
      "evidence": "Vercel 전역 4px 그리드 vs Storybook 전역 spacing/grid 미정",
      "handling": "공식 공통 그리드로 합치지 않음."
    },
    {
      "id": "HM-ISSUE-UI-INTERNAL",
      "status": "open_reference",
      "title": "UI 설명과 CSS 값 차이",
      "evidence": "radius 문서 버튼 8px vs 버튼/Variables 4px; 카드 설명 흰색/HM Brown hover vs CSS alpha white/accent orange",
      "handling": "제품 재현은 실제 구현/캡처 우선, 영상 강제값 없음."
    },
    {
      "id": "HM-ISSUE-MOTION-UNKNOWN",
      "status": "not_provided",
      "title": "영상 전용 기준 미제공",
      "evidence": "로고 원본·여백·최소 크기, 자막 규격, 영상 타입 크기·세이프존·이징·타이밍·데이터 시리즈 팔레트 미확인",
      "handling": "null/후속 항목. 웹 수치로 채우지 않음."
    }
  ],
  "not_defined": {
    "video_font_sizes": null,
    "safe_area": null,
    "motion_durations": null,
    "easing": null,
    "logo_asset": null,
    "logo_clear_space": null,
    "data_series_palette": null
  },
  "provenance_limit": "수동 전사한 구조화 관측·정제 데이터. 원본 전체 HTML 스냅샷/배포 커밋은 확보하지 않았으며 라이브 페이지가 바뀔 수 있음."
}
# R5 회사 CI·한맥 디자인 적용 연결 규칙

사용자 A(2026-10-15): 관측색은 디자이너가 명시 선택한 프로젝트 초안의 역할 후보다. 관측/선언/회사 승인과 현재 원문/과거 원문을 섞지 않는다.

## 연결 순서

1. 대상 회사와 단독/공동주체, 목적·출력 조건을 적는다. 공동 회사는 회사 배열 첫 항목을 대표 회사로 추정하지 않는다.
2. 회사/자산/색 목록과 한맥 정본, A정책의 버전·해시를 pin한다. 로고는 회사별 자산ID·버전·hash를 참조한다. 파일명으로 공식 최신/언어·용도를 확정하지 않는다.
3. CI색 역할은 회사ID+색ID+기록버전으로 참조한다. 현재·원문대조 완료·화면 sRGB값이 있는 색만 후보 연결한다. 원본 화면값을 관측과 다르게 수정하지 않는다.
4. 한맥 30색은 공통 라이브러리로 명시 선택할 때만 사용한다. 회사CI색으로 변환하지 않는다. 한맥색의 company_id는 null로 공통 자격을 드러낸다. 새 프로젝트색은 project_literal과 목적을 적고 원색을 덮어쓰지 않는다.
5. 역할마다 디자이너 선택의 선언·선택 이유·가정을 남긴다. 이 문자열만으로 실제 사람의 선택/identity를 인증하지 않는다. 현재 예시는 합성 설명용이므로 실제 선택 기록과 구분한다.
6. 로고형·공식성/최신성·출력 환경·최종 조합·가독성은 사람 검수 대기다. 구조 통과를 승인으로 바꾸지 않는다. 필요한 내용 검수는 생략하지 않는다.

designer_declaration의 필수 조건은 이 규격의 색 역할 선택에 적용한다. 로고는 자산 참조+선택 메모, 선택 스타일은 명시 ID로 사용 의도를 기록하고 각 항목의 적용성은 별도 사람 검수 대기로 반환한다. 로고/스타일만 있는 기록도 명시 선택·검수 대기이며 선택자 인증/승인 기록이 아니다.

## 8회사 현재 연결

[회사별 현황 JSON](회사별_디자인연결_현황.json)은 자료 참조 목록이다. 역할·로고 선택은 비어 있으며 회사별 화면 템플릿을 확정한 것이 아니다. 자산 원문은 R1 관리 위치에서 읽는다.

CI 로고와 바탕/텍스트 역할은 별개다. 대비가 낮으면 배경판·글자색·배치·허용된 변형을 검토한다. CI 원색을 자동으로 어둡게 하거나 형태를 고쳐 새 공식형으로 만들지 않는다. 원문 CMYK/별색의 프로필 없는 sRGB 환산은 보류한다.

## R4와 함께 쓸 때

R5 계약은 R4의 한맥 design 필드에 가족사 색ID를 억지로 넣지 않는 **별도 프로젝트 초안 기록**이다. linked_r4_record를 쓸 경우 현재 파일 경로·ID·버전·hash만 연결한다. 로고/색의 기획 선택은 R5, 원본 프레임의 픽셀·좌표·관측 주장은 R4에 남긴다. 서로를 덮어쓰지 않는다. R4 참조 검사만으로 회사CI 적용/내용이 검증되는 것은 아니다.

현재 규격은 의도적으로 project_draft·review pending·company_approved=false만 허용한다. 승인 워크플로와 실제 선택자 인증은 R6/R7로 인계한다. 실제 회사 자료를 분석하거나 화면을 자동 생성하는 것은 01-A/후속 단계다.

[기록 규격](디자인적용_기록규격.json) · [합성 설명용 예시](디자인적용_설명용예시.json) · [R5 단계 안내](05_R5_단계별진행안내.md)
# 항목별 판정 운영 기준

2026-10-15 · R7-1 · 사용자 선택 A 반영. 이 문서는 검수 결과를 기록하는 공통 운영 기준이다. 개별 품질 항목·원문 근거·적용 예와 반례는 R7-2, 평가 표본·지표·합격 조건의 검증 계획은 R7-3에서 보완한다.

## 무엇을 검수하는지 먼저 적기

| 검수 대상 | 묻는 질문 | 혼동하면 안 되는 것 |
|---|---|---|
| 분석 기록 | 원본 화면·소리·시나리오와 일치하게 기록했는가 | 원본 영상의 디자인이 나쁘다는 이유로 정확한 기록을 오답으로 만들지 않는다. |
| 기획·시안 | 주어진 목적과 대상에게 내용을 전달할 수 있는 구성인가 | 시안 검수로 최종 렌더의 자막 동기화·깜빡임·음량까지 통과시키지 않는다. |
| 실제 영상 | 해당 버전·재생 조건에서 내용·화면·모션·소리가 적절한가 | 규격 연결 검사나 정지 프레임 확인만으로 전체 재생 품질을 통과시키지 않는다. |
| 규격·검수 기록 | 필요한 참조·버전·시간·좌표·판정 이력이 일관적인가 | 구조가 맞는다는 사실을 내용의 정확성이나 회사 승인으로 확대하지 않는다. |

검수 시작 전에 대상 ID·버전/해시, 목적·시청 대상·사용 환경, 요청 범위, 적용 기준과 버전, 필요한 입력을 적는다. 일부 범위만 검수했다면 일부 결과로 표시한다. 목적상 필수인 항목을 요청 범위에서 빼도 전체 준비 완료로 제안할 수 없다. 필수 범위를 정할 근거가 부족하면 범위 자체의 확인이 필요하다.

## 네 가지 항목 판정

| 판정 | 사용할 조건 | 함께 남길 기록 |
|---|---|---|
| 통과 | 적용되는 기준을 필요한 근거와 검수 방식으로 확인했고 해결되지 않은 해당 오류가 없음 | 확인한 범위·근거·방법·검수자. 버전 변경 시 그대로 재사용하지 않음. |
| 수정필요 | 적용 기준의 위반 또는 목적을 훼손하는 오류가 근거로 확인됨 | 오류 위치·확인 근거·영향·수정 제안·재검수 조건. 의심만으로 확정하지 않음. |
| 판단보류 | 필요한 자료/조건/권한 있는 내용 판단이 없거나, 근거가 모순되거나, 해석이 갈림 | 무엇이 부족한지·해당 대상·질문·답할 사람의 역할·해결 조건. 확인한 부분은 별도로 기록. |
| 비적용 | 그 대상·목적·조건에 해당 기준을 적용할 이유가 없음 | 비적용 이유와 조건. 확인하지 못했다는 이유로 선택하지 않음. |

아직 검사하지 않은 항목은 위 네 가지의 완료 판정으로 만들지 않고 진행 상태를 ‘미검수’로 표시한다. 판정은 근거가 생길 때 기록한다. 사람 답변 대기 중인 항목은 판단보류로 남기되, 접수·담당·답변 상태는 판정과 구분한다.

## 항목 결과에 필요한 정보

최소한 다음 정보를 함께 기록한다. 이 목록은 검수 설계이며 R4 DB 필드나 R6 고정 입력을 이번 단계에서 변경하는 것은 아니다.

- 검수 ID, 대상 참조와 정확한 버전, 검수 목적·범위.
- 기준 ID/버전, 적용 이유 또는 비적용 이유, 해당 목적에서 필수인지와 그 근거.
- 진행 상태, 항목 판정, 확인한 내용과 미확인 부분.
- 원본 근거 참조와 위치. 영상이면 R4의 시간/프레임·좌표를 사용하고, 문서면 페이지/문단 등 실제 위치를 적는다.
- 판단 방법과 담당 역할, 영향·수정 우선순위, 수정 제안/추가 질문.
- 사람 검수가 필요한 경우 질문 대상·버전·근거·판단 범위·대기 상태. 실제 답변이 있기 전에는 검수 완료로 적지 않는다.
- 재검수 조건, 변경/정정 이력, 같은 원인·대상을 묶는 관련 오류 ID.

## 준비상태는 목적과 범위를 붙인 제안

단일 총점을 계산하지 않는다. 각 항목과 미검수/보류 목록을 먼저 보여주고 다음처럼 제안한다. 수정필요와 판단보류가 함께 있으면 둘 다 표시하며 한 상태로 숨기지 않는다.

1. 적용되는 필수항목에 확인된 오류가 있으면 그 목적에 필요한 수정사항을 제시한다. 특히 잘못된 핵심 수치·의미 반전·근거 없는 주장은 미관의 장점으로 상쇄하지 않는다.
2. 적용 필수항목이 미검수이거나 필요한 사람 판단·근거가 대기 중이면 아직 준비 완료로 제안하지 않는다. 부족한 부분과 해결 조건을 명시한다.
3. 필수항목을 필요한 방식으로 확인했고 해결되지 않은 필수 오류/보류가 없으면, 명시된 버전·목적·범위에서 ‘다음 검토로 진행 가능’이라고 제안할 수 있다. 선택 항목의 개선점·잔여 위험은 같이 표시한다.
4. 사용하지 않는 UI 방식이나 관련없는 회사의 미정 가이드까지 전체 작업의 차단 조건으로 삼지 않는다. 다만 해당 자료를 실제로 사용하기로 하면 적용 여부와 필수 조건을 다시 확인한다.

이 제안은 회사의 납품·배포·권한 승인, 사용자의 개인별 내용 확인, 실제 시청효과 입증을 대신하지 않는다.

## 우선순위와 사람 검수

심각도는 예쁜지의 점수가 아니라 해당 목적에서 발생하는 정보 손실과 오해의 영향으로 설명한다. 확인된 핵심 오류, 일반 수정, 선택 개선을 구분하되 획일적인 감점표는 만들지 않는다. 판단의 확실성과 오류의 영향은 별개다. 영향이 클 것 같아도 아직 의심이라면 판단보류로 기록하고 우선 확인을 요청한다.

업무 사실·기획 의도는 해당 내용 담당자, 해석이 갈리는 화면/모션과 가독성은 디자인 검수자 및 필요한 경우 실제 대상 시청자, 회사 규정·사용 권한은 그 범위를 확인할 수 있는 담당자에게 맡긴다. 역할만 정했다고 실제 사람이 검수한 것으로 기록하지 않는다. 사용자의 자료 최신성 확인을 다른 내용·시안·배포 승인에 재사용하지 않는다.

판단이 필요한 운영 선택은 구체적인 비교안과 최소 4개 선택지·추천안을 작성한다. 실제 내용 검수는 정답을 유도하는 네 가지 답에 억지로 맞추지 않고, 대상·버전·근거·질문 범위를 명시하여 자유 답변과 근거를 받을 수 있게 한다. 답변의 확인 범위만 보존하는 R6 정책을 따른다.

## 운영 방식의 설명용 예

아래는 실제 영상을 검수한 결과가 아니다. 개별 품질 기준을 검증한 사례도 아니며 판정 차이를 설명하기 위한 가정이다.

| 가정 | 운영상 처리 |
|---|---|
| 원본 그래프가 잘못됐고 분석 기록은 그 잘못된 수치를 정확히 옮김 | 분석 기록의 해당 전사는 통과 가능. 원본 정보의 정확성은 별도 수정필요로 기록. |
| 원본을 보지 않고 화면이 세련돼 보인다는 이유로 분석 정확성을 통과시킴 | 근거가 없으므로 분석 정확성 판단보류. 외관 평가를 근거로 대체하지 않음. |
| A회사 시안에 B회사 로고를 사용하지 않음 | B회사 로고 항목은 비적용 이유를 기록. B회사 미정 가이드로 A회사 시안 전체를 보류하지 않음. |
| 전체 영상 검수를 요청했으나 자막 일부와 첫 프레임만 확인함 | 일부 검수 결과와 미검수 범위를 표시. 전체 영상 준비 완료 제안 불가. |
| 같은 잘못된 단위 때문에 자막·도표가 함께 오류가 됨 | 위치별 영향을 남기고 같은 원인으로 연결. 두 항목의 감점을 합산하지 않음. |

[R7 진행 안내](00_R7_단계별진행안내.md) · [사용자가 선택한 비교안](02_품질판정방식_검토안.md) · [기존 기반과 보완점](01_기존자료와_보완목록.md)
[
  {
    "id": "SRC-PROJECT-TAXONOMY",
    "kind": "project_design",
    "title": "회사 영상 공통 분류 설계와 사용자 요구",
    "url": null,
    "locator": "backup/2026-10-14_기반정리전/02_지식DB_설계.md",
    "retrieved_on": "2026-10-14",
    "verification": "프로젝트 초안에서 자체 작성",
    "remote_snapshot_hash": null,
    "content_scope": "분류 축·레이아웃·근거 구분",
    "authority": "프로젝트 초안. 회사 표준 승인 아님."
  },
  {
    "id": "SRC-ADOBE-12",
    "kind": "external_principle",
    "title": "Adobe 애니메이션 12원칙",
    "url": "https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html",
    "locator": "공식 설명·명칭",
    "retrieved_on": "2026-10-14",
    "verification": "public_description",
    "remote_snapshot_hash": null,
    "content_scope": "공식 설명·명칭",
    "authority": "범용참고. 회사필수규칙아님."
  },
  {
    "id": "SRC-JORGE-10",
    "kind": "external_principle",
    "title": "Jorge 모션 10원칙",
    "url": "https://www.learnsquared.com/courses/motion-design",
    "locator": "공식 강의 목록의10제목; 유료 강의 본문 미확보",
    "retrieved_on": "2026-10-14",
    "verification": "primary_titles",
    "remote_snapshot_hash": null,
    "content_scope": "공식 강의 목록의10제목; 유료 강의 본문 미확보",
    "authority": "범용참고. 회사필수규칙아님."
  },
  {
    "id": "SRC-CAM-EXTRANEOUS",
    "kind": "external_principle",
    "title": "Mayer·Fiorella 불필요 처리 감소",
    "url": "https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning/F29A19FCD34C542806F736E0661C05F5",
    "locator": "공개 요약의5원칙; 원문 전체 미확보",
    "retrieved_on": "2026-10-14",
    "verification": "primary_abstract",
    "remote_snapshot_hash": null,
    "content_scope": "공개 요약의5원칙; 원문 전체 미확보",
    "authority": "범용참고. 회사필수규칙아님."
  },
  {
    "id": "SRC-CAM-ESSENTIAL",
    "kind": "external_principle",
    "title": "Mayer·Fiorella 필수 처리 관리",
    "url": "https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning/A9E77D0172F905AC957689D1771E2888",
    "locator": "공개 요약의3원칙; 원문 전체 미확보",
    "retrieved_on": "2026-10-14",
    "verification": "primary_abstract",
    "remote_snapshot_hash": null,
    "content_scope": "공개 요약의3원칙; 원문 전체 미확보",
    "authority": "범용참고. 회사필수규칙아님."
  },
  {
    "id": "SRC-IMPECCABLE",
    "kind": "external_principle",
    "title": "Impeccable 레이아웃·타입",
    "url": "https://github.com/pbakaus/impeccable",
    "locator": "추가스킬확보목록의고정커밋layout/typeset/operate 읽기",
    "retrieved_on": "2026-10-14",
    "verification": "pinned_source_review",
    "remote_snapshot_hash": null,
    "content_scope": "추가스킬확보목록의고정커밋layout/typeset/operate 읽기",
    "authority": "범용참고. 회사필수규칙아님."
  },
  {
    "id": "SRC-PROJECT-GUIDANCE",
    "kind": "project_design",
    "title": "정보 전달형 사내 영상 적용 해석",
    "url": null,
    "locator": "2026-10-14 사용자 목적과 기존 DB 명세를 바탕으로 자체 작성",
    "retrieved_on": "2026-10-14",
    "verification": "프로젝트 초안. 실제 영상 효과 검증 전.",
    "remote_snapshot_hash": null,
    "content_scope": "한국어·시간·브랜드·데이터 정확성과 적용 조건",
    "authority": "회사 승인 규칙 아님"
  },
  {
    "id": "SRC-R3-EXPERTISE-SUMMARY",
    "kind": "external_principle",
    "title": "Kalyuga 숙련도 역전 원칙 — 2021 공식 요약",
    "url": "https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/expertise-reversal-principle-in-multimedia-learning/F6793786D8F79519A22E967FC2563839",
    "locator": "Chapter 13 Summary / DOI 10.1017/9781108894333.017",
    "retrieved_on": "2026-10-14",
    "verification": "공식 공개 Summary의 정의 확인. 학술 장 전체·실험·진단도구 미검토.",
    "remote_snapshot_hash": null,
    "content_scope": "숙련도 역전 정의의 요약 수준. 입력 근거에 따른 설명 조정의 프로젝트 참고.",
    "authority": "조건부 외부 참고. 사용자 A는 사용 범위 선택이며 회사 필수 규칙 승인 아님."
  }
]

```

### 실행 5
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; @('02_원칙과레이아웃\03_모션원칙_적용예와반례.md','02_원칙과레이아웃\04_모션원칙_충돌과예외.md','02_원칙과레이아웃\10_확장레이아웃_후보와반례.md')|ForEach-Object {Write-Output $_; Get-Content -LiteralPath (Join-Path $db $_)}; $j=Get-Content -Raw -LiteralPath (Join-Path $db '01_공통용어\공통용어사전.json')|ConvertFrom-Json; $j.terms|Where-Object {$_.axis -eq 'timing'}|Select-Object id,name_ko,definition,include_when,exclude_or_limit,version|ConvertTo-Json -Depth 5; Get-Content -LiteralPath (Join-Path $db '07_실행도구\구형기록_보존검사.py') -Tail 18
```
종료 코드: 0
```text
Warning: truncated output (original token count: 15325)
Total output lines: 900

Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
02_원칙과레이아웃\03_모션원칙_적용예와반례.md
# 모션 원칙별 적용 예와 반례

모든 예는 프로젝트가 작성한 설명용 사례다. 실제 회사 영상·원문 예제·성능 검증 결과가 아니다. 기존43개 ID를 유지했고 사용자 A 선택으로 IP-10만 공식 Summary에 근거한 조건부 참고로 개정했다. 이 파일은 심화카드에서 생성했다.

심화카드 v0.1.2 / SHA256 `76b77be793d1ac56c5486a00e81133f68767c132846d8123c57a337b6c7fa066`.

## AP-01 · Squash and Stretch · 압축과 신장

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `1. Squash and Stretch`

원문 요약: 변형으로 탄성과 무게를 드러내며 부피를 고려한다.
우리 적용 해석: 아이콘 반응에는 후보. 구조물·실측 도형·정확한 데이터는 왜곡 주의. 부피·의미가 유지되는가?

- 적용 예: 확인 아이콘에 짧은 눌림과 복귀를 주어 반응을 표시한다.
- 반례: 교량 단면을 찌그러뜨려 실제 변형량처럼 제시한다.
- 기권·확인 조건: 재료의 실제 변형을 설명하는지 장식 반응인지 불명확하면 기술적 해석을 보류한다.
- 관측 근거: 시간에 따른 형상·비율 변화와 원래 형태로의 복귀. 물체 부피·원본 설정은 별도 근거 없으면 미확정.
- 검토 질문: 형태 변형이 전달을 돕는가, 기술 형상·문자를 왜곡하는가?
- 관련 원칙: MP-06
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-02 · Anticipation · 예비 동작

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `2. Anticipation`

원문 요약: 다음 동작에 앞서 준비를 보여준다.
우리 적용 해석: 큰 변화의 예고로 후보. 모든 등장에 반대 움직임을 넣지 않음. 이해에 도움인가 지연인가?

- 적용 예: 분해도 전환 직전 해당 부품을 표식으로 예고한다.
- 반례: 각 자막마다 반대 이동을 넣어 설명을 지연한다.
- 기권·확인 조건: 준비 동작 전후 표본이 없으면 예비 동작 여부를 확정하지 않는다.
- 관측 근거: 본 동작 전 반대 움직임·정지·표식 등 예고 상태의 존재와 순서.
- 검토 질문: 준비 동작이 다음 변화를 이해하게 하는가, 불필요하게 지연하는가?
- 관련 원칙: MP-04
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-03 · Staging · 주목 대상 연출

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `3. Staging`

원문 요약: 주요 이야기에 주목하도록 구성한다.
우리 적용 해석: 대표 화면과 강조 상태의 초점 확인. 비교 장면은 동등한 두 대상도 의도일 수 있음. 관찰해야 할 정보가 보이는가?

- 적용 예: 침투 경로를 밝히고 배경 설명을 낮춰 주제를 구분한다.
- 반례: 모든 화살표와 제목을 동시에 점멸시켜 초점을 없앤다.
- 기권·확인 조건: 대상·목적이 미제공이면 배치는 관측하되 전달 성공은 판정하지 않는다.
- 관측 근거: 대표 상태의 핵심 대상, 크기·대비·위치·가림과 정보 그룹. 실제 시선 효과는 추정으로 분리.
- 검토 질문: 중요한 정보가 읽히며 보조 정보와 구분되는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-04 · Straight Ahead / Pose to Pose · 순차/주요 상태 설계

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `4. Straight Ahead Action and Pose to Pose`

원문 요약: 순차 제작과 주요 포즈 중심 제작을 구분한다.
우리 적용 해석: 상태→변화→결과의 설계에 참고. MP4만으로 제작 방식을 확정하지 않음. 주요 상태가 먼저 정의됐는가?

- 적용 예: 화면 구성 전 시작·핵심 설명·결과 상태를 계획한다.
- 반례: 완성 MP4에 키프레임 방식이라는 제작 태그를 붙인다.
- 기권·확인 조건: 렌더만 있으면 원본의 제작 접근과 키프레임 구조는 확인 불가다.
- 관측 근거: 시작·주요 상태·종료의 화면. 렌더 영상만으로 straight-ahead/pose-to-pose 제작 방식은 확정하지 않음.
- 검토 질문: 주요 상태와 관계를 계획할 수 있는가? 원본 제작 방식을 추측해 확정하지 않았는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-05 · Follow Through / Overlapping Action · 후속·겹침 동작

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `5. Follow Through and Overlapping Action`

원문 요약: 부속 움직임의 잔여와 시간 차이를 다룬다.
우리 적용 해석: 그룹의 자연스러운 연동에 후보. 데이터 표시·정렬이 늦게 흔들리면 부적합. 핵심 정보의 안정된 시간이 충분한가?

- 적용 예: 설명 아이콘이 정착한 뒤 보조 선이 정착하고 함께 유지된다.
- 반례: 숫자 라벨이 계속 튕겨 안정된 읽기 상태가 없다.
- 기권·확인 조건: 단순 순차 등장인지 관성에 의한 후속 표현인지 근거가 부족하면 나눠 기록한다.
- 관측 근거: 대상·부속 요소의 시작·정착 차이와 잔여 움직임, 중첩 구간.
- 검토 질문: 겹침과 후속 움직임이 역할을 돕는가? 정보가 안정된 채 읽힐 시간이 있는가?
- 관련 원칙: MP-07
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-06 · Slow In / Slow Out · 가속과 감속

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `6. Ease In, Ease Out`

원문 요약: 출발과 정지 부근의 변화 간격을 조절한다.
우리 적용 해석: 도착·이동의 속도 성격을 관찰. 등속 전달·기계 시뮬레이션은 선형도 적합. 목적에 맞는 속도 변화인가?

- 적용 예: 장식 설명 패널이 들어와 부드럽게 정착한다.
- 반례: 등속 이동을 설명하는 물체에 감속을 넣어 측정 의미를 바꾼다.
- 기권·확인 조건: 시계열 표본이 부족하면 원본 이징 곡선값을 추측하지 않는다.
- 관측 근거: 추적 가능한 대상의 시간별 위치·간격 변화. 관측 부족이면 곡선 미확정.
- 검토 질문: 속도 변화가 전달 목적에 맞는가? 등속이 필요한 상황을 배제하지 않았는가?
- 관련 원칙: MP-02
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-07 · Arcs · 호

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `7. Arcs`

원문 요약: 자연스러운 동작의 곡선 경로를 고려한다.
우리 적용 해석: 유기적 대상에 후보. 공정·지도·정밀 축 이동을 무조건 곡선화하지 않음. 경로가 관계를 왜곡하지 않는가?

- 적용 예: 비실측 안내 포인터가 짧은 호로 다른 설명 대상에 이동한다.
- 반례: 배관의 실제 직선 흐름을 예쁜 호로 바꿔 보인다.
- 기권·확인 조건: 카메라·투영이 움직인 경우 화면 경로와 실제 공간 경로를 구분한다.
- 관측 근거: 대상의 화면상 경로와 곡률. 원본 경로 핸들은 미확정.
- 검토 질문: 곡선 경로가 대상 성격에 맞는가? 공간·공정 관계를 왜곡하지 않는가?
- 관련 원칙: MP-05
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-08 · Secondary Action · 보조 동작

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `8. Secondary Action`

원문 요약: 보조 행동은 주 행동을 지원한다.
우리 적용 해석: 주제 이해를 지원할 때만 추가. 정보 읽는 중 반복 장식은 제한. 시선을 뺏지 않는가?

- 적용 예: 핵심 부품 공개에 맞춰 설명선이 나타난 뒤 멈춘다.
- 반례: 본문을 읽는 동안 보조 캐릭터가 반복 춤을 춘다.
- 기권·확인 조건: 보조 요소가 있는 것과 보조 동작이 있는 것을 혼동하지 않는다.
- 관측 근거: 주요 동작과 보조 대상의 변화·주목 경쟁·정보 가림.
- 검토 질문: 보조 동작이 이해를 지원하는가? 읽는 동안 시선을 빼앗지 않는가?
- 관련 원칙: MP-09
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-09 · Timing · 타이밍

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `9. Timing`

원문 요약: 동작의 시간은 성격과 무게 표현에 관여한다.
우리 적용 해석: 등장·정착·읽기·전환의 관계 기록. UI ms를 영상 기준으로 쓰지 않음. 내용과 내레이션을 따라갈 수 있는가?

- 적용 예: 큰 구조물 공개 뒤 명칭과 관계를 읽을 유지 구간을 둔다.
- 반례: 모든 대상에 같은 고정 길이를 적용해 긴 설명을 잘라낸다.
- 기권·확인 조건: 발화와 대상 시청 환경이 없으면 충분한 읽기 시간을 확정하지 않는다.
- 관측 근거: 등장·완성·유지·퇴장 상태의 시간 관계와 내레이션 대응.
- 검토 질문: 장면을 이해하고 읽을 시간이 확보되는가?
- 관련 원칙: MP-01
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-10 · Exaggeration · 과장

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `10. Exaggeration`

원문 요약: 현실을 바탕으로 표현을 강화한다.
우리 적용 해석: 설명을 돕는 강조로 후보. 수치·변형·공간 규모의 사실성은 보존. 무엇이 사실이고 무엇이 강조인지 구분되는가?

- 적용 예: 데이터 도형 밖의 링으로 핵심 항목을 강조한다.
- 반례: 막대 길이를 수치보다 부풀려 성과가 커 보이게 한다.
- 기권·확인 조건: 실측/개념도 구분이 없으면 과장 허용 폭을 확정하지 않는다.
- 관측 근거: 형상·크기·속도·표식의 강조와 실제 데이터/대상의 차이.
- 검토 질문: 강조가 사실·규모·수치의 오인을 만들지 않는가?
- 관련 원칙: MP-08
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-11 · Solid Drawing · 입체·구조 표현

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `11. Solid Drawing`

원문 요약: 입체감·부피·균형 있는 구조를 고려한다.
우리 적용 해석: 도표·3D 대상의 축·깊이·구조에 해석 적용. 2D 화면에 사실주의를 강요하지 않음. 구조가 일관적인가?

- 적용 예: 개념 분해도에서 부품의 연결과 투영을 일관되게 유지한다.
- 반례: 부품 접점을 바꾸거나 장식 그림자를 실제 깊이로 설명한다.
- 기권·확인 조건: 2D 음영만으로 원본이 3D 제작인지 단정하지 않는다.
- 관측 근거: 형태·깊이·투영·축·부분 연결의 일관성. 실제 제작 기법은 미확정.
- 검토 질문: 구조와 공간이 일관되며 설명하려는 관계가 보이는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## AP-12 · Appeal · 매력

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `12. Appeal`

원문 요약: 관심을 끄는 캐릭터와 표현을 지향한다.
우리 적용 해석: 주제·회사 톤·읽기 쉬움을 함께 확인. 장식 수·독특함만 점수화하지 않음. 보고 이해하고 기억할 이유가 있는가?

- 적용 예: 기술 설명 톤에 맞는 간결한 형태와 명료한 리듬을 비교 평가한다.
- 반례: 효과가 많거나 낯설다는 이유만으로 매력 통과를 준다.
- 기권·확인 조건: 주관 평가·시청자 검증 없이 기억률과 이해도 향상을 확정하지 않는다.
- 관측 근거: 주제·시청 목적·형태·리듬·브랜드의 관계. 매력은 관측 사실이 아닌 별도 평가.
- 검토 질문: 주제에 맞고 이해·기억에 도움이 되는가? 독특함만으로 통과시키지 않았는가?
- 관련 원칙: MP-10
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## MP-01 · Timing, Spacing and Rhythm · 시간·간격·리듬

출처: [Jorge 모션 10원칙](https://www.learnsquared.com/courses/motion-design) · public_course_outline · `Lesson 2 / Timing, Spacing and Rhythm`

원문 요약: 공식 강의의 항목명만 확인. 상세 정의는 강의 본문 미검토.
우리 적용 해석: 등장·읽기·강조·휴지의 리듬 확인. 모든 동작을 음악 박자에 고정하지 않음. 전달 순서가 자연스러운가?

- 적용 예: 단계 사이 간격을 달리하고 설명이 완성된 뒤 읽기 시간을 둔다.
- 반례: 음악 박자에 맞추느라 원인 설명 전에 결과가 사라진다.
- 기권·확인 조건: 등장 간격만 보고 정보의 인과·순서를 확정하지 않는다.
- 관측 근거: 사건 간 간격·움직임·읽기 유지·휴지와 음성/음악의 관계.
- 검토 질문: 리듬이 정보 순서와 읽기 시간을 돕는가?
- 관련 원칙: AP-09
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님

## MP-02 · Eases · 이징

출처: [Jorge 모션 10원칙](https://www.learnsquared.com/courses/motion-design) · public_course_outline · `Lesson 2 / Eases`

원문 요약: 공식 강의의 항목명만 확인. 상세 정의는 강의 본문 미검토.
우리 적용 해석: 가속/감속을 목적과 연결. Bézier 피팅 결과를 원본 AE 핸들로 단정하지 않음. 출발·도착의 성격이 맞…7825 tokens truncated…제공 시간·경로를 보존하고 장식 패널만 이징 후보를 검토한다.
- 오용 반례: 전부 이징을 넣으면 속도 변화에 관한 설명이 달라진다.
- 기권 조건: 실측 데이터와 시간 대응이 없으면 실제 운동이라는 판정을 보류한다.
- 허용되는 미사용·예외: 등속 유지가 의도와 데이터에 맞으면 이징 미사용 자체를 실패로 보지 않는다.

## MC-02 · 비교 항목 동시 유지

A/B 공법의 같은 항목을 비교한다.

- 관련 원칙: MR-04, IP-09
- 선택할 판단: 등장은 순차여도 비교할 때는 두 항목을 함께 유지한다.
- 오용 반례: 항상 stagger를 써서 A를 지운 뒤 B를 보여주면 기억 부담을 키울 수 있다.
- 기권 조건: 비교 대상과 대응 항목의 출처가 없으면 비교 적합성을 확정하지 않는다.
- 허용되는 미사용·예외: 동시 공개가 내용 관계에 맞으면 순차 등장 미사용은 실패가 아니다.

## MC-03 · 무음·자막 필요

무음 회의실에서 도표 설명을 본다.

- 관련 원칙: IP-03, IP-08
- 선택할 판단: 음성 중심의 중복 감소 원칙을 자동 적용하지 않고 자막·핵심 용어·단위를 유지한다.
- 오용 반례: 발화와 중복이라는 이유만으로 모든 글자를 삭제하면 정보를 잃는다.
- 기권 조건: 배포 환경과 자막 요구가 없으면 삭제가 아니라 확인을 제안한다.
- 허용되는 미사용·예외: 필요한 중복을 유지했다는 이유만으로 실패를 주지 않는다.

## MC-04 · 장식 카운트와 실적

최종 실적 값만 제공되고 연도별 중간값은 없다.

- 관련 원칙: MR-08, AP-10
- 선택할 판단: 최종값과 단위를 고정하고 카운트 중간값은 연출값으로 표시·분리한다.
- 오용 반례: 중간 숫자를 관측 연도의 실제 실적으로 저장하면 허위 시계열이 된다.
- 기권 조건: 값의 종류가 불분명하면 보이는 숫자는 기록하되 실측 주장만 보류한다.
- 허용되는 미사용·예외: 정지 최종값으로 정확히 전달할 수 있으면 카운트 미사용을 실패로 보지 않는다.

## MC-05 · 부품과 라벨 공동 이동

렌더 MP4만 있고 원본 AE는 없다.

- 관련 원칙: MR-07, MR-03
- 선택할 판단: 대상과 라벨의 시간상 연동은 관측하고 AE parent·인과 관계는 따로 미확인으로 둔다.
- 오용 반례: 같이 움직였으니 parent로 제작했고 실제 인과도 있다는 기록은 근거를 넘는다.
- 기권 조건: 전체 공동 이동만으로 대상을 분리 추적하지 못하면 연동 관측의 확신도도 낮춘다.
- 허용되는 미사용·예외: 구현을 확인하지 못해도 충분한 화면 관측은 지우지 않는다.

## MC-06 · 정지 구조도와 동적 공정

한 화면은 부품 위치를, 다른 화면은 회전·정지 시점을 설명한다.

- 관련 원칙: AP-09, IP-09, MR-06
- 선택할 판단: 위치 읽기는 정지 상태·누적 그림, 시간 관계 설명은 동작 후보로 나눠 비교한다.
- 오용 반례: 모든 정보를 계속 움직이거나 모든 동작을 정지로 바꾸는 것은 서로 다른 과제를 혼동한다.
- 기권 조건: 참고 연구의 과제·표본은 회사 영상과 다르므로 효과를 보장하거나 수치를 전용하지 않는다.
- 허용되는 미사용·예외: 도형이 정지한 동안 자막이 유지되는 것도 정상 시간 사건이다.

## MC-07 · 같은 정보·다른 시청자

초보자와 숙련자의 사전 지식이 입력으로 확인돼 있다.

- 관련 원칙: IP-07, IP-10
- 선택할 판단: 초보자에 개념 소개, 숙련자에 짧은 요약을 조건부 참고로 제안한다. 사용자 A는 참고 사용 범위 선택이며 회사 영상 효과·규칙 승인으로 취급하지 않는다.
- 오용 반례: 부서나 직급만으로 설명 수준을 자동 축소·확대한다.
- 기권 조건: 동일 직무라도 주제별 지식이 다를 수 있으므로 사전 지식 근거가 없으면 unknown이다.
- 허용되는 미사용·예외: 숙련자에게 기본 설명이 꼭 필요하다는 근거가 있으면 간단 소개를 유지할 수 있다.

## MC-08 · 고정 영상과 웹 플레이어

자동재생 영상 옆에 문서가 있고 확대 버튼이 있는 배포 환경을 가정한다.

- 관련 원칙: ACC-01, ACC-02, ACC-03
- 선택할 판단: 콘텐츠 플래시, 자동 움직임·업데이트 제어, 클릭 확대의 감소 모션을 각각 다른 조건으로 검토한다.
- 오용 반례: MP4가 5초 넘는다는 이유만으로 자체 버튼 누락 실패를 주거나 정지 버튼만으로 플래시 안전을 판정한다.
- 기권 조건: 페이지 환경·시간·필수성·실제 검사 근거가 없으면 적용/안전 모두 보류한다.
- 허용되는 미사용·예외: 특정 조건 비적용과 실제 미검사는 다르며 WCAG 전체 적합을 선언하지 않는다.
02_원칙과레이아웃\10_확장레이아웃_후보와반례.md
# 14개 밖의 레이아웃 지원 지식 후보

사용자 A 선택으로 표·순환·조건 분기를 별도 후보로 정리했다. candidate_id는 R2 분류ID가 아니다. 기존 정의를 실제로 만족하는 범위만 기존ID에 연결하고, 맞지 않으면 후보/미분류를 유지한다.

## 표·매트릭스 · LAYOUT-CAND-TABLE

- 선택 조건: 여러 대상의 여러 항목을 정확히 조회·대조할 때
- 읽는 순서: 행·열 제목→대상과 항목의 교차 셀→단위·주석→선택한 차이
- 설계 판단: 같은 항목의 단위·기준·기간을 맞추고 빈칸·미제공·0을 구분한다. 좁은 화면에서는 항목 구간을 나누되 공통 행/열 머리를 유지한다.
- 적용 예: 가상의 공법 A/B를 비용·공기·조건 열로 대응하고 각 열의 단위를 표시한다.
- 반례: 보기 좋게 빈셀을0으로 채우거나 다른 단위를 한열로 비교하고 카드처럼 꾸몄다는 이유로 의미 없이 카드ID를 부여한다.
- 대안: 정확한 값 조회가 목적이 아니면 차트·분할비교·단일초점을 함께 검토한다.
- 기존ID 연결 조건: 행열 표 자체를 카드 그룹으로 자동 기록하지 않는다. 분할 비교의 실제 정의를 만족한 범위만 비교 후보로 연결할 수 있다.
- 미분류 처리: 정보가 맞지 않으면R2의other_candidate/미분류와후보설명을유지한다. 이candidate_id는taxonomy term_id가아니다.
- 기권: 행·열 기준과 단위·미제공 의미가 없으면 정밀 비교 적합성을 보류한다.

## 순환·반복 흐름 · LAYOUT-CAND-CYCLE

- 선택 조건: 마지막 단계에서 앞 단계로 돌아가는 의미가 자료로 확인될 때
- 읽는 순서: 출발·현재 단계→진행 방향→돌아가는 연결과 재시작 조건
- 설계 판단: 원형은 후보다. 반복의 방향·종료 또는 재시작 조건을 명칭으로 표현하고 단계의시간길이가 같다고 암시하지 않는다.
- 적용 예: 점검→조치→재점검으로 돌아가는 절차를 복귀 화살표와 반복 조건으로 설명한다.
- 반례: 단발 접수→검토→승인을 원형으로 배치해 승인 뒤 다시 접수해야 하는 것처럼 보이게 한다.
- 대안: 종료가 있는 일회성 흐름이면 선형 프로세스, 복잡한 반복·여러 연결은 연결 구성 후보를 검토한다.
- 기존ID 연결 조건: 노드·연결 구조가기존연결구성정의에맞으면해당범위의NETWORK후보만연결한다. 닫힌순환전체를PROCESS-LINE으로강제하지않는다.
- 미분류 처리: 기존ID가맞지않는부분은후보유지. 새순환taxonomyID를등록하지않는다.
- 기권: 실제 복귀·반복·종료 근거가 없으면 순환 의미는 보류한다.

## 조건 분기·판단 흐름 · LAYOUT-CAND-BRANCH

- 선택 조건: 조건에 따라 다른 경로로 갈리는 절차를 설명할 때
- 읽는 순서: 입력→조건 질문→각 경로의 라벨→결과·합류
- 설계 판단: 조건 이름과 각 경로의 의미를 적는다. 배치·도형과 실제 조건 근거를 나누며 예/아니오 방향을 바꾸면 라벨도 함께 검토한다.
- 적용 예: 검토 결과에 따라 승인 또는 보완 요청으로 나뉘는 경로를 조건과 함께 보여 준다.
- 반례: 실제 검토 자료가 없는데 마름모를 그려 승인 조건을 지어내거나 예/아니오를뒤집는다.
- 대안: 조건이 없고 순서만 있으면 선형 프로세스, 관계 소개만이면 연결 구성 후보를 검토한다.
- 기존ID 연결 조건: 확인된노드·관계구조가NETWORK정의에맞는범위만연결한다. 분기도형을그렸다는이유로REL-CAUSE나절차진실을확정하지않는다.
- 미분류 처리: 새분기taxonomyID는없고지원지식후보로남긴다. 맞지않으면부분미분류를허용한다.
- 기권: 조건·경로·결과의 시나리오 근거가 없으면 절차 의미는 보류한다.
[
  {
    "id": "CURVE-LINEAR",
    "name_ko": "등속",
    "definition": "일정한 변화율",
    "include_when": "관측 궤적",
    "exclude_or_limit": "루프 외에도 의미상 적합 가능",
    "version": "0.1.1"
  },
  {
    "id": "CURVE-ACCEL",
    "name_ko": "가속",
    "definition": "변화율이 커짐",
    "include_when": "관측 궤적",
    "exclude_or_limit": "원본 핸들 값은 별도",
    "version": "0.1.1"
  },
  {
    "id": "CURVE-DECEL",
    "name_ko": "감속",
    "definition": "변화율이 작아짐",
    "include_when": "관측 궤적",
    "exclude_or_limit": "노이즈·가림 확인",
    "version": "0.1.1"
  },
  {
    "id": "CURVE-INOUT",
    "name_ko": "가속 후 감속",
    "definition": "변화율이 커졌다가 작아짐",
    "include_when": "관측 궤적",
    "exclude_or_limit": "같은 모양도 서로 다른 구현 가능",
    "version": "0.1.1"
  },
  {
    "id": "CURVE-OSCILLATE",
    "name_ko": "진동·정착",
    "definition": "반복 방향·진폭 변화 후 정착",
    "include_when": "관측 진동",
    "exclude_or_limit": "물리 파라미터 유일 복원 금지",
    "version": "0.1.1"
  },
  {
    "id": "TIME-SEQUENCE",
    "name_ko": "순차 발생",
    "definition": "사건이 차례대로 시작 또는 완료",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-SIMULTANEOUS",
    "name_ko": "동시 발생",
    "definition": "사건의 시작 또는 완료가 함께 관측",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-OVERLAP",
    "name_ko": "중첩",
    "definition": "둘 이상 동작의 시간 범위가 겹침",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-DELAY",
    "name_ko": "지연",
    "definition": "대응 사건 사이 시작·완료 시각 차이",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-HOLD",
    "name_ko": "유지",
    "definition": "정보 또는 상태가 식별 가능하게 지속",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-STILL",
    "name_ko": "정지",
    "definition": "대상 또는 화면의 변화가 관측되지 않는 구간",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-LOOP",
    "name_ko": "반복",
    "definition": "상태·동작이 반복",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  },
  {
    "id": "TIME-OVERSHOOT",
    "name_ko": "목표 초과 후 복귀",
    "definition": "최종 상태를 지나친 뒤 돌아오는 변화",
    "include_when": "기준 사건·대상·시간 범위를 함께 기록",
    "exclude_or_limit": "정확한 시각·원본 키프레임을 용어만으로 확정하지 않음",
    "version": "0.1.1"
  }
]
        if not decision or any(decision.get(k)!=v for k,v in {'object_id':r['record_id'],'object_version':r['version'],'approval_kind':review['approval_kind'],'reviewer':review['reviewer'],'approved_scope':review['approved_scope']}.items()):errors.append('대상·종류·범위가 일치하는 별도 사람 검수 결정 없음')
        if decision and (decision.get('state')!='approved' or decision.get('reviewed_at')!=review['reviewed_at'] or not FormatChecker().conforms(decision.get('reviewed_at'),'date-time')):errors.append('승인 결정의 상태·검수 시각 불일치')
        if review['object_version']!=r['version']:errors.append('승인 대상 버전 불일치')
        for ref in evidence:
            if review['evidence_versions'].get(ref)!=evidence[ref]['version']:errors.append('승인 근거 버전 미고정')
    return errors
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    errors=validate_catalogs()
    if args.record:errors+=validate_record(json.loads(args.record.read_text(encoding='utf-8')))
    else:errors+=validate_record(read('04_기록규격/설명용_단계구성_예시.json'))
    result={'valid':not errors,'errors':errors,'scope':'Phase 00 데이터·기록 계약. 실영상 정확도/효과 검증 아님.'}
    if args.output:
        output=args.output.resolve()
        if not output.is_relative_to(BASE):raise ValueError('검사 결과는 Phase 00 안에 저장')
        output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())

```

### 실행 6
```powershell
$db = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\inputs\Phase00'; Test-Path -LiteralPath 'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe'; $text=Get-Content -Raw -LiteralPath (Join-Path $db '02_원칙과레이아웃\03_모션원칙_적용예와반례.md'); [regex]::Matches($text,'(?ms)^## (?:AP-06|MP-02|IP-02|IP-07|IP-10) .*?(?=^## |\z)')|ForEach-Object {$_.Value}; Get-Content -LiteralPath (Join-Path $db '02_원칙과레이아웃\04_모션원칙_충돌과예외.md') -TotalCount 22
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
True
## AP-06 · Slow In / Slow Out · 가속과 감속

출처: [Adobe 애니메이션 12원칙](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) · public_article_sections · `6. Ease In, Ease Out`

원문 요약: 출발과 정지 부근의 변화 간격을 조절한다.
우리 적용 해석: 도착·이동의 속도 성격을 관찰. 등속 전달·기계 시뮬레이션은 선형도 적합. 목적에 맞는 속도 변화인가?

- 적용 예: 장식 설명 패널이 들어와 부드럽게 정착한다.
- 반례: 등속 이동을 설명하는 물체에 감속을 넣어 측정 의미를 바꾼다.
- 기권·확인 조건: 시계열 표본이 부족하면 원본 이징 곡선값을 추측하지 않는다.
- 관측 근거: 추적 가능한 대상의 시간별 위치·간격 변화. 관측 부족이면 곡선 미확정.
- 검토 질문: 속도 변화가 전달 목적에 맞는가? 등속이 필요한 상황을 배제하지 않았는가?
- 관련 원칙: MP-02
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님


## MP-02 · Eases · 이징

출처: [Jorge 모션 10원칙](https://www.learnsquared.com/courses/motion-design) · public_course_outline · `Lesson 2 / Eases`

원문 요약: 공식 강의의 항목명만 확인. 상세 정의는 강의 본문 미검토.
우리 적용 해석: 가속/감속을 목적과 연결. Bézier 피팅 결과를 원본 AE 핸들로 단정하지 않음. 출발·도착의 성격이 맞는가?

- 적용 예: 표식 이동의 정착을 조절하되 실측 대상은 원래 시간 변화를 보존한다.
- 반례: 자연스러워 보이도록 측정 대상의 속도 변화를 바꾼다.
- 기권·확인 조건: 완성 영상의 근사 속도곡선을 원본 AE 핸들값으로 기록하지 않는다.
- 관측 근거: 관측 변화율의 가속·감속·정착. 추적 오차와 피팅 근거.
- 검토 질문: 이징 성격이 동작 역할에 맞는가? 원본 핸들값을 복원한 것처럼 쓰지 않았는가?
- 관련 원칙: AP-06
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님


## IP-02 · 정보 표식

출처: [Mayer·Fiorella 불필요 처리 감소](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning/F29A19FCD34C542806F736E0661C05F5) · publisher_summary · `Chapter 14 Summary / signaling`

원문 요약: 필수 정보의 조직을 표식으로 드러낸다.
우리 적용 해석: 강조·표식·단계번호의대상과순서

- 적용 예: 침투수 경로에 해당하는 선만 표시하고 단계 번호를 연결한다.
- 반례: 모든 항목에 같은 강조색·깜빡임을 준다.
- 기권·확인 조건: 강조가 원인 증명이나 실제 시선 효과를 입증하지는 않는다.
- 관측 근거: 강조색·단계 번호·표식의 대상과 공개 순서.
- 검토 질문: 중요한 정보와 구조를 구분하게 하는가? 모든 항목을 강조하지 않았는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님


## IP-07 · 사전 개념 소개

출처: [Mayer·Fiorella 필수 처리 관리](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning/A9E77D0172F905AC957689D1771E2888) · publisher_summary · `Chapter 19 Summary / pre-training`

원문 요약: 핵심 개념의 이름과 성질을 미리 익힌다.
우리 적용 해석: 낯선기술·구조의짧은전체도·범례

- 적용 예: 새 입사자 영상에서 본 설명 전에 침투수·양압의 명칭과 역할을 소개한다.
- 반례: 짧은 공지에서도 모든 전문용어를 길게 설명한다.
- 기권·확인 조건: 시청자 지식과 용어 난도를 모르면 필요성을 후보로 둔다.
- 관측 근거: 핵심 명칭·구성 요소·역할이 본 설명 전에 소개되는지.
- 검토 질문: 시청자가 모를 개념을 준비하는가? 전문가에게 불필요한 반복은 없는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님


## IP-10 · 숙련도별 설명 조정

출처: [Kalyuga 숙련도 역전 원칙 — 2021 공식 요약](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/expertise-reversal-principle-in-multimedia-learning/F6793786D8F79519A22E967FC2563839) · publisher_summary · `Chapter 13 Summary / expertise reversal`

원문 요약: 초보자에게 유효한 지원이 전문가에게 방해될 수 있다.
우리 적용 해석: 입력·인터뷰·검토 자료 등으로 시청자의 해당 주제 사전 지식이 확인될 때 설명 지원의 깊이를 비교한다.

- 적용 예: 입문자용 개념 소개와 숙련자용 요약을 선택 후보로 나눈다.
- 반례: 기획실은 비전문가라는 이유로 모든 인원의 지식을 낮게 판정한다.
- 기권·확인 조건: 실제 사전 지식 근거가 없으면 대상의 숙련도는 unknown이다.
- 관측 근거: 시청자의 사전 지식은 제공 근거가 있을 때만 기록. 화면에는 개념 소개·요약의 분량과 순서를 관측하며 학습 효과는 별도 평가한다.
- 검토 질문: 시청자의 해당 주제 사전 지식 근거가 있는가? 공식 요약 수준의 참고를 효과 보장·회사 의무 규칙으로 확장하지 않았는가?
- 관련 원칙: 현재 연결 없음
- 기본 추천: 조건부 참고 가능. 회사 필수 규칙 아님


# 원칙이 충돌할 때의 판단 사례

아래 8개는 프로젝트의 설명용 판단이다. 실제 회사 영상 검증 결과나 회사 승인 규칙이 아니다. 효과의 유무·종류만으로 정답을 판정하지 않는다.

## MC-01 · 등속 운동 설명

실측 이동의 속도와 경로를 보여준다. 장식 패널의 이동과 구분한다.

- 관련 원칙: AP-06, MP-02
- 선택할 판단: 측정 대상은 제공 시간·경로를 보존하고 장식 패널만 이징 후보를 검토한다.
- 오용 반례: 전부 이징을 넣으면 속도 변화에 관한 설명이 달라진다.
- 기권 조건: 실측 데이터와 시간 대응이 없으면 실제 운동이라는 판정을 보류한다.
- 허용되는 미사용·예외: 등속 유지가 의도와 데이터에 맞으면 이징 미사용 자체를 실패로 보지 않는다.

## MC-02 · 비교 항목 동시 유지

A/B 공법의 같은 항목을 비교한다.

- 관련 원칙: MR-04, IP-09
- 선택할 판단: 등장은 순차여도 비교할 때는 두 항목을 함께 유지한다.
- 오용 반례: 항상 stagger를 써서 A를 지운 뒤 B를 보여주면 기억 부담을 키울 수 있다.
- 기권 조건: 비교 대상과 대응 항목의 출처가 없으면 비교 적합성을 확정하지 않는다.

```

### 실행 7
```powershell
& 'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe' -B 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1\build_and_check.py'
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
{"catalog_errors": [], "draft_errors": [], "draft_version": "0.1.1", "draft_sha256": "1e4266c3445ffe980a6b82633d94916023a213c17cfa198305892396777d1fd0", "input_hashes_unchanged": true, "card_count": 7, "lookup_hit_counts": {"���": 1, "IP-10": 1, "LAYOUT-CAND-TABLE": 0}}

```

### 실행 8
```powershell
$run = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace\iteration-2\eval-01-회의메모_지식정리\new_skill\run-1'; $draft=Get-Content -Raw -LiteralPath (Join-Path $run 'outputs\회의메모_공통지식초안.json')|ConvertFrom-Json; $v=Get-Content -Raw -LiteralPath (Join-Path $run 'outputs\draft_validation.json')|ConvertFrom-Json; $catalog=Get-Content -Raw -LiteralPath (Join-Path $run 'outputs\catalog_validation.json')|ConvertFrom-Json; $queries=Get-Content -Raw -LiteralPath (Join-Path $run 'outputs\lookup_results.json')|ConvertFrom-Json; [PSCustomObject]@{version=$draft.version;cards=@($draft.cards|ForEach-Object {$_.title});catalog_errors=$catalog.errors;draft_errors=$v.errors;input_files_compared=$v.input_files_compared;input_hashes_unchanged=$v.input_hashes_unchanged;backup_hash_match=$v.backup_hash_match;lookup_keys=@($queries.queries.PSObject.Properties.Name);after_sha256=$v.after_sha256} | ConvertTo-Json -Depth 6
```
종료 코드: 0
```text
Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
{
  "version": "0.1.1",
  "cards": [
    "단계 번호는 정보 관계에 따라 유지한다",
    "표·매트릭스는 기존 확장 후보로 유지",
    "순환·반복 흐름은 복귀 근거를 요구",
    "조건 분기는 조건·경로·결과를 구분",
    "부서명으로 숙련도를 단정하지 않고 설명 깊이를 조정",
    "등속 설비 설명에는 선형 변화율이 적합할 수 있음",
    "CI 관측색은 공식 본문색과 구분"
  ],
  "catalog_errors": [],
  "draft_errors": [],
  "input_files_compared": 28,
  "input_hashes_unchanged": true,
  "backup_hash_match": true,
  "lookup_keys": [
    "등속",
    "IP-10",
    "LAYOUT-CAND-TABLE"
  ],
  "after_sha256": "1e4266c3445ffe980a6b82633d94916023a213c17cfa198305892396777d1fd0"
}

```

## 파일 생성/보강
1. functions.exec에서 tools.apply_patch로 outputs/회의메모_공통지식초안.json v0.1.0 신규 생성. 실제 반환은 오류 없는 {}.
2. 같은 도구로 build_and_check.py 생성 및 strict JSON 중복 키 검사/한국어 문구 보완. 실제 반환은 오류 없는 {}. 이 파일에 실행한 읽기·수정·검사 코드가 보존되어 있다.
3. 지정 Python으로 build_and_check.py 실제 실행: exit_code=0.
4. 빌더는 초기 초안을 outputs/backup/회의메모_공통지식초안_v0.1.0.json에 복사하고 SHA 일치를 확인한 뒤, 참조 버전·출처 위치·해시·검사 범위를 보강해 같은 논리 대상 v0.1.1로 저장.
5. 실제 기존 validate_catalogs() 오류 [], 새 초안 구조·참조 검사 오류 []. 조회 결과 등속=1, IP-10=1, LAYOUT-CAND-TABLE=0. 마지막 것은 조회기가 확장후보 목록을 검색하지 않는 범위 때문이며, 별도 후보 JSON을 직접 대조했다.
6. 28개 허용 읽기 자료의 보강/검사 전후 해시 일치. 입력의 의미·값·상태를 수정한 파일 없음. 이 비교는 읽기 자료 28개의 해당 시점 전후만을 증명하며 DB 전체나 세션 시작 전 상태 검사는 아니다.
7. 최종 초안 SHA256: 1e4266c3445ffe980a6b82633d94916023a213c17cfa198305892396777d1fd0.
8. outputs/설명.md와 이 transcript.md를 apply_patch로 신규 생성.

## 오류·한계
- PowerShell 호출마다 InitializeDefaultDrives/FileSystem provider 경고가 출력됐다. 해당 명령 종료 코드는 0이며 이후 파일 읽기/쓰기·지정 Python 검사는 실제 성공했다. 경고를 숨기지 않고 위 반환에 보존했다.
- 초기 여러 파일/긴 문서의 전체 출력은 도구 한도에서 잘렸다. 필요한 AP-06/MP-02/IP-02/IP-07/IP-10 및 충돌 사례 MC-01은 선택 재조회했다. evidence_manifest는 이 읽기 깊이를 구분한다.
- Python stdout의 등속 문자열이 PowerShell 출력 인코딩에서 깨져 보였으나 저장 JSON은 UTF-8이고 후속 Get-Content/ConvertFrom-Json 확인에서 등속 조회 키와 한국어 제목이 정상 출력됐다.
- 실행스킬 참조가 지시한 05_세스킬_이식설계안.md를 읽으면서 같은 문서의 R8 평가 설계 문단도 함께 출력됐다. 그 문단은 이 작업의 근거나 자기채점에 사용하지 않았다. 다른 실행/채점표/과거평가 원문은 열지 않았다.
- 외부 스킬 원문·원격 자료·CI 바이너리가 포함되지 않은 시험 사본이라는 한계를 유지했다. 기존 조사기록의 read_depth/sections는 과거 선언이며 이번 독립 외부 원문 열람 실적이 아니다.
- validate_catalogs()는 지원하는 기존 목록/연결 검사다. 새 JSON에 R4 영상기록 스키마를 억지 적용하지 않았다. 별도 자체 구조 검사는 내용 진실성·회사 승인·실제 시청효과를 증명하지 않는다.
- R6 전체 원문/자산, R7 품질/연결, 사람 판단/승인, 실제 영상 추출/OCR/좌표·시간·모션 측정은 미수행.
- 운영 정본/고정 목록 재생성·등록·기본 전환 없음. 원래 정본을 수정하지 않아 정본 backup/diff는 없으며, 새 초안의 초기 버전 backup/diff만 생성.
- 질문 도구와 사람 연락은 사용하지 않았다. 판단용 질문·4개 대안·추천안은 결과 JSON에만 저장했다.

## 결과 파일
- outputs/회의메모_공통지식초안.json — v0.1.1, 카드 7개, 판단 안건 3개, 근거 manifest 24개
- outputs/설명.md — 짧은 한국어 설명
- outputs/catalog_validation.json — 실제 기존 목록 검사
- outputs/draft_validation.json — 실제 새 초안의 제한된 검사/보존 증거
- outputs/lookup_results.json — 실제 조회 결과 및 한계
- outputs/input_hashes_before.json, input_hashes_after.json — 읽기 자료 28개 비교
- outputs/backup/회의메모_공통지식초안_v0.1.0.json — 초기 초안 보존
- outputs/draft_v0.1.0_to_v0.1.1.diff — 새 초안 보강 diff
- build_and_check.py — 실행 코드

빌더는 신규 backup을 xb로 생성하므로 동일 경로에 재실행하면 덮어쓰기 대신 중단한다. 기존 결과를 보존한 상태에서 재실행 방식을 정해야 한다.

