from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import sys,json,shutil
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'skill-revision-20261019'
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,digest
from pattern_library import add,select
from render_observations import render
OUT=HERE/'development/H02';OUT.mkdir(parents=True,exist_ok=True)
LIB=HERE/'knowledge/pattern-library.json';LIB.parent.mkdir(exist_ok=True)
assert not LIB.exists(),'Existing library must not be rebuilt'
shutil.copy2(OLD/'knowledge/pattern-library.json',LIB)
original=load(OLD/'development/H02/observations.json');d=deepcopy(original)
d.update(schema_version='video-observation-0.3',skill_version='0.1.0-draft.5',case_id='DEV-H02-PARTS-20261019',reuse_map=None)
d['method']='기존 H02 개발 관측을 레이아웃·전체 흐름·독립 세부로 재구성. 새 영상 분석·독립 내용 검수는 수행하지 않음. 근거 목록을 각 주장과 관련된 시점으로 좁힘.'
d['limitations'].append('이번 수정은 패턴 분리·연결 검증이다. 과거 AI supported를 새 사람 확인으로 승격하지 않음.')
# Keep claim facts unchanged; narrow the over-broad evidence references in the new record.
by_time={Fraction(str(e['actual_seconds'])):e['id'] for e in d['evidence']}
def at(*times):return [by_time[Fraction(str(t))] for t in times]
static=at(12,14.4);mapping={c['id']:static for c in d['claims']}
mapping.update({'c008':at(12,14.4,19.6),'c012':at(12,14.4,19.6),'c014':at(12,12.4,12.8,13.2,13.6),'c015':at(12.4,12.8,13.2,13.6),'c016':at(12.4,12.8,13.2,13.6),'c017':at(12.8,13.2,13.6,14.4),'c018':at(17.6,18,18.4,18.8),'c020':at(12,12.4,12.8),'c021':at(12,12.4,12.8),'c023':at(13,13.4,13.8,14.4),'c024':at(13.6,14.4,17.6,18.8),'c025':at(14.4),'c026':at(14.4),'c027':at(13.2,13.6,14.4,17.2,17.6),'c028':at(14.4),'c029':at(14.4),'c030':at(13.6,14,14.4,17.2,17.6,18)})
for c in d['claims']:
    c['evidence_ids']=mapping[c['id']]
    if 'easing' in c:c['easing']['basis_evidence_ids']=mapping[c['id']]
claims={c['id']:c for c in d['claims']}
for row in d['observation_rows']:row['evidence_ids']=sorted({e for cid in row['claim_ids'] for e in claims[cid]['evidence_ids']})
used={e for c in d['claims'] for e in c['evidence_ids']};d['evidence']=[e for e in d['evidence'] if e['id'] in used]
d['discovery']['forward_evidence_ids']=[e['id'] for e in d['evidence']];d['discovery']['reverse_evidence_ids']=list(reversed(d['discovery']['forward_evidence_ids']))
state=d['layout']['states'][0];state['evidence_ids']=at(12,14.4,19.6)
design_claims={'hierarchy':['c004','c006','c008','c010','c026','c029'],'alignment':['c004','c008','c026','c029'],'spacing':['c014','c026','c029'],'typography':['c006','c008','c010','c026','c029'],'color':['c002','c023','c026'],'background':['c001','c003','c005'],'shapes':['c003','c011','c013','c019','c022','c025']}
for key,spec in state['design_spec'].items():spec['claim_ids']=design_claims[key]
state['claim_ids']=sorted({x for values in design_claims.values() for x in values})

catalog=load(OLD.parent/'phase01a-a5b/trials/H02-r1-with_skill/support/evidence-catalog.json')
assert not check(d,catalog),check(d,catalog)
source=OUT/'observations-first-detail.json';source.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

def register(category,name,cids,uids,definition):
    p={'definition_version':'video-pattern-definition-0.2','category':category,'name':name,'source':{'case_id':d['case_id'],'source_sha256':d['source']['sha256'],'observation_path':str(source),'observation_sha256':digest(source),'claim_ids':cids,'unknown_ids':uids},'definition':definition,'applicability':'원본 한 사례에서 정리한 재사용 후보. 새 문구·화면비·정보 관계·시간 조건에서 재검증한다.','counterexamples':['다른 장면의 실제 적용·가독성·제작 결과는 미시험'],'status':'draft','supersedes':None,'derived_from':['PAT-CARD-0001']}
    path=OUT/f'input-{category.lower()}.json';path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
    return add(LIB,path)

layout_claims=state['claim_ids']
entries=[]
entries.append(register('LAYOUT','상위 주제와 기능 UI를 나누는 전체 배치',layout_claims,['u02','u04'],{'summary':'전체 디자인과 정보 덩어리의 관계. 개별 등장 동작은 포함하지 않는다.','canvas':'16:9; 정성 관계 중심, 정확 좌표·비율 미측정','groups':[{'name':'배경·상징·영문','claim_ids':['c001','c003','c005']},{'name':'상위 주제와 설명','claim_ids':['c008','c010']},{'name':'기능 UI와 표제·본문','claim_ids':['c013','c026','c029']}],'design_dimensions':deepcopy(state['design_spec'])}))
entries.append(register('FLOW','주제 유지와 기능 예시 교체 흐름',['c008','c014','c015','c018','c020','c021','c023','c026','c027','c029','c030'],['u01','u02','u04'],{'summary':'기존 예시를 줄이고 새 기능 예시를 제시한 뒤 회수하는 전체 시간 구조','stages':[{'name':'기존 예시 이동·축소','timing':'12초대 선택 표본','claim_ids':['c020','c021']},{'name':'새 UI 이동·확대','timing':'12.4~13.6초 표본','claim_ids':['c014','c015']},{'name':'테두리·표제·본문 전개','timing':'13초대 이후; 정확 경계 미확정','claim_ids':['c023','c026','c029']},{'name':'유지 뒤 문구·UI 회수','timing':'17초대~18.8초 표본','claim_ids':['c018','c027','c030']}],'overlap_notes':['UI 정착과 테두리·표제 출현은 일부 겹침. 화살표는 완전 직렬 시간표가 아님.'],'stable_context':'대중교통 분석 상위 주제와 배경은 예시 교체 중에도 유지 관측'}))
entries.append(register('CARD','UI 이동·확대·정착과 축소 회수',['c014','c015','c016','c018'],['u01'],{'summary':'직사각형 UI의 위치·크기 동작. 열차·노란 테두리·기능 문구는 필수 구성 아님.','target_role':'주요 직사각형 기능 UI','phases':[{'name':'진입','property':'position','observed_change':'좌상단 쪽에서 오른쪽·아래로 이동해 왼 중앙 정착','claim_ids':['c014']},{'name':'크기 변화','property':'size','observed_change':'확대 후 증가량 감소를 보이며 정착하는 감속 성격','claim_ids':['c015','c016']},{'name':'회수','property':'visibility','observed_change':'오른쪽·아래로 가며 축소 후 소실 표본','claim_ids':['c018']}],'parameters':[{'name':'크기 곡선','status':'observed','value':'정성 감속','unit_or_type':'관측 분류; AE 함수 아님'},{'name':'정확 확대율·시간 경계','status':'unknown','value':None,'unit_or_type':'ratio / seconds'}],'preserve_constraints':['위치·크기 곡선을 별도로 검토','새 UI의 가독성과 읽기 시간을 재검증']}))
entries.append(register('DETAIL','대상 외곽의 노란 테두리 전개',['c022','c023','c024'],['u01'],{'summary':'대상 둘레에 강조 선을 전개하는 세부 동작. 원본의 전체 배치를 함께 적용하지 않는다.','target_role':'강조할 대상의 외곽선','phases':[{'name':'전개','property':'shape','observed_change':'왼쪽·상단부터 강조선이 추가되어 전체 둘레 형성','claim_ids':['c023']},{'name':'유지와 회수','property':'visibility','observed_change':'UI 강조를 유지하다 대상 축소·소실과 함께 보이지 않게 됨','claim_ids':['c024']}],'parameters':[{'name':'원본 강조색','status':'observed','value':'노랑','unit_or_type':'정성 색 분류; 공식 CI값 아님'},{'name':'정확 선폭·리빌 시간','status':'unknown','value':None,'unit_or_type':'pixels / seconds'}],'preserve_constraints':['대상 외곽과의 연결 유지','색과 선폭은 새 배경 대비에 맞춰 재검토']}))
entries.append(register('TEXT','기능 표제와 본문을 순서대로 제시',['c025','c026','c027','c028','c029','c030'],['u04'],{'summary':'기능 표제와 뒤따르는 작은 본문을 나눠 제시·회수하는 텍스트 동작 후보. 정확 리빌 방식은 미확정.','target_role':'기능 표제와 그 아래 본문','phases':[{'name':'표제 제시','property':'visibility','observed_change':'노란 바탕 기능 표제가 먼저 나타남','claim_ids':['c026','c027']},{'name':'본문 제시','property':'visibility','observed_change':'표제 뒤에 세 줄 설명 출현','claim_ids':['c029','c030']},{'name':'회수','property':'visibility','observed_change':'표제가 본문보다 먼저 줄어들어 안 보이는 표본 관측','claim_ids':['c027','c030']}],'parameters':[{'name':'본문 줄 수','status':'observed','value':3,'unit_or_type':'lines in source case; 다른 문구에서 고정 금지'},{'name':'정확 리빌 방식·줄별 시간','status':'unknown','value':None,'unit_or_type':'effect / seconds'}],'preserve_constraints':['표제·본문의 정보 관계와 가독성 유지','정확 리빌을 모르는 상태를 페이드로 확정하지 않음']}))
final_snapshot=entries[-1]['library_snapshot_path'];final_hash=digest(final_snapshot)
occurrence_ids=['layout-main','flow-main','ui-motion','outline-motion','feature-text']
for oid,entry in zip(occurrence_ids,entries):
    payload=next(p for p in load(LIB)['patterns'] if p['id']==entry['pattern_id']);cids=payload['source']['claim_ids']
    object_ids=sorted({claims[c]['object_id'] for c in cids})
    d['pattern_refs'].append({'id':oid,'pattern_id':entry['pattern_id'],'pattern_sha256':entry['pattern_sha256'],'library_path':final_snapshot,'library_sha256':final_hash,'object_ids':object_ids,'current_claim_ids':cids,'match_status':'candidate','differences':['동일 출처의 개발 기록에서 분리한 정의. 새 장면 매칭 시험은 아님.'],'unverified_dimensions':[u for u in payload['source']['unknown_ids']]+['다른 장면 적용 미검증']})
d['reuse_map']={'case_id':d['case_id'],'layout_occurrence_ids':['layout-main'],'flow_occurrence_ids':['flow-main'],'detail_occurrence_ids':['ui-motion','outline-motion','feature-text'],'links':[{'from_id':'flow-main','to_id':x,'relation':'contains','basis_kind':'inferred','claim_ids':d['pattern_refs'][index]['current_claim_ids']} for index,x in [(2,'ui-motion'),(3,'outline-motion'),(4,'feature-text')]]+[{'from_id':'layout-main','to_id':'ui-motion','relation':'anchors_to','basis_kind':'inferred','claim_ids':['c014']},{'from_id':'ui-motion','to_id':'outline-motion','relation':'overlaps','basis_kind':'inferred','claim_ids':['c014','c023']},{'from_id':'outline-motion','to_id':'feature-text','relation':'accompanies','basis_kind':'inferred','claim_ids':['c023','c027','c030']}],'unresolved_ids':['u01','u02','u03','u04']}
d['motion_groups'][0]['pattern_occurrence_ids']=['flow-main','ui-motion','outline-motion','feature-text']
d['motion_groups'][1]['pattern_occurrence_ids']=['ui-motion','outline-motion','feature-text']
assert not check(d,catalog),check(d,catalog)
linked=OUT/'observations-linked.json';linked.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'observations-linked.md').write_text(render(d),encoding='utf-8')
selection=select(final_snapshot,entries[3]['pattern_id'])
(OUT/'selected-outline-only.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'old_bundled_pattern_preserved':'PAT-CARD-0001','separated_patterns':entries,'source_observation':str(source),'linked_case':str(linked),'detail_selection':entries[3]['pattern_id'],'selected_claim_ids':[c['id'] for c in selection['source_claims']],'selected_definition_contains_layout':'design_dimensions' in selection['pattern']['definition'],'fresh_visual_analysis':False,'user_choice_is_not_content_approval':True}
(HERE/'case-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_patterns':[p['pattern_id'] for p in entries],'selected_outline_claims':summary['selected_claim_ids'],'selected_evidence_count':len(selection['source_evidence']),'whole_case_retained':True},ensure_ascii=False))

