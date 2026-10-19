from pathlib import Path
from hashlib import sha256
from collections import Counter
from datetime import datetime,timezone
import json,re
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
audit=json.loads((WORK/'research/ponytail-rea-20261019/source-audit.json').read_text(encoding='utf-8'))
prior=json.loads((WORK/'video-skill-system/research/source-lock.json').read_text(encoding='utf-8'))
candidate=WORK/'skill-pattern-linking-20261019/candidate/company-video-grammar-analyzer'
CODE='코드 일부 반영';DOC='지침·형식 반영';GAP='미구현';EXCLUDE='직접 이식 제외·평가 참고'
details={
'P1':(DOC,'references/judgment-handoff.md','선택 순서는 지침으로만 존재. 실제 후보 조회·대안 평가·선택 실행기는 없음.'),
'P2':(CODE,'scripts/pattern_library.py','번호 등록·단일 항목 추출만 구현. 내용/조건 기반 후보 검색과 재사용 판별은 없음.'),
'P3':(EXCLUDE,None,'전역 활성화 훅·원본 코드 색인기는 의도적으로 설치하지 않음.'),
'P4':(DOC,'SKILL.md','구체 주장·근거 대조 지침. 자동 의미 검수와 전문가 리뷰 실행기는 없음.'),
'P5':(CODE,'scripts/check_record.py','미해결·한계 기록 검사 일부. 재검토 조건을 실행하는 비용/부채 관리기는 없음.'),
'P6':(EXCLUDE,None,'원본 실험의 효과 수치를 영상 효과로 채택하지 않음. 우리 효과 비교는 미실행.'),
'P7':(CODE,'scripts/check_record.py','일부 오류 주입 시험만 구현. 독립 문맥·조건 오염을 통제한 새 비교 시험은 없음.'),
'R1':(CODE,'scripts/check_record.py','원본/프레임/시각/유형 연결 일부. provider/profile/authority/semantic evidence hash 전체 모델은 없음.'),
'R2':(CODE,'scripts/check_record.py','미해결 질문·다음 확인·해소 주장 검사. revision 기반 갱신 도구는 없음.'),
'R3':(CODE,'scripts/check_record.py','open/resolved/withdrawn/out_of_scope 구분만 일부. expected_revision 충돌 제어 없음.'),
'R4':(CODE,'scripts/check_record.py','관측/계산/추론과 supported 해소 주장 자격 일부. 환경·authority 자격 모델 없음.'),
'R5':(CODE,'scripts/check_record.py','추론만으로 관측 요구를 닫는 오류를 거부하는 자체 합성 검사. 시각 진실성 판정 아님.'),
'R6':(CODE,'scripts/check_record.py','선언한 대상×속성의 구간 공백·참조 검사. 전체 재구성 의무/구현 담당/검증 차원 관리 없음.'),
'R7':(CODE,'scripts/check_record.py','등록된 누락 검사와 한계 표시는 있음. 처음 발견하지 못한 대상 탐지는 없음.'),
'R8':(CODE,'scripts/check_record.py','해소 주장 유형·동일 대상·검수 상태 검사 일부. 완전한 근거 권위/환경 검증 아님.'),
'R9':(GAP,None,'최신 검수 판정 묶음 선택·상충 판정 유지 실행기는 없음.'),
'R10':(GAP,None,'영상 명세→편집 가능한 구현→렌더→원본 대조의 역설계 실행 없음.'),
'R11':(CODE,'scripts/pattern_library.py','파일 해시와 고정 스냅샷만 일부. 분석 설정·시간 매핑·검수 판본에 따른 캐시 재사용 관리 없음.'),
'R12':(EXCLUDE,None,'정지 PNG 차이를 영상 의미·모션 성공 판정으로 이식하지 않음.'),
'R13':(EXCLUDE,None,'애니메이션을 비활성화하는 브라우저 캡처를 모션 검증으로 이식하지 않음.'),
'R14':(CODE,'scripts/check_record.py','기록의 스킬 판본 검사·후보 사본 해시 확인. 실제 기본 호출 경로 반영은 안 됨.'),
'R15':(CODE,'scripts/reuse_map.py','사례와 패턴의 역할·관계 연결 일부. 요구→담당 구현→렌더 검증의 의무 장부 없음.'),
'T1':(DOC,'references/judgment-handoff.md','관측과 추론, 분석과 판단의 분리 지침. 별도 이해/평가 실행 흐름은 없음.'),
'T2':(GAP,None,'예산·재시도·실패 보존을 포함한 새 분석 배치 실행기는 없음.'),
'T3':(CODE,'scripts/check_record.py','형식/근거/조합 오류를 분별하는 합성 시험. A/4 의미 오답을 자동 판별하지 못함.'),
'S1':(CODE,'references/output-contract.md','식별·속성·원자 주장 슬롯 추가. 실제 새 자료 행동 개선은 미입증.'),
'S2':(CODE,'scripts/check_record.py','형식 통과와 content_verified=false를 구분. 전체 품질 합격 판정기는 없음.'),
'I1':(DOC,'references/judgment-handoff.md','목적·조건 후보 필드만 존재. 목적별 설계 대안 생성/평가/선택 없음.'),
'I2':(DOC,'references/output-contract.md','내용 검수 상태와 한계 필드. 독립 시각 비평 실행기 없음.'),
'I3':(DOC,'references/judgment-handoff.md','목적·구현 제안 인계 형식. 모션 의도 명세와 결과 효과 대조 없음.'),
'I4':(CODE,'scripts/pattern_library.py','소스 파일 지문과 스냅샷 일부. 실제 생성 디자인/렌더별 비평 대상 고정은 미구현.'),
'I5':(CODE,'scripts/check_record.py','미실행 내용 검사와 형식 통과의 구분. 시각 무결점 검사는 없음.'),
'G1':(DOC,'references/judgment-handoff.md','조건·반례·구현 제안 칸만 있음. 설계 결함 진단→대안→재평가 과정 없음.'),
'G2':(DOC,'references/design-and-patterns.md','디자인 차원과 검수 상태만 일부. 실제 다차원 전문가 리뷰와 변경 판정 없음.'),
'A1':(CODE,'scripts/check_record.py','고유 주장과 검사기 오류 시험 일부. 기준 밖 의미 주장 전수 채점·독립 평가 없음.'),
'A2':(GAP,None,'null 보존은 결과 파일에 사용했으나 새 비교의 시간/토큰/품질 집계기는 구현하지 않음.'),
'M1':(DOC,'references/design-and-patterns.md','카테고리·ID·사용자 결정 기록. 공통 용어/별칭/개정 이력의 새 통합은 없음.'),
'E1':(CODE,'scripts/pattern_library.py','draft 등록 제한과 프로젝트 파일 축적만 구현. 실제 반복 사례에서 규칙 후보 자동 추출 없음.'),
'E2':(EXCLUDE,None,'점수·프로젝트 수만으로 회사 규칙을 자동 승인/전역 승격하는 경로는 의도적으로 제외.'),
'V1':(DOC,'references/pattern-composition.md','조건·반례·변형 기록 형식. 조건 검색·반례 시험으로 채택하는 실행 흐름은 없음.'),
'V2':(EXCLUDE,None,'원본 검사 조건의 한계 참고. 원본 검증기를 그대로 가져오지 않음.')}
assert set(details)=={r['id'] for r in audit['records']}
records=[]
for row in audit['records']:
    assert sha256(Path(row['local_path']).read_bytes()).hexdigest()==row['sha256']
    status,relative,gap=details[row['id']]
    item={**{k:row[k] for k in ('id','repository','commit','path','url','finding')},'implementation_status':status,'current_evidence':None,'remaining_or_exclusion':gap,'behavioral_effect_proven':False}
    if relative:
        path=candidate/relative;assert path.is_file();item['current_evidence']={'path':str(path),'sha256':sha256(path.read_bytes()).hexdigest()}
    records.append(item)
oldrepos={r['repository'] for r in prior['repositories']};newrepos={r['repository'] for r in records}
result={'utc':datetime.now(timezone.utc).isoformat(),'scope':'draft.5의 2026-10-19 조사 반영 감사. 과거 Phase 00 자산의 전체 완료 판정은 재평가하지 않음. 저장소 수·조사 파일 수는 스킬 구현 수가 아님.','survey_history':{'prior_repository_count':len(oldrepos),'new_repository_count':len(newrepos),'overlapping_repositories':sorted(oldrepos&newrepos),'unique_repository_count':len(oldrepos|newrepos),'prior_selected_files':sum(len(r['files']) for r in prior['repositories']),'new_source_review_records':len(records),'prior_consulted_local_skill_names':['shot-composition','design-tokens','animation-principles','motion-design','motion-art-direction','skill-creator','anthropic-skill-creator']},'status_counts':dict(Counter(r['implementation_status'] for r in records)),'fully_adopted_upstream_skill_count':0,'whole_pipeline_implemented':False,'default_installed':False,'note':'상태는 조사 포인트별 증거 분류이며 서로 크기가 다른 기능을 합산한 완성률이 아니다. 코드 일부 반영도 원본 기능 전체나 영상 성능을 입증하지 않는다.','records':records,'prior_repository_scope':[{'repository':r['repository'],'reviewed_file_count':len(r['files']),'source_review_status':r['status'],'new_candidate_adoption_status':'이번 감사에서 기존 Phase 00 구현 상태를 재판정하지 않음; 기존 소스 검토의 채택/변형/보류와 분리해 후속 연결 필요'} for r in prior['repositories']]}
(HERE/'implementation-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 조사와 구현의 현재 차이','','조사한 스킬 전체를 반영한 상태가 아니다. 현재 draft.5는 분석 기록과 패턴 연결 일부를 수정한 개발 후보다. 전문가 판단·실제 역설계·새 영상 실증은 남아 있다.','','## 조사 이력','','이전 11개 저장소(선택 379파일)와 이번 10개 저장소(41개 소스 검토 기록)는 Anthropic/Vercel 2개 저장소가 겹쳐 총 19개 저장소의 조사 이력이다. 저장소 수는 스킬 수나 구현 완료 수가 아니다. 이미 설치돼 참고한 7개 로컬 스킬도 별도로 존재한다.','','## 이번 조사 포인트 41개의 실제 반영','','| 근거 ID | 조사한 구조 | 상태 | 남은 범위 또는 제외 이유 |','|---|---|---|---|']
for r in records:md.append(f'| {r["id"]} | {r["finding"]} | {r["implementation_status"]} | {r["remaining_or_exclusion"]} |')
md+=['','## 큰 작업 범주와 다음 결과물','','1. 분석 신뢰성·근거·기록: 실제 영상에서 원자 주장·속성·시간·범위가 성립하는지 확인하고 실패를 수정한다. 현재 일부 구현.','2. 사례 검색·패턴 재사용: 번호를 꺼내는 기능에서 조건 검색·현재 장면 비교·차이 검수로 확장한다. 현재 번호·스냅샷·조합까지만 구현.','3. 전문가 판단·기획: 목적·제약→대안→선택 근거→비평→수정·재평가를 실제 산출물로 수행한다. 현재 지침·인계 칸 수준.','4. 역설계·제작 검증: 관측 명세→편집 가능한 제작→렌더 대조→내용 변경 재사용 시험을 만든다. 현재 미구현.','','이전 사용자 선택인 “분석 정확도와 근거 기록 우선”을 유지한다. 모든 외부 훅·코드·취향을 통째로 도입하는 계획이 아니다. 전체 적용 완료·기본 승격으로 보고하지 않는다. 기본 적용은 이번 범위 재정리 시점에 보류했다.']
(HERE/'00_조사대비_구현현황.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'repositories':result['survey_history'],'statuses':result['status_counts'],'full_adoption':0},ensure_ascii=False))
