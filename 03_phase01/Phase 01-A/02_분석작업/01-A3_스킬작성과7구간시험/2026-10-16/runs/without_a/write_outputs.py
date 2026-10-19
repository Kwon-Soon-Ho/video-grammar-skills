import json
from pathlib import Path
from fractions import Fraction
root=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기')
base=root/'phase01a-a2-retest/analysis_input/cases/자료013'
case_data={x['case_id']:x for x in json.loads((root/'phase01a-a3/analysis_input/cases.json').read_text('utf-8-sig'))['cases'] if x['case_id'] in ['T01','T02','T03']}
def claim(id,text,times,confidence='high',uncertainty=None):
 return {'id':id,'type':'observation','claim':text,'actual_times_seconds':times,'confidence':confidence,'uncertainty':uncertainty}
data={
'T01':{
'summary':'짙은 청록색 기술 도면풍 배경과 오른쪽 EG-BIM 설명을 유지하면서, 왼쪽에서 서로 어긋난 직사각형 띠들이 들어와 거대한 E를 이룬다. E 표면은 녹색에서 황금빛 주황색으로 바뀌고 내부 도면 선이 드러난다.',
'claims':[
claim('O1','화면 바탕은 중앙이 조금 밝고 가장자리가 어두운 청록색이다. 격자, 겹친 사각 패널, 가로 빛띠가 있으며 큰 Value of 문구가 저대비로 배경에 남아 있다.',[3.5,4.2,5.5]),
claim('O2','3.5초에는 Value of의 오른쪽 아래에 밝은 흰 부분이 조금 남지만, 3.6초에는 전체가 어두운 배경 글자처럼 보인다. 오른쪽 아래 쪽 흰 EG-BIM 제목, 그 아래 Engineering Graphicer for BIM, 한글 설명은 유지된다. 영문 부제의 E, G, BIM이 노란색으로 강조된다.',[3.5,3.6,4.2,5.5]),
claim('O3','왼쪽 화면 경계에서 녹색 직사각형들이 오른쪽으로 진입한다. 3.6초에는 상단 띠가 먼저 길게 들어오고 그 아래 띠들은 덜 들어와 있다. 3.9초에는 위에서 아래로 서로 다른 위치의 다섯 가로 구간이 분명하다. 4.2초에도 위·중간·아래 가로획과 사이의 세로 연결부가 좌우로 어긋난 E 형상이다. 하나의 완성된 E가 동일 속도로 통째 이동하는 모습과는 다르다.',[3.6,3.9,4.2]),
claim('O4','4.2초 이후 각 구간의 왼쪽 경계가 점차 맞춰진다. 4.5초에는 작은 계단 차이가 남고 4.8초에는 차이가 더 작아진다. 5.1초에는 왼쪽 세로 가장자리가 거의 일직선인 큰 E가 된다. E는 왼쪽 절반가량을 차지하며 위와 아래가 화면 밖으로 잘려 있다. 관측상 이동량은 후반으로 갈수록 줄어든다.',[4.2,4.5,4.8,5.1,5.5]),
claim('O5','E 안의 색과 무늬도 변한다. 3.9초에는 주로 녹색 면이고 4.2초에는 연한 올리브색 위에 가는 곡선·다중 평행선·작은 기호가 보인다. 4.5초 황갈색을 거쳐 4.8~5.1초 밝은 주황/금색이 된다. 도로 선형도처럼 휘어진 여러 선과 격자가 E 내부에서 잘려 보인다.',[3.9,4.2,4.5,4.8,5.1],uncertainty='도면의 정확한 공종·지명·수치는 판독하지 않았다.'),
claim('O6','E가 배경의 Value of와 격자를 가리며 전경으로 올라온다. 오른쪽 제목과 설명은 이 과정에서 같은 영역에 머문다. 마지막 5.1~5.5초에는 E의 큰 형태가 유지되어 제목을 읽을 수 있는 구도가 된다.',[4.2,4.8,5.1,5.5])],
'hypotheses':[
{'claim':'E 또는 E 모양의 이미지 합성을 수평 구간으로 나눠 각 구간의 X 위치를 시차 있게 애니메이션했을 가능성이 높다. 마지막 이동량 감소는 감속 보간과 양립한다.','basis':['O3','O4'],'confidence':'medium','uncertainty':'실제 레이어 수, 마스크 구조, 키프레임·이징 수식은 출력 영상에서 확정할 수 없다.'},
{'claim':'도면 이미지를 E 모양에 클리핑하고 색·불투명도 또는 이미지 혼합을 변화시켰을 수 있다.','basis':['O5'],'confidence':'medium','uncertainty':'색상 보간, 별도 오버레이 페이드, 매트 처리 중 무엇을 썼는지 판별할 수 없다.'}],
'uncertainty':['시간은 제공된 0.1초 간격 프레임의 실제 재생 시각이다. 조립과 색 변화의 정확한 시작·종료 프레임은 표본 사이에 있을 수 있다.','글자와 도면은 시각 그래픽으로 관찰했으며 실제 CAD 프로그램 조작이나 제작 소프트웨어를 확인한 것은 아니다.'],
'png_direct':['f_00252_004.200.png'],
'detail_times':[3.6,3.9,4.2,4.5,4.8,5.1]
},
'T02':{
'summary':'녹색 그라데이션 바탕에서 어두운 직사각형 패널들이 왼쪽으로부터 들어오고, 격자와 얇은 프레임·가로 광선이 드러난다. 후반에는 빨강 가로선과 초록 세로선의 십자 표시가 왼쪽 위에서 오른쪽 아래 방향으로 움직인다.',
'claims':[
claim('O1','0.0초에는 중앙이 밝고 네 모서리가 어두운 청록색 그라데이션이 화면을 채운다. 읽을 수 있는 문구나 인물은 없다. 0.15초도 거의 같은 바탕이지만 왼쪽의 어두운 형태가 아주 희미하게 나타난다.',[0,0.15],uncertainty='초기 형태는 저대비이므로 처음 한 픽셀이라도 나타나는 시점은 특정하지 않는다.'),
claim('O2','0.25초에 왼쪽 위의 어두운 가로 직사각형이 식별된다. 0.4~0.7초에는 위쪽의 긴 어두운 패널, 왼쪽 중간의 밝은 작은 패널, 아래쪽의 녹색 가로 패널과 겹친 어두운 띠가 오른쪽으로 확장되거나 이동해 들어온다. 각 띠의 오른쪽 끝이 서로 다른 위치·속도로 진행한다.',[0.25,0.4,0.5,0.7]),
claim('O3','0.4~0.7초 사이에 직교 격자와 그 바깥쪽의 얇은 직사각형 선틀이 점점 잘 보인다. 위쪽과 왼쪽 아래에는 가로로 번지는 청록색 빛띠가 있다. 1.0~1.4초에는 선틀·격자와 패널이 겹친 기술 화면풍 바탕이 뚜렷하다.',[0.4,0.7,1,1.4]),
claim('O4','패널의 이동은 초반에 크고 0.9초 이후에는 작은 위치 변화만 보인다. 1.0~1.4초에는 전체 구도가 거의 안정된다. 배경의 광량·대비 변화가 패널 진입과 동시에 진행된다.',[0.4,0.7,0.9,1,1.4],confidence='medium',uncertainty='별도의 수치 추적 없이 시간순 프레임을 비교한 상대적 속도 관측이다.'),
claim('O5','0.95~1.0초 왼쪽 위 부근에 가는 색선 표시가 희미하게 보인다. 1.2초에는 빨강 가로선과 초록 세로선이 교차하는 십자 표시를 분명히 구별할 수 있다. 1.2, 1.3, 1.4초 순서에서 그 교점이 오른쪽 아래로 이동한다. 1.4초까지 텍스트는 보이지 않는다.',[0.95,1,1.2,1.3,1.4],uncertainty='저대비 시작 부분의 정확한 최초 등장 프레임은 미확정이다.')],
'hypotheses':[
{'claim':'직사각형 여러 개의 수평 위치와 불투명도 애니메이션, 격자·광선 오버레이를 겹쳐 만든 배경일 가능성이 있다.','basis':['O2','O3','O4'],'confidence':'medium','uncertainty':'위치 이동과 폭 확장의 조합을 완전히 분리할 수 없고, 실제 레이어 구조나 사용 도구는 알 수 없다.'},
{'claim':'빨강/초록 십자는 도면 또는 그래픽 편집 환경의 커서/좌표 표시를 연상시키는 장치로 보인다.','basis':['O5'],'confidence':'medium','uncertainty':'실제 프로그램 커서의 녹화인지 별도 애니메이션인지 이 구간만으로 확정할 수 없다.'}],
'uncertainty':['제공 프레임 간격은 0.05초이며 그 사이의 첫 등장 시각이나 정확한 정지 시점은 주장하지 않는다.','검정에 가까운 녹색 그래픽이 많아 첫 0.2초의 미세한 경계는 화면 밝기와 축소에 영향을 받는다.','이 구간의 시각 내용만 분석했으며 음성·음악은 듣지 않았다.'],
'png_direct':['f_00030_000.500.png'],
'detail_times':[0,0.15,0.25,0.4,0.7,1.4]
},
'T03':{
'summary':'배경의 빨강/초록 십자가 이동한 뒤, 점선 사각 영역이 우하향으로 커지면서 흰 Value of 문구가 드러난다. 이후 EG-BIM과 부제가 오른쪽 아래에 나타나고, Value of의 밝은 영역은 축소되어 흐린 배경 글자만 남는다.',
'claims':[
claim('O1','1.0초부터 청록색 격자·다중 사각 패널·가로 빛띠가 배경을 이룬다. 1.2~1.8초에 빨강 가로선과 초록 세로선이 교차하는 십자 표시가 왼쪽 위에서 오른쪽 아래 방향으로 이동한다. 1.8초까지 큰 흰 제목은 아직 없다.',[1,1.2,1.4,1.6,1.8]),
claim('O2','1.9초에 작은 밝은 글자 조각과 짧은 사각 영역이 등장한다. 2.0초에는 V의 윗부분만, 2.1초에는 Val과 다음 글자 일부가 보인다. 점선 사각형의 위·왼쪽 기준은 대체로 유지되고 오른쪽·아래 경계가 뻗으면서 보이는 글자 면적이 넓어진다. 십자는 늘어나는 영역의 오른쪽 끝 부근에 함께 움직인다.',[1.9,2,2.1,2.2,2.3]),
claim('O3','2.2초에는 Value, 2.3초에는 Value o와 f 일부, 2.4초에는 Value of 전체를 읽을 수 있다. 2.5~2.7초에는 큰 굵은 흰 문구가 상단 중앙의 넓은 점선 사각형 안에 머문다. 십자 교점은 사각형의 오른쪽 아래 부근에 자리한다.',[2.2,2.3,2.4,2.5,2.6,2.7]),
claim('O4','2.8초부터 큰 문구 아래 오른쪽 쪽에 E와 M처럼 분리된 회색/흰 글자 조각이 나타난다. 3.0~3.2초에 하이픈과 B, G 등 나머지 부분이 점차 나타나며 3.3~3.6초에는 EG-BIM으로 모인다. 바로 아래 Engineering Graphicer for BIM 부제가 3.0초에는 희미하고 이후 더 밝아진다. E·G·BIM 부분은 노란색이다.',[2.8,2.9,3,3.1,3.2,3.3,3.6]),
claim('O5','3.1~3.5초 Value of의 흰 부분은 한꺼번에 어두워지기보다 왼쪽·위쪽에서 먼저 사라진다. 점선 사각형의 왼쪽·위쪽 경계가 오른쪽 아래로 진행해 흰 글자를 잘라 내고, 지나간 위치에 같은 문구의 어두운 모습이 남는다. 3.4초에는 오른쪽의 ue of 위주로 밝게 남고, 3.5초에는 of의 아래쪽 일부만 밝다. 3.6초에는 밝은 제목과 점선 영역이 없어지고 흐린 Value of만 배경에 남는다.',[3.1,3.2,3.3,3.4,3.5,3.6]),
claim('O6','3.2~3.6초에 EG-BIM 아래 한글 여러 줄 설명이 밝아진다. 최종 구도는 흐린 Value of를 뒤에 두고 오른쪽 아래에 흰 EG-BIM, 노랑 강조가 섞인 영문 부제, 작은 흰 한글 설명을 배치한 모습이다.',[3.2,3.3,3.4,3.6,3.8]),
claim('O7','3.5초부터 화면 왼쪽 위에 새로운 두꺼운 녹색 직사각형이 들어온다. 3.6~3.8초에는 서로 다른 높이의 녹색 구간들이 왼쪽 경계로부터 우측으로 진입하여 다음 형태를 만들기 시작한다. 이 허용 구간 끝에서는 완성된 형태를 확정하지 않는다.',[3.5,3.6,3.7,3.8])],
'hypotheses':[
{'claim':'점선 영역의 확대와 축소에 맞춘 글자 노출은 사각 마스크/매트의 경계를 애니메이션한 방식과 잘 맞는다. 흰 제목 아래에 낮은 불투명도의 동일 문구를 둔 구조일 수 있다.','basis':['O2','O3','O5'],'confidence':'medium-high','uncertainty':'마스크·매트·클리핑의 실제 사용 여부, 별도 텍스트 복제 여부는 출력만으로 확정할 수 없다.'},
{'claim':'십자와 점선은 CAD나 편집 화면의 드래그 선택 동작을 시각적으로 흉내 낸 연출로 해석할 수 있다.','basis':['O1','O2','O3'],'confidence':'medium','uncertainty':'실제 앱 화면 녹화인지 합성 그래픽인지 확정 불가.'},
{'claim':'EG-BIM은 글자별 시간차 노출이나 불투명도/위치 애니메이션을 사용했을 가능성이 있다.','basis':['O4'],'confidence':'medium','uncertainty':'각 글자의 정확한 이동 경로, 순서의 모든 중간 상태, 텍스트 애니메이터 설정은 확인하지 못했다.'}],
'uncertainty':['제공된 표본은 0.1초 간격이다. 시작·완료 시각은 관측 프레임 기준이며 프레임 사이 경계는 확정하지 않는다.','격자와 배경은 유지되지만 아주 작은 변화를 정량화하지 않았다.','한글 설명의 모든 문장을 원문 전사하는 데 목적을 두지 않았다. 오디오 분석은 수행하지 않았다.'],
'png_direct':['f_00126_002.100.png'],
'detail_times':[1.8,1.9,2,2.1,2.3,2.6,3.1,3.2,3.3,3.4,3.5,3.6]
}}
for case,d in data.items():
    folder=base/case
    log=json.loads((folder/'실행기록.json').read_text('utf-8-sig'))
    frame_by_t={float(Fraction(f['actual_playback_seconds'])): f for f in log['frames']}
    for c in d['claims']:
        c['evidence']=[{'path':frame_by_t[t]['path'],'actual_playback_seconds':t,'actual_playback_seconds_rational':frame_by_t[t]['actual_playback_seconds'],'viewed_via':'provided board; selected frames also viewed directly or in detail contact sheet'} for t in c['actual_times_seconds']]
    boards=sorted(folder.glob('board_*.jpg'))
    native_read=set(d.pop('png_direct'))
    for t in d.pop('detail_times'): native_read.add(f'f_{round(t*60):05d}_{t:07.3f}.png')
    d.update({'case_id':case,'condition':'without_skill','allowed_window_seconds':case_data[case]['allowed_window_seconds'],'prompt':case_data[case]['prompt'],'asset_id':case_data[case]['asset_id'],'source_media':case_data[case]['media_path'],'source_sha256':case_data[case]['media_sha256'],'timing_basis':log['timing_status'],'sampling_interval_seconds':0.05 if case=='T02' else 0.1,'audio_status':'not listened, decoded or transcribed','additional_source_extraction':False,'files_read':[str(root/'phase01a-a3/analysis_input/cases.json'),str(folder/'실행기록.json'),str(folder/'boards.json')]+[str(b) for b in boards]+[str(folder/n) for n in sorted(native_read)]+[str(root/f'phase01a-a3/runs/without_a/{case}_detail.png')],'evidence_access_note':'All supplied contact boards for this case were visually inspected in temporal order. Individual PNGs listed in files_read were loaded directly or read to generate the inspected detail board. PNG paths in claim evidence identify the corresponding source frame even when inspected through its supplied board. No skill, answer file, prior report, or other case output was consulted.','output_policy':'First final output; created exclusively and must be preserved.'})
    dest=root/f'phase01a-a3/company-video-grammar-analyzer-workspace/iteration-1/eval-{case}/without_skill/outputs'
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/'observations.json').open('x',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
    lines=[f'# {case} 관측 기록',f"\n허용 구간: {d['allowed_window_seconds'][0]}–{d['allowed_window_seconds'][1]}초. 관측 프레임 간격: {d['sampling_interval_seconds']}초. 시각은 실행기록의 실제 재생 시각이다.", '\n'+d['summary'],'\n## 화면에서 관측한 내용']
    for c in d['claims']:
        lines += [f"\n- **{c['id']} · {', '.join(f'{t:.2f}' for t in c['actual_times_seconds'])}초**: {c['claim']}", f"  신뢰도: {c['confidence']}."+(f" 한계: {c['uncertainty']}" if c['uncertainty'] else ''), '  근거: '+', '.join(f"[{Path(e['path']).name}]({e['path'].replace(chr(92),'/')})" for e in c['evidence'])]
    lines += ['\n## 구현 추정']
    for h in d['hypotheses']: lines += [f"\n- {h['claim']} 근거: {', '.join(h['basis'])}. 신뢰도: {h['confidence']}. 한계: {h['uncertainty']}"]
    lines += ['\n## 불확실성과 확인 범위']+['\n- '+u for u in d['uncertainty']]+['\n오디오는 분석하지 않았다. 추가 원본 추출 없이 제공 보드, 선택 PNG와 그 파생 확대 보드를 사용했다. 제작 프로젝트나 스킬은 읽지 않았다.','\n## 읽은 파일']+['\n- '+x for x in d['files_read']]
    with (dest/'observations.md').open('x',encoding='utf-8') as f: f.write('\n'.join(lines)+'\n')
    print(case, len(d['claims']), 'claims saved', dest)
