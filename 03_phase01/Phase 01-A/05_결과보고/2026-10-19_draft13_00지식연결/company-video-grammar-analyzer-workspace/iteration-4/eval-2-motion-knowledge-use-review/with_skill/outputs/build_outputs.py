from pathlib import Path
import json, hashlib, subprocess, sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[6]
# Locate the explicit task root without reading sibling executions.
ROOT=next(p for p in OUT.parents if (p/'knowledge-linked-skill-20261019/eval-inputs/input.md').is_file())
INPUT=ROOT/'knowledge-linked-skill-20261019/eval-inputs'
SKILL=ROOT/'knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer'
P00=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,data):
 (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).as_posix()}>)'

rows=[
 dict(id='A-M1',case='VC-CASE-A',region='A-02',sheet='contract-reflow',a=96,b=100,
 title='기존 수주 구역 재배치와 비용 정보판·내부 내용 누적',
 info='수주 17.5억원의 구성 옆에 별도 산정 역할인 계약 수행 투입비용을 추가한다. 수주·비용의 합산이나 꺾쇠를 통한 인과는 확인하지 않았다.',
 screen='수주 판이 왼쪽으로 재배치되며 오른쪽에 좁고 세로로 긴 비용 판이 마련된다. 수주 도넛 2개와 내부 금액/비율은 기존 맥락으로 남는다. 균등 2열 격자로 확정하지 않는다.',
 visual='녹색 장 배지·민트 헤더·밝은 둥근 판·도시 배경을 유지하고 새 판의 동전/문서와 설명 캡슐을 누적한다. 정보면/경계/약한 명암과 배경층을 구분한다.',
 steps=[(96,'수주 판과 17.5억원·도넛 2개가 보임'),(96.5,'수주 판 중심 상태 지속; 이후 왼쪽 위치와 비교'),(97,'수주 판 왼쪽 재배치와 비용 판/제목·작은 꺾쇠가 보임'),(97.5,'비용 판 아래 동전 일부'),(98,'동전과 문서 형태를 포함한 도상'),(98.5,'도상 유지; 비용 금액은 아직 안 보임'),(99,'현재까지 투입 캡슐이 보임'),(99.5,'캡슐·도상 유지'),(100,'비용 숫자가 보이기 시작함; 시트에서는 0.7억원으로 읽히지만 원본 크기 전사 미확인, 비용의 끝값 8.7로 저장하지 않음')],
 relation='기존 판 재배치와 새 판 진입은 겹친다. 외형/제목→도상→캡슐→숫자 공개를 구분한다. 100초 창 끝은 비용 완성 시각이 아니다. 103초 다음 창의 8.7억원과 100초 중간 상태를 분리한다.',
 tags=['PROPERTY-POSITION','PROPERTY-VISIBILITY','FUNCTION-REVEAL','FUNCTION-CONTEXT','TIME-SEQUENCE','TIME-OVERLAP'],
 conditions='기존 구성과 별도 지표를 누적해 설명할 때의 후보. 공간이 이미 가득 찼거나 기간·정의가 다른 지표를 기존 값처럼 유지해야 한다면 같은 누적을 강제하지 않는다.',
 diff='A-M2와 달리 기존 수주 구역의 재배치와 새 비용 판 추가를 함께 포함한다. VC-MOTION-02 원본 변형 후보이나 동일 패턴 확정은 아님.',
 unknown='첫 이동/정착 프레임, 비용 카운트의 전체 진행과 완성, 내부 미세 변화, 위치 변화율/이징 원값'),
 dict(id='A-M2',case='VC-CASE-A',region='A-02',sheet='contract-panel',a=103,b=106,
 title='기존 두 지표를 유지하며 실제 매출 판 진입·라벨 보강',
 info='수주 17.5억원·비용 8.7억원을 남기고 실제 발생 매출 및 수주·매출 중복 제외 설명을 추가한다. 세 지표는 같은 산정 역할이 아니다.',
 screen='왼쪽 넓은 수주 판/가운데 좁은 비용 판에 오른쪽 넓은 매출 판을 더한다. 기존 두 판의 전체 재정렬을 가정하지 않는다.',
 visual='오른쪽 판은 따뜻한 경계·밝은 면·약한 그림자를 갖고, 이후 주황 금액의 영역이 된다. 기존 녹색 수주/비용과 대비하는 표현이며 공식 CI색 단정은 안 한다.',
 steps=[(103,'수주·비용 두 판; 오른쪽 매출 판 미가시'),(103.5,'매출 판 미가시'),(104,'오른쪽 바깥 쪽 위치에 매출 판·작은 막대형 표식'),(104.5,'매출 판이 더 안쪽 위치'),(105,'실제 발생 매출 제목이 읽힘'),(105.5,'제목 유지'),(106,'수주·매출 중복 제외 설명이 보임')],
 relation='판 외형 첫 가시성 (103.5,104]초. 판 진입→제목→설명 보강 중 기존 두 지표가 동반 유지된다. 판 정착과 내용 완성은 같은 사건이 아니다.',
 tags=['PROPERTY-POSITION','PROPERTY-VISIBILITY','FUNCTION-REVEAL','FUNCTION-CONTEXT','TIME-SEQUENCE','TIME-HOLD'],
 conditions='기존 두 지표를 보면서 새 설명을 더할 때 후보. 기존 지표의 기간/기준이 바뀌면 같은 값 유지로 오해시키지 않아야 한다.',
 diff='A-M1의 재배치·도상·캡슐 순서를 그대로 복사하지 않는다. 내부 매출 수치/도상 조립은 A-M3로 연결한다.',
 unknown='진입 원점·정확 정착 프레임, 마스크/opacity/레이어 이동 구현, 이징'),
 dict(id='A-M3',case='VC-CASE-A',region='A-02',sheet='contract-number',a=108,b=111,
 title='매출 숫자 정착 뒤 상승 도상 완성: 완료 시차',
 info='실제 발생 매출 12.9억원을 주황 금액으로 강조한다. 수주·매출 중복 제외 문구를 동반한다. 증가 중 표시 숫자는 해당 초의 실적 측정치가 아니다.',
 screen='오른쪽 매출 판 내부: 왼쪽 큰 금액/짧은 밑 막대, 오른쪽 원형 받침과 세로 막대·상승 화살표 도상. 기존 수주/비용 판은 왼쪽 맥락으로 남는다.',
 visual='주황 금액과 주황/금색 입체 막대·상승 화살표, 밝은 받침이 함께 경제성과 이미지를 만든다. 도상은 실제 추세 데이터의 축/스케일로 확인되지 않았다.',
 steps=[(108,'원형 받침이 보임'),(108.5,'받침/낮은 내부 형태'),(109,'낮은 막대 형태'),(109.5,'매출 0.8억원 및 막대 조립 진행'),(110,'10.8억원·막대 성장'),(110.5,'12.9억원 첫 표본 확인'),(111,'12.9억원 유지; 112초의 완성 상승 화살표와 다름'),(112,'기존 연결 PNG를 별도 확인: 12.9억원과 완성된 상승 화살표. 6개 창 밖 문맥 근거')],
 relation='숫자 끝값 최초 관측 경계 (110,110.5]초. 110.5/111/112초 끝값 유지 표본이 있으나 연속 유지 전수 확인은 아님. 도상은 111초 상태→112초 완성 상태 차이가 있어 숫자보다 뒤에 완성된다. 도상의 정확 완료 경계는 이 두 표본 사이의 미검수 과정으로 남긴다.',
 tags=['PROPERTY-VALUE','PROPERTY-VISIBILITY','TIME-DELAY','TIME-OVERLAP','TIME-HOLD'],
 conditions='확정 금액을 제시하며 보조 성과 도상을 조립할 때 후보. 계약번호·날짜에 같은 카운트를 적용하지 않는다. 의미/끝값 관계를 동시 출발·완료 규칙으로 확대하지 않는다.',
 diff='B-M3와 완료 시차라는 검색 개념을 공유하지만 A-M3는 금액+장식적 상승 도상, B-M3는 비중+구성 차트/보조 카드이다. 서로 동일 부품/동일 자산이나 동일 모션으로 합치지 않는다.',
 unknown='카운트 실제 보간식, 막대의 데이터 분모, 화살표 시작/완료 정확 프레임, 실제 3D 제작·원본 키프레임'),
 dict(id='B-M1',case='VC-CASE-B',region='B-02→B-03',sheet='project-reflow',a=136,b=140,
 title='요청·지원 관계도 분산 퇴장과 지원 총량 장면 중첩',
 info='왼쪽 가족사 요청→오른쪽 전문인력/지원← 관계도에서 26건·23.7억원 총량 요약으로 이동한다. 요청과 지원 방향, 금액과 건수 단위 차이를 보존한다.',
 screen='두 정보판과 반대 방향 화살표에서 왼쪽 제목·오른쪽 금액/건수와 받침의 비대칭 구도로 바뀐다. 관계도는 단순 양자 금액 비교표가 아니다.',
 visual='아이보리 곡선 바탕·구리색 장 배지, 파랑 요청/초록 지원 관계를 거쳐 금속적 큰 금액과 작은 건수·받침으로 주목점이 바뀐다.',
 steps=[(136,'가족사 판·전문인력 판·요청/지원 화살표가 보임'),(136.5,'두 판과 화살표 유지'),(137,'관계도 유지'),(137.5,'화살표와 일부 요소의 가시성이 약해짐'),(138,'좌우 바깥쪽의 옛 판과 새 건수·금액이 함께 보임'),(138.5,'왼쪽 제목+오른쪽 수치/받침 구도'),(139,'금액은 중간 표시 상태'),(139.5,'금액 중간 상태가 이어짐'),(140,'26건·23.7억원 상태')],
 relation='옛 판 퇴장/가시성 약화와 새 수치 공개는 138초에 겹친다. 새 장면 완성 후에 옛 판을 없애는 단순 직렬이나 옛 장면 완전 소실 뒤 새 장면 등장으로 쓰지 않는다. 26건과 금액이 동시에 정착했다고 가정하지 않는다.',
 tags=['PROPERTY-POSITION','PROPERTY-VISIBILITY','PROPERTY-VALUE','TIME-OVERLAP','FUNCTION-REVEAL'],
 conditions='관계도 맥락에서 총량 요약으로 넘어갈 때 후보. 관계 방향/세부 비교를 끝까지 읽어야 한다면 퇴장 시점을 따로 검토해야 한다.',
 diff='A의 기존 지표 누적 유지와 달리 관계도를 분산 퇴장시키고 새 구도로 넘긴다. 금액의 변화 중 수치를 실측 시간 변화로 해석하지 않는다.',
 unknown='요청/지원 화살표 각각의 정확 소실 프레임, 옛 판의 완전 퇴장 경계, 수치별 정착 경계, 마스크/opacity/이징'),
 dict(id='B-M2',case='VC-CASE-B',region='B-03→B-04',sheet='project-wipe',a=143,b=146,
 title='대각 경계로 여러 업무 영상 구획 전개',
 info='지원 26건·23.7억원 요약에서 지도/도로·지형 영상의 업무 사례 묶음으로 이동한다. 영상 구획은 금액 분류 차트가 아니다.',
 screen='총량 구도의 왼쪽부터 지도 띠와 사선 경계 영상이 들어온 뒤 세 영상 구획/하단 사례 라벨이 보인다. 대각 분할 기하와 업무 사례라는 정보 역할을 따로 기록한다.',
 visual='밝은 금속적 요약 화면을 지도·도로·지형 영상층으로 전환하고 사선의 흰 경계·갈색 캡슐 라벨로 구획을 묶는다. 실사/CG·원본 자산은 미확인이다.',
 steps=[(143,'23.7억원·26건 총량 구도'),(143.5,'총량 구도 유지'),(144,'왼쪽 지도/도로 영상과 대각 경계, 오른쪽에 총량 일부 잔존'),(144.5,'업무 영상이 대부분 펼쳐진 중간 상태'),(145,'여러 도로·지형 영상이 사선으로 분할'),(145.5,'세 영상 구획과 하단 라벨'),(146,'세 영상 분할·라벨 상태; 내부 도로 시점도 앞 표본과 다름')],
 relation='첫 영상층 가시성 (143.5,144]초. 144초 옛 총량 구도와 새 영상이 겹친다. 경계 전개·세 구획 완성과 안쪽 영상의 카메라/대상 변화는 다른 사건이다. 구획의 정확 완료를 144초로 통일하지 않는다.',
 tags=['PROPERTY-VISIBILITY','TIME-SEQUENCE','TIME-OVERLAP','FUNCTION-REVEAL'],
 conditions='여러 업무 사례를 펼쳐 소개할 때 후보. 서로 다른 시간·범위의 영상을 비교 데이터처럼 읽히게 한다면 구별 표시를 검토한다.',
 diff='완성 화면의 단순 컷 교체가 아니라 대각 경계/여러 구획의 전개이다. 관측된 공개 영역을 AE 마스크 구현으로 단정하지 않는다.',
 unknown='영상별 실제 원본과 시간 범위, 경계별 정확 시작/완료, 내부 카메라 운동의 분해, 마스크 종류/속도 곡선'),
 dict(id='B-M3',case='VC-CASE-B',region='B-04→B-05',sheet='project-panel',a=147,b=150,
 title='지원 비중 숫자 정착 뒤 도넛·막대·보조 카드 후속 채움: 완료 시차',
 info='프로젝트 지원 주요 활동: BIM 설계 19.4억원/3건·약82%가 핵심, BIM 지원 1.6억원/7건·해외사업 지원 1.3억원/1건·디자인 지원 1.4억원/15건이 보조이다. 총량과 하위 유형의 관계이며 금액/건수를 합쳐 하나의 단위로 만들지 않는다.',
 screen='영상 3구획에서 왼쪽 지도 띠+주 도로 영상, 오른쪽 통계판으로 재구성된다. 정보판 안은 큰 BIM 행/아래 3보조 카드/오른쪽 큰 도넛이다. 동급 4행 목록이 아니다.',
 visual='따뜻한 프레임·아이보리 정보면·갈색 주항목/도넛·녹색/파랑/갈색 보조 카드·점무늬·도시 실루엣을 결합한다. 업무 영상은 배경층으로 계속 달라진다.',
 steps=[(147,'세 영상 구획과 하단 라벨'),(147.5,'영상 3구획 유지'),(148,'오른쪽 정보판·미완성 제목·약44%'),(148.5,'약64%·첫 보조 카드, 배경 지도/주 도로 중심으로 재구성'),(149,'약82%·추가 항목, 디자인 지원 카드는 작게 보임'),(149.5,'82% 유지·3카드가 더 채워짐·도넛의 보조 분할색이 추가·디자인 카드가 더 크게 보임'),(150,'대표 구성 상태. 기존 연결 원본 PNG에서 제목/금액·건수/막대/약82% 귀속을 확인')],
 relation='비중 끝값 최초 관측 (148.5,149]초. 149초 82%가 보인 뒤에도 149.5초 도넛 다른 분할색/보조 카드 구성이 보강된다. BIM 행과 작은 카드의 막대도 후속 표본에서 더 채워진다는 기존 기록을 보존하되 정확 길이·데이터 스케일은 측정하지 않았다. 완성 비중 숫자와 진행 중 도형/카드가 한 시점에 공존한다.',
 tags=['REL-PART','PROPERTY-VALUE','PROPERTY-SIZE','PROPERTY-VISIBILITY','TIME-SEQUENCE','TIME-DELAY','TIME-OVERLAP','TIME-HOLD'],
 conditions='실제로 우세한 핵심 비중 1개와 나머지 구성도 설명할 때 후보. 우세 항목이 없거나 구성 분모/단위가 다르면 같은 위계를 강제하지 않는다. 149초 중간 도형 길이를 최종 비율로 판정하지 않는다.',
 diff='A-M3와 완료 시차를 공유하지만 금액+상승 이미지가 아닌 지원 유형의 비중/하위 카드/배경 재구성이다. VC-COMP-04와 연결하며 동일 자산 확인은 아니다.',
 unknown='149초 이후 각 막대/분할색의 정확 종료, 크기 변화의 실제 Scale 여부, 배경 카메라/레이어 원인, 읽기 유지 충분성·음성 관계')
]

source_paths=[INPUT/'input.md',INPUT/'motion/01_계약_수집기록.md',INPUT/'motion/02_프로젝트지원_수집기록.md',INPUT/'motion/03_재사용단위_색인.md',INPUT/'motion/05_근거와_실행기록.md']
src=[dict(id=f'SR{i}',path=str(p),sha256=sha(p),role='provided_input' if i==0 else 'prior_analysis_preserved') for i,p in enumerate(source_paths)]
ev=[]
for r in rows:
 p=INPUT/f'motion/evidence/{r["sheet"]}.jpg'
 ev.append(dict(id='E-'+r['id'],path=str(p),sha256=sha(p),time={'start':r['a'],'end':r['b']},kind='provided_contact_sheet',sample_interval_seconds=0.5,continuous_observation=False,time_mapping_status='imported_labels_and_prior_record_not_revalidated_from_MP4',dimensions={'width':2160,'height':705},transform='prior whole-frame proportional reduction/contact-sheet; original 7680x2160 per input; exact sheet assembly parameters unverified'))
for eid,rel,t in [('E-A112','contract/f_03360_112.000.png',112),('E-B150','project/f_04500_150.000.png',150)]:
 p=ROOT/'value-creation-pilot-20261019/extraction/cases/VALUE'/rel
 ev.append(dict(id=eid,path=str(p),sha256=sha(p),time={'start':t,'end':t},kind='existing_linked_PNG_context' if t==112 else 'existing_linked_PNG',dimensions={'width':7680,'height':2160},time_mapping_status='existing_filename_and_prior_analysis_not_MP4_pts_revalidation',continuous_observation=False))

claims=[];units=[];facets=[];kl=[];uses=[];comps=[];events=[];el=[];reviews=[];unknown=[]
def claim(id,text,ev_ids,src_ids,kind='observed'):
 claims.append(dict(id=id,text=text,basis_kind=kind,evidence_ids=ev_ids,source_record_ids=src_ids));return id
def knowledge(uid,cid,rel,clids,why):
 kl.append(dict(id=f'K{len(kl)+1}',unit_id=uid,concept_id=cid,relation=rel,basis_kind='inferred',claim_ids=clids,rationale=why))
def review(uid,cid,status,reason,evs,cls,scope,next_probe):
 reviews.append(dict(id=f'RV{len(reviews)+1}',unit_id=uid,criterion_id=cid,status=status,reason=reason,evidence_ids=evs,claim_ids=cls,reviewer='AI self-review, 2026-10-19',scope=scope,next_probe=next_probe))
 knowledge(uid,cid,'review_relevant',cls,'관련 지식의 질문을 현재 단위에 선택한다. 실제 판정·근거는 별도 review에 둔다.')
 knowledge(uid,cid,'evaluated_against',cls,'연결된 실제 검토 행의 범위와 상태로만 해석한다. 제작 품질·회사 승인이 아니다.')

for cid,title,summary in [('VC-CASE-A','계약 부문 전체 사례','수주 구성→비용→실제 매출 구역 누적, 녹색/밝은 면과 주황 매출 강조. 본 출력은 96–100/103–106/108–111초 재검토와 112초 기존 문맥 PNG에 한정.'),('VC-CASE-B','프로젝트 지원 전체 사례','요청·지원 관계도→26건·23.7억원 총량→업무 영상→BIM 핵심 비중+보조 3카드. 본 출력은 136–140/143–146/147–150초 표본 재검토.')]:
 units.append(dict(id=cid,kind='case',title=title,observation_status='observed_sampled',definition_version='preserved-input+knowledge-link-local-0.1',summary=summary))

for r in rows:
 id=r['id'];c='C-'+id;ei=['E-'+id]+(['E-A112'] if id=='A-M3' else ['E-B150'] if id=='B-M3' else [])
 si=['SR1' if id.startswith('A') else 'SR2','SR3','SR4']
 claim(c,'[기존 관측 재사용+제공 시트 대조] '+r['relation']+' 표본: '+' / '.join(f'{t}s {x}' for t,x in r['steps']),ei,si)
 ic=claim(c+'-interpretation',r['info']+' 기능·재사용 조건은 화면과 기존 기록에 기초한 분석자의 해석이며 원제작 의도 미확인.',ei,si,'inferred')
 units.append(dict(id=id,kind='detail',title=r['title'],observation_status='observed_sampled',definition_version='local-motion-knowledge-review-0.1',summary=f'{r["case"]}/{r["region"]}: {r["info"]} {r["relation"]}',prior_definition_ref=f'{source_paths[3]}#3-독립-모션-묶음---전체-흐름과-연결',prior_id_preserved=True))
 for dom,key in [('information','info'),('screen','screen'),('visual','visual'),('motion','relation')]:
  facets.append(dict(id=f'F-{id}-{dom}',unit_id=id,domain=dom,name=dom,description=r[key],basis_kind='inferred' if dom=='information' else 'observed',claim_ids=[ic if dom=='information' else c],precision='qualitative',value=None,method='provided contact sheet + prior records; no new extraction'))
 for cid in r['tags']:
  knowledge(id,cid,'classified_as',[c],f'{r["region"]}/{r["a"]}–{r["b"]}초의 대상·속성·시간관계에 한정. {r["relation"]} 기능 태그는 분석자의 해석, 관측·원본 AE 속성·의도 승인과 구분.')
 uses.append(dict(id='USE-'+id,definition_id=id,definition_version='local-motion-knowledge-review-0.1',case_unit_id=r['case'],region=r['region'],content=r['info'],time={'start':r['a'],'end':112 if id=='A-M3' else r['b']},evidence_ids=ei,claim_ids=[c,ic],differences=[r['diff']],unverified=[r['unknown'],'다른 내용/화면비 적용·동일 자산·회사 규칙은 검증하지 않음'],conditions=[{'text':r['conditions'],'validation':'observed_case_only'}]))
 comps.append(dict(**{'from':r['case'],'to':'USE-'+id},relation='contains',basis_kind='inferred',claim_ids=[c]))
 unknown.append(dict(id='U-'+id,unit_id=id,question=r['unknown'],impact='원본 동작의 정확한 구현·전편 완료·새 사례 적용성 확정을 막음. 확인된 단계/관계 수집은 유지.',next_probe='별도 범위 승인 시 해당 경계/대상만 원본 크기 ROI·촘촘한 표본·추출 시간 매핑을 확인. 현재 실행에서는 수행하지 않음.'))
 review(id,'MR-04','pass','기존 기록의 누적/순서/겹침을 시트의 시작·중간·끝과 대조하여 현재 연결 기록에 보존했다. 읽기 순서의 전달 효과나 원본 의도 적합성 통과는 아님.',ei,[c],'6개 기존 창의 기록 일관성·시간관계 보존에 대한 자기 검토','원본 연속 관찰이나 효과 검증은 별도 요청 시')
 review(id,'AP-06','hold','추적한 동일 특징의 진행 중 변화율을 측정하지 않았다. 정착 또는 순서 확인만으로 이징/속도 적합성을 통과시킬 수 없다.',ei,[c],'가감속 원값/곡선의 판정 가능성','해당 대상·같은 속성의 진행 중 표본을 별도 확인하고 오차 포함 변화율 비교')
 review(id,'IP-05','not_reviewed','MP4·오디오·시나리오 입력이 없고 청취하지 않았다. 음성/설명과 동작 대응을 실제 검토하지 않았다.',ei,[c],'실제 발화와 화면 시간 대응','별도 요청과 음성/시나리오 근거 확보 후 대응')
 review(id,'Q-MOTION-01','hold','정보의 표본상 완성 차이는 기록했으나 완성 후 퇴장·발화·시청 조건이 없어 충분한 읽기 시간은 판정할 수 없다.',ei,[c],'실제 시청에서 완성 정보의 읽기 유지 충분성','완성 이후 유지·퇴장/발화/시청 환경을 확보하고 디자인/필요시 시청자 검토')
 if id in ['A-M3','B-M1','B-M3']:
  review(id,'MR-08','pass','변화 중 숫자와 창 끝/끝값을 구별하고 중간 표시를 해당 초의 실적 데이터로 저장하지 않았다. 실제 집계 정확성은 검수하지 않았다.',ei,[c],'분석 기록에서 값 변화의 의미를 과장하지 않았는지 검토','사업 집계 사실·분모는 내용 담당자 근거로 후속 검토')
 if id in ['A-M3','B-M3']:
  knowledge(id,'AP-05','review_relevant',[c],'숫자 정착과 후속 도상 완성의 차이를 살피는 참고 질문. 순차 조립인지 관성의 후속 표현인지 미확인이라 AP-05 적용/효과는 판정하지 않음.')

for case,ids,a,b,summary in [('VC-CASE-A',['A-M1','A-M2','A-M3'],96,112,'수주 재배치와 비용 누적→기존 지표를 남긴 매출 판 추가→숫자/도상의 시차 조립. 100–103/106–108초는 표본 창 사이 미검수.'),('VC-CASE-B',['B-M1','B-M2','B-M3'],136,150,'관계도 퇴장+총량 중첩→총량과 업무 영상의 중첩 전개→영상 배경 재구성과 통계판/카드 누적. 140–143/146–147초는 창 사이 미검수.')]:
 fid=case+'-FLOW-local';cs=['C-'+i for i in ids];es=['E-'+i for i in ids]+(['E-A112'] if case.endswith('A') else ['E-B150'])
 units.append(dict(id=fid,kind='flow',title=case+' 전체 흐름 연결(부분 창)',observation_status='observed_sampled',definition_version='local-flow-0.1',summary=summary))
 uses.append(dict(id='USE-'+fid,definition_id=fid,definition_version='local-flow-0.1',case_unit_id=case,time={'start':a,'end':b},evidence_ids=es,claim_ids=cs,differences=['세부 창을 연결한 이번 지역 흐름. 창 사이 연속 모션을 새 관측한 정의가 아님.'],unverified=['창 사이 및 앞뒤 경계·전체 클립/음성 미검수'],conditions=[{'text':'장 전체 맥락을 찾는 부분 흐름 후보. 창 길이의 합을 정밀 검수 시간/완료율로 사용하지 않음.','validation':'observed_case_only'}]))
 for i in ids:comps.append(dict(**{'from':fid,'to':'USE-'+i},relation='contains',basis_kind='inferred',claim_ids=['C-'+i]))
 for x,y in zip(ids,ids[1:]):comps.append(dict(**{'from':'USE-'+x,'to':'USE-'+y},relation='precedes',basis_kind='observed',claim_ids=['C-'+x,'C-'+y]))
 knowledge(fid,'TIME-SEQUENCE','classified_as',cs,'창별 관측 순서를 연결한 전체 흐름. 창 사이 누락과 동작 내부 중첩은 별도 보존한다.')

def event(id,unit,title,a,b,start=None,end=None):
 x=dict(id=id,unit_id=unit,title=title,status='observed_sampled',time={'start':a,'end':b},claim_ids=['C-'+unit],time_semantics='sample-supported range; not exact event duration')
 if start is not None:x['start_bounds']=start
 if end is not None:x['end_bounds']=end
 events.append(x)
def er(a,b,rel,unit):el.append(dict(**{'from':a,'to':b},relation=rel,basis_kind='observed',claim_ids=['C-'+unit]))
event('EA1-move','A-M1','기존 수주 구역 왼쪽 재배치',96.5,97.5)
event('EA1-panel','A-M1','비용 판/제목 최초 가시성',97,97,[96.5,97])
event('EA1-icons','A-M1','동전→문서 포함 도상',97.5,98)
event('EA1-caption','A-M1','현재까지 투입 캡슐 최초 표본',99,99,[98.5,99])
event('EA1-value','A-M1','비용 숫자 첫 표본(끝값 아님)',100,100,[99.5,100])
er('EA1-move','EA1-panel','overlaps','A-M1');er('EA1-panel','EA1-icons','precedes','A-M1');er('EA1-icons','EA1-caption','precedes','A-M1');er('EA1-caption','EA1-value','precedes','A-M1')
event('EA2-panel','A-M2','매출 판 진입·위치 변화',104,104.5,[103.5,104])
event('EA2-title','A-M2','매출 제목 첫 판독 표본',105,105)
event('EA2-caption','A-M2','중복 제외 설명 첫 표본',106,106)
event('EA2-context','A-M2','수주/비용 판 동반 유지 표본',103,106)
er('EA2-panel','EA2-title','precedes','A-M2');er('EA2-title','EA2-caption','precedes','A-M2');er('EA2-context','EA2-panel','accompanies','A-M2')
event('EA3-number','A-M3','매출 표시 0.8→10.8→12.9억원 끝값 도달',109.5,110.5,end=[110,110.5])
event('EA3-icon','A-M3','받침/막대→111 미완성→112 상승 화살표 완성',108,112,end=[111,112])
event('EA3-hold','A-M3','12.9억원 유지 표본(연속 검수 아님)',110.5,112)
er('EA3-icon','EA3-number','overlaps','A-M3');er('EA3-icon','EA3-number','continues_after','A-M3');er('EA3-hold','EA3-icon','accompanies','A-M3')
event('EB1-exit','B-M1','관계도 약화/좌우 분산 퇴장',137.5,138.5)
event('EB1-new','B-M1','새 건수/금액 등장·증가',138,140)
er('EB1-exit','EB1-new','overlaps','B-M1')
event('EB2-old','B-M2','총량 화면 잔존',143,144)
event('EB2-wipe','B-M2','대각 경계/영상층 공개',144,145.5,[143.5,144])
event('EB2-inner','B-M2','세 도로 영상 구획의 내부 장면 변화',144.5,146)
er('EB2-old','EB2-wipe','overlaps','B-M2');er('EB2-inner','EB2-wipe','accompanies','B-M2')
event('EB3-number','B-M3','비중 약44→64→82% 도달',148,149,end=[148.5,149])
event('EB3-follow','B-M3','도넛 분할색/카드·막대 보강이 82% 도달 뒤에도 이어짐',148.5,150)
event('EB3-size','B-M3','디자인 지원 카드 겉보기 크기/가시성 차이',149,149.5)
event('EB3-bg','B-M3','영상3구획→지도띠/주 도로 배경 재구성',147.5,149)
er('EB3-follow','EB3-number','continues_after','B-M3');er('EB3-follow','EB3-number','overlaps','B-M3');er('EB3-size','EB3-follow','accompanies','B-M3');er('EB3-bg','EB3-number','overlaps','B-M3')

limitations=['기존 prior analysis+6개 0.5초 contact sheet의 재검토. 새 원본 연속 재생·재추출/전편 정밀 관측을 하지 않았다.','입력 MP4 SHA/434.4초/7680x2160/30fps는 제공 메타데이터이며 이번에 MP4 자체나 PTS 매핑을 검증하지 않았다.','112초 PNG는 A-M3의 기존 연결 근거로 확인한 창 밖 문맥이고 150초 PNG는 기존 연결 상세 표본이다. 음성은 듣지 않았다.','시트 축소로 미세 문구/막대 길이/곡선의 정밀 측정은 제한된다. 정확 이징·opacity·mask·Scale/실제3D 제작·제작 의도 미상.','단일 영상의 로컬 후보/사용처이다. 반복 확인·동일 자산·새 목적 효과·회사 규칙 승인·R4 정본 등록·글로벌 활성화·새 화면 제작을 수행하지 않았다.','조회는 정확ID/명시 문자열이다. 기계 검사 통과는 연결/해시/범위 확인이며 의미 정확성·전편 발견/스킬 성능 승인이 아니다.']
doc=['# 기존 모션 6창 — 00 지식 연결 수집 기록','', '판본: local-motion-knowledge-review-0.1 / 분석 스킬 draft.13 개발 후보의 명시 경로 실행. 실제 사용판·정본 변경 없음.','', '## 사례 요약', '', '| 사례 | 정보 관계·구도·표현 | 전체 흐름과 핵심 미상 | 상세 |','|---|---|---|---|', '| VC-CASE-A / A-02 | 수주 17.5억원 구성, 비용 8.7억원, 실제 매출 12.9억원의 다른 역할. 넓은 수주/좁은 비용/넓은 매출 구역. 녹색·밝은 판·도시 배경/주황 성과 도상 | 재배치+비용 누적→매출 판 추가→금액과 도상 조립. 숫자는 먼저 끝값, 상승 화살표는 뒤 완성. 정확 곡선·창 사이·음성 미검수 | [A-M1](#a-m1)·[A-M2](#a-m2)·[A-M3](#a-m3) |', '| VC-CASE-B | 요청↔지원 관계도→26건·23.7억원→업무 영상→BIM 설계 19.4억원/3건·약82%와 보조3유형. 아이보리/구리색·금속적 수치·영상층·정보판 | 관계도 퇴장과 총량 등장 중첩→대각 영상 전개→통계판·카드 누적. 82% 뒤 분할색/카드가 더 채워짐. 읽기 충분성·음성 미검수 | [B-M1](#b-m1)·[B-M2](#b-m2)·[B-M3](#b-m3) |', '', '원본: 가치창출성과 영상_260923_v3.mp4, SHA-256 `be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa`, 제공 메타데이터 434.4초/7680×2160/30fps. MP4/오디오/시나리오를 이번에 받거나 열지 않았다. 기존 전체 상세·문구·정지 장면은 아래 원기록으로 보존한다. 새 창 사이 연결 관측을 만들지 않았다.', '', '## 전체 상세 원문과 범위', '']
for p in source_paths:doc.append('- '+link(p))
doc += ['', '실제 표본 범위는 96–100 / 103–106 / 108–111 / 136–140 / 143–146 / 147–150초다. 112초 기존 PNG는 첫 시차의 끝 문맥, 150초 기존 PNG는 두 번째 시차의 상세 귀속 확인에 사용했다. 창 길이 합은 정밀 검수 시간이나 완료율이 아니다.', '', '두 전체 흐름의 이번 지역 ID는 `VC-CASE-A-FLOW-local@local-flow-0.1`, `VC-CASE-B-FLOW-local@local-flow-0.1`이며 포함된 A-M1~3/B-M1~3은 기존 번호의 뜻을 유지한다. 세부의 새 판본은 기존 상세에 지식 연결을 덧붙인 지역 판본이다. `VC-FLOW-01`의 요약 해석이나 새 시안 동작을 원본으로 섞지 않는다.','']
for r in rows:
 doc += [f'<a id="{r["id"].lower()}"></a>',f'## {r["id"]} — {r["title"]}','',f'정의/사용처: `{r["id"]}@local-motion-knowledge-review-0.1` → `USE-{r["id"]}` → `{r["case"]}/{r["region"]}` / {r["a"]}–{r["b"]}초. 최초 입력 단위와 현재 차이를 유지하는 지역 후보이며 등록/회사 승인 아님.','',f'- 정보 관계·기능 해석: {r["info"]}',f'- 화면 구조·기하: {r["screen"]}',f'- 표현 언어·층: {r["visual"]}','','| 표본(초) | 기존 기록과 현재 시트 대조 |','|---|---|']
 doc += [f'| {t:g} | {x} |' for t,x in r['steps']]
 doc += ['',f'시간 관계: {r["relation"]}','',f'00 분류(분석자의 해석): '+', '.join(f'`{x}`' for x in r['tags'])+'. 역할·속성·시간관계를 같은 종류로 합치지 않는다.', '',f'조합·차이: {r["diff"]}','',f'사용/제외 조건: {r["conditions"]} 관측 사례 기반 조건이며 새 내용/화면비 시험은 하지 않았다.','',f'미상: {r["unknown"]}. 확인된 단계는 보존하고 정밀 구현/전편 완료만 유보한다. 별도 요청 시 해당 경계·대상만 원본 크기 ROI/촘촘한 표본으로 확인한다.','', '근거: '+link(INPUT/f'motion/evidence/{r["sheet"]}.jpg')+' / '+link(source_paths[4], '기존 근거표·시각·프레임 해시')+'. 현재 해시와 대조 메모는 [근거대조](01_근거대조.md).','']
doc += ['## 지식 조회와 선택한 검토','', '정본 카탈로그는 `catalog.json`에 167개(용어 76행=현행75+폐기1, 기본지식65, 품질질문26)와 문맥11개를 경로/해시로 고정했다. 전 항목 의무 적용이 아니다. 실제 18개 ID 조회의 명령·결과·정의/예외는 `knowledge_queries.json`에 있다.','', '| 실제 읽은 지식·문맥 | 이번 적용 이유/제한 |','|---|---|','| TIME-SEQUENCE / TIME-OVERLAP / TIME-DELAY / TIME-HOLD | 사건·대상·범위를 함께 표기한다. 완료 시차는 물리적 관성·실제 공정 순서·정확 키프레임의 증거가 아니다. |','| PROPERTY-VALUE / POSITION / VISIBILITY / SIZE | 표시 값/렌더 위치/보이는 정도/겉보기 크기를 분리한다. AE 레이어·opacity·mask·Scale 원값을 만들지 않는다. |','| FUNCTION-REVEAL / FUNCTION-CONTEXT / REL-PART | 읽는 순서/기존 맥락/구성 관계를 찾는 해석. 격자·색·부품과 같은 축으로 합치지 않는다. |','| MR-04@0.1.1·심화카드 | 실제 단계와 중첩을 보존하는 질문. 순차 공개를 실제 업무 순서로 확정하지 않으며 고정 stagger/UI 시간값을 강제하지 않는다. |','| MR-08@0.1.1·심화카드 / UX-CAND-05 | 숫자의 중간 표시와 끝값을 구분. 보간/장식 여부의 제작 방식이나 사업 집계 사실은 별도다. |','| AP-05 / 심화카드 / UX-CAND-02 | 시간차 관찰의 참고. 단순 순차 조립과 관성의 후속 동작은 구분이 안 되어 적용 효과는 미판정. |','| AP-06·심화카드 | 진행 중 동일 관측량의 변화율·오차를 확인하지 않아 곡선 판정 보류. 정착 표본만으로 감속을 만들지 않는다. |','| IP-05·심화카드 | 오디오/시나리오 없는 실제 음성 대응은 미검수. 화면의 후속 도상 차이를 음성 싱크 오류로 판정하지 않는다. |','| Q-MOTION-01 | 정보 완성 이후 읽고 연결할 구간/퇴장/발화/시청 조건 필요. 표본 창 길이로 읽기 충분성을 통과시키지 않는다. |','| R3 source review의 local-animated-infographic / local-chart-animation / local-motion-art-direction | 정보 그룹/순서·값/단위·대상별 일관성을 참고한다. 고정8frame·실제값 초과·고정 ease/pace는 채택하지 않는다. 외부 원문 설치/실행/복사 없음. |','| R8 현재 안내 / R7 판정운영 | 구조 확인, 내용 재검토, 실제 시청효과, 회사 승인을 분리. R4v0.2와 이번 부속0.1을 자동 동등화/등록하지 않는다. |', '', '### 실제 판정과 미판정','', '| 대상/기준 | 실제 상태 | 확인한 범위/이유 | 다음 확인 |','|---|---|---|---|','| 6창 / MR-04 | pass | 기존 기록과 시트의 순서·중첩을 현재 수집에 보존한 일관성 자기검토. 전달 효과/원제작 의도 판정은 아님 | 원본/시청 효과는 별도 |','| A-M3·B-M1·B-M3 / MR-08 | pass | 중간 표시를 실적 시계열로 저장하지 않고 끝값/단위를 구분 | 사업 집계 사실은 내용 근거 별도 |','| 6창 / AP-06 | hold | 같은 대상의 진행 중 속도 변화율/오차 미측정 | 대상·속성별 촘촘한 표본 |','| 6창 / IP-05 | not_reviewed | 청취/실제 발화 대응을 수행하지 않음 | 오디오/시나리오 확보 후 별도 범위 |','| 6창 / Q-MOTION-01 | hold | 완성 이후 유지·퇴장/발화/시청 조건 부족 | 필요한 구간·디자인/시청자 검토 |','| A-M3·B-M3 / AP-05 | review_relevant만 | 시간 차 참고질문 연결; 관성의 후속 효과인지/읽기에 도움이 되는지는 실제 판정하지 않음 | 필요 시 별도 검토 |', '', '실제 review 행은 `motion.links.json`의 reviews, 관련성은 knowledge_links의 review_relevant, 실제 검토 연결은 evaluated_against로 분리했다. pass는 명시된 분석 기록 보존 범위만 뜻한다.', '', '## 근거·조회·남은 범위', '', '- [근거대조와 현재 해시](01_근거대조.md)', '- [실제 조회 안내와 결과](02_조회안내.md)', '- [연결 편집 원본 JSON](motion.links.json) / [생성 색인](index.json) / [검사 결과](validation.json)', '', '미검수는 창 사이 100–103/106–108/111–112(기존 끝 문맥만)/140–143/146–147초, 6창 밖 상세 모션, 원본 PTS 재검증·연속 움직임·음성·정밀 원값·동일 자산·다른 자료 적용이다. 현재 요청은 기존6창의 기록/지식/사용처/근거 연결까지다. 새 화면·영상·PDF·정본 교체는 수행하지 않았다.', '', '다음 큰 묶음은 사용자 선택 후 가능하다: A(추천) 이번 연결의 2개 시차 사례를 내용/분류 관점에서 검토 — 현재 근거/보류를 확인하고 새 원본 관찰은 유보. B 같은6창의 근거 시간매핑/경계 보강 — 별도 원본 접근 범위가 필요하고 전편은 유보. C 기존 다른 관측 창으로 같은 연결 구조 확대 — 대상 창을 선택하며 새 제작은 유보. D 구조를 동결해 향후 DB 이관 요구만 정리 — 현 기록을 유지하고 추가 관측/실제 이관은 유보. 이번 실행은 선택 의존 작업에 착수하지 않는다.']
(OUT/'00_수집기록.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
src.append(dict(id='SR5',path='00_수집기록.md',sha256=sha(OUT/'00_수집기록.md'),role='current_collection_markdown'))

evidence_doc=['# 근거 대조 — 실제 본 자료와 주장 범위','','이번 AI가 6개 JPG를 실제 표시해 기존 수집 기록의 시작·중간·끝/대상 내부·주변·배경 변화와 비교했다. 시트 2160×705는 표시 도구에서 2048×668로 축소되었다. 기존112/150초 PNG(7680×2160)는 표시 도구에서 2048×576으로 축소되었다. 새 크롭·재추출·연속 재생·음성 분석 없음. 미세 문구와 막대 수치는 이 표시 방식의 한계를 받는다.','', '| 근거 | 실제 범위/종류 | 현재 SHA-256 |','|---|---|---|']
for e in ev:evidence_doc.append(f'| {link(e["path"],e["id"])} | {e["time"]["start"]}–{e["time"]["end"]}초 / {e["kind"]} | `{e["sha256"]}` |')
evidence_doc += ['', '## 중요한 대조 결과','','| 주장/대상 | 현재 근거/위치 | 결과와 확정 수준 |','|---|---|---|','| A-M1 비용 내용 순서 | contract-reflow 97/97.5/98/99/100, 판 내부 | 외형/제목·동전·문서·캡슐·숫자의 순서가 구분된다. 100초 금액은 중간 상태로 취급; 끝값8.7은 이 창의 완성값으로 만들지 않음 |','| A-M2 외형·문구 | contract-panel 103.5/104/104.5/105/106 | 첫 판 가시성(103.5,104]와 뒤 제목/설명 보강을 확인. 마스크/정착 정확 프레임 미확인 |','| A-M3 숫자/상승 도상 | contract-number 109.5/110/110.5/111 + E-A112 오른쪽 판 | 0.8→10.8→12.9, 111에 끝값 유지. 112 PNG에서12.9와 완성 화살표. 시트에는112가 없어 별도 문맥 PNG를 사용했다고 명시 |','| B-M1 퇴장/등장 | project-reflow 137.5/138/138.5 |138초 옛 판이 좌우에 남은 동시에 새 수치가 보임. 단순 순차로 정리하지 않음 |','| B-M2 바깥 경계/안쪽 영상 | project-wipe 143.5/144/144.5/145/146 |144초 새 영상과 옛 총량이 공존. 사선 구획 전개와 내부 도로 시점 변화 분리. 마스크 구현은 미확인 |','| B-M3 숫자/도넛/카드/배경 | project-panel 148/148.5/149/149.5/150 + E-B150 |약44→64→82%.149의82% 뒤149.5 도넛 보조색·디자인 카드가 보강. 막대 후속 진행은 기존 기록과 시각 변화 수준으로 보존; 정확 길이/종료시각 미측정. 배경도3분할→지도띠/주 도로로 재구성 |','| B-M3 실제 내용 귀속 | E-B150 정보판 내부 |BIM설계19.4억/3건·약82%, 보조1.6억/7건·1.3억/1건·1.4억/15건의 서로 다른 금액/건수 표기를 확인. 화면 길이를 실제 스케일로 확정하지 않음 |', '', '## 원래 근거로 돌아가기','','제공 `05_근거와_실행기록.md`는 각 시트의 개별 프레임 파일명/시각/SHA와 기존 추출 실행기록 경로를 포함한다. 그 전체 원문을 SR4로 해시 고정하고 각 주장/사용처에 연결했다. 이번에 해당 개별 프레임 46개·추출로그 전체를 재열람/재해시한 것은 아니다. 원본 MP4의 SHA는 공통입력에서 물려받은 값이다. JPG와 현재 연결 PNG의 해시는 실제 파일에서 계산했다. PTS·편집원점·SAR/색범위/시트 조립 원값은 재검증하지 않았다. 원래 제공된 경로/해시를 새 검증이라고 바꾸지 않았다.', '', '수집의 원본 근거와 00의 분류 근거는 다르다. 00 catalog 해시가 맞아도 영상 내용/시간 진실성이나 권리를 증명하지 않는다. 기존 정본 DB·실제 사용판·이전 수집 문서는 수정하지 않았다.']
(OUT/'01_근거대조.md').write_text('\n'.join(evidence_doc)+'\n',encoding='utf-8')

record=dict(schema_version='video-knowledge-links-0.1',record_id='motion-six-windows-local-20261019',version='0.1.0',source={'sha256':'be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa','duration_seconds':434.4,'metadata_origin':'provided_input_not_MP4_rehash'},source_records=src,evidence=ev,claims=claims,units=units,facets=facets,knowledge_links=kl,uses=uses,composition_links=comps,events=events,event_links=el,reviews=reviews,unknowns=unknown,limitations=limitations,company_approved=False,canonical_registered=False)
save('motion.links.json',record)
commands=[]
def run(args,name):
 cmd=[sys.executable,'-B','-X','utf8',str(SKILL/'scripts/knowledge_links.py')]+args
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 data=json.loads(r.stdout) if r.returncode==0 else {'error':r.stdout,'stderr':r.stderr}
 save(name,data);commands.append(dict(command=cmd,exit_code=r.returncode,result_file=name,stderr=r.stderr))
 if r.returncode:raise RuntimeError(r.stderr)
 return data
run(['check','--catalog',str(OUT/'catalog.json'),'--record',str(OUT/'motion.links.json')],'validation.json')
run(['index','--catalog',str(OUT/'catalog.json'),'--records',str(OUT/'motion.links.json'),'--out',str(OUT/'index.json')],'index-build.json')
for cid in ['TIME-DELAY','PROPERTY-VALUE','TIME-OVERLAP','MR-04','IP-05','Q-MOTION-01']:
 run(['query','--catalog',str(OUT/'catalog.json'),'--index',str(OUT/'index.json'),'--id',cid,'--motion-only'],f'query-{cid}.json')
run(['query','--catalog',str(OUT/'catalog.json'),'--index',str(OUT/'index.json'),'--query','가족사별','--motion-only'],'query-excluded-proposal.json')
run(['query','--catalog',str(OUT/'catalog.json'),'--index',str(OUT/'index.json'),'--query','A-M3','--motion-only'],'query-definition-A-M3.json')
save('commands.json',commands)
qdoc=['# 실제 조회 안내','','실행 가능한 도구: '+link(SKILL/'scripts/knowledge_links.py')+' / Python: '+str(Path(sys.executable)),'','아래 명령은 이 outputs 폴더를 현재 디렉터리로 실행한다. 명령 전체·종료코드는 `commands.json`, 실제 반환 원문은 `query-*.json`이다. 모두 종료0을 확인했다. 원문/부속이 바뀌면 해시검사를 거쳐 색인을 재생성해야 한다.','', '```powershell',f"$py = '{Path(sys.executable).as_posix()}'",f"$tool = '{(SKILL/'scripts/knowledge_links.py').as_posix()}'",'& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --id TIME-DELAY --motion-only','& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --id PROPERTY-VALUE --motion-only','& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --id MR-04 --motion-only','& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --query A-M3 --motion-only',"& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --query '가족사별' --motion-only",'```','','| 실제 질문/명령 | 실제 반환 단위 | 결과 원문 |','|---|---|---|']
for cmd in commands:
 if cmd['result_file'].startswith('query-'):
  d=json.loads((OUT/cmd['result_file']).read_text(encoding='utf-8'))
  qdoc.append(f'| {cmd["command"][-2] if cmd["command"][-1]=="--motion-only" else cmd["command"][-1]} | '+(', '.join(x['unit']['id'] for x in d.get('uses',[])) or '0건')+f' | [{cmd["result_file"]}]({cmd["result_file"]}) |')
qdoc += ['', '## 완료 시차 조회의 실제 내용','','`TIME-DELAY`는 A-M3/B-M3 두 사용처를 반환했다. 각 결과의 unit/definition_version → use.case_unit_id·region·content·time → evidence.path/sha256 → SR1/SR2/SR4 원기록 참조를 따라갈 수 있다. claims와 event_links는 `motion.links.json`에서 확인한다.','', '- A-M3 → VC-CASE-A/A-02, 실제 발생 매출12.9억원 강조. 숫자(110,110.5]초 끝값 도달,111→112초 상승 화살표 완성 차이. E-A-M3 시트와 E-A112 기존 문맥 PNG, 원기록 SR1/SR4.','- B-M3 → VC-CASE-B/B-04→B-05, BIM설계19.4억원/3건·약82%와 보조유형. 비중(148.5,149]초 도달 뒤149.5 도넛/카드 후속 보강. E-B-M3 시트와 E-B150 기존 PNG, 원기록 SR2/SR4.','', '왕복 확인: 사례 VC-CASE-A의 USE-A-M3 → 정의 A-M3@local-motion-knowledge-review-0.1 → TIME-DELAY → 다른 사용처 USE-B-M3 → B-M3의 현재 내용·근거·차이. 반대 방향으로도 use가 정의/사례를 보존한다. 개념 공유는 같은 자산/같은 패턴 확정이 아니다.', '', '`MR-04` 결과는 관련성 연결과 실제 pass 검토(기록의 순서/중첩 보존 범위)를 함께 반환한다. `IP-05`는 not_reviewed, `Q-MOTION-01`은 hold를 반환한다. 관련 원칙이 있다는 이유로 통과하지 않는다. `가족사별` 조회는0건이며 새 시안의 가족사별→유형별 교체를 관측 모션에 포함하지 않았음을 확인했다. 정확ID/부분문자열 조회라0건이 원본 전체의 부재를 증명하지는 않는다.', '', '검사는 참조·해시·시간범위·검토 연결만 확인한다. 원본 정확성/모든 누락/회사 승인/R4 이관/새 화면 성공/일반 검색 성능을 판정하지 않는다.']
(OUT/'02_조회안내.md').write_text('\n'.join(qdoc)+'\n',encoding='utf-8')
print(json.dumps({'output':str(OUT),'units':len(units),'uses':len(uses),'events':len(events),'event_links':len(el),'reviews':len(reviews),'knowledge_links':len(kl),'commands':[{'file':x['result_file'],'exit':x['exit_code']} for x in commands]},ensure_ascii=False,indent=2))
