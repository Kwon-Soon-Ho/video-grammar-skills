import json, sys
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'case-plan.json').read_text(encoding='utf-8'))
ROI=json.loads((ROOT/'with-b-roi/roi-log.json').read_text(encoding='utf-8'))
OUT=ROOT/'company-video-grammar-analyzer-workspace/iteration-1'
VIEWED={
'V03':[98,98.75,99,99.25,100,101,103.75,104],
'V04':[296,298.5,298.75,299,300.75,301,301.25,302],
'V06S':[232,233,234,235,235.5,236,236.5,237,238,238.5,239,239.5,240,240.5,241,242,244,244.5,245.5,246],
'V06W':[236,239,239.5,240.5,241,241.5,242.5,243,244,244.5,246,247,249.5,250]}
CROPS={
'V03':['V03_with_more_98.85','V03_with_more_98.95','V03_with_more_99.05','V03_with_more_99.15','V03_101.0','V03_104.0'],
'V04':['V04_with_more_300.85','V04_with_more_300.95','V04_with_more_301.05','V04_with_more_301.15','V04_with_more_301.3','V04_301.25','V04_301.5','V04_301.75','V04_302.0'],
'V06S':['V06S_242.0','V06S_244.0','V06S_246.0'],
'V06W':['V06W_244.5','V06W_247.0','V06W_249.0','V06W_250.0']}
def eid(t,roi=False):return ('r' if roi else 'f')+str(float(t)).replace('.','p')
def ev(desc,props,times,order,roi=False,kind='unknown',basis=None,status='observed',limits=None):
    return dict(description=desc,properties=props,time_seconds=[min(times),max(times)],evidence_ids=[eid(t,roi) for t in times],direction_order=order,easing=dict(property=props[0],classification=kind,basis=basis or '선택 표본은 변화 존재와 순서를 보여 주지만 동일 특징의 충분한 연속 변위/밝기 측정이 없어 곡선은 미확정.'),status=status,limitations=limits or [])
def ob(id,name,events,parent=None):return dict(id=id,name=name,parent=parent,events=events)
def create(cid):
    c=next(c for c in PLAN['cases'] if c['case_id']==cid)
    log=json.loads(Path(c['input_log']).read_text(encoding='utf-8'))
    evidence=[]
    for f in log['frames']:
        t=float(F(f['actual_playback_seconds']))
        if t in VIEWED[cid]:
            evidence.append(dict(id=eid(t),path=f['path'],actual_seconds=f['actual_playback_seconds'],role='within' if t<c['window_seconds'][1] else 'context_after',sha256=f['sha256'],source_frame_id=f['frame_id'],reported_pts=f['reported_pts'],time_base=f['time_base'],container_cts_ticks=f['container_cts_ticks'],display_ordinal_zero_based=f['display_ordinal_zero_based'],raster=f['raster'],view='native extracted PNG, tool display may downsample'))
    logs=[c['input_log']]
    for r in ROI:
        if r['id'] not in CROPS[cid]:continue
        src=json.loads(Path(r['extraction_log']).read_text(encoding='utf-8'))
        f=next(f for f in src['frames'] if f['frame_id']==r['source_frame_id'])
        t=float(F(r['actual_seconds']))
        evidence.append(dict(r,id=eid(t,True),role='within' if t<c['window_seconds'][1] else 'context_after',source_sha256=f['sha256'],reported_pts=f['reported_pts'],time_base=f['time_base'],container_cts_ticks=f['container_cts_ticks'],display_ordinal_zero_based=f['display_ordinal_zero_based'],view='view_image on native-coordinate ROI; no crop resizing in saved file'))
        if r['extraction_log'] not in logs:logs.append(r['extraction_log'])
    doc=json.loads(Path(c['document_record']).read_text(encoding='utf-8'))
    reads=[str(ROOT/'case-plan.json'),str(ROOT/'output-format.md'),str(ROOT/'skill-draft2/SKILL.md')]+[str(ROOT/'skill-draft2/references'/p) for p in ['evidence-and-records.md','motion-review.md','output-contract.md']]+[str(ROOT/'skill-draft2/scripts'/p) for p in ['evidence_catalog.py','check_observations.py']]+logs+[c['document'],c['document_record'],str(ROOT/'extract.py'),str(ROOT/'with-b-roi/roi-log.json'),str(ROOT/'with_b_crops.py'),str(ROOT/'with-b-evidence-catalog.json')]
    reads += [str(Path(c['input_log']).parent/f'board-{i}.jpg') for i in range(1,3 if cid in ['V03','V04'] else 4)]
    if cid in ['V03','V04']:reads += [str(ROOT/'with-b-more-evidence-catalog.json'),str(ROOT/'requests'/f'A4-L-{cid}_with_more.json')]
    return dict(schema_version='a3-observation-0.1',case_id=cid,source=c['source'],window_seconds=c['window_seconds'],method='개요 시트는 장면 탐색에만 사용. 실제 원본 해상도 PNG를 시간순으로 열람하고 정착 화면에서 요소별 시작을 역추적. 작은 UI/제목은 native 좌표 ROI 열람, V03/V04 짧은 경계는 추가 추출. 연속 재생/오디오 청취는 하지 않음. evidence에는 실제 열람한 이미지/ROI만 포함.',document_mode='provided_revision_document; production_before_or_after_and_approval_status_unverified',audio_reviewed=False,evidence=evidence,objects=[],coverage={},hypotheses=[],limitations=['반개방 구간 [start,end) 분석이며 정확히 end인 이미지는 context_after로만 사용.','선택 프레임 관찰로 프레임 사이 짧은 동작/정확한 시작과 종료를 모두 확인한 것은 아님.','렌더의 시각적 표현만 기록하며 실제 제품 기능·성능·수치 타당성을 인증하지 않음.','문서는 부모가 검증한 원본 메타데이터와 추출 텍스트/locator만 열람. 원본 PPTX/HWP 그림·레이아웃과 음성은 검수하지 않음.'],files_read=reads+[e['path'] for e in evidence],document_source={k:doc[k] for k in ['id','path','sha256','status']},document_correspondence=[])

d=create('V03')
d['objects']=[
ob('layout','전체 레이아웃/상단 제목/격자 바닥',[ev('흰 배경과 투시 격자 바닥, 상단 Easy & Simple 및 단순한 인터페이스 문장, 좌측 설명과 우측 EG-BIM 창의 배치는 유지된다.','position visibility'.split(),[98,99.25,101,103.75],'주제 교체 중에도 상위 틀 고정',kind='not_applicable',basis='정지 배치 관찰; 이동 곡선 대상 아님.')]),
ob('headline','좌측 두 줄 제목',[ev('기능별로 그룹화하여 / 차별화된 디자인에서 정보전달 방식의 / 이미지화로 교체. 98.95 첫 줄 새 글자가 위쪽에서 들어오고 구 글자가 아래로 잘린다. 99.05 첫 줄 교체 후 99.15 두 번째 줄의 같은 방향 교체가 시작된다.','position reveal'.split(),[98.85,98.95,99.05,99.15],'행별 아래 방향 masked replacement; 첫 줄→둘째 줄',True,basis='클리핑된 글자와 서로 다른 문자열이 겹쳐 동일 글자 위치 속도를 안정적으로 재지 못함.'),ev('99.25 새 제목이 읽히고 100–103.75 최종 제목 정착. 둘째 줄 이미지화는 녹색, 첫 줄은 검정.','visibility color'.split(),[99.25,100,103.75],'두 행 완성 후 유지')]),
ob('body','보조 문장/회색 영문/불릿',[ev('Grouping과 기존 설명이 약해지고 새 설명 및 Imaging이 나타난다. 100에는 Imaging의 왼쪽 일부와 옅은 본문, 101에는 전체 영문과 진한 본문이 보인다. 본문은 속성 정보를 이미지와 함께 시각적으로 표현한다는 내용.','visibility reveal'.split(),[98,98.75,100,101],'구 문구 소거→새 문구; 영문은 왼쪽부터 드러나는 양상',limits=['타이핑/마스크/opacity 등 구현 방식은 렌더만으로 미확정.']),ev('101에는 첫 불릿이 진하고 둘째가 옅으며 셋째는 아직 보이지 않는다. 103.75에는 세 불릿이 모두 보인다: 객체별 차별화 속성정보 창, 기본·형상·위치정보 구분, 가독성·가시성 증대.','visibility'.split(),[101,103.75,104],'위쪽 항목부터 아래쪽 항목으로 단계적 가시화',limits=['세 번째 항목의 정확한 시작과 각 항목 fade 곡선은 미확정.'])]),
ob('window','EG-BIM 외곽 창',[ev('큰 둥근 사각 창의 위치·크기는 유지되면서 내부가 기능 구획 안내에서 도형/속성 예제로 바뀐다.','position scale'.split(),[98,99.25,101,103.75],'외곽은 유지; 내부 내용 전환',kind='not_applicable',basis='외곽의 눈에 띄는 이동/크기 변화는 해당 표본에서 관측되지 않음.')]),
ob('guides','노란 메뉴 안내/점선 구획',[ev('객체 주요특성 메뉴, 홈 메뉴, 작업환경 아이콘바, 명령어 아이콘바 및 점선 구획이 98에 보이다가 98.75 약해지고 99에는 원/호 예시가 중심이 된다.','visibility'.split(),[98,98.75,99],'기존 안내 소거와 새 도형 등장 일부 중첩')],'window'),
ob('geometry','내부 원·호·십자·직선/화살표',[ev('98.75 노란 점선 원이 보이기 시작하고 99에 원과 흰 호가 선명하다. 99.25 십자 조준점 및 아래 사선들이 옅게 나타나며 100–101에 아래 일반 선/양방향 화살표/단방향 화살표가 선명해진다.','visibility shape'.split(),[98.75,99,99.25,100,101],'상단 원·호→십자/하단 사선; 일부 중첩',limits=['각 선의 끝점 이동으로 그려지는지 전체 fade인지 모두 분리하지 못함.'])],'window'),
ob('panel','원 객체 속성 패널/호출 라벨',[ev('99.25 오른쪽 속성 패널이 어둡게 보이고 100–101 선명해지며 노란 원 객체 선택 속성창 호출 라벨이 연결된다.','visibility'.split(),[99.25,100,101],'도형 등장과 겹쳐 패널 가시성 증가; 별도 확대는 표본상 확인 못함'),ev('101와104 native ROI에서 선택된 객체 - 원, 기본 정보 행, 원의 치수 도식, 위치 X/Y/Z 표가 같은 배치와 내용으로 유지된다. 지름 8.1502, 반지름 4.0526, 면적 51.5962가 표시되나 숫자의 수학적 타당성은 판정하지 않는다.','internal_content'.split(),[101,104],'정착 후 해당 두 표본 사이 표시 내용 유지',True,kind='not_applicable',basis='내부 값 변화가 아닌 같은 표시 상태 비교.',limits=['커서 이동이나 실제 선택 조작은 이 근거에서 확인되지 않음.'])],'window')]
d['coverage']=dict(overview='전체 배치와 Grouping→Imaging 전환을 검사.',secondary_details='노란 안내/연결 라벨, 원·호·십자/하단 선, 제목 행별 클리핑을 분리 검사.',internal_content='속성 패널 native ROI의 기본/형상/위치정보를 101 및 경계104에서 비교. 창 정착과 내부 등장 시점을 분리.',unresolved=['본문·불릿 개별 시작/이징','원·호·선의 실제 리빌 진행 방향','속성 패널 확대 지시의 다른 구간 실현 여부','이벤트 사이 숨은 짧은 커서/값 변화'])
d['document_correspondence']=[dict(locator='slide[12]/p[2-3]',relation='내용 대응',note='메뉴를 기능별로 그룹화하고 노란 구획으로 설명한다는 문서 내용이 98초 상태와 대응.',evidence_ids=[eid(98)]),dict(locator='slide[13]/p[2-3]',relation='주제 대응/연출 일부 미확인',note='속성 정보를 이미지로 명확하게 전달한다는 문장과 패널 도식은 대응. 우측 속성창 팝업 확대 지시는 본 구간의 가시성 증가와 같다고 단정할 수 없으며 별도 확대를 확인하지 못함.',evidence_ids=[eid(99.25),eid(101),eid(101,True)]),dict(locator='slide[13]/p[1]',relation='시각표 불일치 주의',note='문서의 01:34–01:43은 제작 계획 표기. 실제104 경계도 Imaging이므로 문서 시각을 영상 실제 시각으로 대체하지 않음.',evidence_ids=[eid(104)])]

def save(d):
    p=OUT/f"eval-{d['case_id']}"/'with_skill/outputs';p.mkdir(parents=True,exist_ok=True)
    if d['case_id']=='V04':
        modal=next(o for o in d['objects'] if o['id']=='modal')['events'][1]
        modal['easing']['measurement']={'method':'native ROI에서 동일 팝업 좌우 외곽을 시각적으로 추정; 자동 추적 아님','unit':'native pixel width','samples':[{'actual_seconds':str(F(str(t))),'width_estimate':w,'evidence_id':eid(t,True)} for t,w in [(300.85,135),(300.95,585),(301.05,865),(301.15,975),(301.3,990)]],'error':'정밀 추적 오차 미상. 근사 폭이며 subpixel 측정 아님.','limit':'크기 변화의 후반 감속만 판정. 위치 이징이나 정확한 함수/AE 키프레임으로 확장하지 않음.'}
    (p/'observations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=[f"# {d['case_id']} 시각 관찰",'',f"구간: {d['window_seconds']}초, 끝 경계는 context_after. 오디오 미검수.",'',d['method'],'']
    for o in d['objects']:
        lines += [f"## {o['name']}",'']
        for e in o['events']:
            lines += [f"- {e['time_seconds'][0]}–{e['time_seconds'][1]}초: {e['description']} 방향/순서: {e['direction_order']} 근거: {', '.join(e['evidence_ids'])}. 이징({e['easing']['property']}): {e['easing']['classification']}. {e['easing']['basis']}"]
        lines+=['']
    lines += ['## 문서 대응','']+[f"- {x['locator']}: {x['note']}" for x in d['document_correspondence']]+['','## 미해결/범위','']+['- '+x for x in d['coverage']['unresolved']+d['limitations']]
    (p/'observations.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
save(d)

d=create('V04')
d['objects']=[
ob('layout','헤더/외곽 프레임',[ev('상단 청록 도면 패턴, 도면정보 선택 / 및 정보수정 제목, 흰 배경과 하단 베이지 내용틀은 유지. 내부 단계 표시와 설명은 바뀐다.','position'.split(),[296,299,302],'외곽 고정',kind='not_applicable',basis='외곽 배치 유지 관찰.')]),
ob('tabs','두 단계 탭/설명 문구',[ev('296–298.5 첫 사용자 지정폴더 탭이 활성. 298.75 첫 탭 폭이 줄고 두 번째가 늘면서 활성 녹색이 옮겨간다. 299 두 번째 02 열람하고자 하는 도면정보 선택이 활성이다.','scale color'.split(),[296,298.5,298.75,299],'왼쪽 활성→오른쪽 활성; 첫 탭 축소/둘째 확장',basis='중간 표본 한 개여서 폭 변화 가감속을 확정할 수 없음.'),ev('299 설명은 표시할 도면정보를 도면목록에 추가/삭제하고 수정중 정보를 표시한다는 문장으로 교체. 오른쪽 엑셀 드래그 방식 일괄 수정 문구와 녹색 정확하고 빠른 수정 가능 문구가 도면정보 선택/추가 및 삭제 안내로 교체된다.','visibility internal_content'.split(),[296,298.75,299],'탭 전환과 내용 교체 동반')]),
ob('table','도면 목록/미리보기',[ev('296–298.5 도면번호 열의 붉은 글씨, 주황 행, 분홍 범위 테두리, 아래쪽 손과 수직 점선 화살표가 보인다. 해당 표본의 손 위치와 선택 범위는 유지되어 실제 아래로 드래그하는 연속 동작을 봤다고 할 수 없다.','internal_content'.split(),[296,298.5],'수직 화살표는 아래 방향을 지시; 실제 이동은 미확인',kind='not_applicable',basis='정착된 설명 상태 비교.'),ev('299에는 목록의 보이는 행과 하단 여섯 도면 썸네일이 달라지고 네 번째 썸네일에 주황 테두리. 스크린 내부 화면 교체/보기 변경이 외곽 프레임 안에서 일어난다.','internal_content'.split(),[298.75,299,300.75],'탭 전환 후 새 목록/썸네일 상태',limits=['실제 스크롤 입력인지 합성 화면 교체인지 미확정.'])]),
ob('modal','도면정보 항목 선택창',[ev('300.75에는 팝업이 없다. 301에는 팝업이 커지는 중이고 301.25에는 큰 중앙 팝업이다. 배경 목록을 가리지만 목록 자체가 같은 비율로 확대됐다는 증거는 아니다.','scale visibility'.split(),[300.75,301,301.25],'작은 팝업 등장→확대'),ev('native ROI에서 팝업 외곽 폭이 300.85→300.95→301.05→301.15→301.3로 늘되 증가량이 줄어 정착한다. 중심도 위쪽으로 이동하는 양상이나 위치 곡선은 크기 곡선과 별도로 미확정.','scale position'.split(),[300.85,300.95,301.05,301.15,301.3],'빠른 확대 후 완만하게 정착',True,kind='decelerate',basis='동일 팝업 외곽의 native crop 시각 추정 폭 약135,585,865,975,990px. 첫 네 표본은 0.1초 간격으로 증가량 약450,280,110px가 감소. 마지막 간격0.15초와 정착 상태도 고려. 수동 시각 추정이며 정밀 추적 오차 미상; 정확한 보간 함수 복원 아님.'),ev('선택창 제목과 항목별 체크박스/연결선이 함께 보인다. 본 표본에서는 체크박스가 여러 번 선택되는 순서를 확인하지 못했다.','internal_content'.split(),[301.25,302],'완성된 팝업 유지',kind='not_applicable',basis='확인된 체크 토글 모션 없음; 부재를 영상 전체에 확대하지 않음.')]),
ob('selection','팝업 뒤 두 행 선택 강조',[ev('301.25 아래 013 파일 행이 연한 주황. 301.5 그 행이 진해지고 바로 위 012 행이 연한 주황. 301.75에는 두 행 모두 진한 주황이며 302 경계에도 유지된다.','color internal_content'.split(),[301.25,301.5,301.75,302],'아래 행→윗 행 추가; 하나의 표식이 이동하는 대신 두 선택 상태가 누적',True,basis='각 행의 밝기 비교는 가능하지만 충분한 연속 픽셀 추적이 없어 색/밝기 곡선 미확정.')],'table')]
d['coverage']=dict(overview='1단계 일괄 수정 설명에서2단계 정보 선택으로 넘어가는 구간과 팝업 확대.',secondary_details='탭 너비/색, 손·점선 화살표, 썸네일 테두리, 팝업 외곽과 배경 선택을 분리.',internal_content='native ROI에서 팝업 내부와 뒤쪽 두 행의 누적 강조를 비교. 체크 토글과 배경 행 강조를 혼동하지 않음.',unresolved=['탭 폭과 팝업 위치의 가감속','팝업 체크박스 선택의 정확한 진행','구간 이전 실제 드래그 동작','일부 UI 미세 글씨와 정확한 보기 변경 입력'])
d['document_correspondence']=[dict(locator='slide[34]/p[2-3]',relation='주제 대응/동작 범위 제한',note='엑셀 드래그처럼 여러 도면 정보를 일괄 수정한다는 지시와296 화면의 범위/손/화살표/문구가 대응.296–298.5 정착 표본은 실제 드래그 이동의 직접 증거가 아님.',evidence_ids=[eid(296),eid(298.5)]),dict(locator='slide[35]/p[2-3]',relation='팝업 대응/체크 토글 미확인',note='도면정보 추가·삭제 및 중앙 선택창 팝업은 관측. 여러 체크박스 선택됨이라는 문서 지시와 달리 본 근거에서는 선택창 뒤 두 행의 누적 강조만 명확히 확인.',evidence_ids=[eid(299),eid(301.25),eid(301.75,True)]),dict(locator='slide[34]/p[1]; slide[35]/p[1]',relation='시각표 차이',note='문서05:07–05:15,05:15–05:23 내용이 실제296–302초에 나타난다. 주제별 대응이며 문서 시각과 실제 영상 시각을 동일시하지 않음.',evidence_ids=[eid(296),eid(302)])]
save(d)

for cid in ['V06S','V06W']:
    wide=cid=='V06W';d=create(cid)
    if not wide:
        objs=[ob('landscape','실감형 경관/공정 헤더',[ev('주간 전경에서 전경의 원형 타워가 커지고 아래쪽으로 내려오며 시점이 달라진다. 234에는 야간 타워/도시 조명 장면. 설계 Process와 네 단계 pill, 맞춤형 계획 수립 활성, 실감형 통합모델 캡션이 함께 표시된다.','position scale color'.split(),[232,233,234],'주간 전경→야간 시점; 카메라/장면 시점 변화',limits=['3D 카메라 이동과 편집 전환의 정확한 경계, 광량 가감속 미확정.']),ev('235에는 경관과 녹색·흰색 새 배경이 겹치고235.5에는 새 배경만 남는다.','visibility'.split(),[234,235,235.5],'이전 경관 소거와 새 배경 가시화 중첩')]),ob('title','상단 수평 공사 목표 제목판',[ev('235.5 상단 중앙의 가로로 긴 빈 제목판,236 공사와 영문 일부,236.5 공사 목표 / CONSTRUCTION TARGETS 전체가 보인다.','visibility reveal'.split(),[235.5,236,236.5],'틀→글자 가시화; 판의 확대와 텍스트 확대를 같은 사건으로 확정하지 않음')])]
        times={'s':[236.5,237,238],'q':[238,238.5,239],'t':[239,239.5,240],'e':[240.5,241,242]}
        finish=[242,244,246]; fade=[244,245.5,246]; sub=[244,244.5,245.5]
    else:
        objs=[ob('landscape','좌우 경관 분할/공정 헤더',[ev('좌측에는 주간 하천·교량 전경, 우측에는 야간 타워가 동시 표시된다.236와239 사이 좌측 전경은 거의 유지되고 우측 타워는 작아지고 위로 이동해 주변 광장 영역이 더 보인다. 설계 Process/맞춤형 계획 수립 활성과 좌하단 실감형 통합모델 캡션이 있다.','scale position'.split(),[236,239],'우측 야간 뷰는 후퇴하는 시점; 좌측과 별도',limits=['오른쪽 카메라 경로/속도 곡선은 두 표본만으로 미확정.']),ev('239에는 경관이 있고239.5에는 녹색·흰색 그래픽 배경이다.','visibility'.split(),[239,239.5],'경관→목표 배경',limits=['두 표본 사이 전환 방식은 미확정; 단일본의 중첩 방식 자동 적용 안 함.'])]),ob('title','좌측 세로 공사목표 제목판',[ev('240.5 좌측의 높고 좁은 제목판이 보이고241 공사목표 / CONSTRUCTION TARGET가 읽힌다.','visibility reveal'.split(),[240.5,241],'좌측 제목판→문구; 영문은 단수 TARGET'),ev('247 어두운 제목 글자가249.5 밝은 녹색 계열로 변했다가250 경계에서는 다시 어두워진다. 위치가 이동하는 효과와 분리한 글자 색/광량 변화이다.','color luminance'.split(),[247,249.5,250],'밝아짐→원래 어두운 상태',basis='광량 변화는 보이나 표본 간격이 커 광량 곡선 및 스윕 이동방향 미확정.')])]
        times={'s':[241.5,242.5,243],'q':[242.5,243,244],'t':[244,244.5,246],'e':[246,247,249.5]}
        finish=[244.5,247,249,250];fade=None;sub=[247,249.5,250]
    objs += [ob('cards','네 핵심가치 카드 묶음',[ev('안전·품질·공기·효율의 사진/합성 이미지와 아이콘·녹색 pill을 왼쪽부터 차례로 구축한다. 먼저 생긴 카드가 유지된 상태로 다음 카드가 추가된다.','visibility position'.split(),[times['s'][0],times['q'][1],times['t'][1],times['e'][1]],'안전→품질→공기→효율; 등장 구간 일부 중첩',limits=['전체 카드가 동일 변환/동일 이징을 공유한다고 가정하지 않음.'])]),
    ob('safety','안전 카드와 통신 그래픽',[ev('건설 현장 사진이 옅게 나타나고 선명해진다. 헬멧/방패 아이콘과 안전 pill, 사진 위 wifi 기호 및 녹색 곡선 연결망이 보인다.'+(' 사진은 처음 낮은 위치에서 조금 위로 올라 정착하는 양상.' if not wide else ''),'visibility position'.split(),times['s'],'안전 이미지 가시화→통신선/기호가 포함된 완성 상태',limits=['사진의 위치와 통신선의 리빌/빛 진행은 분리; 선 끝의 정확한 진행 방향·속도 미확정.'])],'cards'),
    ob('quality','품질 카드/현실-모델 비교',[ev('옅은 녹색 면/형상 뒤로 교량·터널 사진과 흰 와이어프레임, 주황 분할선 및 원형 양방향 표식, 드론/파란 조사 원뿔이 보인다. 엄지/별 아이콘과 품질 pill이 함께 완성된다.','visibility shape'.split(),times['q'],'희미한 면/라벨→사진과 모델 비교·드론 선명',limits=['주황 분할선이 실제 슬라이드하는지, 드론이 이동하는지 선택 표본만으로 확정하지 않음.'])],'cards'),
    ob('schedule','공기 카드/보고 UI와 작업자',[ev('공기 아이콘/라벨이 먼저 옅게 보이고 일일 작업보고 화면, 작업자, 크레인 모니터가 겹쳐 나타난다. 달력/스톱워치 아이콘과 pill이 선명해진다.','visibility'.split(),times['t'],'라벨·아이콘과 UI 묶음 가시화; 전체 정착 후에도 내부 확인'),ev('native ROI에서 일일 작업보고,2025.04와4일 표시 및 크레인 모니터의 같은 구성이 비교된다. 이 표본 사이 실제 보고 값 갱신이나 크레인 이동을 확인하지 못했다.','internal_content'.split(),([242,244] if not wide else [244.5,247]),'유지된 표시 상태',True,kind='not_applicable',basis='읽을 수 있는 동일 UI 표식 비교; 화면 전체가 정적이라고 일반화하지 않음.',limits=['미세 UI 글씨 전부 판독하지 않음.'])],'cards'),
    ob('efficiency','효율 카드/회의실·메시지·경고',[ev('회의실/테이블/작업자 이미지가 옅게 들어오며 기어/시계 아이콘과 효율 pill이 선명해진다. 이후 벽 모니터 내용과 말풍선, 연결선 및 큰 녹색 호가 더해진다.','visibility internal_content'.split(),times['e'],'방/기본 이미지→모니터·말풍선·연결 그래픽',limits=['각 요소의 가시성 변화와 실제 공간 이동을 혼동하지 않음.']),ev('native ROI에서 벽 화면의 경고/지도 표식이 앞 표본보다 뒤 표본에서 뚜렷하다. 방 외곽이 이미 정착해도 내부 오버레이는 추가된다.','internal_content visibility'.split(),([242,244] if not wide else [247,249]),'정착한 회의실 내부에 경고 표식 가시화',True,basis='등장 상태는 확인하지만 광량/리빌 변화율은 미측정.')],'cards'),
    ob('subtitle','하단 설명 자막',[ev('대규모 인프라시설과 주변 경관/도시 미학적 가치 문장에서 한맥가족의 BIM기반 건설사업관리 프레임워크는 참여하는 수많은 이해관계자가로 바뀐다.','internal_content'.split(),sub,'앞 설명→프레임워크 설명',kind='not_applicable',basis='문장 교체 시점 범위 관찰; 속도 곡선을 적용하지 않음.')])]
    if fade:
        objs.append(ob('exit','카드 이미지 퇴장',[ev('244 네 이미지가 보이나245.5 사진/UI 층은 옅어지고 아이콘·pill은 선명하다.246 경계에서는 사진/UI가 사라져 제목과 네 아이콘/pill만 남는다.','visibility'.split(),fade,'이미지 층 소거; 아이콘/pill 유지',limits=['끝246은 context_after; 정확한 소거 완료 프레임은 미확정.'])],'cards'))
    else:
        objs.append(ob('hold','창 끝의 이미지 유지',[ev('249.5와250 경계에도 네 카드 사진/UI 및 아이콘/pill이 함께 보인다. 이 분석 창에서는 단일본 끝과 같은 사진층 소거 상태에 도달하지 않는다.','visibility'.split(),[249.5,250],'창 끝까지 사진과 라벨 유지',kind='not_applicable',basis='끝의 보이는 상태 비교; 이후 영상에 퇴장이 없다는 뜻 아님.')],'cards'))
    d['objects']=objs
    d['coverage']=dict(overview='경관→공사 목표 전환과 네 카드의 순차 등장, 자막을 검사. '+('좌우 동시 경관과 좌측 세로 제목판의 초광폭 구성.' if wide else '주야간 순차 경관과 상단 가로 제목판의16:9 구성.'),secondary_details='wifi/곡선 연결망, 드론 조사 원뿔·분할선, 달력/스톱워치, 회의실 메시지/경고/호, 제목 광량과 카드 퇴장을 외곽과 분리.',internal_content='일일 보고/크레인 모니터 및 회의실 벽 화면을 원본 좌표 ROI로 비교. 회의실 내부 오버레이 변화는 긍정 관측, 보고값 갱신은 미확인.',unresolved=['카드별 위치/가시성 곡선과 정확한 시작·끝','네트워크 선의 진행 방향/반복 주기와 개별 빛 이동','드론·주황 비교선·크레인의 짧은 내부 모션','경관 카메라의 정확한 경로/전환 구현','각 작은 UI 텍스트와 보이지 않는 데이터','W250 이후 이미지 퇴장 시점 또는 S와의 전체 길이 대응'])
    d['document_correspondence']=[dict(locator='BodyText/Section0/record[156]/para[22]',relation='문구 대응',note='실감형 통합모델을 활용한 경관 조화/도시 미학적 가치 문장이 초기 자막과 대응. 시각 효과나 성능을 입증하는 문서로 취급하지 않음.',evidence_ids=[eid(236 if wide else 232)]),dict(locator='BodyText/Section0/record[216]/para[32]; record[220]/para[33]',relation='장 구성 및 핵심가치 대응',note='시공 단계와 안전·품질·공기·효율의 네 핵심가치, BIM기반 건설사업관리 프레임워크와 이해관계자 정보 공유 문장이 제목·네 카드·다음 자막과 대응. 문서에는 여기의 레이아웃·등장/퇴장 시각·이징 지시가 없으므로 제작 의도를 복원하지 않음.',evidence_ids=[eid(247 if wide else 242),eid(249.5 if wide else 244.5)])]
    d['variant_comparison']=str(OUT/'eval-V06S/with_skill/outputs/variant-comparison.md')
    save(d)

comparison='''# V06S / V06W 상태 기반 비교

단일본3840×2160(16:9)과 듀얼본7680×2160(32:9)은 하나의 변형 비교 사례다. 원본 해시는 각 observations.json에 고정했다. 같은 초를 대응점으로 쓰지 않고 문구·구성·완성 상태를 맞췄다. 아래 시각은 열람한 실제 sample-table PTS이며 정확한 시작 프레임을 뜻하지 않는다.

|상태|단일 V06S|듀얼 V06W|관측 차이|
|---|---|---|---|
|실감형 경관|232 주간→234 야간|236–239 좌 주간·우 야간 동시|단일은 시간 순서, 듀얼은 공간 분할. 듀얼 우측 야간 뷰는 타워가 작아지며 후퇴하고 좌측은 거의 유지|
|새 배경/제목|235 겹침,235.5 빈 가로판,236.5 완성|239.5 새 배경,240.5 세로판,241 완성|단일 상단 수평 제목판; 듀얼 왼쪽 높고 좁은 제목판. 단일 전환의 중첩을 듀얼에 자동 적용하지 않음|
|제목 표기|공사 목표 / CONSTRUCTION TARGETS|공사목표 / CONSTRUCTION TARGET|한국어 띄어쓰기와 영문 복수/단수 차이|
|안전 이미지 등장|236.5 옅음,237 선명|241.5 등장|상응 시작 차이는 약5초지만 전체의 고정 오프셋으로 쓰지 않음|
|품질 구축|238 희미함,238.5–239 선명|242.5 희미함,243 선명|상응 표본 차이 약4.5초. 사진·와이어프레임·드론/조사 원뿔·주황 분할 표식이라는 의미 묶음은 유지|
|공기 구축|239–240|244–246|보고 UI, 달력/스톱워치, 작업자/크레인 모니터 묶음 유지. 선택 표본으로 정확한 동기 차이를 확정하지 않음|
|효율 구축/내부 표시|240.5–242,244 경고 표식|246–247,249 경고 표식|회의실 외곽 뒤 내부 화면/말풍선/연결선과 경고가 추가되는 대응|
|다음 자막|244.5 새 문장|249.5 새 문장|이 사건의 관측 차이는5초|
|끝의 상태|245.5 사진/UI 감소,246 경계는 아이콘/pill만|249.5와250 경계 사진/UI가 남음|분석 창의 끝 상태가 다르다. 듀얼 영상 이후에도 사진이 영원히 남는다는 뜻 아님|

듀얼은 좌측 제목과 오른쪽 네 카드에 공간을 배분하며, 단일은 제목을 위에 두고 카드를 아래에 배치한다. 단일을 단순 가로 확대/크롭한 구성으로 설명할 수 없다. 같은 개념 요소를 재배치한 것으로 관측되지만 원본 프로젝트의 같은 소스 레이어 사용 여부는 미확정이다.

두 버전의 공기 카드 ROI에서 일일 작업보고와2025.04/4일, 크레인 화면이 대응한다. 이 비교 표본으로 실제 데이터 갱신을 확인하지 못했다. 효율 카드에서는 방 외곽 정착 뒤 경고/지도 표식이 추가되어 외곽 정지와 내부 정지를 구분했다. 듀얼 제목은247→249.5→250에서 어두움→녹색 밝음→어두움으로 변하지만, 이것을 위치 이동이나 정확한 빛 스윕 경로로 단정하지 않았다.

문서는 DOC071 BodyText/Section0/record[156]/para[22]와record[220]/para[33]의 경관 설명/네 핵심가치/프레임워크 문장으로 대응했다. 문서에 타이밍·화면 비율별 연출 지시가 없어 어느 변형이 의도에 더 맞는지 판단하지 않는다. 오디오와 음성 동기는 검수하지 않았다.

직접 근거는 각 버전 observations.json의 f/r ID와 원본 PNG/ROI 경로·해시·PTS에 연결된다. 주요 짝은 S:f236p5↔W:f241p0, S:f238p5↔W:f243p0, S:r242p0/r244p0↔W:r247p0/r249p0, S:f244p5↔W:f249p5, S:f246p0↔W:f250p0이다. 마지막 두 프레임은 context_after다.

미해결: 각 카드의 정확한 easing/소스 레이어 구성, 광선·연결선의 반복 주기, 짧은 UI/드론/분할선 모션, W250 이후 퇴장과 전체 영상의 연속 정렬. 이 결과는 지정 구간의 선택 프레임 시각 관측이며 제품 기능 인증이나 전체 영상의 누락 없음 선언이 아니다.
'''
(OUT/'eval-V06S/with_skill/outputs/variant-comparison.md').write_text(comparison,encoding='utf-8')
print('Saved V03, V04, V06S, V06W and state-based variant comparison')
