from pathlib import Path
import json
from fractions import Fraction
BASE=Path(r'C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
IN=BASE/'analysis_input';OUT=BASE/'runs/retest_b'
A=IN/'cases/자료013/T02';B=IN/'cases/자료005/T05';E=OUT/'cases/자료005/extra1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
audit=read(OUT/'exploration_files_read.json')
track=read(OUT/'tracking_measurements.json')
clean=read(OUT/'clean_measurements.json')
last=read(OUT/'final_measurement_evidence.json')
metric=read(OUT/'exploration_metrics.json')
def ev(folder,name,t,description):return {'path':str(folder/name),'playback_seconds':t,'description':description}
def ea(t,description):
 f=min(read(A/'실행기록.json')['frames'],key=lambda f:abs(float(Fraction(f['actual_playback_seconds']))-t))
 return {'path':f['path'],'playback_seconds':float(Fraction(f['actual_playback_seconds'])),'description':description}
def eb(t,description,native=True):
 folder=E if native else B
 f=min(read(folder/'실행기록.json')['frames'],key=lambda f:abs(float(Fraction(f['actual_playback_seconds']))-t))
 return {'path':f['path'],'playback_seconds':float(Fraction(f['actual_playback_seconds'])),'description':description,'derived_size':f['derived_size']}
common={
 'analysis_stage':'A2 baseline first pass; no grading feedback received',
 'procedure':'Generic neutral observation procedure; no new skill used',
 'coordinate_convention':'Source raster coordinates: x rightward, y downward; coordinates are approximate visual/measurement proxies, not display-aspect claims.',
 'separation':{'observable':'Rendered appearance and pixel/frame comparisons only.','implementation_hypotheses':'No AE layer structure, keyframes, presets, handle values or exact easing curve are identified from the render.'},
 'tools_used':[
  {'tool':'functions.exec / exec_command','usage':'Read only PROCEDURE.md, cases.json and assigned case logs/board lists; enumerate assigned folders and own run output; run bundled Python with -B -X utf8.'},
  {'tool':'functions.exec / view_image','usage':'View assigned overview boards, selected original PNGs, and own derived crops; some host views were resized, so native crops were also inspected.'},
  {'tool':'functions.exec / apply_patch','usage':'Create local exploratory/measurement scripts and this one-time result writer within runs/retest_b.'},
  {'tool':'Python Pillow, NumPy','usage':'Read assigned PNGs, crop, raise crop brightness 2x for low-contrast T02 inspection, frame differences, grid period autocorrelation, edge/axis proxies and endpoint mix regression.'},
  {'tool':'inspect_more.py','usage':'One allowed request, T05 extra1, 10 times within 5.9–6.6, width 3840; generated source is not manually inspected and no outside-window images were requested.'},
  {'tool':'collaboration.send_message','usage':'Status report to the assigning parent agent only; no app thread messages or subagents.'}
 ],
 'technical_limits':[
  'Execution logs report unknown sample aspect ratio and unvalidated exact color range; spatial/color figures concern the decoded raw raster.',
  'No audio was listened to or transcribed; source audio metadata does not support sound-event claims.',
  'SciPy was unavailable on the first measurement attempt. A dependency-free NumPy replacement was used; noisy candidate peaks are exploratory and are not all accepted as object tracks.',
  'Image enhancement was for seeing low-contrast details only. All numeric color and motion proxies use unenhanced source PNGs.',
  'No hidden expected answers, other case media, prior analysis reports or grading files were read.'
 ],
 'source_access_audit':{
  'direct_shared_input_files':[str(IN/'PROCEDURE.md'),str(IN/'cases.json'),str(IN/'inspect_more.py')],
  'direct_assigned_media_and_log_files':sorted(set(audit+[str(A/'boards.json'),str(B/'boards.json')]+[str(A/f'board_{i}.jpg') for i in [1,2,3]]+[str(B/f'board_{i}.jpg') for i in [1,2]])),
  'own_artifacts_read':[str(OUT/n) for n in ['explore.py','measure.py','measure_v2.py','measure_clean.py','final_measurements.py','save_first_pass.py','exploration_files_read.json','exploration_metrics.json','tracking_measurements.json','clean_measurements.json','final_measurement_evidence.json']]+[str(OUT/'crops'/n) for n in ['T02_top_progress.jpg','T02_lower_progress.jpg','T02_axes_native.jpg','T02_grid_native.jpg','T05_title_progress.jpg','T05_card1_native.jpg','T05_card3_native.jpg']],
  'automated_helper_access_not_manual_report_reading':{
   'scope':'The provided inspect_more helper generated T05_extra1.py and decoded only the 10 requested times in the assigned T05 window.',
   'source_video':r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\00_26년 가족사 경영보고 영상\장헌\장헌_최종.mp4',
   'helper_references_visible_in_helper_source':[str(IN/'bounded_base.py'),str(BASE.parent/'phase01a-a2/prepare.py'),str(BASE.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'),str(BASE.parent/'phase01a-a1/후보런타임')],
   'note':'Runtime modules, codec and Python standard-library dependency reads are not expanded into individual library files. No contents of prior analysis/grading reports were returned to or manually read by the analyzer.'
  }
 }
}

t02={**common,'case_id':'T02','asset_id':'자료013','allowed_window_seconds':[0,1.4],
 'examined_time_window_seconds':[0,1.4],'sampling':{'supplied_count':29,'supplied_interval_seconds':.05,'native_raster':[3840,2160],'native_size_confirmed':True,'extra_timestamps':[]},
 'scene_summary':'검녹색 비네트 배경에서 반투명 직사각형, 얇은 선과 격자, 수평 광선, 좌상단의 적색·녹색 십자 표시가 차례로 드러난다. 이 구간에 읽을 수 있는 문구·인물·제품·별도 디스플레이 화면은 보이지 않는다.',
 'objects_events':[
 {'id':'background','subject':'전체 검녹색 배경과 중심 광량','window_seconds':[0,1.4],
  'observable':{'position':'화면 전체. 밝은 중심과 어두운 주변의 구조가 유지된다.','direction':'중심 광점의 명확한 이동은 식별하지 못함.','scale_shape':'중앙이 퍼진 타원형/방사형 명암, 가장자리 비네트.','visibility':'0초부터 전면 존재.','color_brightness':'중심 부근 RGB 중앙값은 0–0.95초 약 [21,70,54], 1.0–1.4초 약 [22,71,57]. 우하 귀퉁이 (3700,2100) 패치는 [2,21,14]에서 [1,3,3]으로 어두워져 완전한 정지색 배경으로 단정하지 않는다.','internal_changes':'후속 도형·격자가 위에 중첩된다. 배경 명암 변화와 전경 합성을 완전히 분리할 수 없다.','overlap':'모든 선·패널 뒤.','observable_acceleration':'추적 가능한 배경 위치 없음; 이동 가감속 비적용.'},
  'evidence':[ea(0,'중심 명암과 어두운 귀퉁이'),ea(.95,'격자 및 전경이 중첩된 상태'),ea(1.4,'귀퉁이는 더 어둡고 중심색은 거의 동일')],
  'uncertainty':'배경 자체 밝기 애니메이션인지 전경/비네트 합성의 영향인지 렌더만으로 미분리.'},
 {'id':'upper_translucent_panel','subject':'상단의 긴 어두운 반투명 직사각형','window_seconds':[.2,1.4],
  'observable':{'direction':'왼쪽 밖에서 오른쪽으로 보이는 범위와 우측 끝이 늘어난다. 후반에는 왼쪽 끝도 화면 안으로 들어온다.','position':'초기 좌상부에 희미한 일부가 보이고, 1.4초에는 대략 x365–2600, y70–505 부근의 긴 패널로 보인다.','scale_shape':'가로로 긴 직사각형을 유지. 전체 경계의 y 위치/보이는 높이도 변해 완전한 수평 강체 이동만으로 확정하지 않는다.','visibility':'0.2–0.3초 어둡게 식별되기 시작, 점차 대비 증가.','color_brightness':'검은색에 가까운 녹색, 내부로 격자가 비쳐 보인다.','internal_changes':'패널 내부에 독립 문구/영상 없음. 내부의 격자는 패널과 별도로 위치·간격이 변한다.','overlap':'상단 광선과 격자에 겹침.','observable_acceleration':'우측 진행은 후반에 완만해진다. 경계 후보 x 약2431(1.05),2537(1.2),2591(1.35)로 0.15초마다 약106→54px. 초반 어두운 경계는 자동 검출이 불안정해 정확한 전체 속도곡선은 보류.'},
  'evidence':[ea(.25,'왼쪽 상단에 패널 일부'),ea(.45,'우측 끝이 더 오른쪽으로 이동'),ea(1.05,'상단 패널 우측 경계'),ea(1.2,'후반 진행량 축소'),ea(1.4,'양 끝과 긴 형태 확인')],
  'uncertainty':'가시성 증가·화면 밖 잘림·주변 격자와의 중첩으로 초기 크기 및 수직 경로는 정밀 분리 불가. 우향 감속이라는 관측이 특정 프리셋의 증거는 아니다.'},
 {'id':'lower_bright_panel','subject':'하단 좌측에서 들어오는 큰 반투명 직사각형','window_seconds':[.25,1.4],
  'observable':{'direction':'좌측 밖에서 우향.','position':'0.3초 우측 끝 약447px, .45초1543, .6초1952, .75초2135, .9초2217, 1.05초2241. 1.2–1.4초에는 약2237→2234로 소폭 왼쪽.','scale_shape':'넓고 낮은 사각형. 하단/우측에 어두운 가는 테두리 또는 그림자가 따른다. 경계의 높이도 조금 바뀌며 보이는 폭은 처음 화면 밖 잘림의 영향을 받는다.','visibility':'초기 작고 흐린 일부에서 선명한 큰 패널로 변화.','color_brightness':'주변보다 밝은 녹색 반투명.','internal_changes':'격자가 비치고, 내부 별도 내용 교체는 보이지 않음.','overlap':'더 아래의 어두운 직사각형·광선과 겹치며, 격자와도 중첩.','observable_acceleration':'등시간 .15초 우측 끝 증가량 1096→409→183→82→24px로 감소. 후반 약7px 안쪽 이동도 보이므로 화면 좌표는 단순 등속이 아니다.'},
  'evidence':[ea(.3,'큰 패널의 일부가 좌측에 나타남'),ea(.45,'우향 큰 진행'),ea(.6,'우측 끝 약1952'),ea(.9,'우향 증가량 작아짐'),ea(1.05,'우측 끝 최대 부근'),ea(1.4,'후반 위치 유지/아주 작은 안쪽 이동')],
  'uncertainty':'후반 가장자리의 작은 후퇴는 위치 오버슈트일 수도 있고 크기 변화·상위 변환과 결합했을 수도 있다. 실제 오버슈트 키프레임/스프링은 구현 가설로만 남긴다.'},
 {'id':'middle_left_panels','subject':'좌중부의 작은 밝은 사각형과 길고 낮은 반투명 띠','window_seconds':[.45,1.4],
  'observable':{'direction':'작은 사각형은 좌측 밖에서 우향하여 .75초 우측 끝 약375, .9초583,1.05초688,1.2초746,1.35초775px. 아래의 낮은 띠도 좌측에서 오른쪽으로 드러난다.','scale_shape':'작은 사각형은 가로보다 세로가 약간 긴 부분이 보이다가 더 넓게 드러남. 띠는 매우 낮고 길다. 원래 폭과 스케일은 잘림 때문에 확정 불가.','visibility':'큰 하단 패널 뒤에 늦게 명확해진다.','color_brightness':'녹색 밝은 면과 밝은 얇은 하단 가장자리.','internal_changes':'내용/문구 없음; 격자와 밝은 띠가 내부로 비침.','overlap':'작은 사각형 아래쪽이 낮은 띠와 겹치는 영역에서 더 밝다.','observable_acceleration':'작은 사각형의 .15초 우향 변화량 약208→105→58→29px로 줄어 감속이 관측됨. 띠의 곡선은 별도 정량화하지 못함.'},
  'evidence':[ea(.45,'좌측 중하부의 낮은 띠'),ea(.75,'좌중부 작은 사각형'),ea(.9,'작은 사각형 우측 끝'),ea(1.2,'후반 진행량 감소'),ea(1.4,'작은 패널과 낮은 띠의 중첩')],
  'uncertainty':'띠의 독립 이동과 사각형 하단 밝기 효과는 일부 구간에서 겹쳐 분리하기 어렵다.'},
 {'id':'dark_lower_rectangle_and_strokes','subject':'더 아래의 어두운 직사각형/가는 검은 수평선','window_seconds':[.45,1.4],
  'observable':{'direction':'낮은 어두운 면과 수평선의 우측 끝이 초기보다 오른쪽으로 나타난다.','scale_shape':'밝은 큰 패널보다 아래로 내려앉은 어두운 직사각형이 부분적으로 겹친다. 가는 긴 수평선이 그 위/아래에 보이고 일부 우측 세로 테두리가 확인된다.','visibility':'밝은 큰 패널보다 낮은 대비. .6–.9초부터 더 뚜렷.','color_brightness':'거의 검은 녹색 선/면.','internal_changes':'패턴 변화 없이 다른 패널·격자·광선이 겹침.','overlap':'큰 밝은 패널 하단을 가로지르고 아래로 이어진다.','observable_acceleration':'전체적으로 진행이 완만해 보이지만 정확한 동일 경계 추적은 미확정, 별도 easing 분류 보류.'},
  'evidence':[ea(.6,'큰 패널 아래쪽의 낮은 어두운 면'),ea(.9,'긴 어두운 수평선과 우측 세로 경계'),ea(1.4,'최종 중첩 형태와 선')],
  'uncertainty':'선이 별도 그래픽인지 같은 패널의 외곽/그림자인지 구현 수준으로 분리할 수 없다.'},
 {'id':'grid_and_frame','subject':'화면을 넓게 덮는 격자 및 바깥 이중 테두리','window_seconds':[.15,1.4],
  'observable':{'direction':'격자가 드러나면서 우상단 모서리는 안쪽(좌하 방향)으로 이동하고 셀 간격은 줄어든다.','scale_shape':'가로·세로 직선 격자, 뒤틀림이나 회전은 확인되지 않음. 0.6→1.35초 우측 깨끗한 영역의 수평 주기 약120→107px로 작아져 실제 격자 축소가 관측된다.','position':'상단 격자선의 같은 밝은 띠는 y약264(.6),292(.75),312(.9),327(1.05),339(1.2),347(1.35).','visibility':'0.15–.3초 매우 희미한 선, .6초 선명해지고 1.4초까지 대비 증가.','color_brightness':'회녹색/청록색 얇은 선. 오른쪽·중앙이 더 잘 보이고 테두리 바깥은 어둡다.','internal_changes':'격자 셀 내용 변화는 없고 간격/전체 보이는 범위/밝기가 바뀐다.','overlap':'반투명 패널 내부에서도 보이며 패널마다 대비가 달라진다. 광선은 격자 위에 밝게 중첩.','observable_acceleration':'기간 후반의 간격 축소 및 상단선 아래 이동량이 줄어드는 경향. y 증가가 28→20→15→12→8px/.15초로 줄어, 정속 이동/축소는 아님.'},
  'evidence':[ea(.3,'희미한 격자'),ea(.6,'측정 가능한 격자 주기와 상단선'),ea(.9,'상단선 더 아래, 셀 간격 작아짐'),ea(1.35,'주기 약107, 상단선 y347'),ea(1.4,'이중 테두리와 격자 지속')],
  'uncertainty':'상단선·격자주기는 proxy이고 밝기/압축 영향으로 수 px 오차 가능. 정확한 스케일 중심·카메라 줌·레이어 부모는 알 수 없다. 초기 .6초 이전 자동 peak 후보는 잡음이 많아 채택하지 않았다.'},
 {'id':'horizontal_glints','subject':'상단·하단의 길고 부드러운 청록색 광선','window_seconds':[.3,1.4],
  'observable':{'direction':'상단 광선의 밝은 중심/띠가 좌측 부근에서 오른쪽으로 퍼지고 이동한다. 하단 광선도 뒤이어 좌측에서 우향하며, 가장 아래쪽/오른쪽에는 별도의 흐린 빛이 늦게 보인다.','position':'상단 약 y300 부근, 하단 약 y1800 부근. 마지막에는 아래쪽 우측에도 흐린 청록색 광점.','scale_shape':'가로로 길고 끝이 부드럽게 흐려지는 빛; 회전/날카로운 형태변화는 보이지 않음.','visibility':'상단 .3–.45초부터, 하단 .6–.7초부터 뚜렷. 아래 우측 빛은 .9–1.4초에서 확인.','color_brightness':'청록색 광량 증가 후 긴 잔광처럼 퍼짐.','internal_changes':'밝은 중심과 꼬리의 분포가 변화하므로 고정된 선의 단순 fade로만 설명하지 않는다.','overlap':'격자/패널을 가로지르는 밝은 띠.','observable_acceleration':'이동과 밝기분포/퍼짐이 동시에 변해 단일 중심점의 속도곡선은 신뢰성 있게 분리하지 못했다.'},
  'evidence':[ea(.3,'초기 상단 빛'),ea(.6,'상단 빛의 우향 분포와 하단 빛 출현'),ea(.9,'하단 광선이 길게 뻗음'),ea(1.4,'3개 높이대의 빛 분포 확인')],
  'uncertainty':'glow 폭 변화·노출과 위치 이동이 결합함. 정확한 광선 개수/효과 종류는 렌더에 기반한 시각적 묶음이다.'},
 {'id':'red_green_cross','subject':'좌상단 적색 수평축·녹색 수직축과 중앙의 작은 적색 사각형','window_seconds':[.85,1.4],
  'observable':{'direction':'늦게 희미하게 드러난 뒤 우하향.','position':'교점 proxy는 .95초(166,232),1.0(176,254),1.1(204,314),1.2(252,382),1.3(316,448),1.4(398,496).','scale_shape':'적색 가로선과 녹색 세로선은 서로 직각을 유지하며 최종 길이는 각 약600px. 초기 좌측/상단은 프레임 밖 잘림. 교점에 작은 속 빈 적색 정사각형이 뒤에 더 뚜렷해진다.','visibility':'녹색이 .9초에 분명히 검출되고 적색은 .95초 이후 분명. .85–.9초 부근은 아주 희미하여 첫 발현 프레임을 확정하지 않음.','color_brightness':'적색·녹색 선의 대비가 증가.','internal_changes':'작은 중심 사각형이 교점과 함께 이동. 선의 길이 증가처럼 보이는 초반은 잘림/광량으로 설명 가능하여 스케일 증가로 단정하지 않는다.','overlap':'격자와 패널 위에 놓여 보임.','observable_acceleration':'x는 등시간 .1초 변화량28→48→64→82px(1.0 이후)로 증가하므로 우향 성분 가속이 관측된다. y는60→68→66→48px로 중간에 가장 빠르고 마지막에 감소한다. 전체 경로를 한 개의 일정한 ease 이름으로 환원하지 않는다.'},
  'evidence':[ea(.9,'희미한 녹색 세로선과 십자 형태'),ea(1.0,'교점(176,254) 부근'),ea(1.1,'중앙 작은 사각형과 교점'),ea(1.2,'우하향'),ea(1.4,'우향 증가량 확대 및 가로세로 약600px')],
  'uncertainty':'색차 기반 교점 오차 약2–5px, 매우 희미한 시점은 더 큼. 두 축/사각형이 하나의 레이어인지 알 수 없다.'}
 ],
 'temporal_order':[{'window':[0,.15],'event':'검녹색 중심 명암이 먼저 존재.'},{'window':[.15,.35],'event':'격자/긴 패널들이 매우 희미하게 드러남.'},{'window':[.3,.65],'event':'상단 광선과 큰 하단 패널의 우향 진행이 뚜렷해짐.'},{'window':[.6,.9],'event':'하단 광선과 작은 좌중부 사각형/띠가 뒤따르고 격자는 축소하며 대비 증가.'},{'window':[.85,1.4],'event':'십자축·작은 중앙 사각형이 뒤늦게 나타나 우하향, 패널 우향은 감속하며 유지 상태로 접근.'}],
 'implementation_hypotheses':[{'hypothesis':'직사각형들은 이동과 opacity, 격자는 축소와 opacity를 조합했을 가능성.','status':'가설; 실제 속성/부모/키프레임/효과는 미확인.'},{'hypothesis':'큰 하단 패널의 후기 경계 후퇴는 작은 overshoot일 수 있음.','status':'가설; 격자와 다른 화면 크기 변화가 결합했을 가능성과 구분 불가.'},{'hypothesis':'십자표시는 위치 경로와 밝기 변화가 결합됐을 가능성.','status':'가설; 정확한 곡선/구현 미확인.'}],
 'measurement_evidence':{'accepted_axis_samples':last['T02_axes'],'grid_period_and_top_samples':[r for r in clean if r['t'] in [.6,.75,.9,1.05,1.2,1.35]],'raw_measurement_files':[str(OUT/'tracking_measurements.json'),str(OUT/'clean_measurements.json'),str(OUT/'final_measurement_evidence.json')]},'unresolved':['초기 어두운 상단 패널의 정밀 수직 경로와 크기 변화','광선의 광량 변화와 위치 이동의 정확한 분리','아래 어두운 면/선의 별도 오브젝트 여부','1.4초 이후 정착/퇴장 여부는 지정 구간 밖이므로 판단하지 않음']}

t05={**common,'case_id':'T05','asset_id':'자료005','allowed_window_seconds':[5.9,6.6],'examined_time_window_seconds':[5.9,6.6],
 'sampling':{'supplied_count':22,'supplied_interval_seconds':'1/30','source_raster':[3840,1080],'supplied_png_size':[1920,540],'supplied_pngs_are_native':False,'extra_timestamps_requested':['5.9','6','181/30','182/30','6.1','6.2','6.3','6.4','6.5','6.6'],'extra_native_png_size':[3840,1080],'extra_log':str(E/'실행기록.json')},
 'scene_summary':'사장교와 건설부재가 있는 2026년 경영현황 보고 표지에서, 도시·강 배경 위의 01 실적 및 계획 화면으로 겹쳐 전환된다. 새로운 화면의 수주/매출/영업이익 3개 카드와 카드 안의 목표 막대·비어 있는 실적 영역·빈 달성률 고리를 별도로 확인했다.',
 'objects_events':[
 {'id':'whole_scene_transition','subject':'표지→실적 및 계획 전면 겹침 전환','window_seconds':[5.9,6.6],
  'observable':{'position_direction':'장면 구성물들이 화면을 가로지르는 뚜렷한 위치 이동 없이 같은 자리에서 겹쳐 보이는 비율이 바뀐다.','scale_shape':'각 장면 자체 구성의 스케일/회전 변화는 관측하지 못함. 두 장면의 서로 다른 로고 크기를 한 로고의 축소 이동으로 오인하지 않는다.','visibility':'5.9–6.0초 표지 유지,6.033초 새 장면이 이미 옅게 보임.6.1–6.2초 두 장면이 겹치고6.3초 표지 흔적만 희미. 약6.4초 육안상 새 화면이 거의 완성되며6.467초 이후 픽셀도 거의 유지된다.','color_brightness':'표지의 짙은 교량/부재가 약해지고 흰 카드와 밝은 하늘·도시 배경의 비율이 증가. 전면 백색 플래시나 완전 검정 중간 프레임 없음.','internal_changes':'배경·로고·글자·카드가 같은 전환 흐름으로 교체된다.','overlap':'이전 큰 제목과 새 제목이 동시에 겹치고, 이전 교량이 새 카드/고리 안으로 비쳐 보이는 중간 상태가 명확하다.','observable_acceleration':'입출현의 종류만으로 추측하지 않고 전후 끝점 혼합 비율을 측정했다. proxy α는 6.033=.200,6.1=.524,6.2=.825,6.3=.959,6.367=.992로 증가량이 줄어든다. 1/30초 프레임 차이도 약9.69→8.57→7.13…→1.56→1.11→.54 RGB 단계로 감소한다. 따라서 불투명도/혼합 변화는 초기에 빠르고 끝으로 갈수록 느려지는 관측. 물체 위치의 가감속은 비적용.'},
  'evidence':[eb(6,'표지 유지'),eb(181/30,'겹침 전환 첫 변화'),eb(6.1,'양 장면의 제목·배경·카드 중첩'),eb(6.2,'새 장면이 우세'),eb(6.3,'표지 흔적이 약해짐'),eb(6.4,'새 화면이 거의 완성'),eb(6.6,'후반 유지')],
  'uncertainty':'두 끝점의 선형 RGB 혼합 회귀는 실제 opacity 측정이 아닌 화면 혼합 proxy이다. 압축·색처리 잔차 약0.7–1.1/255가 있어 exact easing 함수와 실제 전환 길이/핸들을 확정하지 않는다.'},
 {'id':'outgoing_cover','subject':'표지 배경: 사장교·물·하늘·산·건설부재와 하단 대각 면','window_seconds':[5.9,6.4],
  'observable':{'direction':'교량/구름/물결/건설부재의 독립 이동은 없음. 전환으로 가시성이 감소.','scale_shape':'우측 큰 사장교, 앞쪽 콘크리트 거더/교각 단면, 묶인 검은 강재/봉, 우측 고리 달린 콘크리트 부재, 수면 반사. 하단 옅은 파란 대각 면과 흰 사선도 유지된 모양으로 사라짐.','visibility':'5.9–6.0초 명확,6.033초부터 약해지고6.3초에는 희미한 흔적.','color_brightness':'파란 하늘과 회색 콘크리트/검은 부재가 밝은 새 배경에 희석됨.','internal_changes':'차량 이동, 물결 진행, 부재 변형/교체는 관측되지 않음.','overlap':'전환 중 새 도시 스카이라인과 카드 아래로 겹쳐 보임.','observable_acceleration':'독립 공간 이동은 관측 안 됨. 가시성 감소율은 전체 전환의 감속 패턴에 따름.'},
  'evidence':[eb(5.9,'사장교·부재·반사·대각 선'),eb(6.1,'이전 교량이 카드 안으로 비침'),eb(6.3,'이전 부재와 교량의 흐린 흔적')],
  'uncertainty':'정지 사진처럼 보이며 이 창에서는 거의 같은 픽셀. 영상 전체에서 정지인지까지 확장하지 않는다.'},
 {'id':'outgoing_cover_type','subject':'표지의 큰 장헌 로고·짧은 파란 선·2026년·경영현황 보고','window_seconds':[5.9,6.4],
  'observable':{'direction':'원래 위치와 글자 모양을 유지하며 약해짐.','scale_shape':'좌측 큰 로고, 회색 연도, 짙은 남색 큰 제목, 그 사이 짧은 파란 가로선. 글자별 모핑/자간 변화 없음.','visibility':'5.9–6.0초 유지; 이후 새 작은 로고와 새 제목 뒤/위로 유령처럼 겹친 뒤 사라짐.','color_brightness':'회색/남색/로고 적청색이 점차 옅어짐.','internal_changes':'숫자 카운트/문구 교체 없이 이 글자 집합 자체 가시성 감소.','overlap':'새 01·실적 및 계획·누적 실적 글자와 중첩되어 이중 문구가 보이는 중간 구간.','observable_acceleration':'독립 위치 가감속 없음. 전체 전환과 동일한 가시성 변화.'},
  'evidence':[eb(5.9,'표지 문자와 로고'),eb(6.033333,'두 크기의 로고와 두 제목이 동시에 보임'),eb(6.2,'큰 표지 제목은 옅고 새 제목은 선명')],
  'uncertainty':'두 로고가 겹치므로 한 로고의 위치·크기 애니메이션으로 판단하지 않는다.'},
 {'id':'incoming_background','subject':'새 도시·강 배경 및 흰 곡선 장식','window_seconds':[6.033333,6.6],
  'observable':{'position_direction':'화면 아래 도시와 다리/강이 같은 위치에서 더 뚜렷해짐. 구름·도시·물의 독립 이동 없음.','scale_shape':'초광폭 도시 스카이라인·산·강 반사, 우측 햇빛. 하늘 위의 흰 가는 곡선 다발, 좌측 옅은 파란 면, 화면 중앙의 가는 세로 이음처럼 보이는 선.','visibility':'6.033초 희미,6.2초 우세,6.4–6.6초 유지.','color_brightness':'밝은 하늘/흰색과 파란색.','internal_changes':'도시·강·흰 곡선 내부의 독립 파형/흐름은 6.467–6.6초에서 관측되지 않음.','overlap':'모든 카드와 새 좌측 문구 뒤. 이전 교량/하단 사선과 겹치는 중간 상태.','observable_acceleration':'공간 이동 추적 대상 없음. 전체 fade 변화율만 관측.'},
  'evidence':[eb(6.033333,'새 도시가 밑에서 겹쳐 보임'),eb(6.3,'새 도시와 흰 곡선이 선명'),eb(6.6,'배경의 도시·물·곡선·중앙 가는 선')],
  'uncertainty':'중앙 가는 세로선이 이미지의 이음/디자인인지 소스 처리 흔적인지는 판단하지 않는다.'},
 {'id':'incoming_left_title','subject':'새 좌측 작은 로고·01·실적 및 계획·부제·붉은 밑줄·회색 보조문','window_seconds':[6.033333,6.6],
  'observable':{'position_direction':'새 화면 내 각 문구/선은 처음 식별 가능한 시점부터 같은 위치에 있다.','scale_shape':'작은 장헌 로고, 빨간 01, 남색 실적 및 계획, 2026년 1~8월 누적 실적, 짧은 빨간 수평선, 회색 더 나은 내일을 위한 지속 가능한 성장을 만들어가겠습니다.','visibility':'함께 더 선명해짐. .4 이후 거의 유지.','color_brightness':'적색 번호/밑줄, 남색 제목/부제, 회색 보조문.','internal_changes':'단어별 출현이나 글자 모핑/카운트 없음.','overlap':'초기 표지의 큰 로고·큰 제목과 겹침. 새 보조문도 초기부터 희미하게 함께 보인다.','observable_acceleration':'독립 위치/크기 가감속은 없음; 전체 가시성 증가율이 감속.'},
  'evidence':[eb(6.033333,'새 작은 로고·01·제목·보조문이 흐리게 함께 존재'),eb(6.1,'표지 문자와 중첩'),eb(6.4,'새 문구 고정'),eb(6.6,'밑줄과 작은 보조문 확인')],
  'uncertainty':'읽기 가능한 범위에서는 별도 시차를 확인하지 못했으며 1/30초 미만의 지연까지 부정하는 것은 아니다.'},
 {'id':'incoming_cards','subject':'3개의 둥근 흰 카드와 카드 제목/번호/구분선','window_seconds':[6.033333,6.6],
  'observable':{'position_direction':'좌→우로 나란한 세 카드가 같은 자리에서 더 뚜렷해짐. 슬라이드/회전/확대 증거 없음.','scale_shape':'얇은 테두리·은은한 가장자리 음영이 있는 둥근 흰 직사각형 3개. 01 수주,02 매출,03 영업이익. 각 상단에 옅은 번호·남색 제목·얇은 수평 구분선.','visibility':'세 카드의 번호/제목/구분선과 면이 전환 중 함께 드러남. 왼쪽부터 차례로 들어오는 순서는 관측되지 않음.','color_brightness':'흰/아주 옅은 청색 면, 옅은 파란 번호, 남색 제목.','internal_changes':'카드 외곽은 고정되고 아래 차트도 같은 자리에서 선명해짐.','overlap':'이전 교량이 카드 면/제목 뒤에 비쳐 보이는 중간 프레임.','observable_acceleration':'공간 가감속 없음; 가시성 변화는 전면 전환과 동행.'},
  'evidence':[eb(181/30,'세 카드 제목이 동시에 희미하게 보임'),eb(6.1,'고정된 카드의 중첩 전환'),eb(6.3,'둥근 테두리와 구분선'),eb(6.6,'세 카드 유지')],
  'uncertainty':'카드가 실제로 별도 레이어인지, 이미 완성된 장면 이미지인지 확인할 수 없다.'},
 {'id':'card_internal_charts','subject':'카드 내부의 목표 막대·목표 금액·빈 실적 영역·달성률 고리·기준선','window_seconds':[6.033333,6.6],
  'observable':{'position_direction':'각 차트 요소는 고정 위치. 하단 기준선에 놓인 목표 막대와 옆의 고리가 유지된다.','scale_shape':'세 카드에 2026년 목표 / 1~8월 실적 / 달성률 레이블. 목표 값은 수주60억,매출64억,영업이익7억. 각 목표 값 아래 낮고 굵은 옅은 청색 막대 1개. 가운데 실적 칸에는 해당 창에서 숫자/실적 막대가 보이지 않으며, 우측은 연한 단색 빈 고리.','visibility':'겹침 초반부터 같은 완성 높이/같은 고리 모양이 흐리게 보이다가 선명해짐.','color_brightness':'막대와 고리 모두 옅은 청회색/청색. 값과 레이블은 남색. 유색 달성 구간이 새로 채워지는 모습은 없음.','internal_changes':'6.1–6.6초 네이티브 crop에서 목표 막대 높이·고리 두께/지름·기준선 길이 및 표시 값 변화는 관측되지 않음. 숫자 카운트/달성률 숫자/링 회전·채움/실적 막대 성장 없음.','overlap':'6.1–6.3초 보이는 교량·케이블·수면은 차트 내부 콘텐츠 변화가 아니라 이전 배경이 겹쳐 보이는 것과 일치한다.','observable_acceleration':'내부 차트 기하의 가감속 비적용: 별도 기하 변화가 관측되지 않음. 가시성만 전환과 함께 변한다.'},
  'evidence':[eb(6.033333,'희미한 목표 값·막대/고리의 초기 실루엣'),eb(6.1,'네이티브 수주/영업이익에서 이미 동일 높이와 고리'),eb(6.3,'표지 교량 흔적이 고리/막대 위에서 약해짐'),eb(6.4,'목표막대와 빈 실적/고리 확인'),eb(6.6,'60억·64억·7억 및 비어 있는 나머지 데이터 영역 유지')],
  'uncertainty':'실적/달성률이 빈 것은 이 구간의 관측이다. 6.6초 이후 차트 애니메이션은 지정 구간 밖이므로 추측하지 않는다. 아주 작은 디코딩 픽셀 변동을 내부 애니메이션으로 분류하지 않는다.'}
 ],
 'temporal_order':[{'window':[5.9,6],'event':'표지 그대로 유지.'},{'window':[6,6.0333333333],'event':'이 사이에 전환 시작; 6.033 프레임에서 새 화면이 이미 약20% 혼합된 상태.'},{'window':[6.0333333333,6.3],'event':'배경·로고·문구·카드·내부 차트가 겹쳐 바뀜; 순차적 카드 entrance 증거 없음.'},{'window':[6.3,6.4666666667],'event':'표지 잔상이 약해지고 새 화면 유지로 접근;6.433→6.467에 작고 넓게 퍼진 색상 잔차 변화 존재.'},{'window':[6.4666666667,6.6],'event':'기하와 내용은 육안상 유지. 프레임차는 대체로 0.0003–0.036 RGB 단계 수준.'}],
 'implementation_hypotheses':[{'hypothesis':'두 정지 장면을 opacity cross-dissolve했을 가능성이 매우 높다.','status':'렌더와 끝점 혼합 모델이 일치하는 구현 가설. 실제 편집기/레이어 수는 미확인.'},{'hypothesis':'혼합 변화가 ease-out 성격을 가진다.','status':'초반이 빠르고 끝이 느리다는 관측은 지지됨. 정확한 수학 함수·프리셋·키프레임 곡선은 미확인.'},{'hypothesis':'6.433→6.467의 작은 전체 색 잔차 변화가 인코딩/색상 양자화에서 생겼을 수 있다.','status':'가능성. 차트 구분선이 독립적으로 새로 그려졌다는 초기 의심은 위치/형태 증거가 없으므로 채택하지 않음.'}],
 'measurement_evidence':{'mix_proxy_samples':last['T05_mix'],'model':'alpha = sum((I_t-I_6.0)*(I_6.6-I_6.0))/sum((I_6.6-I_6.0)^2), RGB pixels on all supplied half-size PNGs; a proxy, not actual AE opacity.','frame_difference_samples':metric['T05'],'native_crop_files':[str(OUT/'crops'/n) for n in ['T05_title_progress.jpg','T05_card1_native.jpg','T05_card3_native.jpg']]},
 'unresolved':['정확한 easing 함수와 실제 opacity 키프레임은 식별 불가','전환 완성의 마지막 미세 색 변화는 압축/양자화와 구분 곤란','작은 보조문과 카드 내부까지 확인했지만 6.6초 이후의 실적/달성률 애니메이션 여부는 범위 밖']}

md02='''T02 / 0.000–1.400초 최초 관찰

검녹색 비네트 위에 긴 반투명 사각형, 작은 좌중부 사각형과 낮은 띠, 격자와 이중 테두리, 수평 청록색 광선이 드러납니다. 사각형은 대체로 왼쪽 밖에서 우향하고, 격자는 셀 간격이 줄며 안쪽으로 모입니다. 배경 중심색은 거의 유지되지만 귀퉁이는 더 어두워져 배경 전체를 단순 정지로 분류하지 않았습니다.

큰 하단 사각형의 우측 끝은 0.3/0.45/0.6/0.75/0.9/1.05초에 약447/1543/1952/2135/2217/2241px입니다. 등시간 변화량이 줄어 우향 감속이 보이며 후반의 약7px 후퇴는 위치 오버슈트인지 다른 크기 변화의 결합인지 미확정입니다. 작은 좌중부 사각형도 우향 변화량이 줄어듭니다. 격자 간격은 0.6초 약120px에서 1.35초107px로 줄며 후반 변화가 작아집니다.

늦게 나타나는 적색 가로축·녹색 세로축과 중앙의 작은 사각형은 우하향합니다. 교점은 1.0초(176,254)에서1.4초(398,496)로 이동합니다. x 방향 등시간 변화량은 커지고 y 방향은 중간에 빠른 뒤 줄어, 하나의 일반 entrance 규칙으로 easing을 단정하지 않았습니다. 광선의 위치와 광량은 함께 바뀌므로 별도 정확한 속도곡선은 미분류입니다.

원본 3840×2160 PNG29장, 개요3장과 네이티브 영역 crop을 확인했습니다. 증거 시점·파일·불확실성·모든 입력/도구 감사 목록은 T02_observations.json에 있습니다. 실제 AE 레이어·키프레임·프리셋을 식별했다는 뜻은 아닙니다.
'''
md05='''T05 / 5.900–6.600초 최초 관찰

사장교와 건설부재가 있는 경영현황 보고 표지에서, 도시·강 배경의 실적 및 계획 화면으로 겹쳐 전환됩니다. 5.9–6.0초는 유지되고6.033초에 새 로고·제목·카드가 이미 옅게 보이며6.1–6.3초 두 장면이 겹칩니다. 약6.4초부터 새 화면이 육안상 거의 완성되고6.467–6.6초는 기하와 내용이 유지됩니다. 서로 크기가 다른 두 로고의 중첩을 한 로고의 축소 이동으로 분류하지 않았습니다.

새 화면의 작은 로고·빨간01·제목·부제·붉은 밑줄·회색 보조문, 둥근 카드3개와 얇은 구분선까지 확인했습니다. 카드 제목은 수주/매출/영업이익, 목표는60억/64억/7억입니다. 목표 막대는 처음 확인되는 시점부터 같은 높이이며, 가운데 실적 칸과 우측 달성률 고리에는 이 창 안에서 새로운 수치·실적 막대·유색 링 채움이 보이지 않습니다. 표지 교량이 고리 안에 비치는 중간 상태는 배경 중첩으로 설명됩니다.

끝점 혼합 proxy는6.033초 .200,6.1초 .524,6.2초 .825,6.3초 .959로 증가량이 줄어듭니다. 입출현이라는 명칭과 별개로 혼합 변화가 초반에 빠르고 후반에 느리다는 증거가 있습니다. 정확한 함수·키프레임 핸들은 미확정입니다.6.433→6.467의 작은 광범위 색상 차이는 관측했지만 구분선의 독립 그리기 애니메이션으로 판단할 위치/형태 증거는 없습니다.

제공 PNG22장은1920×540으로 원본의 절반이었습니다. 지정 구간 내10개 시점을3840×1080으로 추가 추출해 작은 문구와 차트 내부를 네이티브 crop으로 비교했습니다. 모든 근거·불확실성·입력 및 도구 목록은 T05_observations.json에 있습니다. 이후 차트 진행은 범위 밖이므로 추측하지 않았습니다.
'''
for case,data,narrative in [('T02',t02,md02),('T05',t05,md05)]:
 jp=OUT/(case+'_observations.json');mp=OUT/(case+'_observations.md')
 for p in [jp,mp]:
  if p.exists():raise RuntimeError('Preserve first pass: '+str(p))
 with jp.open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
 with mp.open('x',encoding='utf-8') as f:f.write(narrative)
 print(json.dumps({'saved_first_pass':case,'json':str(jp),'narrative':str(mp)},ensure_ascii=False))
