import json
from pathlib import Path
from fractions import Fraction
B=Path('phase01a-a5b').resolve();R=B/'trials/H01-r2-with_skill';S=R/'support';O=R/'outputs';O.mkdir(exist_ok=True)
input_data=json.loads((R/'input.json').read_text(encoding='utf-8'))
rows=json.loads((S/'rows.json').read_text(encoding='utf-8')); bypath={f['path']:f for f in rows}; bytime={float(Fraction(f['actual_playback_seconds'])):f for f in rows}
crops=json.loads((S/'crops.json').read_text(encoding='utf-8'))
direct=[0,.4,.8,3.2,6.4,8,3.5,3.7,4.4,4.8,6.6,6.7,6.8,6.9,7,7.1,7.4,.2,.6,1.2,7.2,7.3,7.6]
E=[]; F={};C={}
for t in direct:
 f=bytime[t];eid='f_'+str(t).replace('.','_');F[t]=eid;E.append({'id':eid,'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'context_after' if t==8 else 'within'})
for n,c in enumerate(crops,1):
 f=bypath[c['parent_path']];t=float(Fraction(f['actual_playback_seconds']));eid=f'c{n:02d}';C[(t,Path(c['path']).stem.split('_')[-1])]=eid;E.append({'id':eid,'path':c['path'],'actual_seconds':f['actual_playback_seconds'],'role':'context_after' if t==8 else 'within','parent_path':c['parent_path'],'crop_xyxy_native_pixels':c['crop_xyxy_native_pixels']})
def f(t):return F[t]
def c(t,k):return C[(t,k)]
def ev(desc,props,t,refs,order,ease='unknown',basis='선택 표본에서 방향/변화는 보이나 같은 속성의 진행 중 변화율을 충분히 비교하지 않아 가감속 미확정.',limitations=None,measurement=None):
 e={'description':desc,'properties':props,'time_seconds':t,'evidence_ids':refs,'direction_order':order,'easing':{'property':props[0],'classification':ease,'basis':basis},'status':'observed','limitations':limitations or []}
 if measurement:e['easing']['measurement']=measurement
 return e
objects=[]
def obj(id,name,events,parent=None,**kw):objects.append(dict(id=id,name=name,parent=parent,events=events,**kw))
obj('bg','남색·청록 사선 띠 배경',[
 ev('시작은 짙은 남색 면이 대부분이며 좌상단 청록 모서리와 우하단 사선 면이 보인다. 0.2~0.6초에는 상부 파랑 띠의 수평 끝선은 아래로, 하부 청록 띠의 수평 시작선은 위로 진행한다. 0.8~1.2초에는 평행한 사선 띠들로 화면이 채워진다.',['reveal_boundary_position','visible_area'],[0,1.2],[f(0),f(.2),f(.4),f(.6),f(.8),f(1.2)],'위 파랑 띠: 위→아래 / 아래 청록 띠: 아래→위, 시간상 겹침',limitations=['띠의 실제 레이어 이동과 마스크/성장 리빌을 렌더만으로 분리하지 못했다. 대각선의 방향을 곧바로 실제 이동 벡터로 쓰지 않았다.']),
 ev('좌상단 청록 면의 낮은 수평 끝이 시작보다 아래로 내려와 정착한다. 이후 오른쪽 위의 넓은 청록 광택, 중앙 어두운 그라데이션, 우하단 어두운 사선은 제목과 로고의 공통 바탕으로 유지된다.',['position','brightness'],[0,6.4],[f(0),f(.2),f(.4),f(.8),f(1.2),f(3.2),f(6.4)],'좌상단 면 끝: 하향; 넓은 광택/그림자는 띠 형성과 함께 노출',limitations=['작은 광택의 독립 이동 경로/밝기 곡선은 추적하지 않았다. 배경 전체가 픽셀 단위로 완전히 정지했다는 판정은 아니다.'])])
obj('headline','왼쪽 대형 문구 Value of',[
 ev('1.2초에 작은 꺾인 획, 1.4초에 V의 하부 조각이 보인다. 1.8초에는 V와 다음 글자들의 어두운 휘어진 면, 2.2초에는 Val 쪽이 밝고 평평해진다. 2.6초에는 Value가 거의 펴지고 다음 부분이 위로 말린 채 남는다. 3.0초에 Value of의 정면 글자가 읽히며 위쪽 어두운 뒤면 조각은 3.2초에도 잔존하고 3.5초 표본에서는 보이지 않는다.',['shape_deformation','reveal','brightness'],[1.2,3.5],[f(1.2),c(1.4,'left'),c(1.8,'left'),c(2.2,'left'),c(2.6,'left'),c(3.0,'left'),f(3.2),f(3.5)],'V→a/l→u/e→o/f, 왼쪽에서 오른쪽으로 진행하는 말림/펴짐; 진행 경계 위에 어두운 글자 면이 남음',limitations=['종이처럼 휘는 투영 형태는 관측했지만 3D 회전축·페이지컬 효과 종류·각도·실제 두께는 미확정. 단순 위치 이동/확대라고 단정하지 않는다.']),
 ev('완성된 Value of는 왼쪽 아래 같은 위치에서 밝은 흰색에서 낮은 대비의 회청색으로 약해진다. 3.2초보다 3.5~3.7초가 어둡고 4.4초에는 낮은 대비로 남는다. 작은 로고가 밝아지는 동안 큰 문구는 배경 수준으로 약화된다.',['brightness','visibility'],[3.2,4.8],[f(3.2),f(3.5),f(3.7),f(4.4),f(4.8)],'위치 유지하며 밝기 감소; 완전 소실 아님',limitations=['픽셀 밝기 변화와 실제 opacity/색 애니메이션을 구분하지 못했다. 밝기 변화율은 미측정.']),
 ev('지도 T가 왼쪽으로 지나오면서 큰 문구의 오른쪽부터 덮인다. 7.1초에는 문구 전체가 남고 7.2초에는 지도 위에 of의 옅은 형상이 겹쳐 보이며 7.3초에는 오른쪽 글자들이 지도에 가려진다. 7.4~7.7초와 8초 문맥에서는 왼쪽 Valu 부근만 남는다.',['occlusion','visible_area'],[7,8],[c(7.0,'title'),c(7.1,'title'),f(7.2),c(7.3,'title'),c(7.4,'title'),c(7.5,'title'),c(7.7,'title'),f(8)],'가림 경계가 오른쪽→왼쪽; 오른쪽 부분 소실, 왼쪽 잔존','not_applicable','가림 관계의 변화이며 큰 문구 자체의 이동 속도로 해석하지 않는다.',limitations=['7.2초의 투과/겹침이 실제 알파·혼합·효과 중 무엇인지 미확정. 문구 전체의 페이드아웃으로 기록하지 않음.'])],text='Value of')
obj('logo','오른쪽 아래 TOVA 워드마크',[
 ev('3.4초에 작은 흰 사선 띠가 나타난 뒤 T, O, V, A가 왼쪽부터 시간차를 두고 같은 하단 경계에서 위로 올라와 조립된다. 4.0초에는 전체가 읽히지만 A의 하단은 아직 부드럽고 4.3초에는 단단한 흰색 외곽으로 정착한다.',['position','reveal','edge_softness'],[3.2,4.3],[f(3.2),c(3.4,'logo'),f(3.5),c(3.6,'logo'),f(3.7),c(3.8,'logo'),c(4.0,'logo'),c(4.3,'logo')],'T→O→V→A의 상향 등장, 서로 중첩',limitations=['같은 하단 부근에서 잘리는 리빌이 관측되지만 실제 AE 매트/레이어 설정은 알 수 없다.']),
 ev('4.3초 이후 워드마크의 외곽과 크기는 관측 표본에서 유지된다. 7.0~7.3초 지도 T가 뒤를 통과할 때에도 작은 로고는 밝고 선명하게 앞에 남는다.',['position','scale','occlusion'],[4.3,8],[c(4.3,'logo'),f(4.8),f(6.4),f(7),f(7.1),f(7.2),f(7.3),f(7.6),f(8)],'작은 로고 정착→지도 T가 뒤로 통과→작은 로고 유지','not_applicable','정착/앞뒤 관계 관측이며 진행 중 속도 분류의 대상이 아니다.')],text='TOVA',information_relation='Value of의 수식 대상이며 영문 약어 풀네임과 한국어 정의문이 바로 아래에 종속된다.')
obj('logo_t','워드마크 첫 글자 T',[
 ev('T의 흰 상단 모서리가 위로 올라오며 감속해 정착한다. 다른 글자의 수치가 아닌 T 자체의 흰 상단을 추적했다.',['position_y'],[3.4,4],[c(3.4,'logo'),f(3.5),c(3.6,'logo'),f(3.7),c(3.8,'logo'),c(4.0,'logo')],'상향→감속→정착','decelerate','0.1초 간격 T 상단 y가 1482,1388,1320,1293,1286px; 이동량 절댓값 94,68,27,7px로 감소한다. 4.0초에도1286px.',measurement={'samples_time_seconds':[3.4,3.5,3.6,3.7,3.8,4.0],'samples_y_native_pixels':[1482,1388,1320,1293,1286,1286],'roi_xyxy_native_pixels':[1930,1100,2230,1540],'method':'minRGB>200인 T 흰면의 최소 y, RGB 원본 추출 PNG','units':'원본 raster pixel, second','uncertainty':'블러·압축·문턱값에 따른 약2~8px. 하단의 리빌은 별도이며 상단 특징만 비교.','limits':'AE 속도/Influence나 정확한 보간 함수 복원 아님; 첫 가속구간은 미확인.'})],parent='logo')
obj('logo_o','워드마크 O',[
 ev('3.5초 낮은 흰 곡선 조각이 나타나고 3.6~3.8초 위로 올라와 열린 원형 외곽이 완성된다.',['position_y','reveal'],[3.5,4],[f(3.5),c(3.6,'logo'),f(3.7),c(3.8,'logo'),c(4.0,'logo')],'T보다 뒤에 시작해 위로 상승',limitations=['O 자체의 연속 위치 수치를 추적하지 않아 T의 감속 판정을 복사하지 않았다.'])],parent='logo')
obj('logo_v','워드마크 V',[
 ev('3.6초에는 낮은 세로 조각과 오른쪽 사선 조각으로 보이고 3.8초에는 V의 두 팔이 올라와 읽힌다. 4.0초에는 정착한 로고 일부로 남는다.',['position_y','reveal'],[3.5,4],[f(3.5),c(3.6,'logo'),f(3.7),c(3.8,'logo'),c(4.0,'logo')],'O와 겹치면서 그 뒤에 상향 등장',limitations=['V 자체의 위치 변화율과 정확한 시작 프레임은 미확정.'])],parent='logo')
obj('logo_a','워드마크 A',[
 ev('3.7초 우측에 낮은 흰 조각, 3.8초 부분 A가 보이고 4.0초에는 글자가 거의 올라와 하단의 부드러운 잔여 경계가 남는다. 4.3초에는 흰 A 전체가 정착한다.',['position_y','reveal','edge_softness'],[3.7,4.3],[f(3.7),c(3.8,'logo'),c(4.0,'logo'),c(4.3,'logo')],'네 글자 중 마지막으로 위로 올라와 정착',limitations=['A 자체의 변화율 미측정, 원본 키프레임 미제공.'])],parent='logo')
obj('logo_accents','O 안쪽과 A 오른쪽의 노란 사선 세 줄',[
 ev('O 안의 노란 사선은 3.6초 부분 노출되고 3.8초에는 세 줄이 선명하다. A 오른쪽 세 줄은 그보다 늦게 3.8초 하단에 옅은 조각으로 보이고 4.0~4.3초에는 선명한 노랑으로 완성된다. 이후 지도 T 앞에서도 유지된다.',['reveal','brightness','position_y'],[3.6,8],[c(3.6,'logo'),c(3.8,'logo'),c(4.0,'logo'),c(4.3,'logo'),f(6.4),f(7.2),f(8)],'O 안쪽 세 줄→A 오른쪽 세 줄, 각 글자 등장에 종속',limitations=['세 줄 개별 속도/광량 곡선과 독립 움직임 여부는 미확정. 장식선을 별도 데이터/커서로 해석하지 않는다.'])],parent='logo')
obj('tagline','영문 풀네임 TOtal Vehicle Assignment',[
 ev('4.3초 A 하단 우측에 끝 글자의 작은 일부가 나오고 4.4~4.6초에는 …nment→…icle Assignment→…otal Vehicle Assignment처럼 앞부분이 가려진 상태로 오른쪽으로 밀려 나온다. 4.7초 전체 문구가 읽히고 4.8~4.9초 정착한다. TO, V, A가 노란색이고 나머지는 흰색이다.',['position_x','reveal'],[4.3,5],[c(4.3,'logo'),f(4.4),c(4.5,'logo'),c(4.6,'logo'),c(4.7,'logo'),f(4.8),c(4.9,'logo')],'A 뒤쪽/하단 가림 경계에서 오른쪽으로 나옴; 보이는 문구는 뒤쪽 단어부터 전체로 확장','in_out','문구 오른쪽 끝 x가 4.3~4.8초에 2821,2918,3094,3220,3272,3284px. 0.1초 이동량97→176→126→52→12px로 관측된 진행 중 가속 후 감속.',measurement={'samples_time_seconds':[4.3,4.4,4.5,4.6,4.7,4.8,4.9],'samples_right_x_native_pixels':[2821,2918,3094,3220,3272,3284,3284],'roi_xyxy_native_pixels':[2810,1490,3330,1540],'method':'maxRGB>180인 영문 끝의 최대x. A의 고정 끝보다 오른쪽에 있는 마지막 t를 추적.','units':'원본 raster pixel, second','uncertainty':'약2~8px;4.3초는 아주 작은 잔여 획이라 더 불확실.','limits':'가려진 시작 전체 곡선은 불명; 보이는 구간의 가속-감속 성격만 판정.'}),
 ev('정착한 풀네임은 로고 오른쪽 아래에 붙어 한국어 설명보다 위에 남고 지도 진입 동안에도 유지된다.',['position','visibility'],[5,8],[f(6.4),f(7.1),f(7.3),f(8)],'풀네임 정착→국문 정의문 등장→지도 뒤 통과','not_applicable','유지 상태의 관측.')],parent='logo',text='TOtal Vehicle Assignment')
obj('definition','로고 아래 두 줄 한국어 정의문',[
 ev('5.4초 첫 줄 전체가 낮은 대비로 읽힌다. 이어 둘째 줄이 왼쪽부터 길어져 5.6초에는 분석하는 한국형, 5.8초에는 한국형 통합 교통 수 부근까지, 6.0초에는 프로그램까지 보이고 6.4초에는 입니다.까지 완성된다. 같은 동안 이미 보이는 첫 줄과 둘째 줄의 밝기도 증가한다.',['text_reveal','brightness'],[5.4,6.4],[c(5.4,'detail'),c(5.6,'detail'),c(5.8,'detail'),c(6.0,'detail'),c(6.4,'detail')],'첫 줄 노출→둘째 줄 왼쪽→오른쪽 순차 노출, 밝아짐과 중첩',limitations=['첫 줄 시작/개별 글자 경계는5.4초보다 앞의 세밀 표본으로 검증하지 않았다. 타입라이터 구현/알파 순차 방식은 미확정. 밝기 곡선과 리빌 속도 수치는 미측정.']),
 ev('완성문은 로고 아래 왼쪽 정렬 두 줄이다. 한국형 통합 교통 수요분석 프로그램만 굵은 노랑, 나머지는 연한 회백색이며 지도 T가 통과할 때도 로고와 함께 앞에 남는다.',['text','color','occlusion'],[6.4,8],[c(6.4,'detail'),f(6.4),f(7.1),f(7.2),f(7.3),f(8)],'다중 교통수단 열거→한국형 통합 분석 프로그램 정의; 내용 교체 없이 유지','not_applicable','문구/정보 관계와 유지 상태의 관측.')],parent='logo',text_lines=['TOVA는 도로, 버스, 도시철도, 지역간 철도, 항공 및 해운 여객교통수요를 통합적으로','분석하는 한국형 통합 교통 수요분석 프로그램 입니다.'],information_relation='도로·버스·도시철도·지역간 철도·항공·해운의 여객교통수요를 통합 분석하는 프로그램이라는 정의. 영상에서 보이는 주장으로 기록하며 실제 기능 검증 아님.')
obj('map_t','화면을 크게 가로지르는 지도 질감 T',[
 ev('6.4초에는 없고 6.6초 오른쪽 위에 가는 흰 사선이 나타난다. 6.7~6.9초에는 흰 사선 면이 왼쪽으로 넓게 진입하며 7.0~7.1초 중앙 세로 기둥이 보여 큰 T 형태가 된다. 상부 가로획의 아래선 높이는 대체로 일정하고 T 전체가 왼쪽으로 이동해 7.6초 무렵 정착한다.',['position_x','visible_area'],[6.4,8],[f(6.4),f(6.6),f(6.7),f(6.8),f(6.9),f(7),f(7.1),f(7.2),f(7.3),f(7.4),f(7.6),f(8)],'화면 오른쪽→왼쪽, 처음 가속 후 감속하여 왼쪽 절반에 정착','in_out','y=700px에서 지도 T의 왼쪽 경계x:6.6~7.4초에3366,3226,2866,2246,1526,848,362,128,34. 0.1초 이동량140→360→620→720→678→486→234→94px. y=1000px 기둥 왼쪽 경계도7.0~7.6초2558→1876→1392→1154→1066→1038→1034px로 감속.',measurement={'samples_time_seconds':[6.6,6.7,6.8,6.9,7.0,7.1,7.2,7.3,7.4],'samples_left_x_at_y700_native_pixels':[3366,3226,2866,2246,1526,848,362,128,34],'method':'고정 원본 y=700 행에서 minRGB>130,채널차<12인 첫 픽셀. y=1000 기둥은 화면가장자리 클리핑을 피한 보조 추적. support/measurements.json 참조.','units':'원본 raster pixel, second','uncertainty':'약2~8px 및 블러/명암에 따른 경계 문턱값 오차. 진행 중 수백px 변화보다 작음.','limits':'정착 후 y700 경계는 화면 왼쪽에 근접해 클리핑 영향. 크기/내부 지도 변형 곡선과 분리하며 AE 정확 곡선 복원 아님.'}),
 ev('처음 흰 T 면 내부 지도 선은 거의 안 읽히는 흐림이다. 7.0~7.2초에는 흐린 도로망이 보이고 7.3초에는 촘촘한 회색 지도선이 선명해진다. 7.6초에는 지도선의 내용이 정착 T 내부에 남고 8초 문맥에서도 유지된다. T의 아래쪽은 어두운 명암 그라데이션을 띤다.',['internal_detail_sharpness','internal_content','brightness'],[6.8,8],[f(6.8),f(6.9),f(7),f(7.1),c(7.2,'overlap'),f(7.3),c(7.6,'overlap'),f(8)],'바깥 T의 좌향 이동과 동시에 내부 지도 흐림→선명',limitations=['원본 효과의 blur 반경·초점·내부 지도 자체의 독립 줌/이동은 미확정. 지도 지역명/수치/교통 결과 UI는 판독하지 못했다. 외곽이 정착했다고 내부 모든 픽셀이 정지한다고 확정하지 않는다.']),
 ev('큰 지도 T는 Value of의 오른쪽을 덮지만 작은 TOVA 로고·영문 풀네임·정의문 뒤로 지나간다. 7.2초의 겹침에서는 옅은 큰 문구가 지도에 비쳐 보이고 7.3초에는 지도 쪽이 우세해진다. 8초 경계에서도 왼쪽 문구 잔존, 큰 지도 T, 오른쪽 작은 로고와 정의문이 공존한다.',['occlusion','layer_relation'],[7.1,8],[f(7.1),f(7.2),f(7.3),f(7.6),f(8)],'배경/큰 문구보다 앞, 작은 로고/설명보다 뒤에 놓인 겹침','not_applicable','앞뒤 관계의 관측이며 별도의 위치 속도 분류 아님.')])
common=[B/'trial-instructions.md',B/'common-task.md',B/'common-output-format.md',B/'trial_tools.py',B/'boards.py',B/'common-tools/check_observations.py',R/'input.json']
skill=B/'candidate/company-video-grammar-analyzer';common += [skill/'SKILL.md']+list((skill/'references').glob('*.md'))
logs=[B/'cases/A5-T/H01/실행기록.json',B/'cases/A5-T/H01-r2-with_skill-extra1/실행기록.json',B/'cases/A5-T/H01-r2-with_skill-extra2/실행기록.json']
boards=[l.parent/f'board-{n}.jpg' for l in logs for n in [1,2]]
base_read={str(Path(e.get('parent_path',e['path']))) for e in E}
programmatic_png=sorted(base_read | {f['path'] for f in rows if 'extra' in f['path']})
read_files=[str(p) for p in common+logs+boards]+programmatic_png+[c['path'] for c in crops]+[input_data['source_path'],str(S/'measurements.json')]
d={'schema_version':'a3-observation-0.1','case_id':'H01','source':{'path':input_data['source_path'],'sha256':input_data['sha256'],'verification':'원본 bytes 직접 SHA256 재계산; 기본/추가 두 추출 로그의 입력 전후 해시와 일치'},'window_seconds':[0,8],'method':'기본21개 표본의 보드2장으로 전후 흐름 탐색; 허용 추출기로추가1차24장/2차16장. 총 보드6장 탐색. 원본 PNG23장 직접 시각 열람, RGB native 무배율크롭28개 생성·전부 열람. 크롭 픽셀 좌표와 부모 PNG 매핑 보존. 선택 표본 비교와 T·풀네임·지도 T 경계의 native pixel 추적으로 관측. 연속 영상 재생/오디오 분석 없음. 8초는context_after.','document_mode':'none','audio_reviewed':False,'evidence':E,'objects':objects,'coverage':{'overview':'[0,8) 대상. 배경 형성→말린 Value of의 순차 펼침→밝기 약화와 TOVA의 글자별 상향 조립→영문 풀네임 우향 등장→국문 정의문 순차 노출→지도 T 좌향 진입/정착. 정착 상태에서 역추적해 보강했으며 정확한 프레임 단위 이벤트 경계는 표본 간 범위로만 기록.','secondary_details':'좌상단 청록 모서리, 띠의 수평 끝선, 부드러운 광택/그림자, 타이포의 어두운 말린 면과 밝은 가장자리, 로고 글자별 흐린 하단, O/A의 노란 세 줄, 영문 노란 약어 글자, 지도와 큰 제목의 일시 겹침 및 왼쪽 문구 잔존을 검사.','internal_content':'이 구간은 브랜딩 타이틀/프로그램 정의이며 소프트웨어 창·버튼·선택 상태·커서·수치 그래프는 열람 표본에서 보이지 않는다. T 내부는 흐린 도로망에서 선명한 도로망으로 변한다. 국문 두 줄과 영문 풀네임 판독 완료; 도시/지도 지명과 실제 교통 데이터 값은 확인하지 않았다.','unresolved':['배경 띠의 실제 이동과 마스크/성장 구분, 정확한 방향 벡터/개별 가감속','Value of 말림의 3D축·형태 보간·밝기 곡선','O/V/A 및 노란 장식선 각자의 속도곡선','국문 첫 줄의 정확한 최초 시작, 순차 리빌과 밝기 증가의 구현 분리','지도 내부 독립 줌/이동 여부와 흐림 효과 설정','8초 이후의 완결/퇴장 상태는 범위 밖']},'hypotheses':[],'limitations':['음성·싱크 미검수. 제작 문서 없음, 정상 무문서 분석.','선택 프레임 관측이며 연속 재생/모든 프레임 검수가 아니다. 보드는 탐색용이고 직접 근거는 열람한 PNG/무배율 크롭에만 연결.','추출 로그의 playback mapping/PTS 일치와 원본 해시는 확인. SAR 미상·RGB 변환 색범위 정확성 미검증을 유지하며 색을 공식 CI/AE 값으로 환산하지 않음.','이징 분류는 렌더 관측량의 변화율 성격이며 AE키프레임·정확한 함수·Influence를 복원하지 않음.','회사 공통 문법·승인·제작 의도·실제 소프트웨어 기능/조작으로 확대하지 않음. 8초 경계는 이후 문맥이며 영상 전체 최종 상태를 뜻하지 않음.'],'files_read':sorted(set(read_files)),'measurement_support_path':str(S/'measurements.json'),'review_record':{'claim_evidence_reverse_check':'각 대상의 현재 특징이 해당 ROI에 포함되는지, T 수치를 O/V/A에 복사하지 않았는지, 제목 가림을 이동으로 쓰지 않았는지 저장 전 역대조 완료.','source_time_connection':'원본 해시 직접 재계산, 로그 actual_playback_seconds 사용. 요청시각과 actual이 이번 표본에서는 일치.','human_intervention':'none','ai_model':'parent inherited exact host ID unavailable','source_raster':[3840,2160]}}
(O/'observations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
md='''# H01 · 0–8초 관측 초안

원본: `01_(T).mp4`, SHA256 `ac83de770d91d1ce9d484e7f74c7b4c3b579db9b68c1e6b5775a3ec2e543de5c` 직접 재확인. 문서 없음, 음성 미검수. 8초는 분석 창 이후 문맥이다.

- **0–1.2초:** 남색 바탕 위 상부 파랑 띠의 수평 끝은 아래로, 하부 청록 띠의 시작은 위로 진행해 사선 배경이 채워진다. 좌상단 청록 모서리도 시작보다 아래에 정착한다. 실제 레이어 이동과 리빌 방식은 미확정.
- **1.2–3.5초:** 왼쪽 아래 작은 획에서 `Value of`가 왼쪽부터 말림을 펴며 만들어진다. 1.8초 V/다음 글자의 어두운 휘어진 면, 2.2초 Val, 2.6초 Value, 3.0초 전체 정면 문구가 읽힌다. 위로 말린 어두운 조각은 3.2초에도 남지만 3.5초에는 보이지 않는다.
- **3.2–4.8초:** 큰 `Value of`는 위치를 유지하며 회청색으로 약해진다. 완전 소실은 아니다. 동시에 오른쪽 아래 TOVA가 T→O→V→A 순서로 같은 하단 경계에서 위로 올라와 조립된다. T의 상단 y는 3.4/3.5/3.6/3.7/3.8초에 1482/1388/1320/1293/1286px로, 이동량이94→68→27→7px로 줄어 **상향 감속**한다. O/V/A의 곡선은 별도로 미확정이다.
- **3.6–4.3초:** O 내부 노란 세 줄이 먼저, A 오른쪽 노란 세 줄이 나중에 노출된다. A 하단의 흐린 잔여 경계까지 사라진 4.3초에는 흰 워드마크가 정착한다.
- **4.3–4.9초:** 영문 `TOtal Vehicle Assignment`가 A 뒤/아래에서 **오른쪽으로** 밀려 나온다. 처음에는 끝 글자와 뒷단어만 보이고 4.7초 전체가 읽힌다. 끝 x 이동량97→176→126→52→12px/0.1초로 관측된 구간은 가속 후 감속 성격이다. TO/V/A가 노랑이다.
- **5.4–6.4초:** 첫 줄이 옅게 읽힌 뒤 둘째 줄이 왼쪽부터 길어지고 전체 밝기도 증가한다. 5.6초 `분석하는 한국형`, 5.8초 `…통합 교통 수`, 6.0초 `…프로그램`, 6.4초 `…입니다.`까지 완성된다. 정의문은 다음 두 줄이며 핵심구절은 굵은 노랑이다.

  TOVA는 도로, 버스, 도시철도, 지역간 철도, 항공 및 해운 여객교통수요를 통합적으로  
  분석하는 **한국형 통합 교통 수요분석 프로그램** 입니다.

- **6.4–8초:** 6.6초 오른쪽 위 가는 흰 사선에서 큰 지도 T가 진입한다. T는 오른쪽→왼쪽으로 움직이며 중간에 빨라졌다가 정착 전 느려진다. y700에서 0.1초 이동량140→360→620→720→678→486→234→94px, 기둥 경계는7.6초 무렵 정착한다. 내부는 흐린 지도에서7.3초 선명한 도로망으로 바뀐다. 큰 T는 `Value of` 오른쪽을 덮고, 작은 TOVA·풀네임·정의문 뒤를 지난다. 7.2초에는 큰 문구의 옅은 형상이 지도와 겹치지만 7.3초 이후 오른쪽 글자가 가려진다. 8초에도 왼쪽 `Valu` 부근은 남는다.

보드6장 탐색, 원본PNG23장 직접 열람, native RGB크롭28개 열람, 추가추출40장(24+16)을 사용했다. 근거 PNG/크롭·실제 표시시각·native좌표는 JSON에 연결했으며 측정 원자료는 `support/measurements.json`에 있다. 소프트웨어 UI 조작/커서/수치 그래프는 검사 표본에서 관측되지 않았다.

남은 불확실성: 배경의 이동/리빌 구현, 말림의 정확한3D축과 곡선, O/V/A별 가감속, 국문 첫 줄의 최초 시작과 밝기/리빌 분리, 지도 내부의 독립 줌/이동. 이징 수치는 RGB 경계의 렌더 관측이며 AE키프레임 복원은 아니다. 8초 이후는 조사하지 않았다.
'''
(O/'observations.md').write_text(md,encoding='utf-8')
(S/'read-files.json').write_text(json.dumps({'files_read':d['files_read'],'direct_png_visual_paths':[bytime[t]['path'] for t in direct],'crops_visual_paths':[x['path'] for x in crops],'programmatic_png_paths':programmatic_png},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'objects':len(objects),'events':sum(len(x['events']) for x in objects),'evidence':len(E),'direct_png':len(direct),'crops':len(crops),'programmatic_png':len(programmatic_png)},ensure_ascii=False))
