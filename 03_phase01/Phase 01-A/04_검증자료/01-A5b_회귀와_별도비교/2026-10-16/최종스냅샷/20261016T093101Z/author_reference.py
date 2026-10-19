from pathlib import Path
import json,datetime
from fractions import Fraction
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
W=read(B/'windows.json');CS=read(B/'reference/crops.json');out=[]
def build(cid,core,detail,unjudgable):
 w=next(x for x in W if x['case_id']==cid);aid={'H01':'A5-T','H02':'A5-A','H03':'A5-K','H04':'A5-K'}[cid]
 fs=[]
 for phase in [cid,'REF-'+cid]:fs+=read(B/'cases'/aid/phase/'실행기록.json')['frames']
 atoms=[]
 for tier,items in [('core',core),('detail',detail)]:
  for i,(target,prop,text,times) in enumerate(items,1):
   evidence=[]
   for t in times:
    f=next(f for f in fs if Fraction(f['actual_playback_seconds'])==Fraction(str(t)))
    evidence.append({'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'sha256':f['sha256']})
   atoms.append({'id':f'{cid}-{tier[0].upper()}{i:02}','source_id':aid,'window_id':cid,'target':target,'property_or_relation':prop,'state_or_direction_or_order':text,'time_bracket':[min(times),max(times)],'evidence':evidence,'tier':tier,'judgable':True,'reason_if_unjudgable':None})
 return {'case_id':cid,'source_sha256':w['sha256'],'window_seconds':w['window_seconds'],'atoms':atoms,'unjudgable_properties':unjudgable,'native_crop_evidence':[x for x in CS if x['case_id']==cid],'boundary_scoring_note':'time_bracket is an observed event/state span, not automatically an onset bracket. Only separately stated boundary events use boundary tolerance. Exact time evidence must match log.'}
out.append(build('H01',[
('배경','appearance','푸른/청록 사선 띠 배경이 처음부터 있고 초반 띠 위치·밝기/흐림이 변한 뒤 대체로 유지된다',[0,.4,.8,1.2]),
('Value of','reveal_order','영문이 왼쪽 V부터 오른쪽 of까지 순차로 풀려 드러난다',[1.4,1.8,2.2,2.6,3]),
('Value of','text','완성되는 문구는 Value of',[3,3.2]),
('TOVA 로고','reveal','Value of 뒤 우측에서 흰 가로 조각→TOVA 로고의 아래쪽/후속 획까지 단계적으로 완성된다',[3.4,3.8,4,4.2]),
('Value of','visibility','완성된 Value of는 점차 어두운 회색으로 약해지지만 남는다',[3.2,3.8,4.6,6.4,7.6]),
('로고 아래 한국어','reveal','로고 완성 뒤 설명 두 줄이 부분 문구에서 완전한 두 줄로 드러나고 진해진다',[5.4,5.6,6,6.4]),
('거대한 T','position_reveal','우상단 흰 사선/지도 조각이 들어와 좌하 방향으로 점유를 넓혀 거대한 T 형태가 된다',[6.4,6.6,6.8,6.9,7.1,7.3,7.6]),
('로고와 설명','relation','큰 T가 생긴 뒤에도 앞의 TOVA 로고와 설명이 전경에 남고 Value of는 그 뒤쪽 회색으로 남는다',[6.4,7.2,7.6])
],[
('Value of','shape','등장 중 글자에 말림/접힘처럼 휘어진 어두운 면과 밝은 앞면이 따로 보여 단순 전체 페이드에 그치지 않는다',[1.8,2.2,2.6,3]),
('TOVA','color_detail','흰 로고 획 안/오른쪽 끝에 노란 사선 작은 획들이 추가된다',[3.8,4.2,4.6]),
('로고 영문 풀네임','text','작은 풀네임은 TOtal Vehicle Assignment (표시 대소문자는 이 형태)',[4.6,5.6,6.4]),
('로고 영문 풀네임','color','TO/V/A 등 대응 첫 부분이 노란색이며 나머지 문자는 흰색',[4.6,6.4]),
('한국어 설명','text','도로, 버스, 도시철도, 지역간 철도, 항공 및 해운 여객교통수요를 통합적으로 분석하는 한국형 통합 교통 수요분석 프로그램이라는 문구',[6.4,7.6]),
('한국어 설명','color','둘째 줄 한국형 통합 교통 수요분석 프로그램이 노란색으로 강조된다',[5.6,6.4]),
('큰 T 내부','sharpness','흰 면의 흐린 내부가 선명한 도로 지도 선으로 드러난다',[6.9,7.1,7.3,7.6]),
('TOVA 설명','reveal_order','첫 줄 뒤 둘째 줄은 한국형부터 더 긴 강조 구절과 입니다까지 이어진다',[5.6,6,6.4])
],['정확한 AE 속성·함수/핸들 값','Value of 말림의 실제 3D 회전축','정밀 이징은 동일 속성 진행 중 변화율 측정 없이는 unknown 허용']))
out.append(build('H02',[
('전체','layout','열차 사진과 거대한 반투명 A 위에 Public Transport/대중교통 분석 주제 및 UI 예시 창들이 중첩된다',[12,14,18.8]),
('기존 노란 UI','position_size','12초 전경의 노란 테두리 표/지도 창은 오른쪽 아래로 움직이며 작아진다',[12,12.4,12.8,13.2]),
('다음 지도 UI','position_size','처음 좌상단 작은 지도창이 아래·오른쪽으로 와 왼 중앙의 큰 창으로 확대 정착한다',[12,12.4,12.8,13.2,13.6]),
('UI 아래','text','전경 예시의 소제목은 대중교통 요금 설정기능',[13.4,14.6,16.8]),
('소제목과 본문','order','UI 전개 뒤 노란 소제목과 아래 흰 본문이 등장해 기능 설명을 이룬다',[13,13.4,14.2,14.6]),
('전경 UI','exit_position_size','후반 전경 UI는 오른쪽 아래로 작아지며 이동하고, 다른 작은 예시와 함께 사라진다',[17.8,18.2,18.4,18.6,18.7,18.8]),
('주제','persistence','예시 퇴장 뒤에도 열차/A/대중교통 분석 제목과 주제 설명은 남는다',[18.6,18.8,19.6])
],[
('전경 지도 UI','outline','검은 외곽의 지도창이 정착할 무렵 노란 강조 테두리가 왼/상부터 추가되어 전체 둘레를 이룬다',[13,13.4,13.8,14.6]),
('전경 지도 UI 내부','content','다색 노선 지도 왼쪽에 요금/노선 표 대화상자가 있고 메뉴/도구막대도 보인다',[13.4,14.6,16.8]),
('노란 소제목','exit_reveal','후반 소제목은 오른쪽 끝부터 없어져 폭이 줄고 왼 작은 노란 조각만 남은 뒤 소실된다',[16.8,17.2,17.4,17.6]),
('소제목 아래 본문','exit_visibility','흰 기능 설명은 제목 축소와 겹쳐 약해져 사라진다',[17,17.4,17.8,18]),
('주변 선/노드','motion','얇은 흰 곡선 위 검은 점·노란 점이 있고 화면 하단/좌측 점 위치가 시간에 따라 달라진다',[12,14,16.8,18.2]),
('주제 설명','text','현실적으로 이용가능한 모든 대중교통 경로를 탐색하여, 대중교통 분석 결과의 현실적 설명력을 향상시킵니다.',[18.6,19.6]),
('기능 본문','meaning','대중교통 수단&노선에 따라 기본 요금, 거리, 추가거리 및 요금 등 통행항수요 규제/통합항수요 규제 문구는 별도 정밀판독 필요; 확실한 부분은 기본 요금·거리·추가거리 및 요금 설정 설명',[13.4,14.6])
],['원본 촬영 열차의 실제 속도','정밀 위치/크기 easing은 같은 특징 추적 없이는 unknown 허용','작은 UI 모든 행 숫자/선택 상태의 실제 조작']))
out.append(build('H03',[
('초기 장면','layout','수신기1·수신기2·수신기3(저가형) 사진이 좌→우, 아래 비교표',[25,29.4]),
('초기 제목','text','장비 비교 화면임에도 실제 좌상단 표시는 데이터 분석 방법',[25,29.4]),
('표','numeric_relation','Matrice300RTK 1cm+1ppm; 수신기1 0.6cm+0.5ppm; 수신기2/3 1cm+1ppm을 대응한다',[25,29.4]),
('장면 전환','visibility_order','장비/표가 약해지는 동안 두 지도 패널이 작게 겹쳐 생겨 확대되어 새 장면으로 교체된다',[29.6,29.7,29.8,29.9,30,30.2,30.6]),
('새 제목','text','좌상단이 데이터 취득 방법 소개로 바뀐다',[29.8,30.1,30.2]),
('지도 내부 드론 아이콘','position','두 지도 안에서 드론 아이콘이 노란 경로를 따라 이동한다; 왼 지도는 상단에서 우측 세로 변을 아래로 진행',[30.6,31.4,32.2,33.4,34.6]),
('아래 설명','numeric_text','드론 비행 경로 / 비행고도:50m / 비행속도:2m/s가 후행 등장',[31.6,32,32.3,32.6])
],[
('수신기3','color_motion','사진 테두리 및 수신기3(저가형) 라벨이 옅은 상태와 주황 강조 상태를 반복해 보인다',[25,25.2,25.8,26,27.2,28,28.2,29.4]),
('표의 수신기3 열','color','수신기3 마지막 열은 주황 글자/옅은 배경으로 다른 수신기와 구분된다',[25,28,29.4]),
('지도 둘','layout','왼쪽은 세로로 긴 운동장 정사영, 오른쪽은 넓은 사선 항공사진이며 흰 둥근 외곽을 유지',[30.6,32.6,34.6]),
('지도 경로','internal_content','보라 핀 다섯 점과 노란 연결선이 있으며 오른쪽은 WP1~WP5 표기',[30.6,32.6]),
('하단 문구','order','드론 비행 경로가 먼저 읽힌 뒤 고도/속도 오른쪽 흰 상자가 채워진다',[31.6,31.9,32,32.1,32.3]),
('원고 대응','document_relation','DOC064 장비 상세/취득 방법 내용을 실제로 보여주지만 원고 예정21~27/27초이후 실촬영과 이번25~35초 실제 배치가 다르다',[25,30.6,34.6])
],['지도 아이콘의 실제 드론 위치 동기 정확성','수신기 강조의 정확한 주기/AE 속성','패널 확대의 정밀 easing은 동일 특징 측정 없이 unknown 허용']))
out.append(build('H04',[
('전체','layout','실촬영 하늘/작은 드론 위 좌상단 청록 제목, 우상단 세로 지도 inset, 하단 자막',[66,70,75.6]),
('하단 자막','text_change','경로 비행에서 착륙으로 교체되고 뒤에도 유지된다',[66.8,67,67.7,75.6]),
('좌상단 제목','text_change','드론 비행 시험 진행에서 드론 비행 시험 종료로 바뀐다',[66.8,67,67.3,67.5,67.8]),
('넓은 실촬영','framing_motion','67초대 이후 하늘에서 아래 운동장/건물/지평선이 더 많이 들어오는 하향 재프레이밍이 있다',[67.1,68,69.6,70.4,71.4]),
('실촬영 컷','shot_change','71.4→71.5 사이 넓은 운동장 장면에서 하늘 속 더 크게 보이는 드론 장면으로 급격히 교체된다',[71.4,71.5]),
('실촬영 후반','position_relation','큰 드론이 있는 뒤 장면에서 지면/나무/인물이 더 드러나고 드론이 그 높이 쪽으로 내려와 보인다; 창 끝 착지 완료는 보이지 않음',[71.6,72.8,74,75.6]),
('지도 내부','position','inset 자체는 고정되어도 안의 흰 드론 아이콘은 좌측 노란 세로 경로를 위로 가 상단 왼 핀 부근에 머문다',[66,66.8,67.8,71.4,75])
],[
('제목 패널','shape_visibility','기존 제목 소실 뒤 좁은 세로 청록 조각→가로 폭이 넓어진 제목 패널로 나타난다. 실제 3D 구현은 미상',[67,67.3,67.5,67.8]),
('자막과 제목','order','착륙 자막이 새 시험 종료 제목의 완성보다 먼저 보인다',[67,67.7,67.8]),
('지도','internal_content','세로 운동장 지도 안의 보라 핀 다섯 개/노란 경로/흰 모서리 테두리는 유지',[66,67.8,75]),
('지도 드론 아이콘','brightness','도착부 아이콘에 밝은 원형/반투명 링 강조의 강약·면적 변화가 있다',[66.8,67.8,71.4,75]),
('후반 드론','appearance','확대된 실제 드론 상부에 작은 붉은 빛이 보인다',[71.5,72.2,73,74.2]),
('원고 대응','document_relation','DOC064 착륙 예정50~61초/분석방법61~71초와 달리 이번66~76초 실제 화면은 경로비행→착륙이며 분석방법 슬라이드가 아니다',[66,70,75.6])
],['실제 비행 고도/속도 및 지도와의 프레임 단위 동기','실사 드론/카메라 혼합 운동의 easing','창 끝 착지 완료 여부는 이번 범위로 확정 불가']))
# One provisional unreadable item must not become a fabricated reference detail.
h2=out[1];h2['atoms']=[x for x in h2['atoms'] if x['id']!='H02-D07']
h2['unjudgable_properties'].append('기능 설명 마지막 줄은 reference ROI 하단이 잘려 정확 전사를 기준에 넣지 않음; 새 native decode 예산은 추가하지 않음')
payload={'version':'pretrial-reference-draft-1','author':'root AI','human_gold':False,'primary_outputs_seen':0,'authored_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'criteria':out,'scope':'selected 36 visual seconds, no audio. One record per semantic atom; no duplicate credit. Unknown true-indeterminate easing not a missed atom. Reference audit still required before seal.'}
(B/'reference/reference-draft.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print([(x['case_id'],sum(a['tier']=='core' for a in x['atoms']),sum(a['tier']=='detail' for a in x['atoms'])) for x in out])
