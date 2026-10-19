from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import json

ROOT=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase01a-a2-retest')
IN=ROOT/'analysis_input';OUT=ROOT/'runs/retest_a'
P01=IN/'cases/자료013/T01';P04=IN/'cases/자료005/T04'
E01=OUT/'cases/자료013/extra1';E04=OUT/'cases/자료005/extra1'
def readj(p):return json.loads(p.read_text(encoding='utf8'))
def evidence(folder,name,t,note=''):
    return {'path':str(folder/name),'actual_frame_time_seconds':float(Fraction(str(t))),'actual_frame_time_fraction':str(Fraction(str(t))),'note':note}
def orig(folder,ordinal,t,note=''):
    return evidence(folder,f'f_{ordinal:05d}_{float(Fraction(str(t))):07.3f}.png',t,note)
def source_sampling(folder):
    l=readj(folder/'실행기록.json')
    return {'log_path':str(folder/'실행기록.json'),'complete_target_selection':l['complete_target_selection'],'timing_status':l['timing_status'],'frames':[{'path':f['path'],'actual_time_fraction':f['actual_playback_seconds'],'actual_time_seconds':float(Fraction(f['actual_playback_seconds'])),'derived_size':f['derived_size']} for f in l['frames']], 'audio_status':l['audio_status'],'sar_status':l['sar_status'],'color_range_accuracy_validated':False}
common={
    'phase':'A2 neutral first-pass raw observations; before grading',
    'language':'ko',
    'new_skill_used':False,
    'saved_at_utc':datetime.now(timezone.utc).isoformat(),
    'method':'할당 구간의 개요 보드를 시간 순서로 보고, 정착 화면을 역추적한 뒤 원본 폭 PNG의 대상별 크롭과 표본 좌표·픽셀 차이를 비교했다. 관측과 구현 추정을 분리했다.',
    'tools_used':['functions.exec orchestration','exec_command / PowerShell','view_image (including detail=original for native crop sequences)','apply_patch (own scripts only)','provided inspect_more.py bounded extraction using supplied Python -B -X utf8','Python Pillow and NumPy for crops, simple thresholds, edge estimates, frame differences'],
    'not_performed':['외부 AI API 호출','AE 또는 CU 조작','이전 분석·정답·채점 파일 열람','오디오 청취/전사','구간 밖 미디어 시각 검사','스킬 생성'],
    'measurement_cautions':['픽셀 좌표는 제공 raster에서의 근사값이며 SAR가 0/1로 보고되어 실제 디스플레이의 정밀 길이로 주장하지 않는다.','RGB 변환의 범위 정확도는 추출 로그에서 미검증이다. 밝기 수치는 상대 비교다.','밝기 임계값과 1행 edge 검출은 글자 경계·텍스처·압축의 영향을 받는다. 특히 T01 5.3초 top-bar edge 검출 x=1584는 내부 도면선을 잡은 이상값으로 외곽 이동의 근거에서 제외했다.','정지 판정은 검사 표본에서 위치·형태 변화가 보이지 않는다는 뜻이며 모든 프레임이 완전히 동일하다는 뜻은 아니다.'],
    'implementation_hypotheses_policy':'레이어 수, 마스크/핸들, 표현식, 키프레임 보간, 프리셋은 렌더 영상만으로 확정하지 않았다. 아래 구현 가설은 관측과 별개이며 검증되지 않았다.'
}

t01={**common,'case_id':'T01','asset_id':'자료013','allowed_window_seconds':[3.5,5.5],
    'actual_inspected_start_seconds':3.5,'actual_inspected_end_seconds':5.5,
    'frame_sampling':[source_sampling(P01),source_sampling(E01)],
    'extra_evidence_requested':{'helper':str(IN/'inspect_more.py'),'tag':'extra1','width':3840,'requested_times':['3.5','211/60','212/60','213/60','214/60','215/60','3.6','4.8','5','5.1','5.3','5.5'],'purpose':'3.5초의 작은 밝은 잔상·가이드가 어떻게 사라지는지 확인하고 E 정착 후 내부 변화를 원본 크롭으로 비교'},
    'observations':[
        {'object_id':'T01-bg','subject':'검정·녹색 배경, 미세 격자, 반투명 사각 패널과 외곽 선, 수평 녹색 광대',
         'time_seconds':[3.5,5.5],'position_direction':'격자 교차점과 사각 패널 테두리는 같은 위치에 남는다. 카메라 이동을 뒷받침하는 공통 이동은 보이지 않는다.',
         'scale_shape_orientation':'직교 격자·사각형을 유지하며 회전/형태 변형은 식별하지 못했다.',
         'visibility_color_brightness':'주변부가 검고 중앙과 오른쪽이 녹색으로 밝다. 수평 광대와 격자의 약한 명암 변동은 있으나 독립된 이동 방향·속도를 확정할 만큼 두드러지지 않는다.',
         'internal_change':'배경 오른쪽·Value of 뒤 고정 영역의 5.1→5.3초 평균 절대 RGB 차이는 약 1.00/0.46 수준이고 채널 차이 10 초과 픽셀은 거의 없다. 밝기 변화와 압축을 분리할 수 없어 미세한 광량 곡선은 미분류.',
         'overlap_order':'큰 E가 들어오면서 격자와 Value of의 왼쪽 부분을 가린다. 오른쪽의 제목·설명은 앞쪽에서 읽힌다.',
         'easing':'위치 변화가 검출되지 않아 위치 가감속 비적용. 배경 광량의 정확한 곡선은 미분류.',
         'evidence':[orig(P01,210,'3.5'),orig(P01,300,'5'),orig(P01,330,'5.5')],
         'uncertainty':'패널을 별도 렌더 요소로 구성했는지는 알 수 없다.'},
        {'object_id':'T01-value','subject':'배경의 큰 반투명 Value of 문자와 시작점의 흰 of 일부',
         'time_seconds':[3.5,5.5],'position_direction':'큰 녹색 문자 자체는 고정. 3.5초에는 of의 아래 부분이 흰 띠처럼 밝고, 3.516667초에 그 흰 부분의 위 경계가 아래로 내려가며 좁아져 3.533333초에는 사라진다.',
         'scale_shape_orientation':'큰 문자의 전체 크기와 형태·회전은 유지. 밝게 보이는 부분의 세로 가시 범위만 줄어든다.',
         'visibility_color_brightness':'3.5초 밝은 흰 부분 → 3.516667초 얇은 흰 부분 → 3.533333초 녹색 반투명 문자만 남음.',
         'internal_change':'문자 아래쪽의 청록색 잔상 띠도 제목 뒤쪽으로 얇아져 3.583333초에는 작은 조각만 보이며 3.6초에는 거의 안 보인다.',
         'overlap_order':'흰 of 부분과 청록 띠는 EG-BIM 뒤에서 겹치며 주 제목의 흰 글자는 계속 앞에 보인다.',
         'easing':'수 프레임 안에 가시 범위가 줄어드는 방향은 확인. 짧은 시작 잔여 구간이고 경계에 잔상이 있어 특정 가감속 곡선은 미분류.',
         'evidence':[orig(E01,210,'3.5'),orig(E01,211,'211/60'),orig(E01,212,'212/60'),orig(E01,215,'215/60'),{'path':str(OUT/'T01_subframe_artifact_sequence.png'),'actual_frame_times_seconds':[3.5,211/60,212/60,3.55,214/60,215/60,3.6]}]},
        {'object_id':'T01-guide','subject':'제목 오른쪽의 얇은 녹색 세로선·붉은 가로선·작은 붉은 사각 교차 표시와 흰 점선 모서리',
         'time_seconds':[3.5,3.6],'position_direction':'교차점은 대략 x3350, y1200 부근에 고정. 선과 사각 표시가 오른쪽으로 이동한다고 볼 근거는 없다.',
         'scale_shape_orientation':'수직/수평 방향 유지. 흰 점선 모서리와 청록 띠의 가시 세로 범위가 감소한다.',
         'visibility_color_brightness':'3.5초 선명하게 보이고 3.55~3.583333초에 약해지며 3.6초에는 거의 소실. 3.7초 표본에는 선·교차 표시가 식별되지 않는다.',
         'internal_change':'별도 텍스트 변화 없음. 가이드형 도형의 형태를 기록한 것이며 편집 UI/레이어 핸들이라고 단정하지 않았다.',
         'overlap_order':'가로 붉은 선은 제목 M 앞쪽을 약하게 지나며, 일부 청록 잔상은 제목 뒤에 있다.',
         'easing':'이동 속도 비적용. 소실의 밝기 곡선은 선이 매우 가늘고 압축 영향이 있어 미분류.',
         'evidence':[orig(E01,210,'3.5'),orig(E01,213,'3.55'),orig(E01,215,'215/60'),orig(P01,216,'3.6'),orig(P01,222,'3.7')]},
        {'object_id':'T01-E-pieces','subject':'왼쪽에서 들어와 큰 E를 이루는 상단 가로·상부 세로·중간 가로·하부 세로·하단 가로의 직사각형 구간',
         'time_seconds':[3.5,5.5],'position_direction':'높이별 구간이 서로 다른 수평 위치에서 오른쪽으로 진행하여 하나의 E 외곽으로 정렬된다. 3.5초에는 상단 가로 조각의 끝만 왼쪽 위에 보이고, 3.6초에는 하부 세로 구간도 왼쪽에 들어온다. 3.8초에는 여러 높이의 조각이 모두 보이며 아직 왼쪽 경계가 계단처럼 어긋나 있다. 4.8~5.1초에 경계가 대략 x580으로 정렬된다.',
         'scale_shape_orientation':'각 구간의 가로·세로 크기와 수평/수직 모서리는 유지되어 보인다. 전체 확대보다 수평 이동과 화면 경계의 잘림으로 E의 보이는 면적이 커진다. 회전은 관측되지 않았다. 최종 E의 위·아래는 화면 밖으로 잘린다.',
         'visibility_color_brightness':'짙은 녹색 조각에서 시작해 4.2초 올리브색, 4.4초 황갈색, 4.6~4.8초 금색/주황색으로 밝아진다. 얇은 어두운 가장자리/그림자도 함께 움직인다.',
         'internal_change':'도면선이 점차 드러나며 별도 항목 T01-E-inside에서 후속 변화를 기록했다.',
         'overlap_order':'상단 가로가 먼저 보인다. 하부 세로가 뒤따르고 이후 여러 높이의 가로·세로 구간이 겹쳐 정렬된다. 상부 세로·중간 가로·하단 가로의 최초 등장 서로 간 순서는 0.1초 간격 및 화면 잘림 때문에 정확히 확정하지 않았다. E는 뒤의 Value of, 격자와 일부 수평 선을 가린다. 오른쪽 본문과 직접 겹치지 않는다.',
         'easing':'상단 가로 오른쪽 경계의 근사 x는 3.5:121, 3.6:598, 3.7:1084, 3.8:1413, 3.9:1617, 4.0:1772, 4.2:1967, 4.4:2078, 4.6:2133, 4.8:2153, 5.1:2153. 초반 3.5~3.7초 간격은 비슷하거나 조금 증가한 뒤 이후 이동량이 계속 작아져 정착한다. 다른 구간도 끝에 감속하지만 서로 시간차가 있다. 튐/역방향 overshoot는 표본에서 보이지 않는다. 특정 보간 함수는 확정하지 않는다.',
         'evidence':[orig(P01,210,'3.5'),orig(P01,216,'3.6'),orig(P01,228,'3.8'),orig(P01,252,'4.2'),orig(P01,276,'4.6'),orig(P01,288,'4.8'),orig(P01,306,'5.1'),{'path':str(OUT/'T01_left_sequence.png'),'actual_frame_times_seconds':[3.5,3.6,3.7,3.8,3.9,4.0,4.2,4.4,4.6,4.8,5.0,5.5]},{'path':str(OUT/'T01_topbar_edge_exploratory.json'),'note':'5.3초 자동 edge 이상값 제외'}],
         'uncertainty':'다섯 기하 구간이라는 관측 분류는 실제 레이어 수가 아니다. 시작이 허용 구간 이전인 구간의 전체 출발 곡선은 알 수 없다.'},
        {'object_id':'T01-E-inside','subject':'큰 E 안의 도로/교차로 같은 도면, 숫자·점선·곡선, 얇은 직교 격자',
         'time_seconds':[4.0,5.5],'position_direction':'E 구간이 이동하는 동안 내부 도면도 그 구간과 함께 보이는 위치가 바뀐다. 정착 후 5.1~5.5초에는 도로 윤곽의 공통 이동/회전을 확정할 만한 변화는 보이지 않는다.',
         'scale_shape_orientation':'도로 곡선·짧은 표기·격자 구조를 유지. 독립된 모핑이나 도면 내용 교체는 확인하지 못했다.',
         'visibility_color_brightness':'4.0~4.2초 희미한 도면선이 보이기 시작해 4.6초 무렵 노랑/연두 선으로 잘 읽힌다. E 외곽 정착 뒤에도 얇은 격자와 선의 밝기가 달라진다. 5.1초의 일부 격자는 5.3초보다 밝고 5.5초에도 도면·바탕의 광량이 변한다.',
         'internal_change':'원본 크롭의 E 내부는 5.1→5.3초 평균 절대 RGB 차이 약 7.05, 채널 차이 10 초과 영역 약 23%; 같은 시기 고정 배경보다 크다. 상단 E 내부도 평균 약 10.35의 차이. 따라서 외곽이 멈췄다는 이유로 내부를 완전 정지로 처리하지 않았다.',
         'overlap_order':'도면과 격자는 E의 보이는 영역에 한정되어 있고 E 바깥 배경 도면 격자와는 밝기·색이 다르다.',
         'easing':'내부 광량 변화는 양성 관측. 밝은 띠가 흐르는지, 격자 밝기 변조인지, 섞임 정도 변화인지 분리할 만큼 시간 표본이 충분하지 않아 방향·주기·정확한 가감속은 미분류.',
         'evidence':[orig(P01,240,'4'),orig(P01,252,'4.2'),orig(P01,276,'4.6'),orig(E01,306,'5.1'),orig(E01,318,'5.3'),orig(E01,330,'5.5'),{'path':str(OUT/'T01_held_texture_sequence.png'),'actual_frame_times_seconds':[4.8,5,5.1,5.3,5.5]},{'path':str(OUT/'T01_hold_diff_exploratory.json')}]},
        {'object_id':'T01-main-title','subject':'흰색 굵은 EG-BIM 및 어두운 그림자',
         'time_seconds':[3.5,5.5],'position_direction':'오른쪽 중간에 이미 표시되어 있으며 3.6~4.0초에 좌우 외곽이 약간 가운데로 좁아진다. y 상·하단은 대체로 고정.',
         'scale_shape_orientation':'3.6초 밝은 본체 bbox 약 [2272,1075,3255,1300] → 4.0초 [2277,1075,3249,1300]. 가로 폭이 약 11px 좁아지는 미세 정착은 확인하되, 전체 scale·자간·각 글자 위치 중 무엇이 원인인지는 미분류. 회전 없음.',
         'visibility_color_brightness':'흰 본체는 계속 읽히고 어두운 그림자 유지. 3.5초의 뒤쪽 흰 of 잔상은 주 제목에서 분리했다.',
         'internal_change':'문구는 바뀌지 않는다. 4.1~5.5초 bbox는 표본에서 동일.',
         'overlap_order':'배경 Value of와 잔상보다 앞. E 오른쪽에 공간을 두고 위치.',
         'easing':'가로 좁아짐의 크기가 3.6→3.7보다 후반에 작아지는 정착 경향. 1~수px 변화여서 정확한 easing은 미분류.',
         'evidence':[orig(P01,216,'3.6'),orig(P01,222,'3.7'),orig(P01,240,'4'),orig(P01,306,'5.1'),{'path':str(OUT/'T01_geometry_exploratory.json')}]},
        {'object_id':'T01-subtitle','subject':'Engineering Graphicer for BIM 한 줄, E/G/BIM의 노랑 강조',
         'time_seconds':[3.5,5.5],'position_direction':'x는 거의 고정한 채 위로 조금 올라가 정착한다. 흰 글자 상단 y 약 1362(3.5초)→1357→1354→1353→1352(3.9~4.0초).',
         'scale_shape_orientation':'줄의 폭·글자 형태와 수평 방향은 대체로 고정. 분명한 확대/회전 없음.',
         'visibility_color_brightness':'흰 일반 글자와 노란 E/G/BIM 강조가 계속 표시된다. 색 교체는 확인되지 않는다.',
         'internal_change':'문구 변화 없음.',
         'overlap_order':'주 제목 아래, 본문 위. 본문 정착보다 이르게 대략 제자리에 도달한다.',
         'easing':'위쪽 이동량이 대략 5→3→1~2→1px로 감소하여 감속 정착. 구간 시작 이전의 출발은 알 수 없다.',
         'evidence':[orig(P01,210,'3.5'),orig(P01,216,'3.6'),orig(P01,228,'3.8'),orig(P01,240,'4'),{'path':str(OUT/'T01_geometry_exploratory.json')}]},
        {'object_id':'T01-body','subject':'오른쪽 네 줄 한국어 설명; 위쪽 두 줄과 아래쪽 두 줄',
         'time_seconds':[3.5,5.5],'position_direction':'좌측 정렬 x 약 2278은 유지하며 각 두 줄 묶음이 위로 이동. 위쪽 첫 줄 상단은 y1516(3.5)→1506(3.6)→1500(3.7)→1496(3.8)→1491(4.1). 아래쪽 묶음은 더 늦게 올라오며 마지막 줄 밝은 bbox 하단이 1729(3.6)→1716→1708→1703→1696(4.3)으로 줄어든다.',
         'scale_shape_orientation':'글자 크기·줄의 수평 방향 유지. 아래 묶음이 올라오며 위 묶음과의 간격이 줄어 최종 네 줄 간격으로 정착.',
         'visibility_color_brightness':'3.5초 위쪽은 회백색, 아래쪽은 더 어둡게 보인다. 위 묶음이 먼저 밝아지고 아래 묶음이 뒤따라 3.8~4.3초에 밝은 흰 글자로 읽힌다. 3.5초 아래 글자를 부재로 취급하지 않았다.',
         'internal_change':'문구·강조의 굵기 구조는 유지되며 글자가 바뀌거나 한 글자씩 타이핑되는 증거는 없다.',
         'overlap_order':'위 두 줄 선행, 아래 두 줄 후행. 4.3~5.5초에는 위치가 유지.',
         'easing':'각 묶음의 위쪽 이동량이 줄어드는 감속을 관측. 밝기 증가의 정확한 곡선은 별도로 확정하지 않았다.',
         'evidence':[orig(P01,210,'3.5'),orig(P01,216,'3.6'),orig(P01,228,'3.8'),orig(P01,246,'4.1'),orig(P01,258,'4.3'),{'path':str(OUT/'T01_body_native_sequence.png'),'actual_frame_times_seconds':[3.5,3.6,3.7,3.8,3.9,4]},{'path':str(OUT/'T01_geometry_exploratory.json')}]},
        {'object_id':'T01-thin-line','subject':'본문 아래쪽/왼쪽으로 길게 이어지는 얇은 검은 수평선',
         'time_seconds':[3.5,5.5],'position_direction':'대략 y1755 부근에 같은 높이로 남는다.',
         'scale_shape_orientation':'수평의 가는 선을 유지. E가 들어오면서 왼쪽의 보이는 범위가 달라진다.',
         'visibility_color_brightness':'어두운 배경에서는 잘 안 보이고 밝은 E 경계/녹색 패널에서 대비되어 보인다.',
         'internal_change':'독립적인 선 그리기 진행은 확인되지 않았다.',
         'overlap_order':'E의 채워진 부분은 선을 덮고 열린 부분과 오른쪽 아래 공간에서는 선이 남는다.',
         'easing':'좌표가 고정되어 이동 가감속 비적용. 가시 길이 변화는 겹침에 의한 것으로 보이나 별도 마스크 구현은 확정하지 않는다.',
         'evidence':[orig(P01,210,'3.5'),orig(P01,240,'4'),orig(P01,300,'5'),{'path':str(OUT/'T01_body_native_sequence.png')}]}
    ],
    'implementation_hypotheses':[
        {'hypothesis':'E의 여러 수평 구간에 시간차를 둔 수평 변환과 색/명도 변화를 적용했을 수 있다.','basis':'높이별 외곽이 서로 다르게 진행하고 마지막에 일치','not_established':'실제 분할 방식·레이어 수·마스크·효과·보간 함수'},
        {'hypothesis':'본문 두 묶음에 상향 이동과 가시성 증가를 함께 적용했을 수 있다.','basis':'고정 x에서 y가 감소하며 글자가 밝아짐','not_established':'opacity 변화인지 다른 밝기/합성 처리인지'},
        {'hypothesis':'시작의 흰 부분과 청록 잔상은 움직이는 가시 경계 또는 잔상 처리로 사라졌을 수 있다.','basis':'밝은 위 경계가 아래로 진행하고 가시 영역 축소','not_established':'실제 wipe/마스크 종류 및 의도'}
    ],
    'uncertainty_summary':['E 구간의 서로 다른 시작점과 초기 속도는 허용 구간 전의 모습이 없어 완결해서 알 수 없다.','3.5초 시작 잔상·작은 선의 방향과 소실은 추가 1/60초 표본으로 확인했으나 이름/기능은 확정하지 않았다.','E 내부 후반 변화는 광량 변화까지 확인되며 독립된 도면 기하 움직임과 정확한 주기/방향은 미분류.','카메라, 가이드형 도형의 구현, 텍스트 가로 폭 정착의 실제 속성은 확정하지 않았다.'],
    'extraction_issues':['기본 T01 프레임과 추가 프레임 모두 3840×2160. 추출 완료 및 PTS 매핑 일치가 로그에 보고됨.','PNG 전체 view_image 호출은 UI에서 2048×1152로 축소되었으므로 작은 요소는 원본 크롭을 다시 표시했다.','오디오 미분석, SAR 불명 및 색 범위 검증 미완료.']
}

def graph_event(oid,name,goal,interval,samples,end,hold,ev):
    return {'object_id':oid,'subject':name+' 카드 내부의 파란 실적 막대·실적 숫자·파란 도넛 호·중앙 달성률 숫자','time_seconds':interval,
      'position_direction':'막대는 고정된 바닥선에서 위쪽으로 높아지고 폭과 x는 유지. 숫자 라벨은 막대 상단을 따라 위로 올라간다. 도넛은 고정 중심·반지름에서 12시를 시작으로 시계 방향의 파란 호가 늘어난다. 중앙 %는 같은 자리에 있다.',
      'scale_shape_orientation':'막대 높이와 호의 각도 범위가 증가. 막대 상단의 둥근 모서리 유지. 도넛 전체가 회전/확대되는 움직임은 보이지 않는다.',
      'visibility_color_brightness':'활성 전에는 파란 막대·실적 값·중앙 %가 안 보이고 연회색 도넛만 있다. 활성 후 밝은 파랑이 나타나며 짙은 남색 숫자가 증가. 회색 목표 막대와 목표 '+goal+'은 유지.',
      'internal_change':{'observed_samples':samples,'final_observed':end,'held_after_seconds':hold,'note':'표시 정수는 반올림 차이가 있을 수 있다. 막대·호·숫자가 함께 증가한다는 관측이며 동일한 내부 계산식을 쓴다고 확정하지 않는다.'},
      'overlap_order':'파란 호가 기존 연회색 링의 일부를 채우고 나머지 회색 호는 계속 보인다. 중앙의 흰 공간과 숫자에 파란 호가 겹치지 않는다. 다른 카드의 완성 그래프는 유지된다.',
      'easing':'후반의 동일 시간 간격 증가량이 작아져 감속 정착하는 경향이 명확하다. 최초 활성 시점이 표본 사이에 있으므로 극초반의 가속 구간/정확한 보간 함수는 미분류. overshoot·되감기는 표본에서 관측되지 않았다.',
      'evidence':ev}

t04={**common,'case_id':'T04','asset_id':'자료005','allowed_window_seconds':[6,18],
    'actual_inspected_start_seconds':6,'actual_inspected_end_seconds':18,
    'frame_sampling':[source_sampling(P04),source_sampling(E04)],
    'extra_evidence_requested':{'helper':str(IN/'inspect_more.py'),'tag':'extra1','width':3840,'requested_times':['6','6.1','6.2','6.3','6.4','6.5','7.8','8','8.1','8.2','8.4','8.6','8.8','9','9.2','14.8','15','15.2','15.4','15.6','15.8','16','16.2','16.4','16.6','16.8','17','17.2','17.4','17.6','17.8','18'],'purpose':'축소 기본 프레임을 원본 폭으로 보완하고 dissolve·카드 내부·유지 배경을 비교'},
    'observations':[
      {'object_id':'T04-transition','subject':'교량 표지 화면에서 실적 및 계획 화면으로의 전환',
       'time_seconds':[6,6.5],'position_direction':'6.0초는 교량·케이블/주탑·강과 하늘, 전경의 콘크리트 제품·긴 어두운 관/철근 묶음, 왼쪽 로고와 2026년 경영현황 보고가 보인다. 6.1~6.3초 이 내용이 옅어지는 동안 새 화면의 로고·제목·세 카드·도시 수변 배경이 같은 자리에서 짙어진다. 6.4~6.5초에는 새 화면만 읽힌다.',
       'scale_shape_orientation':'양쪽 화면의 대표 모서리/문자 위치에 이동이 확인되지 않는다. 두 화면이 겹친 상태이며 슬라이드나 확대 증거는 없다.',
       'visibility_color_brightness':'이전 화면의 가시성 감소와 새 화면의 가시성 증가가 동시에 진행. 전체 영상은 파란 하늘·강의 밝은 톤 유지.',
       'internal_change':'교량과 전경 제품은 형태가 바뀌는 대신 사라지고, 도시·세 카드가 나타난다.',
       'overlap_order':'6.1~6.3초에 이전 표지 문구/로고와 새 실적 문구/로고가 서로 다른 위치에서 동시에 보이고 교량은 카드 안쪽 뒤로 비친다. 새 카드 세 개의 명확한 순차 등장 증거는 없다.',
       'easing':'6.0과 6.5초를 양 끝으로 둔 단순 RGB 혼합계수 근사: 6.1초 0.524,6.2초 0.824,6.3초 0.959,6.4초 0.993. 새 화면 쪽 변화량이 후반 작아지는 감속형 가시성 전환을 지지한다. 감마/색 변환과 동시 변화가 있어 실제 opacity 또는 특정 곡선을 확정하지 않는다.',
       'evidence':[orig(E04,180,'6'),orig(E04,183,'6.1'),orig(E04,186,'6.2'),orig(E04,189,'6.3'),orig(E04,192,'6.4'),orig(E04,195,'6.5'),{'path':str(OUT/'T04_transition_sequence.png'),'actual_frame_times_seconds':[6,6.1,6.2,6.3,6.4,6.5]},{'path':str(OUT/'T04_transition_mix_exploratory.json')}]},
      {'object_id':'T04-bg','subject':'새 화면의 하늘·흰 곡선 다발·산/도시 스카이라인·다리·강과 반사, 밝은 왼쪽 그라데이션',
       'time_seconds':[6.4,18],'position_direction':'하늘과 화면 위쪽의 여러 가는 흰 곡선, 하단의 산/도시/수변 구조와 반사는 같은 좌표에 유지. 공통 pan/zoom이나 물결의 이동을 확인하지 못했다.',
       'scale_shape_orientation':'흰 곡선과 배경 구조의 형태·크기가 유지. 중앙 근처의 가는 수직 경계도 유지된다.',
       'visibility_color_brightness':'밝은 하늘색/흰 배경. 도시와 수면은 하단 띠에 보인다. 지속적인 발광 파동은 식별하지 못했다.',
       'internal_change':'8→9.2초 배경 하늘 평균 절대 RGB 차이 약0.009, 도시/수면 약0.058이며 채널 차이10 초과 픽셀 없음. 14.8→15.2초 이들 영역은 비교상 동일. 9.2→14.8초의 약0.24/0.72 차이는 주로 아주 작은 RGB 차이이며 구조 이동 근거로 부족하다.',
       'overlap_order':'밝은 카드들이 도시 위쪽 하늘 공간 앞에 놓이고 도시/수면은 카드 아래에서 계속 읽힌다.',
       'easing':'위치·형태 변화가 보이지 않아 위치/크기 가감속 비적용. 아주 작은 RGB 차이를 별도 밝기 애니메이션으로 분류하지 않았다.',
       'evidence':[orig(E04,240,'8'),orig(E04,276,'9.2'),orig(E04,444,'14.8'),orig(E04,456,'15.2'),orig(E04,540,'18'),{'path':str(OUT/'T04_hold_diff_exploratory.json')}]},
      {'object_id':'T04-left-type','subject':'왼쪽 회사 로고, 빨간 01, 실적 및 계획, 2026년 1~8월 누적 실적, 빨간 짧은 밑줄, 회색 작은 문장',
       'time_seconds':[6.4,18],'position_direction':'상단 왼쪽부터 세로로 정렬된 위치를 유지. 작은 문장은 ‘더 나은 내일을 위한 지속 가능한 성장을 만들어가겠습니다.’로 읽힌다.',
       'scale_shape_orientation':'문자와 로고 크기·수평/수직 정렬 유지. 빨간 밑줄은 같은 길이에 머물며 독립된 선 그리기 진행은 보이지 않는다.',
       'visibility_color_brightness':'로고 빨강/파랑, 01과 밑줄 빨강, 제목·부제 남색, 작은 문장 회색을 유지. 도입 dissolve 이후 독립적 점멸/색 교체 없음.',
       'internal_change':'문구 변경 없음. 8→9.2초 좌측 영역의 평균 절대 RGB 차이0.009,16.8→18초0.00055로 관측상 유지.',
       'overlap_order':'상단 흰 곡선·밝은 배경 앞. 세 카드보다 왼쪽에 분리되어 배치.',
       'easing':'6.4초 이후 위치/크기 변화가 없어 비적용. 도입 가시성은 T04-transition에 기록.',
       'evidence':[orig(E04,195,'6.5'),orig(E04,276,'9.2'),orig(E04,540,'18'),{'path':str(OUT/'T04_left_detail_native.png'),'actual_frame_time_seconds':6.5}]},
      {'object_id':'T04-card-shells','subject':'세 개의 밝은 둥근 사각 카드, 흰 외곽선/옅은 그림자, 큰 연파랑 01/02/03, 수주/매출/영업이익 제목, 가로 구분선·작은 라벨',
       'time_seconds':[6.4,18],'position_direction':'수주-매출-영업이익이 왼쪽에서 오른쪽 순서로 나란하며 카드 외곽·제목·구분선 위치가 유지.',
       'scale_shape_orientation':'라운드 사각형, 일정한 카드 크기와 수평 배열 유지. 각 카드의 목표/실적 막대 바닥선과 원형 중심도 고정.',
       'visibility_color_brightness':'흰/매우 옅은 하늘색 카드, 연파랑 번호와 가는 선, 남색 제목/라벨을 유지.',
       'internal_change':'각 카드에 2026년 목표,1~8월 실적,달성률 라벨이 처음부터 보인다. 실적 내용만 차례로 활성화되며 카드 자체는 이동하지 않는다.',
       'overlap_order':'독립 카드 사이에 작은 간격. 그래프는 카드 안쪽에 유지되며 인접 카드 침범 없음.',
       'easing':'도입 이후 외곽 위치·크기 가감속 비적용. 카드 고정만으로 내부 정지 판정을 하지 않았다.',
       'evidence':[orig(E04,195,'6.5'),orig(E04,240,'8'),orig(E04,480,'16'),orig(E04,540,'18'),{'path':str(OUT/'T04_card1_native_sequence.png')},{'path':str(OUT/'T04_card2_native_sequence.png')},{'path':str(OUT/'T04_card3_native_sequence.png')}]},
      {'object_id':'T04-goal-rings','subject':'각 카드의 회청색 목표 막대·60억/64억/7억 및 연회색 빈 도넛 링',
       'time_seconds':[6.4,18],'position_direction':'각 목표 막대는 같은 고정 바닥선과 높이, x위치에 유지. 세 카드 목표값은 서로 다르지만 목표 막대 높이는 비슷하다.',
       'scale_shape_orientation':'목표 막대 폭·높이와 도넛 원의 전체 크기 유지. 회색 링은 이후 파란 호가 차지하지 않은 부분에 남는다.',
       'visibility_color_brightness':'목표 막대와 목표값은 도입부터 표시. 파란 실적이 활성화되기 전까지는 실적 막대/값 및 도넛 중앙 %가 비어 있다.',
       'internal_change':'수주 빈 상태는8.0까지, 매출은15.4까지, 영업이익은16.666667의 기본 표본까지 보인다. 그래프별로 회색 배경을 유지하는 시간이 다르다.',
       'overlap_order':'파란 호가 회색 링을 시계 방향으로 차지하며 회색의 가시 각도가 줄어든다. 목표 막대와 실적 막대는 별도 x에서 나란히 비교된다.',
       'easing':'목표 막대의 높이 변화는 관측되지 않아 비적용. 회색 호의 가시 범위 변화는 파란 호 이벤트와 함께 기록.',
       'evidence':[orig(E04,240,'8'),orig(E04,462,'15.4'),orig(P04,500,'50/3'),orig(E04,540,'18')]},
      graph_event('T04-orders','수주','60억',[8,9.2],
        [{'time':8,'actual':None,'percent':None},{'time':8.1,'actual':'12억','percent':20},{'time':8.2,'actual':'22억','percent':37},{'time':25/3,'actual':'33억','percent':56},{'time':8.4,'actual':'38억','percent':63},{'time':8.6,'actual':'47억','percent':79},{'time':8.8,'actual':'52억','percent':88},{'time':9,'actual':'55억','percent':91},{'time':9.2,'actual':'55억','percent':92}],
        {'actual':'55억','percent':92},[9.2,18],
        [orig(E04,240,'8'),orig(E04,243,'8.1'),orig(E04,246,'8.2'),orig(P04,250,'25/3'),orig(E04,258,'8.6'),orig(E04,270,'9'),orig(E04,276,'9.2'),{'path':str(OUT/'T04_card1_native_sequence.png'),'actual_frame_times_seconds':[7.8,8,8.1,8.2,8.4,8.6,8.8,9,9.2]}]),
      graph_event('T04-sales','매출','64억',[15.4,16.6],
        [{'time':15.4,'actual':None,'percent':None},{'time':15.6,'actual':'9억','percent':14},{'time':47/3,'actual':'14억','percent':21},{'time':15.8,'actual':'22억','percent':34},{'time':16,'actual':'31억','percent':48},{'time':16.2,'actual':'36억','percent':56},{'time':16.4,'actual':'38억','percent':60},{'time':16.6,'actual':'39억','percent':61}],
        {'actual':'39억','percent':61},[16.6,18],
        [orig(E04,462,'15.4'),orig(E04,468,'15.6'),orig(E04,474,'15.8'),orig(E04,480,'16'),orig(E04,486,'16.2'),orig(E04,498,'16.6'),{'path':str(OUT/'T04_card2_native_sequence.png'),'actual_frame_times_seconds':[14.8,15,15.2,15.4,15.6,15.8,16,16.2,16.4,16.6,16.8]}]),
      graph_event('T04-profit','영업이익','7억',[50/3,17.6],
        [{'time':50/3,'actual':None,'percent':None},{'time':16.8,'actual':'1억','percent':7},{'time':17,'actual':'3억','percent':41},{'time':17.2,'actual':'4억','percent':60},{'time':17.4,'actual':'5억','percent':68},{'time':17.6,'actual':'5억','percent':71},{'time':17.8,'actual':'5억','percent':71},{'time':18,'actual':'5억','percent':71}],
        {'actual':'5억','percent':71},[17.6,18],
        [orig(P04,500,'50/3'),orig(E04,504,'16.8'),orig(E04,510,'17'),orig(E04,516,'17.2'),orig(E04,522,'17.4'),orig(E04,528,'17.6'),orig(E04,540,'18'),{'path':str(OUT/'T04_card3_native_sequence.png'),'actual_frame_times_seconds':[16.4,16.6,16.8,17,17.2,17.4,17.6,17.8,18]}])
    ],
    'temporal_order':[{'time_window':[6,6.4],'event':'표지에서 실적 화면으로 겹쳐 사라짐/나타남'},{'time_window':[6.4,8],'event':'세 카드와 회색 목표/링 상태 유지'},{'time_window':[8,9.2],'event':'수주 실적과 달성률 증가'},{'time_window':[9.2,15.4],'event':'수주 완성 상태·나머지 빈 실적을 오래 유지'},{'time_window':[15.4,16.6],'event':'매출 증가'},{'time_window':[50/3,17.6],'event':'영업이익 증가'},{'time_window':[17.6,18],'event':'세 그래프 최종값 유지; 구간 안에서 퇴장 없음'}],
    'implementation_hypotheses':[{'hypothesis':'처음의 두 화면을 가시성 혼합으로 전환했을 수 있다.','basis':'고정된 두 화면 내용의 중첩과 단조로운 가시성 변화','not_established':'실제 opacity keyframe, gamma, easing 함수 또는 편집 효과'},{'hypothesis':'막대 높이, 도넛 호의 가시 각도, 숫자 표시를 각 카드의 공통 진행도에 연결했을 수 있다.','basis':'한 카드 안의 세 표현이 동시 증가하고 같은 최종 상태에 도달','not_established':'레이어 수, scaleY 대 path 변화 대 마스크, trim path 사용, 숫자 표현식, 반올림 규칙'}],
    'uncertainty_summary':['활성 시작은 수주8.0~8.1초, 매출15.4~15.6초, 영업이익16.666667~16.8초 사이이며 더 촘촘한 전 프레임 검사는 하지 않았다.','숫자의 각 중간 단계는 표본값이며 매 프레임 증감 규칙과 정확한 종료 프레임은 확정하지 않았다.','감속 경향은 긍정적으로 관측되나 정확한 curve·초기 가속·키프레임 함수는 미분류.','새 배경 수면·하늘의 독립 움직임은 표본 비교에서 확인되지 않았으며 움직인다고 추정하지 않았다.'],
    'extraction_issues':['기본 제공 T04 PNG는 로그상 1920×540으로 원본3840×1080의 절반 크기였다. 이에 원본 폭3840으로 32개 추가 프레임을 bounded helper로 성공 추출했다.','추가 추출 로그는 목표 선택 완료·PTS 매핑 일치를 보고한다.','오디오 미분석, SAR 불명 및 색 범위 검증 미완료.']
}

generated_visuals={
    'T01':['T01_artifact_native_sequence.png','T01_body_native_sequence.png','T01_left_sequence.png','T01_subframe_artifact_sequence.png','T01_held_texture_sequence.png'],
    'T04':['T04_transition_sequence.png','T04_card1_native_sequence.png','T04_card2_native_sequence.png','T04_card3_native_sequence.png','T04_left_detail_native.png']
}
audit_files=[OUT/'explore_reads.json',OUT/'explore2_reads.json',OUT/'explore3_reads.json']
audit_paths=[]
for p in audit_files:audit_paths+=readj(p)
for obj,case_folder,extra_folder,boards in [(t01,P01,E01,['board_1.jpg','board_2.jpg']),(t04,P04,E04,['board_1.jpg','board_2.jpg','board_3.jpg','board_4.jpg'])]:
    obj['files_read']={
      'manual_input_text':[str(IN/'PROCEDURE.md'),str(IN/'cases.json'),str(IN/'inspect_more.py'),str(case_folder/'실행기록.json'),str(extra_folder/'실행기록.json')],
      'manual_overview_images':[str(case_folder/b) for b in boards],
      'source_pngs_read_for_visualization_or_measurement':sorted(set(p for p in audit_paths if str(case_folder) in p or str(extra_folder) in p)),
      'own_derived_files_read': [str(OUT/n) for n in generated_visuals[obj['case_id']]] + [str(p) for p in audit_files] + ([str(OUT/'T01_geometry_exploratory.json'),str(OUT/'T01_hold_diff_exploratory.json')] if obj['case_id']=='T01' else [str(OUT/'T04_hold_diff_exploratory.json')]),
      'own_scripts_executed':[str(OUT/'explore.py'),str(OUT/'explore2.py'),str(OUT/'explore3.py'),str(OUT/'save_first_pass.py')],
      'bounded_helper_indirect_reads':{'media_path':next(c['media_path'] for c in readj(IN/'cases.json')['cases'] if c['case_id']==obj['case_id']), 'helper_dependencies':[str(IN/'bounded_base.py'),str(ROOT.parent/'phase01a-a2/prepare.py'),str(ROOT.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json')], 'note':'승인된 inspect_more.py 실행이 내부적으로 사용한 경로다. 이 의존 파일들의 본문을 분석 목적으로 직접 열람하지 않았다. Python/Pillow/NumPy/PyAV의 시스템·라이브러리 파일은 이 작업 자료 열람 목록에서 제외.'}
    }
    obj['first_pass_preservation']='이 JSON과 대응 .md는 exclusive-create 모드로 최초 한 번 저장했다. 이후 보완은 별도 파일명으로만 수행해야 한다.'

md01='''# T01 최초 관찰 — 3.500~5.500초

왼쪽의 직사각형 구간들이 서로 시간차를 두고 오른쪽으로 들어와 큰 E로 정렬된다. 상단 가로 구간이 먼저 보이며, 이후 여러 높이의 구간이 계단처럼 어긋난 상태를 거쳐 4.8~5.1초 무렵 왼쪽 경계가 맞는다. 상단 오른쪽 끝의 근사 좌표는 3.7초 x1084 → 4.0초 x1772 → 4.4초 x2078 → 4.8초 x2153이다. 후반 이동량이 줄어드는 감속은 확인되며 정확한 보간 함수는 알 수 없다. 초록 조각은 올리브/갈색을 거쳐 금빛 주황으로 밝아진다.

E 외곽이 정착한 뒤에도 내부를 정지로 처리할 수 없다. 도로/교차로 같은 도면의 윤곽은 유지되지만 5.1~5.5초 격자와 도면선·바탕 밝기가 변한다. 5.1→5.3초 원본 내부 크롭의 평균 절대 RGB 차이는 약7.05이며 같은 시기 고정 배경보다 크다. 독립된 도면 이동 방향이나 주기까지는 확인하지 못했다.

오른쪽 EG-BIM은 이미 보이는 상태에서 가로 폭이 아주 조금 좁아져 정착한다. 영문 부제는 약10px 올라가고, 한국어 설명은 위 두 줄이 먼저, 아래 두 줄이 나중에 위로 올라가며 밝아진다. 각 묶음의 이동량은 끝부분에서 작아진다. 배경 Value of·격자·사각 패널의 위치는 유지된다.

3.5초의 작은 보조 변화도 있다. 배경 of의 아래 흰 부분은 3.516667초 더 얇아지고 3.533333초에는 사라진다. 제목 뒤 청록 잔상 띠는 아래쪽으로 좁아지며 사라지고, 오른쪽의 녹색 세로선·붉은 가로선/작은 사각 표시도 3.6초에 거의 소실된다. 실제 편집 핸들인지 여부는 단정하지 않았다. 본문 아래 얇은 검은 수평선은 높이가 유지되며 E와의 겹침 때문에 보이는 범위가 달라진다.

근거: 기본 PNG 21개와 1/60초 간격을 포함한 추가 PNG 12개. `T01_subframe_artifact_sequence.png`, `T01_body_native_sequence.png`, `T01_held_texture_sequence.png` 및 JSON의 실제 시점/경로를 참조한다. 원본은3840×2160이며 오디오·정밀 SAR·절대 색범위는 검증하지 않았다. 위치/가시성/내부 광량의 관측과 레이어·마스크·키프레임 가설은 JSON에서 분리했다. 최초 결과이며 채점·기대 답안은 읽지 않았다.
'''
md04='''# T04 최초 관찰 — 6.000~18.000초

6.0초 교량 표지 화면이 6.1~6.3초 옅어지는 동안 실적 및 계획 화면의 로고·문구·세 카드와 도시 수변 배경이 같은 자리에서 나타난다. 6.4~6.5초에는 새 화면만 읽힌다. 두 화면의 중첩과 후반 변화량 감소를 관측했으며, 실제 전환 효과·opacity 곡선은 확정하지 않았다.

새 화면의 카드 외곽·제목·구분선·작은 라벨·회색 목표 막대는 고정이고 내부 실적만 차례로 변한다. 수주에서는 8.0초 빈 상태 → 8.1초12억/20% → 8.4초38억/63% → 9.0초55억/91% → 9.2초55억/92%가 보인다. 이후 이 값은18초까지 유지된다. 매출은15.4초 빈 상태 → 15.6초9억/14% → 16.0초31억/48% → 16.6초39억/61%로 진행한다. 영업이익은16.666667초 빈 상태 → 16.8초1억/7% → 17.0초3억/41% → 17.6초5억/71%에 도달해18초까지 유지된다.

각 파란 막대는 바닥선을 고정하고 위로 자라며 폭은 유지된다. 실적 숫자는 막대 위를 따라 올라간다. 도넛은 중심/반지름을 유지하면서12시에서 시계 방향으로 파란 호가 늘고 중앙 %가 증가한다. 회색 호는 남은 부분에 계속 보인다. 각 증가의 후반 변화량이 작아져 감속 정착하는 경향은 확인되며, 최초 활성 프레임과 극초반 가속·정확한 보간 함수는 표본 사이여서 미분류다.

왼쪽 로고·빨간01·실적 및 계획·부제·짧은 빨간 선·회색 작은 문구, 상단 흰 곡선, 하늘·도시·강·반사는 도입 이후 위치와 형태를 유지한다. 하늘/수면의 자체 이동은 원본 표본 비교에서 확인되지 않았다. 카드가 고정되어 있다는 이유로 내부 그래프까지 정지로 취급하지 않았다.

기본 제공 PNG는1920×540으로 축소되어 있어 허용 구간 안에서3840×1080 PNG32개를 추가 추출했다. `T04_transition_sequence.png`와 세 `T04_card*_native_sequence.png`, 실제 프레임 시점/경로는 JSON에 기록했다. 추출/PTS 매핑은 로그상 완료이나 오디오·정밀 SAR·절대 색범위는 검증하지 않았다. 최초 결과이며 채점·기대 답안은 읽지 않았다.
'''

outputs=[(OUT/'T01_observations.json',json.dumps(t01,ensure_ascii=False,indent=2)),(OUT/'T01_narrative.md',md01),(OUT/'T04_observations.json',json.dumps(t04,ensure_ascii=False,indent=2)),(OUT/'T04_narrative.md',md04)]
for p,content in outputs:
    if p.exists():raise FileExistsError(f'Preserve first pass: {p}')
for p,content in outputs:
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(content+'\n')
print(json.dumps({'saved_once':[str(p) for p,_ in outputs]},ensure_ascii=False,indent=2))
