from pathlib import Path
import json,datetime,hashlib
from fractions import Fraction
root=Path.cwd();case=root/'phase01a-a5b/legacy/V05';aux=case/'analysis-support';out=case/'outputs';out.mkdir(exist_ok=True)
i=json.loads((case/'input.json').read_text(encoding='utf-8-sig'));s=json.loads((aux/'selection.json').read_text(encoding='utf-8'));c=json.loads((aux/'crops.json').read_text(encoding='utf-8'))
frames=s['frames'];by_path={f['path']:f for f in frames.values()}
evidence=[]
for j,crop in enumerate(c,1):
 f=by_path[crop['parent_path']]; evidence.append({'id':f'c{j}','path':crop['path'],'actual_seconds':f['actual_playback_seconds'],'role':'within','parent_path':crop['parent_path'],'crop_xyxy_native_pixels':crop['crop_xyxy_native_pixels'],'transform':'native RGB crop; no resize'})
original_times=[0,3.6,4,4.4,4.8,5.2,5.6,6,6.4,8]
for t in original_times:
 f=frames[str(float(t))]; evidence.append({'id':'f'+str(t).replace('.','_'),'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'within'})
def ev(desc,props,a,b,refs,direction,kind='unknown',basis='선택 표본에서 변화는 확인하였으나 진행 중 변화율을 충분히 분리하지 못함.',limits=None,status='observed'):
 return {'description':desc,'properties':props,'time_seconds':[a,b],'evidence_ids':refs,'direction_order':direction,'easing':{'property':','.join(props),'classification':kind,'basis':basis},'status':status,'limitations':limits or []}
objects=[]
def obj(id,name,events,parent=None,**kw):objects.append(dict(id=id,name=name,parent=parent,events=events,**kw))
obj('bg','야간 책상·듀얼 모니터 배경',[
 ev('도시 야경, 두 모니터, 책상·키보드·전화·마우스를 가진 어두운 실내 배경. 왼 모니터는 CAD 도면, 오른 모니터는 도면 목록과 미리보기 그리드이다. 초반의 흐림·어두움이 약해져 3.6초에는 비교적 선명해진다. 모니터 외곽이 소폭 우하 방향으로 커 보이는 변화도 있으나 카메라와 합성 배경 변환은 분리 불가.',['visibility','brightness','sharpness','position'],0,3.6,['f0','c1','c5','f3_6'],'어둡고 흐린 배경 → 더 밝고 선명한 배경'),
 ev('배경의 왼 CAD 도면과 오른 목록의 주황 선택 행은 3.6/6/8초에서 큰 배치가 유지된다. 전경 그래픽이 겹쳐 보이는 범위를 가린다. 제공 표본에서 배경 UI 조작을 확정할 만한 전환은 찾지 못했다.',['internal_content'],3.6,8,['f3_6','f6','f8'],'모니터 내부 주요 도면·선택행 유지','not_applicable','이 사건은 선택 표본 간 상태 비교이며 속도 분류 대상이 아님.', ['가려진 영역과 표본 사이의 짧은 내부 변화는 미검수'])])
obj('ko','국문 주제 제목 인터페이스',[
 ev('0초에는 전경 제목이 보이지 않는다. 0.4초에는 분리된 자소 일부가 낮거나 다른 밝기로 떠 있고 0.6/0.8/1.0/1.2초로 가며 자소가 채워져 인터페이스가 된다. 글자 사이 간격도 좁아져 읽을 수 있는 한 단어로 모인다.',['position','visibility','character_assembly'],0,1.6,['f0','c1','c2','c3','c4','c5','c6'],'분산된 자소/넓은 간격 → 완성 단어/좁은 간격',basis='자소별 가시성과 간격 변화는 보이나 글자마다 동일 특징을 수치 추적하지 않아 속도 분류는 미확정.',limits=['c1~c3은 왼 가장자리 일부가 ROI 밖이다. 전체 위치는 기본 보드로 교차 확인했다.']),
 ev('완성된 흰색 굵은 인터페이스가 화면 오른쪽의 주제 제목으로 유지된다. 영문 단어는 이 제목 위쪽 배후에 더 크게 놓인다. 5.6초 등 일부 표본에서는 제목 왼부분이 직선 경계로 잘린 상태이고 뒤 표본에서 복원된다. 영구 퇴장이 아니다.',['visibility','position'],1.6,10.9333333333,['c6','c10','f5_6','f6','f8','c40'],'주제 제목 유지; 중간 부분 가림/복원',basis='정착 후 간헐적 부분 가시성 변화이며 연속 이동 곡선은 추적하지 않음.')],text='인터페이스')
obj('en','영문 Interface와 녹색 직사각 리빌 영역',[
 ev('1.2초 국문 뒤에 없던 영문이 1.6초에는 Interfa…로 부분 노출되고 2초에는 Interface 전체가 보인다. 짙은 녹색 사각 영역과 흰 점선 테두리의 오른쪽 경계가 오른쪽으로 진행하며 글자를 드러낸다. 글자 자체 크기 변화와 사각 영역 확장을 동일시하지 않는다.',['reveal','frame_width','visibility'],1.2,2.4,['c5','c6','c7','c8'],'왼쪽 영문부터 오른쪽 끝까지 드러남',basis='두 진행 상태의 영역 확장을 확인했으나 초반/후반 진행 변화율을 비교할 표본이 부족.'),
 ev('2.4초에는 완전한 녹색 영역과 점선 테두리가 유지되다가 2.8초에는 왼 I가 어두워지고 왼 경계가 오른쪽으로 들어온다. 3.2초에는 사각 면과 점선이 거의 사라지며 영문 전체가 반투명한 회색 잔상처럼 남는다. 3.6초 이후에도 큰 회색 영문이 남아 있다.',['reveal','visibility','brightness'],2.4,6,['c8','c9','c10','f3_6','f6'],'사각 영역 왼쪽부터 걷힘 → 큰 회색 영문 잔존',basis='사각 리빌과 글자 밝기가 함께 변하므로 단일 opacity나 위치 이징으로 환원 불가.',limits=['실제 마스크/opacity 속성 및 정확한 곡선 미확정'])],text='Interface')
obj('en_cross','영문 리빌 사각 영역의 빨강/초록 십자·작은 사각 표식',[
 ev('1.6초 영문 오른끝 부근에 빨강 가로선이, 2/2.4초에는 우하단 경계의 빨강 작은 사각과 긴 초록 세로선·빨강 가로선이 보인다. 3.2초에는 흐린 선·사각 일부만 남는다.',['position','visibility','brightness'],1.6,3.2,['c6','c7','c8','c9','c10'],'리빌 진행 중 경계 표식 등장 → 약화',basis='미세 선의 밝기와 경계 위치가 함께 바뀌어 독립 가감속 미확정.')],parent='en')
obj('paragraph','오른쪽 주제 설명 3행',[
 ev('2.4초에는 없던 설명이 2.8초에 첫 행부터 낮은 밝기로 등장하고 3.2초에는 3행이 서로 다른 밝기로 보이며 3.6초에는 전체가 밝아진다. 줄 단위로 위에서 아래로 읽히도록 등장한다. 일부 핵심 문구는 굵다.',['visibility','brightness','line_order'],2.4,3.6,['c8','c9','c10','f3_6'],'1행 → 2행 → 3행',basis='행별 혼합/밝기 차이는 확인되지만 정확한 시작과 곡선은 선택 표본 사이에 있음.'),
 ev('내용은 사용자 경험과 편의성, 메뉴 단순화, 듀얼모니터를 활용한 새로운 작업공간을 연결한다. 끝 표본까지 오른쪽 제목 아래에 유지된다.',['content','information_relation'],3.6,8,['f3_6','f6','f8'],'주제 아래 설명, 왼쪽 두 UI 예시의 설명 근거','not_applicable','정착 문구와 정보 관계 관찰.')],text='사용자 경험을 바탕으로 사용자의 편의성을 최우선적으로 고려하여\n기존의 복잡한 인터페이스에서 벗어나 메뉴를 단순화하고,\n듀얼모니터기능을 활용한 새로운 작업공간을 제공합니다.')
obj('g','화면 왼쪽을 크게 차지하는 녹색 G',[
 ev('3.6초에는 곡선 조각과 점선이 먼저 보이고 4초에는 큰 G 형태의 희미한 면/선이 나타난다. 4.4→4.8→5.2초에는 같은 외곽의 녹색 면이 점점 강해진다. G의 위·아래는 화면 밖으로 잘린 큰 크기이고 가로 획이 중앙을 가로지른다. 이 표본들에서는 큰 G 자체의 확장/회전을 확인하지 못했다.',['visibility','brightness','shape'],3.6,5.2,['f3_6','f4','f4_4','f4_8','f5_2'],'가이드 곡선 → 희미한 G → 녹색 면 강화',basis='면의 명도/혼합 비율을 수치 추적하지 않아 곡선 미확정.',limits=['큰 화면 점유 면적은 등장/밝기 변화이며 크기 확대라고 단정하지 않음']),
 ev('5.2초 뒤 큰 G의 녹색 면과 위치는 유지되면서 5.6/6초에 밝은 민트색 윤곽선 일부가 진행해 나타난다. 우상단 잘린 끝과 내측 곡선을 따라 선이 보인다. 9.6/10.933초에도 G와 윤곽·내부 곡선이 남아 있다.',['outline_reveal','visibility'],5.2,10.9333333333,['f5_2','f5_6','f6','c39','c40'],'녹색 면 유지 + 밝은 윤곽선 드러남',basis='윤곽 진행을 충분히 촘촘히 보지 않아 선 길이 곡선은 미확정.')])
obj('g_guides','G 주변의 흰 실선/점선 원호',[
 ev('3.6초에는 여러 곡선 조각, 4초에는 외곽 큰 점선 호와 내측 실선 호가 보인다. 4.4/4.8초에는 G 오른쪽과 화면 왼아래를 가로지르는 곡선들이 다른 길이/위치로 겹친다. 5.2초에는 외곽의 긴 얇은 실선이 남고 5.6초에는 상당 부분 약해진다.',['position','reveal','visibility'],3.6,5.6,['f3_6','f4','f4_4','f4_8','f5_2','f5_6'],'조각 호 출현 → 확장된 원호 중첩 → 잔여 선 약화',basis='복수 선과 G면의 중첩으로 같은 선 끝점의 연속 이동인지 리빌인지 분리 불가.',limits=['선을 전부 하나의 회전 물체로 분류하지 않음'])],parent='g')
obj('g_cross','G 내부 호를 따라 이동하는 CAD식 십자 표식과 궤적',[
 ev('5.6초 G 위쪽에 빨강 가로선과 작은 원형 중심 표식이 생긴다. 6초 이후에는 빨강 사각 중심·가로선과 초록 세로선의 표식이 왼쪽으로 내려와 6.1→6.2→6.3초에 왼쪽 아래에서 오른쪽 아래로 굽는 호를 따라 진행한다. 표식 뒤로 흰 실선 궤적이 길어지고 위쪽 호는 노란 점선으로 보인다. 8초에는 표식이 아래 호 끝에 도달한 상태다.',['position','path_reveal','visibility'],5.6,8,['f5_6','c12','c13','c14','c15','c16','f8'],'G 상부 → 왼 측면 → 좌하단 → 아래쪽 오른방향',kind='decelerate',basis='동일한 빨강 작은 사각 중심을 native crop에서 육안 추정: t=6.0 (536,868), 6.1 (535,1155), 6.2 (590,1376), 6.3 (669,1541), 단위 원본 raster px. 0.1초당 이동 약287,228,183px로 감소. 표식 위치 추정 오차 약±10px; 경로 전체의 단일 보간함수는 미확정.',limits=['위 수치는 native raster 좌표이며 SAR 미상으로 정밀 표시공간 좌표는 아님','상부 원형 표식과 하부 사각 표식의 완전한 동일 객체 여부는 별도 미확정']),
 ev('9.6/10.933초에는 흰 호와 희미한 아래 표식의 잔존이 보인다. 끝까지 가이드가 완전히 사라지지는 않는다.',['visibility'],9.6,10.9333333333,['c39','c40'],'흰 호/표식 희미한 잔존','not_applicable','분석 창 끝 잔존 상태 관찰.')],parent='g')
obj('left_panel','전경 왼쪽 CAD UI 패널과 노란 둥근 프레임',[
 ev('5.8초 ROI에는 아직 전경 패널이 없고 6초에는 위쪽 왼편에 작은 패널이 있다. 6.2/6.4/6.6초로 가며 패널이 커지고 중심이 아래·오른쪽으로 옮겨져 7.2초에는 큰 CAD 화면으로 정착한다. 패널 안은 위쪽 평면/선형도와 아래쪽 종단·수치표로 구성된다.',['position','scale','visibility'],5.8,7.2,['c11','c30','c31','c32','c33','c34'],'작은 상단 패널 → 확대하면서 아래·오른쪽 → 정착',kind='decelerate',basis='동일 노란 외곽의 native raster 폭을 육안 추정: 6.0초 약410px, 6.2초 약795px, 6.4초 약858px, 6.6초 약856px. 진행중 두 증가량 약385/63px로 감소해 크기에는 감속 성격. 중심 y도 약677→819→908→956px로 0.2초 이동량이 감소한다. 오차 약±10px. x의 변화율은 가변이고 동일 감속으로 분류하지 않는다.',limits=['scale 감속 및 중심 y 하강 감속의 시각 추정. AE 키프레임, 정확한 최종 배율/곡선 미확정']),
 ev('7.2초 이후 왼쪽 패널의 노란 프레임과 도면 주요 특징은 정착 위치를 유지한다. 7.4초 뒤 우측 패널이 뒤에서 전개되어도 왼쪽 패널이 함께 밀려나거나 축소되는 것으로 보이지 않는다.',['position','scale'],7.2,10.9333333333,['c34','c35','c36','c37','c38','c39','c40'],'왼 패널 고정, 두 번째 패널만 오른쪽으로 노출','not_applicable','왼 프레임 왼/위/아래 모서리와 CAD 상단 곡선이 같은 위치를 유지하는 표본 비교.')])
obj('left_glow','왼 패널 상단을 따라 변하는 황색 빛',[
 ev('6초 작은 패널 상단 중앙 쪽에 있던 노란 번짐이 6.2초에는 상단의 왼쪽 부근에서 강한 별모양 빛으로 보인다. 6.4/6.6/7.2초에는 왼 위 모서리에 붙어 있고 상단 테두리를 따라 밝은 가로 띠가 있다. 이후에도 왼 위 밝은 점이 남아 있다. 빛 위치와 패널 위치를 구분한다.',['position','brightness','light_extent'],6,10.9333333333,['c30','c31','c32','c33','c34','c40'],'상단 중앙 부근 번짐 → 좌상단 별모양/가로빛 → 잔존',basis='패널 확대·이동을 제거한 빛의 독립 궤적을 수치 추적하지 않았으므로 이징 미확정.')],parent='left_panel')
obj('left_inside','왼 패널 내부 메뉴·명령 영역',[
 ev('6.6/7.2초의 같은 도면 구성이 유지되면서 상단 메뉴·하단 명령 영역의 갈색/노란 강조가 7.0/7.2/7.6초에는 강하고 8.6/9.6/10.933초에는 더 어둡게 보인다. 내부의 넓은 작업 도면과 바깥 프레임이 고정되어도 메뉴 영역의 밝기 변화는 별개다.',['internal_content','brightness'],6.6,10.9333333333,['c33','c19','c34','c35','c27','c39','c40'],'메뉴·명령 영역 황색 강조 강화 → 어두운 상태',basis='강조 영역 밝기 변화는 확인하였으나 선택 상태나 명령 실행으로 연결할 UI 표식은 판독하지 못함.',limits=['실제 소프트웨어 조작 여부, 메뉴별 선택 이동, 데이터 값 갱신은 미확정'])],parent='left_panel')
obj('left_caption','왼쪽 예시 제목·설명',[
 ev('6.6초에는 없고 6.8초에는 노란 띠 위 단순한 메뉴…가 왼쪽부터 노출된다. 7초에는 넓은 작업…까지, 7.2초에는 전체 제목이 보인다. 아래 첫 설명 행은 7.2초, 두 번째 행은 7.6초에 확인된다.',['reveal','visibility','line_order'],6.6,7.6,['c17','c18','c19','c20','c21','c22'],'제목 왼→오른쪽 리빌 → 설명 1행 → 설명 2행',basis='제목 가림 경계와 줄 등장 순서는 확인. 경계 진행/글자 밝기 곡선은 미확정.'),
 ev('8.2/8.6초 등 일부 표본에서는 제목과 설명의 오른쪽 끝이 사각 경계처럼 중간에서 잘려 있다가 8.4/9.6/10.933초에는 다시 전체가 보인다. 문구 교체나 영구 퇴장으로 기록하지 않는다.',['visibility','partial_occlusion'],8.2,10.9333333333,['c25','c26','c27','c28','c29'],'오른쪽 일부 잘림 ↔ 전체 복원',basis='간헐적인 부분 가시성 변화만 확인. 제작 의도/마스크 원인은 미확정.')],text='단순한 메뉴구성 / 넓은 작업공간\n꼭 필요한 기능으로만 단순화한 메뉴구성\n메뉴의 효율적인 공간배치로 넓은 작업공간 확보',information_relation='왼 CAD 예시에 메뉴 단순화·작업공간 확보의 두 이점을 설명')
obj('right_panel','두 번째 CAD UI 패널과 노란 프레임',[
 ev('7.2초에는 왼 패널만 보이고 7.4초 왼 패널 오른쪽 뒤에 두 번째 노란 테두리가 드러난다. 7.6초에는 검은 내부가 먼저 크게 보이고 7.8초에는 왼측 도면 일부, 8초에는 다수의 도면/표, 8.2초에는 오른쪽 흰 속성 패널이 부분 노출되고 8.4초에 완전히 읽을 수 있는 두 패널 나란한 상태가 된다. 창의 상하 높이는 거의 같고 오른쪽 모서리 및 창 버튼은 오른쪽으로 옮겨간다. 왼 패널의 가림이 풀리며 오른 패널의 내부 노출도 늘어난다.',['position','reveal','internal_content','visibility'],7.2,8.4,['c34','c21','c35','c36','c37','c25','c38'],'왼 패널 뒤 얇은 테두리 → 오른쪽 전개 → CAD내용 → 흰 속성 패널',kind='decelerate',basis='동일 오른쪽 노란 수직 프레임을 native crop에서 추정한 x: 7.6초 약1480, 7.8초 약1865, 8.0초 약2048, 8.2초 약2110, 8.4초 약2125px. 같은 0.2초 간격 이동량 약385/183/62/15px로 감소. 오차 약±10px. 가려진 왼 외곽은 비교할 수 없으므로 패널 전체 크기 변화는 미확정.',limits=['노출 면적 증가와 패널 자체 확대를 구분. 내부 도면이 실제 편집된 것으로 단정하지 않음']),
 ev('8.4/9.6/10.933초에서 두 번째 패널은 왼쪽에 평면/종단도, 오른쪽에 작은 표·단면도, 더 오른쪽에 밝은 속성창이 배치된 상태로 유지된다. 속성창에는 색상 255,259,0처럼 보이는 작은 항목이 있으나 판독이 불안정하여 수치 전사를 채택하지 않는다. 확실히 읽히는 도형 수치는 지름 8.1502, 반지름 4.0526, 면적 51.5962이다. 이는 내부 UI 표시값일 뿐 영상 전체 계산 결과를 뜻하지 않는다.',['internal_content','position'],8.4,10.9333333333,['c38','c39','c40'],'두 패널 정착, 오른 속성창 유지','not_applicable','선택된 정착 프레임의 UI 상태 비교.',limits=['내부 선택표식의 미세 변화·실제 계산 갱신·모든 수치 전사 미검수'])])
obj('right_caption','오른쪽 듀얼모니터 제목·설명',[
 ev('7.6초에는 오른쪽 아래에 가느다란 노란 세로 조각, 7.8초에는 모니터, 8초에는 듀얼모니터가 보인다. 노란 제목 띠는 오른 끝을 거의 유지하며 왼쪽으로 펼쳐져 글자가 오른쪽부터 역방향으로 드러난다. 8.2초 설명 첫 행, 8.4초 두 번째 행 조각, 8.6초에 전체 두 행이 보인다.',['reveal','visibility','line_order'],7.6,8.6,['c22','c23','c24','c25','c26','c27'],'제목 오른쪽→왼쪽 리빌 → 설명 1행 → 2행',basis='방향과 순서는 확인. 제목 리빌 폭/행별 밝기 곡선을 수치 추적하지 않아 이징은 미확정.'),
 ev('9.6/10.933초에도 오른쪽 정렬된 노란 제목과 흰 두 행 설명이 유지된다. 두 번째 행의 더욱 넓어진 작업공간이 굵다.',['visibility','information_relation'],9.6,10.9333333333,['c28','c29'],'듀얼모니터 기능 → 분리/연동 → 작업공간 확대','not_applicable','정착 문구와 정보 관계 관찰.')],text='듀얼모니터\n듀얼모니터의 화면 분리 및 연동기능으로\n더욱 넓어진 작업공간 제공')
obj('layout','전체 정보 계층 및 구간 말 상태',[
 ev('주제 소개는 오른쪽 인터페이스 제목·설명으로 먼저 정착하고 왼쪽에는 큰 녹색 G와 기술 도형 가이드가 겹친다. 그 위 노란 프레임의 UI 예시 하나가 먼저 커져 들어온 뒤 두 번째 패널이 오른쪽으로 분리 전개된다. 두 예시에 각각 노란 소제목과 흰 설명이 붙는다. 주제 설명이 주장, UI 패널과 하단 문구가 기능 사례의 관계다.',['information_relation','sequence'],0,10.9333333333,['f0','c6','f3_6','f4_4','c34','c35','c38','c40'],'제목 → 영문/설명 → G/가이드 → 왼 UI/설명 → 오른 UI/설명','not_applicable','개별 사건의 근거를 연결한 관측 순서. 기능 실제 검증이나 회사 의도 추론은 하지 않음.'),
 ev('마지막 10.933초 표본까지 제목·G·두 UI·하단 문구가 남아 있다. 지정 창 안에서 전체 퇴장은 관측되지 않았다. 끝 경계는 10.9666666667초 미포함이며 그 사이 약0.033초는 직접 보지 않았다.',['visibility'],9.6,10.9666666667,['c39','c40'],'구간 말 정착 유지','not_applicable','마지막 제공 표본까지의 존재 확인.')])
read=[str((case/'input.json').resolve()),str(root/'phase01a-a5b/common-task.md'),str(root/'phase01a-a5b/common-output-format.md'),str(root/'phase01a-a5b/candidate/company-video-grammar-analyzer/SKILL.md')]
read += [str(root/'phase01a-a5b/candidate/company-video-grammar-analyzer/references'/n) for n in ['evidence-and-records.md','motion-review.md','output-contract.md']]
read+=i['raw_extraction_logs'];read += [str(root/'phase01a-a4/cases/A4-G/V05'/f'board-{n}.jpg') for n in [1,2,3]]
read += list(dict.fromkeys([e['path'] for e in evidence]+[x['parent_path'] for x in c]))
read += [str(root/'phase01a-a5b/candidate/company-video-grammar-analyzer/scripts'/n) for n in ['check_observations.py','evidence_catalog.py']]
d={'schema_version':'a3-observation-0.1','case_id':'V05','source':i['source'],'window_seconds':i['window_seconds'],'method':'기본 보드 3장으로 시간순 전체를 훑고 정착 상태에서 역추적. 원본 전체 PNG 10장과 기존 raw log PNG에서 무배율 RGB native crop 40개를 실제 열람. 첫 29개 중 패널 ROI의 상단이 잘린 한계를 발견하여 11개 fullpanel ROI를 추가해 같은 원본 특징을 대조. 새 영상/음성 디코딩 없음. 시각은 로그 actual_playback_seconds를 사용. 가감속은 같은 대상·속성의 육안 raster 위치/폭 추정만 채택.','document_mode':'none','audio_reviewed':False,'evidence':evidence,'objects':objects,'coverage':{'overview':'0~10.933333초: 기본 29시각/보드3장 전체, 원본 전체10장 직접 확대 열람. 0~10.9666666667초 요청 창 끝 중 마지막 약0.033초는 표본 없음.','secondary_details':'영문 사각 프레임·십자, G 주변 원호/점선·십자 궤적, 노란 UI 프레임과 좌상단 빛, 하단 문구의 리빌/부분 가시성을 native crop에서 확인.','internal_content':'배경 듀얼 모니터의 CAD/목록 상태, 전경 왼 CAD 메뉴 강조와 내부 도면, 오른 창이 검은 공간에서 CAD/흰 속성창으로 드러나는 순서 및 구간 말 유지 확인.','unresolved':['국문 각 자소·영문 사각 리빌·밝기·G 면·선·빛 각각의 가감속 함수는 미확정','G 외곽이 정지한 동안의 일부 윤곽 진행 방향과 완전한 소실 경계는 모든 프레임을 보지 않아 미확정','간헐적인 문구 부분 잘림의 제작 의도/원인 미확정','배경 및 전경 내부 UI의 미세 선택 변화와 실제 명령 실행 미확정','정확한 원본 AE 키프레임/마스크/불투명도 구현과 회사 공통 문법·의도는 미확정']},'hypotheses':[],'limitations':['무문서 경로: 제작 전 원고/문서 대조 대상 없음','음성은 범위 밖이며 듣기/디코딩/전사/싱크 검수 없음','원본 MP4는 접근/재해시하지 않고 제공 추출 로그의 고정 원본 해시와 PNG 해시·표시시각 provenance를 helper로 연결','SAR unknown, raw raster RGB 변환의 range_accuracy_validated=false. 공식색/정밀 표시공간 치수로 해석하지 않음','선택 프레임 분석으로 짧은 중간 상태 누락 가능. 전 구간 연속 재생 또는 모든 프레임 검수 아님','일부 초기 crop의 상단/왼쪽이 잘려 있음을 11개 보강 crop 및 전체 원본으로 보완. 생성/열람 총40개로 한도 도달','가감속 수치는 시각적 대략치이며 ±10px 추정 오차, AE easing influence/보간함수 복원 아님','직접근거 crop은 parent_path와 native xyxy를 기록하여 helper --crops로 RGB 픽셀 일치 검증'], 'files_read':read,'review_log':{'substantive_review_started_utc':'2026-10-16T08:18:08Z','crop_created_count':40,'crop_visually_read_count':40,'native_full_frame_directly_viewed_count':10,'overview_boards_viewed_count':3,'raw_extraction_logs_read_count':3,'new_decoded_frames':0,'human_review':'none; AI observation only','prior_outputs_or_grading_read':False}}
# Unreliable colour tuple is explicitly excluded; retain only confidently read values above.
d['objects'][12]['events'][1]['description']=d['objects'][12]['events'][1]['description'].replace('속성창에는 색상 255,259,0처럼 보이는 작은 항목이 있으나 판독이 불안정하여 수치 전사를 채택하지 않는다. ','속성창의 작은 색상 항목은 판독이 불안정하여 수치 전사를 채택하지 않는다. ')
finished=datetime.datetime.now(datetime.timezone.utc).isoformat();d['review_log']['analysis_completed_utc']=finished
(out/'observations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
md='''# V05 독립 관측 초안

원본 A4-G의 [0, 10.9666666667)초. 문서 없음, 음성 미검수. 본격 열람 시작 2026-10-16T08:18:08Z. 기본 보드 3장, 전체 원본 PNG 10장, native RGB crop 40개를 확인했다. 새 영상 디코딩은 하지 않았다.

- 0~1.6초: 야간 듀얼 모니터 배경이 선명해지는 동안 국문 **인터페이스**의 자소가 따로 나타나고 간격이 좁아져 단어로 모인다(c1~c6). 각 자소의 가감속은 미확정.
- 1.6~2초: 큰 **Interface**가 녹색 사각 영역의 오른쪽 확장으로 드러난다. 점선 테두리·빨강/초록 십자 표식이 동반된다. 2.8~3.2초에는 사각 면과 선이 걷히거나 약해지고 회색 영문은 남는다(c6~c10).
- 2.8~3.6초: 오른쪽 설명이 위에서 아래 3행 순서로 밝아진다. “사용자 경험을 바탕으로 사용자의 편의성을 최우선적으로 고려하여 / 기존의 복잡한 인터페이스에서 벗어나 메뉴를 단순화하고, / 듀얼모니터기능을 활용한 새로운 작업공간을 제공합니다.”(c9,c10,f3_6).
- 3.6~5.2초: 흰 실선·점선 원호가 겹쳐 나타난 뒤 같은 위치의 큰 녹색 **G**가 점차 강해진다. G 자체의 확대/회전은 확인하지 못했다. 면, 윤곽선, 주변 가이드는 별도 변화다(f3_6~f5_6).
- 5.6~8초: 빨강/초록 십자 표식이 G 위쪽에서 왼쪽을 거쳐 아래 호로 진행한다. 뒤로 흰 궤적, 위쪽에는 노란 점선이 남는다. 동일 사각 중심의 6.0/6.1/6.2/6.3초 이동량이 약287/228/183px로 줄어 해당 하강 호 구간은 **감속 성격**이다(c12~c15). 육안 추정 오차 약±10px, 정확한 함수는 미확정.
- 5.8~7.2초: 왼 CAD 패널이 작은 상단 상태에서 커지며 아래·오른쪽으로 이동해 정착한다. 6.0/6.2/6.4초 폭은 약410/795/858px로, **크기 변화는 감속**이다. 중심 y의 하강도 감속하며 x 곡선은 미확정. 노란 둥근 외곽과 좌상단 별모양 빛이 동반된다(c30~c34). 빛의 독립 속도는 미확정.
- 6.8~7.6초: 왼 노란 소제목 **단순한 메뉴구성 / 넓은 작업공간**이 왼쪽부터 리빌된다. 이어 “꼭 필요한 기능으로만 단순화한 메뉴구성”, “메뉴의 효율적인 공간배치로 넓은 작업공간 확보”가 1행→2행으로 나타난다(c18~c22).
- 7.4~8.4초: 두 번째 노란 패널이 왼 패널 뒤에서 오른쪽으로 전개된다. 검은 내부→CAD 도면→오른쪽 흰 속성창 순서로 드러난다. 왼 패널은 외곽과 내부 특징이 그대로 유지된다. 오른 패널 오른쪽 프레임은 7.6/7.8/8.0/8.2/8.4초 약1480/1865/2048/2110/2125px로 **오른쪽 이동이 감속**한다. 가림 해소를 전체 크기 확대라고 기록하지 않았다(c35~c38,c25).
- 7.6~8.6초: 오른 노란 제목은 얇은 조각→모니터→**듀얼모니터**로 오른쪽부터 왼쪽으로 리빌된다. 이어 “듀얼모니터의 화면 분리 및 연동기능으로 / 더욱 넓어진 작업공간 제공”이 1행→2행으로 나타난다(c22~c27).
- 내부 UI: 왼 도면은 유지되지만 메뉴·명령 영역의 갈색/노란 강조는 강화 후 어두워진다. 오른 속성창과 도면은 8.4/9.6/10.933초 비교에서 유지된다. 실제 명령 실행이나 계산 갱신은 확인하지 못했다(c33~c40).
- 8.2/8.6초 일부 왼 소제목·설명의 오른 끝은 사각 경계처럼 잘렸다가 다른 표본에서 복원된다. 5.6초 국문 주제에도 일부 잘림이 보인다. 이를 문구 교체나 영구 소실로 해석하지 않았다(c25~c29,f5_6).

오른쪽 주제/설명이 전체 주장이고, 왼쪽 두 UI 예시와 노란 소제목은 메뉴 단순화 및 듀얼모니터 작업공간 이점을 보여주는 하위 사례다. 마지막 10.933초까지 G·주제·두 예시·문구가 남는다. 분석 끝 경계 직전 약0.033초는 표본이 없다.

불명확: 자소별 이징, 영문 사각 리빌/밝기, G면·윤곽 및 주변 원호·빛의 개별 곡선, 간헐적 부분 가림의 원인, 미세 UI 선택 상태. AE 키프레임·제작 의도·회사 공통 문법은 확정하지 않는다. SAR 및 RGB range 정확도 제한을 보존했다. 원본 해시·실제 표시시각·PNG/crop 연결을 스킬 helper로 검사하며 이 검사는 내용 정답 판정이 아니다.
'''
(out/'observations.md').write_text(md+'\n분석 완료 UTC: '+finished+'\n',encoding='utf-8')
start=datetime.datetime.fromisoformat('2026-10-16T08:18:08+00:00');end=datetime.datetime.fromisoformat(finished)
effort={'case_id':'V05','substantive_review_started_utc':start.isoformat(),'analysis_completed_utc':finished,'ai_elapsed_seconds':(end-start).total_seconds(),'ai_elapsed_basis':'본격 첫 기본 보드 열람부터 최초 결과 작성 완료까지 wall-clock','actual_human_work_seconds':0,'human_work_basis':'사용자 참여/검수 없음','tokens_used':None,'token_status':'host_not_exposed_unknown','native_rgb_crops_created':40,'native_rgb_crops_read':40,'original_png_direct_views':10,'overview_boards':3,'new_video_or_audio_decoding':False,'first_output_frozen':True,'revision_feedback_received':False,'freeze_meaning':'최초 observations.json/md는 내용 수정 피드백 없이 완료; 구조/provenance 검사 결과와 해시를 별도 기록'}
(out/'run-effort.json').write_text(json.dumps(effort,ensure_ascii=False,indent=2),encoding='utf-8')
freeze={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [out/'observations.json',out/'observations.md']};(aux/'frozen-output-sha256.json').write_text(json.dumps(freeze,indent=2),encoding='utf-8')
print(json.dumps({'objects':len(objects),'events':sum(len(x['events']) for x in objects),'evidence':len(evidence),'completed_utc':finished,'elapsed_seconds':effort['ai_elapsed_seconds']},ensure_ascii=False))
