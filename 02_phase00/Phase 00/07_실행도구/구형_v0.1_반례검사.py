from 구형기록_보존검사 import *
from 지식조회 import lookup,palette
import copy
base=read('04_기록규격/설명용_단계구성_예시.json'); tests=[]
def case(name,edit,expect_valid=False,contains=None):
    d=copy.deepcopy(base);edit(d);errors=validate_record(d)
    tests.append({'name':name,'expected_valid':expect_valid,'actual_valid':not errors,'passed':((not errors)==expect_valid) and (contains is None or any(contains in e for e in errors)),'expected_error_contains':contains,'evidence':errors})
case('설명용 예는 초안으로 통과',lambda d:None,True)
case('없는 한맥 토큰 차단',lambda d:d['design']['palette_role_bindings'].update(background='MISSING'))
case('분류축에 다른 용어 연결 차단',lambda d:d['segments'][0]['classification'].update(layout=['PURPOSE-PROCESS']))
case('폐기 PIP ID 신규 사용 차단',lambda d:d['segments'][0]['classification'].update(art_direction=['STYLE-PIP']))
case('끝이 시작보다 빠른 시간 차단',lambda d:d['segments'][0].update(period={'start_s':5,'end_s':3,'time_basis':'presentation_timeline','uncertainty_s':0.1}))
case('알 수 없는 시간 기준에 숫자 넣기 차단',lambda d:d['segments'][0].update(period={'start_s':0,'end_s':3,'time_basis':'unknown','uncertainty_s':None}))
case('설명용 예의 승인 차단',lambda d:d['review'].update(state='approved'))
case('없는 근거 연결 차단',lambda d:d['claims'][0].update(evidence_refs=['MISSING']))
case('설명용 예를 실제 관측으로 승격 차단',lambda d:d['claims'][0].update(support_mode='rendered_observation'))
case('날짜 형식 검사 활성',lambda d:d['review'].update(reviewed_at='어제'))
case('프로필 버전 불일치 차단',lambda d:d['design'].update(profile_ref='hanmac-video@9.0.0'))
case('정밀도 없는 수치 추정 차단',lambda d:d['segments'][0]['beats'][0].update(support_mode='numerical_estimate',measurement={'value':115}))
case('중복 ID 차단',lambda d:d['claims'][0].update(id=d['evidence'][0]['id']))
case('NaN 수치 차단',lambda d:d['segments'][0]['period'].update(start_s=float('nan'),end_s=1))
case('중복 근거 원배열 검사',lambda d:d['evidence'].append(copy.deepcopy(d['evidence'][0])),contains='ID 중복')
case('중복 시나리오 원배열 검사',lambda d:d['scenario_segments'].append(copy.deepcopy(d['scenario_segments'][0])),contains='ID 중복')
case('빈 분류 배열 이유 필수',lambda d:d['segments'][0].update(classification={'layout':[]}),contains='미분류 이유')
case('근거 대상이 없는 frame 차단',lambda d:d['evidence'][0].update(kind='frame',target_id='MISSING'),contains='원본 추출 대상')
case('수치 주장 측정 필수',lambda d:d['claims'][0].update(support_mode='numerical_estimate',measurement=None),contains='수치 추정')
def outside(d):
    d['segments'][0]['period']={'start_s':1,'end_s':2,'time_basis':'presentation_timeline','uncertainty_s':0.1}
    d['segments'][0]['beats'][0]['period']={'start_s':5,'end_s':6,'time_basis':'presentation_timeline','uncertainty_s':0.1}
case('모션 상위 시간 포함 관계',outside,contains='상위 구간 시간 밖')
case('반쪽 시간 오류에서 검증기 종료 없이 차단',lambda d:d['segments'][0]['beats'][0].update(period={'start_s':1,'end_s':None,'time_basis':'presentation_timeline','uncertainty_s':None}),contains='반쪽')
tests.append({'name':'페이드·확대 방향 한정어 보존','passed':lookup('페이드아웃')[0]['qualifiers']['direction']=='exit' and lookup('확대')[0]['qualifiers']['direction']=='increase','evidence':'조회 방향한정어 exit/increase'})
tests.append({'name':'미확인 정의 기본조회 제외','passed':not lookup('IP-10'),'evidence':'기본 조회 결과가 빈 목록'})
tests.append({'name':'미확인 항목 명시조회 허용','passed':len(lookup('IP-10',include_pending=True))==1,'evidence':'명시 include_pending 조회'})
tests.append({'name':'기본 한맥 조회 UI 선택참고 제외','passed':len(palette()['colors'])==30 and not palette()['optional_styles'],'evidence':'30색, 선택스타일0'})
tests.append({'name':'선택 UI 참조는 명시 조회','passed':len(palette(True)['colors'])==46 and len(palette(True)['optional_styles'])==28,'evidence':'알파16+참고10+레시피18 포함'})
result={'tests':tests,'passed':sum(t['passed'] for t in tests),'total':len(tests),'scope':'자료 계약과 조회 반례. 실제 영상이나 스킬효과 테스트 아님.'}
out=BASE/'08_검증결과/R4_04_구형_v0.1_반례검사.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':result['passed'],'total':result['total'],'failures':[t for t in tests if not t['passed']]},ensure_ascii=True))
if result['passed']!=result['total']:raise SystemExit(1)
