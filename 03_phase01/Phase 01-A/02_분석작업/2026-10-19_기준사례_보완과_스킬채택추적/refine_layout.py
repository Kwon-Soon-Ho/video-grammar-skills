from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer/scripts'))
from check_record import check
from render_observations import render
def load(p):return json.loads(Path(p).read_text('utf-8'))
cat=load(HERE/'evidence-catalog.json')
for code in ['NEW-N','NEW-P']:
 p=HERE/'records'/code/'observations.json';d=load(p);old=d['layout']['states'][0]
 if code=='NEW-N':
  old['design_spec']['background']['description']='남청 기술 배경의 좌측 점·망과 하단 푸른 곡선·작은 교차점. 세 ROI에서 도입 밝아짐과 이후 위치 유사 상태를 확인. 원본 레이어 독립성·정확 속성은 미확정.'
  old['design_spec']['shapes']['description']='사선 로고 리본, 구멍/날개/철근을 가진 긴 거더와 오른쪽 단면, 분할 철근 판과 후반 넓은 마감 판. 곡선 화살표와 형상에 밀착한 청록 외곽 강조를 분리한다. 설명은 어두운 띠·청록 양끝선·흰 글자, 자막은 별도 진한 사각 바탕.'
  old['design_spec']['typography']['description']='흰 산세리프 한글. 좌상단 리본, 굵은 도해 설명, 하단 자막의 세 위계. 오른쪽 짧은 설명과 왼쪽 긴 설명은 다른 길이/폭이다. 영상 표기는 켄틸레버, 상단의 시공시와 하단의 시공 시를 각각 보존. 서체명·폰트 크기 원값은 미확정.'
  old['design_spec']['spacing']['description']='초광폭 왼쪽 큰 대각 구조와 오른쪽 정면 단면 사이 어두운 여백. 설명 띠는 각 모델 위에, 공통 자막은 두 영역 아래 중앙. 175초 왼쪽 설명의 선 간격 약1473 native px. 개별 요소의 실제 3D/AE 앵커값은 아님.'
  plan=[('construction-intro',[166,168.8],168,['left-label','edge-highlight','top-slab']),('two-view-emphasis',[168.8,174],170,['edge-highlight','top-slab']),('late-assembly',[174,181],177,[])]
 else:
  old['design_spec']['alignment']['description']='카드 위쪽에서 세로 연결선이 설명 프레임 아래 원형 접점으로 이어진다. 프레임 안 두 가로 화살촉 띠는 수직으로 쌓인다. 기존 노란 묶음은 왼쪽 고정, 새 분홍 묶음은 중앙 등장 후 오른쪽 이동.'
  old['design_spec']['color']['description']='어두운 녹갈색 지도/남청 바다, 청록 횡성, 노랑·연두 경찰청, 붉은색/분홍 강원 묶음, 밝은 카드 면. 행별 등장·한 차례 강조·기본 붉은색 복귀를 구분하고 공통 점멸 주기를 만들지 않는다.'
  old['design_spec']['spacing']['description']='반투명 프레임 아래 기관 카드, 그 사이 세로 연결선. 지도 경계·지명을 일부 비치게 두며 하단 자막과 횡성 강조 사이 간격을 둔다. 51.5~53초 분홍 기관 묶음이 오른쪽으로 가며 중앙 여백을 만든다.'
  plan=[('existing-agency',[40,41.4],40,['gangwon','gangwon-face','regional-frame','regional-row1','regional-row2','regional-link']),('two-agency-build',[41.4,51.5],47,[]),('right-reposition',[51.5,53],52,[])]
 states=[]
 for name,span,t,exclude in plan:
  s=deepcopy(old);s['id']=name;s['time_seconds']=span;s['element_object_ids']=[o['id'] for o in d['objects'] if o['id'] not in exclude]
  es=[e for e in d['evidence'] if F(e['actual_seconds'])==F(str(t)) and 'crop_xyxy' not in e]
  s['evidence_ids']=[es[0]['id']]
  s['composition']=old['composition']+' 이 상태의 시간 구간: '+str(span)+'초. 출현·퇴장·유지의 정확 범위는 개별 주장과 흐름에 따름.'
  s['claim_ids']=[c['id'] for c in d['claims'] if c['content_review']=='supported' and c['object_id'] in s['element_object_ids']]
  for spec in s['design_spec'].values():spec['claim_ids']=s['claim_ids']
  states.append(s)
 d['layout']['states']=states
 assert not check(d,cat),(code,check(d,cat))
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');p.with_suffix('.md').write_text(render(d),encoding='utf-8')
print('각 기준 사례의 전체 디자인을 3개 화면 상태로 나누고 변화 범위·문구·별도 효과를 반영')
