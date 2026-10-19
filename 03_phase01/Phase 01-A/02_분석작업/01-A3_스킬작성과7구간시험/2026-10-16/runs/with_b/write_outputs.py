from pathlib import Path
from fractions import Fraction as F
import json,sys
R=Path.cwd();A=R/'phase01a-a3';P=A/'runs/with_b'; S=A/'company-video-grammar-analyzer'; packet=json.loads((A/'analysis_input/cases.json').read_text(encoding='utf-8'));cases={c['case_id']:c for c in packet['cases']}
common=[S/'SKILL.md',*[S/'references'/n for n in ['evidence-and-records.md','motion-review.md','output-contract.md']],S/'scripts/evidence_catalog.py',S/'scripts/check_observations.py',A/'analysis_input/cases.json',A/'analysis_input/inspect_more.py']
D={}
def init(cid,boards,crops,logs):
 c=cases[cid]; folder=Path(c['evidence_folder']); orig=folder/'실행기록.json'; ld=json.loads(orig.read_text(encoding='utf-8')); ev=[];read=[*common,orig,*[folder/b for b in boards]]
 # Every original T04-T06 frame is visible in the viewed sequential overview boards.
 selected=ld['frames'] if cid!='T07' else [f for f in ld['frames'] if float(F(f['actual_playback_seconds'])) in [8.2,8.5,8.8,9.1,9.4,9.7,10,10.3]]
 for f in selected:ev.append({'id':'f'+str(len(ev)+1),'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'requested_seconds':f['requested_playback_seconds'],'role':'context_after' if F(f['actual_playback_seconds'])>=F(str(c['allowed_window_seconds'][1])) else 'within','viewed_as':'temporal overview board','raster':f['raster'],'derived_size':f['derived_size'],'transforms':f['transforms']})
 for name in crops:
  meta=P/(name+'.json');read.extend([meta,P/(name+'.png')]); rows=json.loads(meta.read_text(encoding='utf-8'))
  for x in rows:
   # Only rows 0-13 were viewed directly; 14 shares a source with wholeui endpoint.
   if name=='T07_rows' and rows.index(x)==14:continue
   ev.append({'id':'f'+str(len(ev)+1),'path':x['path'],'actual_seconds':x['actual_seconds'],'role':'context_after' if F(x['actual_seconds'])>=F(str(c['allowed_window_seconds'][1])) else 'within','viewed_as':'native ROI individually or native ROI temporal panel','source_frame':x['source'],'crop_native_xyxy':x['crop_native'],'resize':None});read.extend([Path(x['path']),Path(x['source'])])
 read.extend(logs);D[cid]={'schema_version':'a3-observation-0.1','case_id':cid,'source':{'path':c['media_path'],'sha256':c['media_sha256']},'window_seconds':c['allowed_window_seconds'],'method':'時間順 overview → 정착 화면 역추적 → 원본 raster ROI 및 경계 선택 표본. 실제 시각은 검증된 추출 로그의 actual_playback_seconds 사용. 연속 재생/오디오 검수는 수행하지 않음.','document_mode':'none','audio_reviewed':False,'evidence':ev,'objects':[],'coverage':{'overview':'요청 구간의 제공 시간순 overview 확인','secondary_details':'각 대상 이벤트 참조','internal_content':'각 대상 이벤트 참조','unresolved':[]},'hypotheses':[],'limitations':['선택 표본 검사이며 모든 프레임 검사가 아님. 정확한 시작·종료는 표본 사이 범위로 해석.','원본 AE 속성·키프레임·보간 함수·제작 의도는 렌더에서 확정하지 않음.','RGB 변환의 색 범위 정확도 미검증. 압축 픽셀을 공식 CI 색으로 해석하지 않음.','오디오/원고 대응 미검수. Phase 00 정본 미제공으로 용어 ID 연결 없음.'],'files_read':list(dict.fromkeys(str(x.resolve()) for x in read))}
 return D[cid]
def obj(cid,oid,name,parent=None):D[cid]['objects'].append({'id':oid,'name':name,'parent':parent,'events':[]})
def event(cid,oid,desc,props,span,times,order,kind='unknown',basis='선택 표본에서 변화는 확인했으나 정확한 속도 곡선은 미확정.',limit=None):
 d=D[cid];refs=[]
 for t in times:
  e=min(reversed(d['evidence']),key=lambda e:abs(float(F(e['actual_seconds']))-t));refs.append(e['id'])
 next(x for x in d['objects'] if x['id']==oid)['events'].append({'description':desc,'properties':props,'time_seconds':span,'evidence_ids':list(dict.fromkeys(refs)),'direction_order':order,'easing':{'property':props[0],'classification':kind,'basis':basis},'status':'observed','limitations':limit or []})
init('T04',['board_1.jpg','board_2.jpg','board_3.jpg','board_4.jpg'],['T04_order','T04_sales','T04_profit'],[P/'cases/자료005/graphnative/실행기록.json'])
obj('T04','screen','표지에서 실적 화면으로 전환')
event('T04','screen','6.0초 교량/제조 부재/로고와 2026년 경영현황 보고 표지에서, 6.333초 실적 및 계획 화면이 우세해지고 6.667초 정착. 도시·강 배경과 3개 카드가 드러난다.',['visibility'],[6,6.667],[6,6.333,6.667],'표지 → 중첩 혼합 → 실적 화면','unknown','이 케이스의 overview 간격 1/3초는 짧은 혼합의 정확한 곡선 판정에 부족.')
obj('T04','layout','실적 화면 공통 텍스트·배경·카드')
event('T04','layout','좌측 장헌 로고, 01, 실적 및 계획, 2026년 1~8월 누적 실적. 오른쪽 수주·매출·영업이익 카드에 2026년 목표, 1~8월 실적, 달성률. 목표 60억/64억/7억의 회색 막대와 비어 있는 연한 원형 궤도가 먼저 있고, 파란 실적만 뒤에 순서대로 증가. 카드 제목·기준선·배경 외곽은 정착 후 같은 배치를 유지.',['position','internal_state'],[6.667,18],[6.667,8,13,15.333,17.667,18],'프레임/목표 선행 → 수주 → 긴 유지 → 매출 → 영업이익','not_applicable','공통 틀의 거시적 위치 유지 관찰. 내부 실적 모션은 아래 개별 속성으로 분리.')
for oid,name,span,ts,vals in [('order','수주',[8,9.667],[8,8.2,8.333,8.7,9,9.333,9.667],'8.0초 없음 → 8.2초 22억/37% → 8.333초 33억/56% → 8.7초 50억/84% → 9.0초 55억/91% → 9.333초 55억/92%'),('sales','매출',[15.333,16.7],[15.333,15.7,16,16.333,16.7],'15.333초 없음 → 15.7초 16억/25% → 16.0초 31억/48% → 16.333초 38억/59% → 16.7초 39억/61%'),('profit','영업이익',[16.7,18],[16.7,17,17.333,17.7,18],'16.7초 없음 → 17.0초 3억/41% → 17.333초 5억/66% → 17.7초 5억/71% (18.0초 경계 문맥도 동일)')]:
 obj('T04',oid,name+' 실적 그래프','layout')
 for prop,desc in [('size','파란 실적 막대가 하단 기준선에서 위로 자란다. 숫자 라벨도 막대 위를 따라 위로 이동한다.'),('internal_state','실적 수치와 달성률 숫자가 증가한다. '+vals+'.'),('reveal','파란 원호가 12시에서 시계방향으로 늘어나며 회색 궤도를 덮는다.')]:
  event('T04',oid,desc,[prop],span,ts,'수주 → 매출 → 영업이익; 각 카드의 막대·수치·원호는 함께 진행','decelerate','원본 ROI에서 초기 증가폭이 크고 후반 증가폭이 작아져 정착하는 ease-out 성격. 숫자 예: 매출 31→38→39, 원호 48→59→61. 막대 및 원호도 같은 후반 둔화를 육안 대조. 정밀 함수/픽셀 추적 오차는 미상.',['정수 표시 반올림 때문에 숫자가 먼저 같은 값이 될 수 있다. 18초는 context_after이며 전체 영상 최종값을 뜻하지 않는다.'])
D['T04']['coverage'].update(secondary_details='카드 테두리·제목 구분선·바닥 기준선·원형 회색 궤도 확인. 별도 강조광은 표본에서 확인되지 않음.',internal_content='세 카드 모두 원본 ROI로 막대·숫자·원호를 확인. 수주 55억/92%, 매출 39억/61%, 영업이익 5억/71%는 분석창 말미 값.',unresolved=['짧은 화면 혼합의 상세 속도는 T04 개요만으로 미확정.','각 그래프의 시작 프레임 및 정밀 easing 함수는 미확정.'])
init('T05',['board_1.jpg','board_2.jpg'],['T05_titles','T05_blend_roi'],[P/'cases/자료005/blendnative/실행기록.json',P/'T05_blend_measure.json',P/'measure.py'])
obj('T05','old','교량·부재 표지와 큰 로고/제목')
event('T05','old','5.9~6.0초 표지 유지. 이후 교량/전경 부재, 큰 장헌 로고, 2026년 경영현황 보고가 같은 자리에서 옅어져 사라진다. 6.1초에는 새 화면과 동시 노출, 6.3초에는 매우 약한 잔상이 남는다.',['visibility'],[5.9,6.4],[5.9,6,6.033,6.1,6.2,6.3,6.4],'기존 화면 감쇠와 새 화면 증가가 겹침','decelerate','혼합 진행률의 변화폭이 초기 크고 후반 작음. 끝점 RGB 혼합 적합치: 6.033=0.2007, 6.1=0.5243, 6.2=0.8248, 6.3=0.9587, 6.4=0.9936. 이는 원본 opacity가 아닌 영상의 혼합 진행 근사.')
obj('T05','new','실적 및 계획 화면·3개 카드')
event('T05','new','작은 좌상단 로고, 빨간 01, 실적 및 계획, 2026년 1~8월 누적 실적, 빨간 짧은 밑줄과 회색 보조문장, 3개 카드 및 도시/강 배경이 겹쳐 진해진다. 로고가 축소 이동하는 한 물체라기보다 서로 다른 크기/위치의 두 로고가 함께 보이는 화면 혼합이다.',['visibility'],[6,6.4],[6,6.033,6.1,6.2,6.3,6.4],'전체 새 화면이 함께 출현; 개별 카드 순차 등장으로 보이지 않음','decelerate','6.0~6.4초 ROI의 혼합 증가가 후반 둔화. 0.1초당 혼합 진행 증가 약 0.524→0.301→0.134→0.035로 감소. 감속/ease-out이며 위치 속도가 아님.')
event('T05','new','6.4~6.6초 새 화면 배치 유지. 수주/매출/영업이익 목표 60억/64억/7억과 회색 막대·빈 원형이 보이며 파란 실적값은 이 구간에 아직 없다.',['internal_state'],[6.4,6.6],[6.4,6.5,6.6],'전환 정착 후 빈 실적 상태 유지','not_applicable','정착 상태의 반복 표본 확인.')
D['T05']['measurements']=[json.loads((P/'T05_blend_measure.json').read_text(encoding='utf-8'))]
D['T05']['coverage'].update(secondary_details='새/구 로고, 짧은 선, 카드 테두리와 배경의 중첩을 확인.',internal_content='혼합 중 이미 목표 숫자·회색 막대·원형 궤도가 함께 나타남. 파란 실적 증가 미시작.',unresolved=['실제 opacity/키프레임 핸들은 불명.','색 공간·압축 및 화면 내부 변화가 RGB 혼합 적합치에 오차를 만들 수 있음.'])
init('T06',['board_1.jpg','board_2.jpg','board_3.jpg'],['T06_ui_transition','T06_model','T06_light','T06_copy'],[P/'cases/자료013/uinative/실행기록.json'])
obj('T06','bg','녹색 격자·큰 황갈색 E·우측 소개 문구')
event('T06','bg','큰 황갈색 E와 설계선 질감, 녹색 격자/띠/비네트, 흐린 배경 영문, 우측 EG-BIM 및 Engineering Graphicer for BIM, 한국어 소개문이 유지된다. 노란 E/G/BIM 강조가 있고 소개문은 설계도면 관리와 2D·3D 동시 Cross Check, 3D Viewer를 설명한다.',['position','internal_state'],[10.6,15.5],[10.6,12,13.9,15.5],'UI와 모델의 변화 동안 우측 문구/바탕은 같은 배치','not_applicable','시작·중간·끝 overview 및 12초 문구 ROI 확인.')
obj('T06','browser','노란 테두리 도면 목록 창')
event('T06','browser','10.6~10.75초 좌상단 큰 도면 목록 창이 있다. 이후 오른쪽 아래로 이동하면서 작아지고 약 11.6~12초 뒤쪽 창으로 남는다. 상단 목록의 4번째 행과 썸네일 첫줄 4번째 선택은 관찰 동안 유지된다.',['position','size'],[10.6,12],[10.6,10.75,11,11.167,11.3,11.583,12],'우하 이동+축소 → 뒤쪽에 겹침','decelerate','11초 이후 변위와 크기 변화가 후반으로 갈수록 작아져 약 11.6~12초 정착하는 시각적 감속. 최초 가속 구간/정밀 함수는 미상.')
obj('T06','cad','앞쪽 노란 테두리 CAD 상세 도면 창')
event('T06','cad','11.3초 전후 목록 창 아래/왼쪽에 희미한 두 번째 창이 겹쳐 나타나고 오른쪽으로 움직여 12초 전경 CAD 창이 된다. 검정 도면 안에 흰 부재 입체도, 정면도, 하단 3개 도면 및 색선/표제가 보인다. 뒤쪽 목록은 소멸하지 않고 상단 띠가 남는다.',['visibility','position'],[11.167,12],[11.167,11.3,11.45,11.583,11.733,12],'희미한 CAD가 전면에서 진해짐; 뒤 목록과 공존','unknown','혼합량 증가와 우측 이동을 모두 확인. 프레임이 겹치고 외곽 위치도 달라 가시성 곡선을 위치 곡선으로 환원하지 않음.')
event('T06','cad','12~12.85초 도면 외곽과 내부 도면 배열이 유지. 별도 구조물 모델이 나중에 앞쪽으로 나타나 CAD 일부를 가린다.',['internal_state'],[12,13],[12,12.567,12.85,13],'CAD 내용 정착 → 전면 모델로 부분 가림','not_applicable','원본 ROI와 시간순 overview 비교. 가림 영역은 이후 내부 검사 불가.')
obj('T06','model','철근·콘크리트 단면 모델')
event('T06','model','12.85초에는 독립 모델이 없고 약 13초부터 CAD 중앙 하단 부근에 작게 나타난다. 우하 방향으로 전개되며 크게 확대되어 13.9초 무렵 정착. 왼쪽의 청록/분홍/노랑 철근, 오른쪽 콘크리트와 3개 검은 부품 및 상단 고리가 보인다.',['size','position','visibility'],[12.85,14],[12.85,13,13.15,13.3,13.5,13.7,13.9,14],'작게 출현 → 우하 확대 → 정착','decelerate','13.15→13.5의 확대폭이 크고 13.5→13.9의 증가폭이 작아지는 ease-out 성격. 외곽을 시각 비교했으며 정밀 오차 미상.',['투영 각도가 대체로 유지되어 별도 회전을 확정하지 않음. 확대·위치 변화와 독립 회전은 구분.'])
obj('T06','modeldetail','모델 흰 윤곽과 뒤의 반투명 사다리꼴 면','model')
event('T06','modeldetail','모델과 함께 가는 흰 외곽선 및 뒤쪽에서 펼쳐진 회색 반투명 면이 보인다. 철근과 콘크리트의 내부 단면은 모델 확대에 따라 함께 커지며 별도의 내부 조립/움직임은 표본에서 식별되지 않는다.',['size','internal_state'],[13,14.4],[13.15,13.5,13.9,14.4],'모델 확대와 동반 → 유지','decelerate','모델과 같은 후반 확대 둔화를 원본 ROI에서 확인; 내부 독립 변형은 확인되지 않음.')
obj('T06','windows','뒤쪽 두 UI 창 재배치')
event('T06','windows','모델이 큰 상태가 된 뒤 약 14.0~14.533초 뒤쪽 두 UI가 더 작아지며 우하 쪽으로 재배치된다. 목록 창의 상단과 좌측 부분이 다시 더 많이 드러나고 CAD는 그 앞에서 유지된다. 모델은 이 동안 전면에 남는다.',['size','position'],[13.9,14.667],[13.9,14.1,14.25,14.383,14.533,14.667],'모델 정착 후 UI 두 장 축소·우하 이동','decelerate','overview에서 14.1~14.38 변화가 크고 14.533~14.667 정착. 시각 추정이며 정밀 추적은 미수행.')
obj('T06','flare','모델 상단 좌측의 금빛 광점과 수평 광선')
event('T06','flare','14.533초 희미하거나 없는 광효과가 14.6~14.8초 모델 왼쪽 상단에서 강해지고 오른쪽으로 길게 뻗은 수평 금빛 선을 만든다. 14.9~15.1초 밝게 유지한 뒤 15.2~15.5초 다소 약해지며 끝 경계에서도 남아 있다.',['brightness','visibility'],[14.533,15.5],[14.533,14.6,14.7,14.8,14.9,15,15.1,15.2,15.35,15.5],'밝기 증가 → 강한 빛 → 약화; 주 광점은 모델 좌상단 근처 유지','unknown','native ROI에서 밝기 상승·후반 약화는 확인. 포화된 광핵과 광폭이 함께 변해 정확한 가감속은 미확정. 빛의 밝기 변화를 위치 이동으로 해석하지 않음.',['15.5초에도 빛이 남음; 완전 소멸을 주장하지 않음.'])
D['T06']['coverage'].update(secondary_details='노란 외곽선, 두 창의 중첩, 모델 흰 테두리/반투명 면, 후발 금빛 수평광을 별도 확인.',internal_content='목록 창 4번째 행/썸네일 선택 유지, 상세 CAD의 3D/2D 복합 도면, 철근 단면을 원본 ROI로 확인. 가린 부분은 미검수.',unresolved=['빛 밝기의 정확한 시간곡선, 창 혼합과 이동 각각의 정밀 곡선 미확정.','전면 모델에 가려진 뒤쪽 UI 내부의 이후 변화는 확인 불가.'])
init('T07',['overview.jpg','ui-detail.jpg'],['T07_rows','T07_thumbs','T07_wholeui'],[P/'cases/자료013/selections/실행기록.json'])
obj('T07','layout','EG-BIM 소개 화면과 노란 테두리 도면관리 창')
event('T07','layout','녹색 격자·큰 황갈색 E·설계선 배경, 우측 EG-BIM 소개문과 좌상단 노란 테두리 UI의 외곽 위치/크기는 선택 표본에서 유지된다. UI 왼쪽 폴더트리, 상단 버튼, 표의 열, 썸네일 격자도 같은 배치다. 내부 선택 상태는 아래와 같이 변한다.',['position','size'],[8.2,10.4],[8.2,9.3,10.4],'외곽 고정 동안 내부 선택 순서 진행','not_applicable','시작·중간·끝 native 전체 UI 및 overview 비교.')
obj('T07','rows','표의 주황 선택 행','layout')
obj('T07','thumbs','썸네일 주황 테두리와 이름 바','layout')
for oid,word,order in [('rows','표 선택','첫 행 → 둘째 행 → 셋째 행 → 넷째 행 (아래 방향)'),('thumbs','첫 줄 썸네일 선택','첫 칸 → 둘째 칸 → 셋째 칸 → 넷째 칸 (오른쪽 방향)')]:
 event('T07',oid,word+'이 순차로 바뀐다. 8.2초 첫 항목이 우세하고 둘째가 희미하게 겹치기 시작, 8.25~8.4초 두 항목이 동시에 주황색으로 보이며 8.5초 둘째가 정착. 9.0초 둘째 유지, 9.1~9.3초 둘째와 셋째 혼합, 9.5초 셋째 정착. 9.9~10.1초 셋째와 넷째 혼합, 10.2~10.4초 넷째 정착.',['internal_state','visibility'],[8.2,10.4],[8.2,8.25,8.3,8.35,8.4,8.5,9,9.1,9.2,9.3,9.5,9.9,10,10.1,10.2,10.4],order+'; 이전 강조 감쇠와 다음 강조 증가가 겹친다.','unknown','각 항목의 고정 자리에서 이전·다음 색이 동시에 존재하는 교차 혼합을 확인. 위치가 연속 이동하는 하나의 표식으로 단정하지 않는다. 짧은 혼합의 정확한 가감속은 미측정.',['첫 전환 시작은 허용 구간 앞에 걸쳤을 가능성. 8.2초 이전 시작을 추정 확정하지 않음.'])
obj('T07','relation','표와 썸네일의 대응 선택','layout')
event('T07','relation','상단 표의 항목 번호 001→002→003→004와 하단 첫 줄 썸네일 번호가 같은 순서로 대응한다. 표는 아래 방향, 썸네일은 오른쪽 방향으로 선택 대상이 바뀌며 각 전환에서 양쪽 선택 강조가 함께 겹친다. 도면 썸네일 내용 자체의 개별 애니메이션은 표본에서 확인되지 않는다.',['internal_state'],[8.2,10.4],[8.2,8.3,8.5,9.2,9.3,10,10.2,10.4],'표 행/썸네일 동시 대응; 목록 스크롤은 관찰되지 않음','not_applicable','행과 썸네일 native ROI의 시간 대응 확인. UI 외곽 이동과 내부 상태 변경을 분리.')
D['T07']['coverage'].update(secondary_details='노란 창 테두리, 주황 행 강조, 썸네일 테두리/이름 바를 각각 확인. 커서 이동/클릭은 표본에서 식별되지 않아 원인으로 주장하지 않음.',internal_content='전체 UI native 처음·중간·끝 및 선택 경계 ROI 확인. 행은 하향, 썸네일은 우향으로 1→2→3→4. 전환 중 두 상태 동시 노출.',unresolved=['첫 전환 시작이 허용구간 앞인지 불명.','선택 강조 혼합의 정확한 easing 함수/사용자 클릭 여부는 불명.'])
# Preserve first final outputs; abort if a final already exists.
sys.path.insert(0,str(S/'scripts'));from check_observations import check
for cid,d in D.items():
 d['files_read']+= [str(P/x) for x in ['crops.py','catalog_run.py','evidence_catalog.json']]
 if cid=='T05':d['files_read'] += [str(P/'crops_blend.py')]
 if cid=='T06':d['files_read'] += [str(P/'crops_ui.py')]
 if cid=='T07':d['files_read'] += [str(P/'crops_sel.py')]
 errs=check(d)
 if errs:raise ValueError((cid,errs))
 out=A/'company-video-grammar-analyzer-workspace/iteration-1'/('eval-'+cid)/'with_skill/outputs';out.mkdir(parents=True,exist_ok=True)
 with (out/'observations.json').open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
 lines=[f'# {cid} 영상 관측 초안',f"허용 구간 {d['window_seconds'][0]}–{d['window_seconds'][1]}초. 문서 없음, 오디오 미검수. AI 렌더 관측이며 제작 의도/AE 구현 확정이 아님.",'']
 for o in d['objects']:
  lines += ['## '+o['name']]
  for e in o['events']:lines += [f"- {e['time_seconds'][0]}–{e['time_seconds'][1]}초: {e['description']} 순서: {e['direction_order']} 이징: {e['easing']['classification']} — {e['easing']['basis']} (근거 {', '.join(e['evidence_ids'])})"]
 lines+=['','## 검사 범위와 미해결',d['coverage']['overview'],d['coverage']['secondary_details'],d['coverage']['internal_content'],*['- '+v for v in d['coverage']['unresolved']+d['limitations']],'','프레임 실제 시각·원본/ROI 좌표·열람 파일 목록은 observations.json 참조. 구조 검사는 내용 정답 판정이 아니다.']
 with (out/'observations.md').open('x',encoding='utf-8') as f:f.write('\n\n'.join(lines))
 print(cid,'structure_passed',len(d['evidence']),'evidence',len(d['objects']),'objects')
