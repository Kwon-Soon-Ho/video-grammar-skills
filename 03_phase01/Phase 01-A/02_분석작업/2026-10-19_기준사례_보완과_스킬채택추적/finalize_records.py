from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,digest,check
from source_coverage import summarize
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
coverage=load(WORK/'internal-video-audit-20261019/source-coverage.json')
for r in coverage['records']:
 p=HERE/'records'/r['source_id']/'observations-linked.json';r.update(path=str(p),sha256=digest(p))
write(HERE/'source-coverage.json',coverage);result=summarize(coverage,load(HERE/'evidence-catalog.json'));write(HERE/'coverage-result.json',result)
issues=[]
for iid,code,uid,state,cids,note in [
 ('N-background','NEW-N','u01','addressed_with_limits',['c035'],'세 배경 ROI의 위치 유사·밝아짐 이후 유지 확인. 모든 픽셀/원본 레이어 독립성 판정 아님.'),
 ('N-arcs-and-sway','NEW-N','u02','partial',['c037','c038','c039','c051'],'한 차례 화살표 강조와 구조물의 왕복 기울임을 분리. 화면 투영 경사 가감속은 확인했지만 화살표 정확 강도 곡선·원본 동기화 설정은 남음.'),
 ('N-label-completion','NEW-N','u03','addressed_with_limits',['c040','c041'],'완성 문구와 외곽 폭 정착의 시각 차이를 확인. 원본 폰트명·실제 마스크 설정은 미확정.'),
 ('P-connector','NEW-P','u02','addressed_with_limits',['c048','c050','c058'],'생성 중 유색 영역의 위쪽 성장, 정착 뒤 무늬 유지, 이후 묶음 이동을 구분. 최종 퇴장은 관측 창 밖.'),
 ('P-row-emphasis','NEW-P','u03','addressed_with_limits',['c045'],'기존 노란 행과 새 분홍 행의 한 차례 강조를 대조. 반복 주기/동기화 전제를 채택하지 않음.')]:
 before=WORK/'internal-video-audit-20261019/records'/code/'observations.json';after=HERE/'records'/code/'observations-linked.json'
 issues.append({'id':iid,'source_case':code,'before':{'path':str(before),'sha256':digest(before),'unknown_id':uid},'after':{'path':str(after),'sha256':digest(after),'unknown_id':uid},'state':state,'answer_claim_ids':cids,'answer':note,'scope_note':'새 관측 창은 이전보다 넓다. 같은 창의 review_ledger 규칙을 우회하지 않고 확장 사례의 별도 보완 장부로 연결.','quality_acceptance':False})
ledger={'schema_version':'expanded-case-review-0.1','reviewer':'same_agent_context','issues':issues,'counts':{'addressed_with_limits':4,'partial':1},'discovery_completeness':False,'original_intent_confirmed':False,'new_discoveries':[{'case':'NEW-N','finding':'화면 표기 켄틸레버를 캔틸레버로 읽은 과거 c028을 기각하고 c040으로 정정','claims':['c028','c040']},{'case':'NEW-N','finding':'176초 이후 형상 밀착 강조·마감 판을 별도 대상으로 추가','claims':['c045','c046','c048','c049']},{'case':'NEW-P','finding':'지도는 유지되고 기관 묶음만 오른쪽으로 이동하는 후속 배치','claims':['c044','c050','c051','c053']}]}
write(HERE/'expanded-review-ledger.json',ledger)
registration=load(HERE/'knowledge/registration-result.json')
lines=['# 두 기준 사례의 검토안과 현재 위치','', '사용자 선택 ①에 따라 기존 두 장면의 미해결과 전후 문맥을 보완했다. 현재 스킬은 여전히 draft.8 개발 작업본이다. 이번 묶음은 실제 사례·패턴 정의·조사 반영 추적을 추가했으며 스킬 전체 생성 완료가 아니다.','', '## 관측 범위','', '- 노듈러: 166~181초, 15초. 앞뒤 문맥 164/165초와181초 이후는 별도 근거 역할로 구분한다.','- PG: 40~53초, 13초. 38/39초·53초 이후와79~82초는 문맥 표본이며 중간 전체를 분석한 것이 아니다.','- 두 원본 전체 약630.272초 중 상세 기록 창 합계28초. 기록 창 밖602.272초. 두 창도 전수 native 프레임 검수·독립 정답·회사 승인 완료는 아님.','', '## 기존 미해결 5개','']
for x in issues:lines.append('- '+x['id']+' / '+x['state']+': '+x['answer'])
lines+=['','## 이번에 바로잡은 기록','', '- 노듈러 완성 설명의 영상 표기는 “켄틸레버 바닥판 시공시 동바리 역할 수행”. 하단 자막은 “켄틸레버 바닥판 시공 시 동바리 역할도 수행하는 다목적 부재입니다.”로 구분한다. 통상 용어로 자동 교정하지 않는다.','- 왼쪽 설명은174초 문구 전체가 읽히지만 외곽선 간격은174.8초 무렵까지 정착 중이다.','- 화살표의 등장·유지·소실, 구조물의 왕복 기울임, 176초 이후 외곽 강조, 마감 판의 가림을 별도 사건으로 남겼다.','- PG 생성 중의 선 노출 경계 성장과 정착 뒤 무늬의 위치, 후속 기관 묶음 이동을 나눴다. 기존 노란 행을 새 분홍 행의 반복 점멸과 묶지 않는다.','', '## 번호 연결','', '기존6개 정의를 보존하고 새12개를 초안으로 등록했다. 총18개 중 이번 새 정의는 다음과 같다. 새 문구·화면비 재제작 성공을 확인한 라이브러리는 아니다.','']
lib=load(HERE/'knowledge/pattern-library.json')
for p in lib['patterns'][6:]:lines.append('- '+p['id']+': '+p['name'])
lines+=['', '- 노듈러 왼쪽/오른쪽 설명은 같은 PAT-TEXT-0002를 인용하되 오른쪽의 가감속을 왼쪽 측정에서 복사하지 않았다.','- PG 두 정책 행은 같은 PAT-TEXT-0003에 서로 다른 등장·강조 시각을 연결했다.','- 전체 배치/전체 흐름/독립 세부를 조합한 사례 연결14개 모두 candidate다. 승인·재사용 성공·검증된 정답으로 승격하지 않았다.','', '## 외부 스킬 조사와 실제 반영','', '기존41개 조사 포인트를 draft.8 파일 지문과 연결해 갱신했다. 원본 정적 검토 범위는 full17/selected24 항목이며 전체 저장소 감사·원본 테스트 실행이 아니다. 현재 지침·형식10/코드 일부21/미구현4/직접 이식 제외·평가 참고6이며 서로 다른 크기의 항목을 합친 완료율이 아니다. 전문가 대안/비평·상충 판정 관리·편집 가능한 재제작/렌더 비교가 남는다.','', '## 다음 사용자 판단','', '이 사례의 기록 밀도·분류가 충분한지 검토하거나, 다른 장면에서 같은 방식이 통하는지 확인하거나, 한 원본 전체로 확장하거나, 남은 정밀 수치의 필요 범위를 정할 수 있다. 다음 묶음은 사용자 선택 후 시작한다.']
(HERE/'00_기준사례_검토안과_현재위치.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'coverage':result,'tracked_issues':ledger['counts'],'new_definitions':registration['new_definitions'],'global_skill_version_unchanged':'draft.8'},ensure_ascii=False))
