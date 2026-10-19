"""Author a disclosed, previously exposed H02 development case; never blind accuracy evidence."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import sys,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OUT=HERE/'development/H02';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,PROPERTIES,digest
from render_observations import render
from pattern_library import add
old=load(WORK/'phase01a-a5b/trials/H02-r1-with_skill/outputs/observations.json')
catalog=load(WORK/'phase01a-a5b/trials/H02-r1-with_skill/support/evidence-catalog.json')
frames=[f for f in catalog['frames'] if '/cases/' in Path(f['path']).as_posix() and 12<=Fraction(str(f['actual_playback_seconds']))<=20]
frames=sorted({f['actual_playback_seconds']:f for f in frames}.values(),key=lambda f:Fraction(str(f['actual_playback_seconds'])))
evidence=[{'id':f'f{i:02d}','path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'context_after' if Fraction(str(f['actual_playback_seconds']))==20 else 'within'} for i,f in enumerate(frames)]
eids=[e['id'] for e in evidence];span=[12,20]
d={'schema_version':'video-observation-0.2','skill_version':'0.1.0-draft.4','case_id':'DEV-H02-20261019','source':old['source'],'window_seconds':span,'method':'已노출 H02의 기존 전체 개요 시트 2장과 native 12.0/14.4초, 기존 ROI c01/c03/c06 재열람; 기존 기준답안 D01/D08도 읽은 개발 사례. 새 독립 시험 아님.','document_mode':'none','audio_reviewed':False,'files_read':[str(WORK/'phase01a-a5b/reference/reference.json')],'evidence':evidence,'objects':[],'observation_rows':[],'claims':[],'unknowns':[],'discovery':{'forward_evidence_ids':eids,'reverse_evidence_ids':list(reversed(eids)),'unresolved_ids':[]},'layout':{},'motion_groups':[],'pattern_refs':[],'review':{},'handoff':None,'limitations':['이전 결과·기준답안이 알려진 개발 사례. AI 수동 재기록이며 독립 성능 개선 실험 아님.','선택 개요 표본은 연속 재생·전 프레임 판독이 아님. 정확한 onset/offset·AE 값·오디오는 미검수.','배경 정밀 움직임과 UI 내부의 모든 셀·버튼 문구, 서체·색의 정확한 값은 미검수.','전체 디자인을 정성 기록했으나 고유 주장 분모 전수 확정·전체 내용 검수 완료를 주장하지 않음.']}
groups={}
def target(oid,name,shape,extras):
    props=['identity',*extras]
    obj={'id':oid,'name':name,'parent':None,'shape_description':shape,'required_properties':props,'excluded_properties':{p:'이 대상의 해당 속성에 별도 변화/주장을 현재 개발 범위에서 요구하지 않음; 필요한 새 쟁점에는 다시 검토' for p in PROPERTIES-set(props)},'identity':{'status':'reviewed','label':name,'candidates':[],'claim_ids':[]}}
    d['objects'].append(obj);groups[oid]=[]
    cid=claim(oid,'identity','identity',name+' 형태/대상으로 식별한다.');obj['identity']['claim_ids']=[cid]
    return obj
def claim(oid,prop,facet,text,kind='observed',review='supported',easing=None):
    cid=f'c{len(d["claims"])+1:03d}'
    item={'id':cid,'object_id':oid,'property':prop,'facet':facet,'time_seconds':span,'statement':text,'basis_kind':kind,'evidence_ids':eids,'content_review':review}
    if easing is not None:item['easing']=easing
    d['claims'].append(item);groups[oid].append(cid);return cid
def unknown(oid,question):
    uid=f'u{len(d["unknowns"])+1:02d}'
    d['unknowns'].append({'id':uid,'object_id':oid,'question':question,'state':'open','reason':'현재 개발 재열람의 표본·해상도 또는 검수 범위로 확정하지 않음','required_basis_kind':'observed','next_probe':'해당 원본 ROI와 시간 경계의 기존 표본을 우선 보강·대조','resolution_claim_ids':[]});return uid
target('bg','열차 사진 배경','흰색·청색 열차와 역 플랫폼을 가로로 채운 사진; 화면 전반이 어둡게 조정됨',['color'])
claim('bg','color','value','배경은 청회색·검정의 어두운 톤으로 전경 문구·UI와 구분된다.')
target('glyph','대형 영문 A','화면 왼쪽과 중앙 아래에 이어진 큰 대각 획·가로획·하부 벌어진 획; 숫자 4로 단정하지 않는다',['position'])
claim('glyph','position','value','대형 A가 왼쪽 화면 대부분에 걸치고 UI와 선 뒤의 배경층에 남는다.')
target('english','Public Transport 영문','오른쪽 위 두 줄의 큰 반투명 산세리프 영문',['text'])
claim('english','text','value','Public / Transport 두 줄이 큰 한글 제목 뒤에 겹쳐 있다.')
target('headline','대중교통 분석 제목','오른쪽 중앙의 굵은 흰색 한글',['text'])
claim('headline','text','value','주제 제목은 대중교통 분석이며 선택한 구간의 뒤쪽까지 유지된다.')
target('topic-body','주제 설명 두 줄','대중교통 분석 제목 바로 아래 작은 흰 문구; 일부 구절 굵기 강조',['text'])
claim('topic-body','text','value','현실적으로 이용가능한 모든 대중교통 경로를 탐색하여, / 대중교통 분석 결과의 현실적 설명력을 향상시킵니다.가 제목 아래에 배치된다.')
target('orbit','가는 궤적 선과 노드','흰 곡선/타원 궤적과 검정·노랑 원형 노드',['position'])
claim('orbit','position','direction','개요 표본에서 선을 따라 원형 노드 위치가 달라진다. 세부 경로 속도는 확정하지 않는다.')
target('main-ui','지도·표 UI 예시','검은 외곽의 지도 UI; 회색 바탕에 다색 노선과 표 창',['position','size','internal_state','visibility'])
move=claim('main-ui','position','direction','12초대 좌상단의 지도창이 오른쪽·아래쪽으로 이동해 왼쪽 중앙에 정착한다.')
grow=claim('main-ui','size','direction','12.4~13.6초 표본에서 같은 지도 UI의 가로·세로 외곽이 커진다.')
motion_basis=[e['id'] for e in evidence if Fraction(str(e['actual_seconds'])) in (Fraction('12.4'),Fraction('12.8'),Fraction('13.2'),Fraction('13.6'))]
ease=claim('main-ui','size','easing','진행 중 확대 증가량이 후반에 줄어드는 감속 성격이다. 위치 감속과 별도로 크기에서 본 정성 판단이다.',easing={'classification':'decelerate','basis_evidence_ids':motion_basis,'method':'12.4/12.8/13.2/13.6초의 같은 외곽 증가를 개요 시트와 기존 ROI로 비교; 정밀 좌표 측정 안 함','limitation':'기존 기준답안 노출; 정확한 함수·AE 곡선·측정 오차 미상'})
claim('main-ui','internal_state','value','진입 중 노선 지도 위 왼쪽에 표 형식 설정 창이 드러나며 정착 표본에는 노선 지도와 요금 표 창이 함께 보인다.')
exit_c=claim('main-ui','visibility','direction','17.6초 이후 UI가 오른쪽·아래쪽으로 가며 축소되고 18.8초 표본에는 주요 예시창이 보이지 않는다. 정확한 소실 시점은 미확정.')
target('previous-ui','기존 노란 테두리 UI와 작은 예시들','초반 중앙의 노란 테두리 창과 우하단의 작은 예시 창들',['position','size'])
claim('previous-ui','position','direction','초반 큰 노란 예시창이 우하단으로 이동한다. 겹치는 작은 예시들의 개별 교체·가림 경계는 미확정이다.')
claim('previous-ui','size','direction','초반 큰 노란 예시창은 우하단으로 가면서 작아진다.')
target('yellow-outline','지도 UI의 노란 강조 테두리','지도 UI 바깥을 둘러싼 밝은 노란 선',['shape','visibility'])
border=claim('yellow-outline','shape','order','지도 UI가 정착할 무렵 왼쪽·상단부터 노란 강조 테두리가 추가되어 둘레를 이룬다. 기존 ROI와 개요 표본을 대조한 범위다.')
claim('yellow-outline','visibility','presence','정착한 지도 UI의 노란 둘레 강조는 유지 후 예시창 축소·소실과 함께 화면에서 사라진다.')
target('feature-title','대중교통 요금 설정기능 표제','지도 UI 아래 노란 직사각형 바탕의 굵은 검정 글씨',['text','visibility'])
title=claim('feature-title','text','value','표제는 대중교통 요금 설정기능이다.')
claim('feature-title','visibility','order','지도 UI 아래에 표제가 나타나고 17초대에 본문보다 먼저 줄어들며 보이지 않게 된다. 정확한 리빌 방식은 미확정이다.')
target('feature-body','요금 설정 설명 세 줄','노란 표제 아래의 작은 흰색 세 줄 문구',['text','visibility'])
body=claim('feature-body','text','value','대중교통 수단&노선에 따라 / 기본 요금, 거리, 추가거리 및 요금, / 통합환승요금제를 쉽게 적용하도록 설계가 보인다.')
claim('feature-body','visibility','order','표제 뒤에 세 줄 설명이 나타나고 예시창 퇴장 무렵 사라진다. 정확한 줄별 시작과 소실 경계는 추가 검수 대상이다.')
u1=unknown('main-ui','정확한 확대율·속도 곡선·진입/퇴장 경계는 무엇인가?')
u2=unknown('previous-ui','겹친 우하단 작은 예시 창 각각의 정체와 가림/교체는 어떻게 다른가?')
u3=unknown('orbit','노드·궤적의 세부 이동과 배경 자체의 시간 변화는 무엇인가?')
u4=unknown('feature-body','문구별 등장·퇴장 경계와 실제 원본 글꼴·색 값은 무엇인가?')
for obj in d['objects']:
    for prop in obj['required_properties']:
        cids=[c['id'] for c in d['claims'] if c['object_id']==obj['id'] and c['property']==prop]
        d['observation_rows'].append({'id':obj['id']+'-'+prop,'object_id':obj['id'],'property':prop,'time_seconds':span,'review_state':'reviewed','change':'changed' if prop!='identity' and obj['id'] in ('main-ui','previous-ui','yellow-outline','feature-title','feature-body','orbit') else 'unchanged','evidence_ids':eids,'claim_ids':cids,'unknown_ids':[],'reason':''})
all_ids=[c['id'] for c in d['claims']]
spec={
'hierarchy':'열차 배경·큰 A·연한 영문 위에 흰 주제 제목을 두고, 왼쪽 전경 UI와 노란 기능 표제로 예시를 강조한다.',
'alignment':'주제 제목과 설명은 오른쪽에서 왼쪽 정렬, 기능 표제·본문은 왼쪽 지도 UI의 왼쪽 변에 맞춘다.',
'spacing':'화면을 좌측 UI와 우측 설명 두 덩어리로 나누고 UI 바로 아래 표제·세 줄 설명을 붙인다. 정확한 간격은 미측정.',
'typography':'굵은 흰 한글 주제 제목, 더 큰 연한 영문 두 줄, 작은 흰 설명, 노란 바탕의 굵은 검정 기능 표제. 정확한 서체·pt는 미상.',
'color':'청회색·검정의 어두운 배경, 흰 주요 문구와 가는 궤적, 노란 표제·테두리·노드, 지도 내부의 다색 노선.',
'background':'열차 사진이 화면을 채우고 대형 A와 영문이 겹친다. 정확한 레이어 불투명도·합성 방식은 미상.',
'shapes':'지도/표 직사각형 UI, 검정과 노란 외곽, 노란 직사각형 표제, 흰 곡선/타원과 원형 노드가 함께 보인다.'}
d['layout']={'canvas':{'aspect_ratio':'16:9','coordinate_system':'3840x2160 native raster; 여기서는 정성 관계만 기록'},'states':[{'id':'layout-settled','time_seconds':span,'evidence_ids':eids,'composition':'12~20초 변화가 있는 구간의 전체 디자인 목록. 14.4초 native를 정착 대표로 삼고 전후 차이는 대상 주장·모션에 연결한다.','element_object_ids':[o['id'] for o in d['objects']],'claim_ids':all_ids,'design_spec':{k:{'description':v,'basis_kind':'observed','precision':'qualitative','claim_ids':all_ids} for k,v in spec.items()},'unresolved_ids':[u2,u3,u4]}],'unresolved_ids':[u1,u2,u3,u4]}
d['motion_groups']=[{'id':'flow','level':'flow','name':'기존 예시 축소 → 새 지도창 이동·확대 → 테두리/표제/설명 → 유지 → 축소 퇴장','time_seconds':span,'object_ids':[o['id'] for o in d['objects']],'claim_ids':[move,grow,border,title,body,exit_c],'pattern_occurrence_ids':[]},{'id':'detail','level':'detail','name':'크기 감속·노란 선 전개·내부 표·문구와 노드의 세부 변화','time_seconds':span,'object_ids':['main-ui','yellow-outline','feature-title','feature-body','orbit'],'claim_ids':[ease,border,*groups['orbit'],*groups['feature-title'],*groups['feature-body']],'pattern_occurrence_ids':[]}]
d['review']={'content_reviewed_claim_ids':all_ids,'claim_denominator_complete':False,'remaining_scope':['선택한 주장은 기존 원본·표본에 수동 재대조. 디자인 서술 전체의 원자화와 개별 작은 예시 식별은 미완료.','독립 새 자료 성능·반복 일치·전체 누락률·공수 절감 미검증.']}
d['handoff']={'purpose':{'text':'대중교통 분석이라는 주제 아래 요금 설정 UI를 기능 예시로 연결한다는 화면 해석','basis_kind':'inferred','claim_ids':[title,body]},'information_relation':{'text':'오른쪽은 상위 주제, 왼쪽 UI·노란 표제·작은 본문은 구체 기능 예시라는 해석','basis_kind':'inferred','claim_ids':[title,body]},'observed_claim_ids':[move,grow,ease,border,title,body,exit_c],'preserve_claim_ids':[border,title,body],'open_unknown_ids':[u1,u2,u3,u4],'condition_candidates':[{'condition':'상위 주제를 유지하며 작은 기능 UI와 설명을 함께 제시할 때의 후보','reason':'이 사례에서 주제 제목과 UI/기능 표제가 함께 보임','claim_ids':[title,body],'counterexample':None,'validation_state':'untested'}],'implementation_options':[{'proposal':'UI 프리컴프의 위치·크기를 따로 조절하고 테두리 리빌·문구를 별도 제어하는 방식의 새 구현 후보','basis_kind':'inferred','claim_ids':[move,grow,border],'verification_needed':'실제 편집·렌더 대조, 다른 문구 길이와 화면비에서 가독성·순서 검증'}]}
errors=check(d,catalog);assert not errors,errors
source=OUT/'observations.json';source.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'observations.md').write_text(render(d),encoding='utf-8')
pattern={'category':'CARD','name':'이동·확대 UI 기능 예시와 노란 강조','source':{'case_id':d['case_id'],'source_sha256':d['source']['sha256'],'observation_path':str(source),'observation_sha256':digest(source),'claim_ids':[move,grow,ease,border,title,body,exit_c]},'design_spec':{'layout':spec['hierarchy']+' '+spec['alignment'],'typography':spec['typography'],'color':spec['color'],'information_relation':'오른쪽 상위 주제와 왼쪽 구체 기능 예시; 목적은 추론'},'motion_spec':{'flow':d['motion_groups'][0]['name'],'detail':d['motion_groups'][1]['name'],'timing':'원본 12~20초의 선택 표본; 진입 12.4~13.6초, 정착·설명 뒤 17.6~18.8초 퇴장 관측; 정확 경계 미검수','properties':'위치와 크기를 따로 기록. 크기 감속은 정성 판단. 테두리와 문구는 별도 변화.','unknowns':[u1,u2,u3,u4]},'applicability':'정보 전달형 UI 기능 예시의 후보. 문구 길이·요소 수·화면비·읽기 시간은 새 장면에서 재검증. 실제 원제작 의도·회사 공통 규칙으로 사용 금지.','counterexamples':['새 내용 적용·다른 화면비는 미시험'],'status':'draft','supersedes':None}
pattern_input=OUT/'pattern-input.json';pattern_input.write_text(json.dumps(pattern,ensure_ascii=False,indent=2),encoding='utf-8')
receipt=add(HERE/'knowledge/pattern-library.json',pattern_input)
(OUT/'pattern-registration.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps({'structure_passed':True,'catalog_provenance_checked':True,'ai_manual_reinspection':True,'claim_denominator_complete':False,'blind':False,'new_holdout':False,'accuracy_effect_proven':False,'objects':len(d['objects']),'claims':len(d['claims']),'open_unknowns':len(d['unknowns']),'pattern':receipt},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'objects':len(d['objects']),'claims':len(d['claims']),'unknowns':len(d['unknowns']),'first_pattern':receipt['pattern_id'],'independent_accuracy_test':False},ensure_ascii=False))
