from pathlib import Path
from fractions import Fraction
import json,hashlib,datetime
B=Path.cwd()/'phase01a-a5b'; R=B/'trials/H01-r1-without_skill'; S=R/'support'; O=R/'outputs'; O.mkdir(exist_ok=True)
inp=R/'input.json'; c=json.loads(inp.read_text(encoding='utf-8-sig'))
logpaths=[Path(c['input_log']),B/'cases/A5-T/H01-r1-without_skill-extra1/실행기록.json',B/'cases/A5-T/H01-r1-without_skill-extra2/실행기록.json']
logs=[json.loads(p.read_text(encoding='utf-8')) for p in logpaths]
allrows=[r for d in logs for r in d['frames']]; lookup={r['path']:r for r in allrows}
crops=json.loads((S/'crops.json').read_text(encoding='utf-8'))
ev=[]; times={}; cropids={}
for k,d in enumerate(logs[:2]):
 for r in d['frames']:
  t=r['actual_playback_seconds']; eid=('b' if k==0 else 'a')+str(r['display_ordinal_zero_based'])
  ev.append({'id':eid,'path':r['path'],'actual_seconds':t,'role':'context_after' if Fraction(t)==8 else 'within'})
  times[Fraction(t)]=eid
for i,cr in enumerate(crops):
 r=lookup[cr['parent_path']]; eid='c'+str(i+1)
 ev.append({'id':eid,'path':cr['path'],'actual_seconds':r['actual_playback_seconds'],'role':'within'})
 cropids[Path(cr['path']).stem]=eid
def ids(*ts):return [times[Fraction(str(t))] for t in ts]
def cr(*names):return [cropids[n] for n in names]
def event(desc,props,t,evs,direction,classification='unknown',basis='선택 정지 프레임으로 방향과 순서는 확인되나 속도 곡선은 산출하지 않음.',status='observed',limits=None):
 return {'description':desc,'properties':props,'time_seconds':t,'evidence_ids':evs,'direction_order':direction,'easing':{'property':props[0],'classification':classification,'basis':basis},'status':status,'limitations':limits or []}
objects=[]
objects.append({'id':'background','name':'남색·청록 사선 띠와 부드러운 명암 배경','parent':None,'events':[
event('0초에는 어두운 남색 바탕, 왼쪽 위 청록 조각, 오른쪽 아래 사선 경계가 보인다. 0.1–0.4초 위쪽 짙은 파랑 영역은 아래쪽으로 넓어지고 아래쪽 청록 영역의 윗경계는 위로 올라온다. 0.5–0.8초 청록 영역이 위쪽까지 채워지며 좌하→우상으로 기울어진 넓은 띠 배열이 완성된다. 오른쪽 위 밝은 원형 번짐과 하단의 어두운 명암이 남는다.',['visible_boundary_position','appearance'],[0,1],ids(0,.1,.2,.3,.4,.5,.6,.7,.8,1),'위쪽 영역 하향 확장과 아래쪽 영역 상향 확장 후 사선 배경 유지','unknown','등간격 표본에서 경계 이동 변화가 보이나 서로 다른 띠/가림 경계가 겹쳐 한 객체의 속도로 확정하지 않음.',limits=['실제 레이어 이동과 마스크 확장 구분 불가.']),
event('1초 이후 제목·로고가 나타나는 동안 주요 사선 배경 배치는 유지된다. 6.5초 이후 오른쪽 사선 경계 쪽에서 흰 지도 영역이 끼어든다.',['appearance'],[1,7.6],ids(1,3.2,4.8,6.4,6.6,7.2,7.6),'배경 유지 → 지도 T 추가','not_applicable','배경 배치 유지와 새 전경 추가에 관한 관측.') ]})
objects.append({'id':'value','name':'대형 문구 Value of','parent':None,'events':[
event('1초에는 문구가 없고 1.2초에는 좌하단 작은 밝은 선 조각이 있다. 1.4–1.8초 V 부근이 가늘게 말린 형태로 커지고, 2초 Va, 2.4초 Valu, 2.6초 Value와 다음 글자 일부, 2.8초 Value of의 대부분, 3.2초에는 정방향 Value of가 완성되어 읽힌다. 2.0–3.2초 진행 경계 위쪽에 어두운 글자가 세로로 비틀리고 휘어진 모습이 함께 나타나며 경계는 왼쪽에서 오른쪽으로 진행한다. 완성된 흰 글자의 기준 위치는 좌측 하부에 유지된다.',['shape','visible_content','position'],[1,3.4],ids(1,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8,3,3.2,3.4)+cr('curl_1.6','curl_2.4','curl_2.8'),'V 쪽 → Value → of; 말린/뒤집힌 외형이 오른쪽으로 지나가며 정방향 글자가 남음','unknown','복합 형태·밝기·가림 변화라 좌표 하나로 속도나 회전축을 확인하지 못함.',limits=['페이지 말림과 유사한 외형은 관측되지만 사용 효과, 실제 3D, 회전축은 미상.']),
event('3.2–3.4초의 밝은 Value of는 3.6초에 어두워지기 시작하고 4초에는 회색으로 낮아져 흰 TOVA 로고보다 약한 대비가 된다. 이후 같은 위치를 유지하며, 7.2초 지도 T의 세로획이 of 위를 겹쳐 가리고 7.4–7.6초에는 왼쪽 Valu 정도만 노출된다.',['appearance','occlusion'],[3.2,7.6],ids(3.2,3.4,3.6,3.8,4,6.4,7,7.2,7.4,7.6),'밝은 흰색 → 낮은 대비 회색 → 지도 T에 부분 가림','unknown','밝기 감소와 중첩은 확인. 불투명도/색상 중 어떤 제어인지와 시간 함수는 미상.') ]})
objects.append({'id':'logo','name':'TOVA 로고','parent':None,'events':[
event('3.2초에는 로고가 없고 3.4초에 오른쪽 영역 하단 기준선 부근에 흰 가로 조각이 보인다. 3.6초 T와 O 일부, 3.8초 T/O/V 및 A 일부, 4초 TOVA가 읽히며 4.2초에는 모양이 정돈된다. 각 글자가 같은 수평 하단선 부근에서 위로 솟고 T→O→V→A 순서로 올라와 완성된다. 흰 기하학적 영문과 O 내부 노란 사선 2개, A 오른쪽 노란 사선 3개가 보인다.',['position','visible_content'],[3.2,4.2],ids(3.2,3.4,3.6,3.8,4,4.2),'아래 기준선에서 위로, 글자 진행은 왼쪽 T부터 오른쪽 A','decelerate','3.6→3.8→4.0→4.2에서 글자별 남은 상향 이동이 줄며 정지하는 모습. 정량 좌표/동일 위상은 미측정이므로 정성 분류.',limits=['글자별 시작·종료 프레임과 원본 키프레임 수치는 미상.']),
event('4.2초 이후 로고는 화면 오른쪽 아래 절반에서 같은 크기와 위치를 유지한다. 지도 T가 들어오는 7.0–7.6초에도 로고가 지도 앞쪽에서 읽힌다.',['position','occlusion'],[4.2,7.6],ids(4.2,4.8,6.4,7,7.2,7.4,7.6),'로고 고정; 지도보다 앞','not_applicable','선택 프레임 간 기준 위치 유지 관측.') ]})
objects.append({'id':'expansion','name':'로고 오른쪽 작은 영문 TOtal Vehicle Assignment','parent':'logo','events':[
event('4.2초에는 영문이 없고 4.3초 A 오른쪽 아래에서 마지막 t 일부가 나온다. 4.4초 nment, 4.5초 icle Assignment, 4.6초 Otal Vehicle Assignment, 4.8초 TOtal Vehicle Assignment 전체가 보인다. 글자 자체는 오른쪽으로 이동하며 A 뒤에 가려져 있던 앞부분까지 차례로 노출된다. 완성 뒤 같은 위치를 유지한다. TO, V, A가 노란색이며 나머지는 흰색이다.',['position','occlusion','visible_content'],[4.2,5.2],ids(4.2,4.3,4.4,4.5,4.6,4.8,5.2)+cr('subtitle_4.3','subtitle_4.4','subtitle_4.5','subtitle_4.6','subtitle_4.8'),'A 뒤 → 오른쪽, 어미가 먼저 노출되고 전체 영문이 완성','in_out','4.3→4.4의 작은 우향 이동보다 4.4→4.5 이동이 크고, 4.6→4.8에는 남은 이동이 작아진다. native 크롭 시각 비교에 기반한 정성 분류.',limits=['정확한 좌표·이징 함수는 미측정.']) ]})
objects.append({'id':'body','name':'로고 아래 한국어 설명문 두 줄','parent':'logo','events':[
event('5.2초 첫 줄 대부분이 희미하게 보이기 시작하고 5.4초에 더 길고 뚜렷해진다. 5.6초 둘째 줄 분석하는 한국형까지, 5.8초 한국형 통합 교통 수까지, 6초 노란 프로그램까지, 6.2초 입니다.까지 완성된다. 6.4초에는 더 밝고 선명하게 읽힌다. 기준 위치가 움직이기보다는 읽을 수 있는 범위가 첫 줄→둘째 줄 및 좌→우로 늘고 대비가 높아진다. 완성 문구: TOVA는 도로, 버스, 도시철도, 지역간 철도, 항공 및 해운 여객교통수요를 통합적으로 / 분석하는 한국형 통합 교통 수요분석 프로그램 입니다. 한국형 통합 교통 수요분석 프로그램은 노란 굵은 글씨, 나머지는 밝은 회색이다.',['visible_content','appearance'],[4.8,6.4],ids(4.8,5.2,5.4,5.6,5.8,6,6.2,6.4)+cr('body_5.2','body_5.6','body_6','body_6.4'),'첫 줄 왼쪽부터 → 둘째 줄 왼쪽부터 → 마지막 입니다.; 대비 증가','unknown','문자별 등장 범위와 대비 변화가 겹쳐 불투명도/가림 속도는 분리 측정하지 못함.'),
event('설명문은 TOVA의 의미를 밝히는 하위 정보다. 열거된 교통수단을 통합 분석한다는 문장과 노란색 한국형 통합 교통 수요분석 프로그램이 같은 설명에 속한다. 6.4초 이후 지도 진입 중에도 문구는 로고 아래에서 유지된다. 수치, 버튼, 표, 메뉴, 조작 커서는 보이지 않는다.',['visible_content'],[6.4,7.6],ids(6.4,7,7.2,7.4,7.6)+cr('body_6.4'),'로고 아래 두 줄 설명 유지','not_applicable','화면의 정보 관계 및 유지 상태 관측.') ]})
metrics=json.loads((S/'map-measurements.json').read_text(encoding='utf-8'))
map_ev=cr(*[Path(x['path']).stem for x in crops if Path(x['path']).stem.startswith('map_')])
me=event('6.5초까지 지도 T가 보이지 않고 6.567초 오른쪽 위 사선 경계 부근에서 얇은 흰 영역이 시작된다. 6.667–6.9초 흰 사선 영역이 왼쪽으로 빠르게 커지고, 6.967–7.167초 넓은 윗가로획과 아래로 뻗는 세로획이 들어와 큰 T형임이 드러난다. 7.267–7.567초 남은 좌향 이동이 줄며 왼쪽 중앙에 멈춘다. 윗가로획 하단의 높이는 거의 일정하고 세로획의 좌측 경계가 왼쪽으로 움직인다. 오른쪽 노출 경계는 기존 배경 사선과 맞물린다.',['visible_boundary_position','occlusion'],[6.5,7.667],map_ev+ids(6.4,6.6,6.8,7,7.2,7.4,7.6),'오른쪽 사선에서 진입 → 수평으로 왼쪽 진행 → 감속·정지','in_out','native RGB 경계 좌표: y=800에서 6.567/6.667/6.767/6.867초 x=3300/3208/2935/2391로 0.1초당 이동량 92/273/544px(증가). y=1000에서 6.967/7.067/7.167/7.267/7.367/7.467/7.567/7.667초 x=2802/2088/1525/1211/1085/1043/1032/1032로 0.1초당 714/563/314/126/42/11/0px(감소).',limits=['가시 경계를 측정한 것이며 실제 AE position, 레이어 부모 관계, 마스크 방식은 확정 불가.','화면 왼쪽으로 잘린 y=800 경계는 7.367초 이후 속도 측정에 사용하지 않음.'])
me['easing']['measurements']={'method':'PNG native RGB 고정 y행에서 min(R,G,B)>140인 첫 x. 각 행은 제목/로고가 없는 높이. 실제 시각은 로그의 rational 초 사용.','units':{'time':'seconds','position':'native RGB pixel','delta':'pixels per 0.1 second (equal interval samples)'},'samples':metrics['rows'],'error':'정수 경계 및 안티앨리어싱/지도 선 때문에 1~수 px 오차 가능; 오차 분포 미측정. PTS는 1/30초 격자. SAR 미상.','limitations':'같은 추적 속성에서 전·후반 별도 행 사용; 절대 AE 좌표나 이징 파라미터가 아님.'}
objects.append({'id':'mapT','name':'회색 도로 지도가 채워진 거대한 T형 그래픽','parent':None,'events':[me,
event('지도 T 내부는 흰 바탕의 가는 회색 도로망과 블록, 원형·방사형 연결선으로 구성된다. 진입 초반 6.8–7.1초에는 지도 무늬가 흐리고 7.2초에 도로망이 구분되며 7.3초 이후 가는 선이 선명해진다. T 세로획 하단은 어두워지는 명암이다. 별도 UI 패널이나 수치 데이터는 없다.',['appearance','visible_content'],[6.8,7.667],ids(6.8,7,7.2,7.4,7.6)+cr('map_106_15','map_43_6','map_109_15','map_73_10','map_23_3'),'흐린 지도 → 선명한 도로망','unknown','선명도 변화는 직접 확인하였으나 블러 수치와 변화 함수는 미상.',limits=['지도 지명·도시 실명은 판독·식별하지 못함. 축척이나 실지역이라고 단정하지 않음.']),
event('지도 T가 왼쪽 Value of의 일부를 가리는 동안 오른쪽 TOVA 로고·영문 확장명·한국어 설명은 T 위에서 유지된다. 지도 T는 7.567–7.667초 표본에서 위치가 같고 7.6초 전체 화면에서도 자리를 잡은 상태다. 8초 문맥 프레임도 유사하지만 8초는 분석 구간 밖이다.',['occlusion','position'],[7,7.667],ids(7,7.2,7.4,7.6,8)+cr('map_227_30','map_23_3'),'배경 → Value of → 지도 T → TOVA/하위 설명의 중첩 관계','not_applicable','중첩과 정지 상태에 관한 관측. 8초는 context_after로만 참조.') ]})
files=[str(B/n) for n in ['trial-instructions.md','common-task.md','common-output-format.md','trial_tools.py']]+[str(inp)]+[str(p) for p in logpaths]
files += [str(B/'cases/A5-T/H01'/n) for n in ['board-1.jpg','board-2.jpg']]
files += [r['path'] for r in allrows]
files += [x['path'] for x in crops]
files += [str(S/n) for n in ['extra-request-1.json','extra-request-2.json','crops.json','map-measurements.json','analyze_evidence.py','write_output.py']]
files += [c['source_path']]
obs={'schema_version':'a3-observation-0.1','case_id':'H01','source':{'path':c['source_path'],'sha256':hashlib.sha256(Path(c['source_path']).read_bytes()).hexdigest()},'window_seconds':[0,8],
'method':'무문서 관측. 기본 0.4초 간격 PNG 21장(8초는 문맥 프레임), 기본 탐색 보드 2장, 공통 extra 도구 2회 24+18장. 기본 21장과 extra1 24장은 전체 프레임 직접 열람, extra2 18장은 native RGB 무배율 크롭으로 열람. 문구/말림/지도 관찰에 총30개 native RGB 크롭. 지도 경계 픽셀 추적은 support/map-measurements.json. 원본은 해시 확인만 수행했으며 추가 디코더나 음성 사용 없음.','document_mode':'none','audio_reviewed':False,'evidence':ev,'objects':objects,
'coverage':{'overview':'[0,8) 전체 구성을 표본으로 관측. 배경 형성→Value of 말림 펼침→TOVA 글자별 상승→영문 우향 등장→한글 2줄 점진 등장→지도 T 좌향 진입과 정착.','secondary_details':'Value of 대비 감소, 로고 노란 사선, 영문 TO/V/A 노란색, 한국어 노란 강조, 지도와 제목/로고의 앞뒤 관계 확인.','internal_content':'로고 아래 영문·한국어 텍스트, 지도 내부 도로망과 흐림 해소 확인. 소프트웨어 내부 UI/메뉴/데이터 조작은 이 구간에 관측되지 않음.','unresolved':['정확한 폰트명·효과명·키프레임·이징 함수 값','지도 도시/지명 및 실제 축척','제목 말림의 정확한 회전축과 마스크 구성','각 문자 최초 가시 프레임·최종 정착 프레임은 표본 사이 범위로만 앎']},
'hypotheses':[],
'limitations':['원본 AE 프로젝트·문서는 제공되지 않았다. 렌더 결과의 형태와 가시 경계를 기술하며 구현 방식은 확정하지 않는다.','모든 초는 추출 로그 actual_playback_seconds와 연결했다. 요청시각 6.55 등 일부는 다음 30fps 프레임으로 선택되므로 실제값 197/30 등을 사용했다.','8초 PNG는 context_after이며 [0,8)의 사건으로 계산하지 않는다.','전체 PNG의 도구 표시가 2048×1152로 줄어든 경우가 있어 작은 글자는 native RGB 크롭으로 확인했다. 표시 내부 추가 리사이즈 여부는 미상.','기본 로그의 RGB 범위 정확도 미검증·SAR 미상 제약을 유지한다. 색은 정성 묘사, 위치 수치는 native 래스터 좌표다.','소스 해시는 직접 읽어 입력·기본 로그 전후 해시와 일치 확인했다. PNG/크롭 연결은 finish 공통 검증에 맡긴다.','음성·0–8초 밖 구간·다른 trial·기준답안·기존 스킬은 열람하지 않았다.'],'files_read':list(dict.fromkeys(files))}
(O/'observations.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2),encoding='utf-8')
md='''# H01 · 0–8초 관측 (무문서)

- 0–0.8초: 남색·청록 영역이 위/아래에서 넓어져 좌하→우상 사선 띠 배경을 형성한다. 1초에는 배경이 완성되어 있다.
- 1.2–3.4초: 좌측 하부에서 **Value of**가 왼쪽부터 말리듯 펼쳐진다. 2초 Va, 2.4초 Valu, 2.8초 Value of 대부분, 3.2초 정방향 문구가 완성된다. 경계 위의 어두운 글자가 세로로 비틀려 올라간 모양도 보인다. 3.6–4초 문구는 회색으로 어두워진다.
- 3.4–4.2초: 오른쪽의 **TOVA**가 아래 기준선에서 T→O→V→A 순서로 올라와 멈춘다. O 내부 노란 사선 2개와 A 오른쪽 노란 사선 3개가 보인다.
- 4.3–4.8초: **TOtal Vehicle Assignment**가 A 뒤에서 오른쪽으로 나온다. 4.3초 마지막 t부터, 4.4초 nment, 4.5초 icle Assignment, 4.8초 전체가 노출된다. TO/V/A는 노란색이다. 후반 이동량이 줄며 멈춘다.
- 5.2–6.4초: 로고 아래 한글 설명이 첫 줄→둘째 줄, 좌→우 순서로 점차 나타나고 밝아진다. “TOVA는 도로, 버스, 도시철도, 지역간 철도, 항공 및 해운 여객교통수요를 통합적으로 / 분석하는 **한국형 통합 교통 수요분석 프로그램** 입니다.” 굵은 표시 부분은 화면에서 노란색이다. 6.2초 전체 문장이 있고 6.4초 더 선명하다.
- 6.567–7.667초: 오른쪽 사선에서 **지도 무늬의 큰 T**가 왼쪽으로 들어와 정착한다. y=800 경계 x는 6.567/6.667/6.767/6.867초에 3300/3208/2935/2391px로 가속하고, y=1000 세로획 경계는 6.967/7.067/7.167/7.267초에 2802/2088/1525/1211px로 이동량이 감소한다. 7.567/7.667초는 1032px로 같다. 이 관측은 가속 후 감속을 지지하며 AE 함수는 미상이다.
- 지도는 6.8–7.1초 흐리다가 7.2–7.3초 선명한 회색 도로망으로 바뀐다. T는 Value of 일부를 가리지만 TOVA와 하위 설명은 앞에서 유지된다. 지도 내부 UI·버튼·수치 표시는 관측되지 않는다.

근거는 observations.json의 기본 PNG 21장·보강 전체 PNG 24장·native RGB 크롭 30개에 연결했다. 추가 추출은 2회 42장이고 원본 SHA-256은 입력과 일치한다. 8초는 구간 밖 문맥 프레임으로만 사용했다.

미해결: AE 레이어/마스크/말림 효과와 정확한 키프레임·이징 수치, 폰트명, 지도 지역명·축척, 표본 사이의 정확한 등장 경계. 문서와 음성은 범위에 없다.
'''
(O/'observations.md').write_text(md,encoding='utf-8')
(S/'files-read.json').write_text(json.dumps(obs['files_read'],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(O),'evidence_count':len(ev),'objects':len(objects),'sha256':obs['source']['sha256']},ensure_ascii=False))
