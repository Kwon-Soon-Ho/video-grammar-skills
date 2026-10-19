from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from pypdf import PdfReader
O=Path(__file__).resolve().parent;R=O.parent
P=R/'output/pdf/20261019_value_creation_knowledge_and_design_pilot.pdf'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
pages=PdfReader(str(P)).pages
assert len(pages)==8
assert all(p.extract_text().strip() for p in pages)
write(O/'report-qa.json',{'utc':datetime.now(timezone.utc).isoformat(),'pdf_sha256':sha(P),'pages':8,'visual_review':{'reviewed_pages':[1,2,3,4,5,6,7,8],'corrected_and_rechecked':[5,6],'state':'passed','scope':'page layout and legibility; not independent design evaluation'},'proof_review':{'static_states':12,'mechanism':'two contact sheets plus selected individual full-resolution frames','actual_motion_rendered':False},'limitations':['PDF의 스토리보드는 축소 개괄. 원본 해상도 검토는 proofs/PNG 사용.','교차검증자·사용자 이해도 시험 미실시.']})
readme='''# 가치창출 영상 - 두 사례 기록과 새 화면 시범

사용자 지정 원본으로 교체했다. 우측 푸른 변경안은 적용하고 “변경없음”은 좌측 원문을 유지했다.

## 바로 볼 것
- 제출 PDF 3쪽: 계약의 새 16:9 화면 / 4쪽: 모션 흐름 제안
- 제출 PDF 5쪽: 지원의 새 9:16 두 상태 / 6쪽: 모션 흐름 제안
- proofs/A-state-5.png, B-state-2.png, B-state-5.png: 큰 화면 검토
- knowledge-cards.json: 원본 관측·전체 디자인 언어·기능 해석·보호/가변·후보 비교·반례
- numeric-baseline-ledger.json: 영상과 변경 시나리오의 차이
- research-application.json: 조사 소스에서 이번 시범에 가져온 판단 방식
- motion-proposals.json: 전체 흐름과 세부 동작 제안

## 현재 위치
두 사례의 개발 시범까지다. 실제 영상/오디오 싱크, 다른 주제로의 전이, 사용자 이해도는 미검증이다.
현재 스킬 draft.9, 기존 패턴 DB와 이전 실패·잠금 기준을 수정하지 않았다.
새 번호는 로컬 후보다. 원본 32:9 스타일의 모든 표현을 이번의 간결한 요약 디자인으로 대체한다는 결정이 아니다.

## 다음 큰 선택
1. 원본 기록과 새 화면을 함께 검토해 유지할 언어/변형 범위 결정(추천)
2. 한 장면의 실제 모션 시범
3. 다른 주제로 재사용 시험
4. 원본 디자인 자산과 조합 기록 보강

## 보관
publication-receipt.json이 존재하고 해시가 맞아야 D: 보관 완료다.
미실행/실패 시 publication-status.json을 확인한다. 기존 재기획 보고서도 미보관이면 함께 정상 보관을 요청한다.
'''
(O/'00_먼저읽기.md').write_text(readme,encoding='utf-8')
write(O/'publication-status.json',{'state':'prepared_for_normal_approval','previous_replanning_retry_this_turn':'failed before execution: automatic approval review model capacity','prior_report_attempts_known_before_final_retry':3,'pdf':str(P),'pdf_sha256':sha(P),'records_local':str(O),'no_bypass':True})
print('report QA and review guide written')
