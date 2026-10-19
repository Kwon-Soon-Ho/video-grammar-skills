from pathlib import Path
import json,hashlib,subprocess,sys
O=Path(__file__).resolve().parent
W=next(p for p in O.parents if (p/'AGENTS.md').exists())
S=W/'knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer'
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,d): (O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(name,t): (O/name).write_text(t.strip()+'\n',encoding='utf-8')
R={'schema_version':'video-knowledge-links-0.1','record_id':'RC-STATIC-134-172-KNOWLEDGE','version':'local-v1-draft13','source':{'sha256':'be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa','duration_seconds':434.4,'metadata_authority':'provided only; MP4 not available'},'company_approved':False,'canonical_registered':False}
for k in ['source_records','evidence','claims','units','facets','knowledge_links','uses','composition_links','events','event_links','reviews','unknowns']:R[k]=[]
for n,f in enumerate(sorted((O/'prior').glob('*.md'))):R['source_records'].append({'id':'SRC'+str(n),'path':'prior/'+f.name,'sha256':sha(f),'role':'provided prior analysis, unchanged' if f.name!='input.md' else 'provided source metadata'})
src={r['path'].split('/')[-1]:r['id'] for r in R['source_records']}
def ev(i,path,t,kind,**kw):R['evidence'].append({'id':i,'path':path,'sha256':sha(O/path),'time':{'start':t,'end':t},'kind':kind,**kw})
ev('E1','evidence/134.png',134,'provided_full_frame',dimensions=[7680,2160]);ev('E2','evidence/172.png',172,'provided_full_frame',dimensions=[7680,2160])
for a in json.loads((O/'roi-manifest.json').read_text(encoding='utf-8')):
    ev(a['id'],'evidence/'+Path(a['path']).name,134 if a['id'].startswith('e1') else 172,'crop',parent_id='E1' if a['id'].startswith('e1') else 'E2',box_ltrb_exclusive=a['box_ltrb_exclusive'],transform=a['operation'])
def claim(i,t,e,b='observed',s=None):R['claims'].append({'id':i,'text':t,'basis_kind':b,'evidence_ids':e,'source_record_ids':[src[x] for x in (s or ['02_전체상세.md','01_부품과조합.md'])],'observation_origin':'이번 PNG/ROI 자기 재대조; 기존 기록의 상세는 별도 원문 보존' if b=='observed' else '이번 분석자의 계산/해석'})
claim('C1','E1 두 역할판 사이 위 파랑 프로젝트 요청은 오른쪽, 아래 녹색 전문인력 지원은 왼쪽을 가리킨다. 왼쪽 가족사 사업, 오른쪽 기술개발센터 전문인력 참여. 움직임 방향은 관측하지 않았다.',['E1','e1_arrows','e1_roles'])
claim('C2','E1 좌상 장 표식, 우상 제목/설명, 좌우 흰 유광 둥근 정보판과 중앙 관계 여백. 좌판 2열×4행 회사 로고; 우판 헤더 아래 BIM 설계·BIM 지원과 세로 구분선 2개, 하부 모니터 업무 묶음.',['E1','e1_roles','e1_logos'])
claim('C3','E1 업무 이미지 묶음은 큰 중앙 모니터와 좌우 모니터 총3대, 선반, 책2묶음, 양끝 화분2개. 왼쪽 평면도, 중앙 건물 와이어프레임, 오른쪽 세계지도와 건축 이미지2개. 선반/받침/그림자로 패널 하부 전경을 만든다.',['E1','e1_work'])
claim('C4','E2 설명은 기술개발센터가 실제 투입한 인력과 비용을 기준으로 / 23.7억 원을 가치창출성과로 산정했습니다. 큰 금색 입체 23.7억원과 뒤 옅은 큰 윤곽·잎 가지를 확인. 산정 타당성·카운트업은 확인하지 않았다.',['E2','e2_value','e2_number'])
claim('C5','E2 오른쪽 TDC/기술개발센터 표기의 흰색·짙은 녹색 유리 다층 건물과 원형 기단. 따뜻한 창빛·작은 내부 실루엣·조경·출입부가 보인다. 실제 사옥/실제 내부 인물인지 미확정.',['E2','e2_building'])
claim('C6','E2 별도 명찰4개: 건물 위 BIM 지원, 왼쪽 BIM 설계, 오른쪽 디자인 지원, 앞/아래 해외사업 지원. 흰 유광 둥근판+갈색 글씨; 건물/기단 둘레에 배치·일부 겹침.',['E2','e2_building'])
claim('C7','E1 로고 행우선: 한맥기술,saman(주)삼안,(주)장헌 JANGHEON,(주)장헌산업,(주)피티씨,HALLA 한라산업개발,BR(주)바른컨설턴트,山河종합기술(주). E2 좌→우는 같은 핵심 도상/이름8개이고 HALLA/피티씨 순서가 바뀐다. 가로형2×4에서 세로형 원근 가로열로 달라지며 동일 타일 자산/실제 이동 여부는 미확정.',['E1','E2','e1_logos','e2_logos'])
claim('C8','두 화면은 크림 배경, 흰 유광 면과 짙은 글자, 금갈색 장표식, 반사·곡선·빛의 깊이 표현을 공유. E1은 청/녹으로 주체를 구분하고 E2는 금색 성과값·받침과 녹색 건물 면으로 전경을 만든다. 공식 CI색·AE 재질값은 미확정.',['E1','E2'])
claim('C9','E1 두 역할판의 분할은 공통 기준 비교보다 요청/지원 연결을 나타내며 E2 명찰은 실제 건물 부위 설명보다 기관 서비스 범주의 주변 주석으로 해석한다. 화면 배치와 실제 공간/업무 구역은 같다고 볼 근거가 없다.',['E1','E2','e1_arrows','e2_building'],'inferred')
claim('C10','입력 치수7680×2160 및 실제 PNG 치수에서 7680/2160=32/9 화면비. 두 표본 시각 차172-134=38초는 표본 간격이며 연속 관측시간이나 읽기시간이 아니다.',['E1','E2'],'calculated',['input.md'])
claim('C11','E1 장표식2/TDC와 문구는 E2에서 같은 외형 가족으로 재출현. E1 헤더는 청색 건물 도상/가족사 사업과 녹색 사람3명/전문인력 참여의 도상+굵은 역할명+구분선+회색 설명 구성이다.',['E1','E2','e1_roles'])
claim('C12','E1 책 등 일부 작은 영문은 기존 전체 상세의 필수 의미를 바꾸지 않는 하위 표현이다. 이번 원본크기 ROI에서 BIM/ENGINEERING/GLOBAL PROJECTS, DESIGN SOLUTIONS가 보인다. 책2묶음은 유지하고 작은 책 장수·모든 도면 글자는 정밀 계수/전사하지 않았다.',['e1_work'])
def unit(i,k,t,summary,status='observed_static',v='v1'):
    R['units'].append({'id':i,'kind':k,'title':t,'observation_status':status,'definition_version':v,'summary':summary,'status':'local candidate; not canonical','definition_reference':'prior/01_부품과조합.md' if i.startswith('RC-COMP') or i.startswith('RC-LAYOUT') else 'prior/00_사례요약.md'})
unit('RC-CASE-001','case','134초 요청·지원 사례','가족사 사업과 기술개발센터 전문인력의 양방향 관계. 전체 사례 상세는 prior/02_전체상세.md RC-CASE-001을 보존.','observed_static','provided-r2 + knowledge-local-v1')
unit('RC-CASE-002','case','172초 가치창출성과 사례','23.7억원 성과값·8회사열·센터 건물 및 주변4명찰. 산정 데이터는 미확보.','observed_static','provided-r2 + knowledge-local-v1')
defs=[
('RC-LAYOUT-001@v1','layout','역할판 구성·요청/지원 연결','두 역할판 좌우+중앙 반대 방향 라벨 화살표. 상부 표식/제목, 좌 회사격자·우 업무 묶음. 단일 관측 후보.'),
('RC-LAYOUT-002@v1','layout','성과값·회사열·건물 무대','왼쪽 큰 금색 성과값, 중앙 원근 회사열, 오른쪽 건물/기단+지원 명찰. 투명판/곡선받침/빛으로 공간 조합.'),
('RC-COMP-001@v1','component','장 표식','금갈색 육각 배지2/TDC+오른쪽 짧은 장문구. 두 시각에서 외형 반복; 지속 과정/동일 픽셀 미검증.'),
('RC-COMP-002@v1','component','회사 로고 타일','흰 유광 둥근판+고유색 로고/회사명. E1 가로형2×4와 E2 세로형 원근8가로열을 같은 외형 가족 후보로 연결. 컨테이너는 가변; 동일 자산 미확정.'),
('RC-COMP-003@v1','component','역할 헤더','광택 원형 도상+굵은 역할명+가는 밑선+작은 회색 설명. E1 좌청색 건물/우녹색 사람3명은 같은 구성 가족의 다른 의미 도상.'),
('RC-COMP-004@v1','component','방향 라벨 화살표','곡선 몸체+큰 화살촉+흰 알약 라벨+광택 테두리. 요청 우향/지원 좌향 두 공간 사용처. 이동·드로온 미관측.'),
('RC-COMP-005@v1','component','지원 명찰','흰 유광 둥근판+갈색 서비스명. E2 건물 위/좌/우/앞의4개 별도 부품. E1 원형 BIM 도상과 동일 부품으로 합치지 않는다.'),
('RC-COMP-006@v1','component','성과 수치 조형','큰 금색 입체23.7억원+뒤 옅은 큰 윤곽+양옆 잎가지+받침/반사. 하위 윤곽/잎에 번호 추가 없음. 카운트업 미관측.'),
('RC-COMP-007@v1','component','업무 이미지 묶음','모니터3대와 선반/책2묶음/화분2개. 중앙 큰 와이어프레임 화면, 좌 평면도, 우 지도·건축 사진. 독립 교체/검색 후보; 소품은 하위 구성.'),
('RC-COMP-008@v1','component','기관 건물/기단 묶음','TDC/기술개발센터 건물+원형 기단. 흰 외벽/짙은 녹색 유리/창빛/실루엣/조경/출입부는 하위. 명찰005는 별도 부품.')]
for row in defs:unit(*row)
for i,k,t in [('Q-FLOW-001','flow','134→172 전개 조사'),('Q-MOTION-001','detail','화살표 동작 조사'),('Q-MOTION-002','detail','회사 타일 재배치 조사'),('Q-MOTION-003','detail','수치·빛·창 내부 동작 조사')]:unit(i,k,t,'기존 조사 번호 보존. 관측된 모션 정의가 아닌 조사 대상; 인접/연속 표본 미확보.','unobserved','provided investigation-v1')
def facet(u,d,n,t,c,b='observed'):
    R['facets'].append({'id':'F'+str(len(R['facets'])+1),'unit_id':u,'domain':d,'name':n,'description':t,'basis_kind':b,'claim_ids':c})
for u,c in [('RC-CASE-001',['C1','C2','C3']),('RC-LAYOUT-001@v1',['C1','C2'])]:
    facet(u,'information','정보 관계','좌 가족사 사업→우 전문인력에 요청, 우→좌 인력 지원. 공통 지표 비교가 아닌 역할 연결.',['C1','C9'],'inferred')
    facet(u,'screen','영역·격자','두 흰 역할판과 중앙 여백. 좌판 로고2열×4행은 부분 격자이며 전체 정보유형과 다르다. 우판 헤더→BIM항목→업무 묶음.',['C2'])
    facet(u,'visual','디자인 언어','크림/흰 유광 바탕·곡선 빛·약한 반사. 청/녹 원형 헤더와 모서리/화살표가 주체별 묶음. 굵은 역할명→회색 설명의 타입 위계.',['C2','C8','C11'])
    facet(u,'motion','시간 범위','134초 한 점의 가시 상태. 화살촉의 좌우 방향만 보이며 등장·순서·정착·퇴장·시간적 정지는 미관측.',['C1'])
for u in ['RC-CASE-002','RC-LAYOUT-002@v1']:
    facet(u,'information','정보 관계','설명은 실제 투입한 인력·비용 기준23.7억원 산정. 회사열·센터·서비스 범주의 관련 배치이며 회사별 배분액/산술식은 없다.',['C4','C9'],'inferred')
    facet(u,'screen','영역·격자','왼쪽 수치-중앙 회사열-오른쪽 건물의 가로3구역. 회사열은 원근 가로배열. 명찰4개가 건물 둘레에 배치. 실제시설 좌표표가 아니다.',['C4','C5','C6','C7'])
    facet(u,'visual','디자인 언어','크림/금색 실내 무대·기둥·벽·부드러운 바닥반사. 금색 입체성과값과 투명판/금색곡선받침, 녹색유리건물/흰단상이 전경. 명찰은 흰 바탕과 갈색 글씨.',['C4','C5','C6','C8'])
    facet(u,'motion','시간 범위','172초 한 점. 뒤 숫자윤곽·평행광선·창 실루엣의 존재와 움직임은 별도. 카운트업/이징/카메라/창내부 변화 미관측.',['C4','C5'])
facet('RC-COMP-007@v1','screen','묶음/하위/배치','RC-LAYOUT-001@v1 오른쪽 정보판 하부 전경. 모니터/선반/책/화분은 하위 구성; 역할 헤더003과 동반하되 하나로 병합하지 않음.',['C2','C3'])
facet('RC-COMP-007@v1','visual','업무 표상','중앙 화면 크기/정면성·양옆화면 기울기·검은 프레임, 흰 선반과 화분/책이 광택 역할판 앞에서 업무 이미지를 이룬다. 특정 프로그램 실UI 시연으로 확정하지 않는다.',['C3','C12'])
facet('RC-COMP-008@v1','screen','묶음/하위/배치','RC-LAYOUT-002@v1 오른쪽 중심의 건물+기단. 지원명찰005는 별도이며 건물 주변 배치의 기준 대상.',['C5','C6'])
facet('RC-COMP-008@v1','visual','기관 표상','녹색유리 정면의 흰 TDC/기술개발센터 표기, 따뜻한 창빛과 흰 원형단상/금속 측면, 조경을 함께 보존. 투영/제작도구/실사옥 미확정.',['C5'])
facet('RC-COMP-005@v1','information','지원 범주','BIM지원/설계/디자인지원/해외사업지원. 기관 업무범주의 명찰로 해석하며 각 부위별 실제 업무나 순위는 미확인.',['C6','C9'],'inferred')
facet('RC-COMP-002@v1','screen','반복/차이','E1 2×4격자 행우선과 E2 8가로열에서 HALLA/피티씨 순서교환. 영문 부속문구의 크기/줄바꿈 차이는 보존.',['C7'])
def use(i,u,case,t,e,c,diff,unv,condition):R['uses'].append({'id':i,'definition_id':u,'case_unit_id':case,'time':{'start':t,'end':t},'evidence_ids':e,'claim_ids':c,'differences':[diff],'unverified':[unv],'conditions':[{'text':condition,'validation':'observed_case_only'}],'definition_version':next(r['definition_version'] for r in R['units'] if r['id']==u)})
use('U-L1','RC-LAYOUT-001@v1','RC-CASE-001',134,['E1'],['C1','C2'],'첫 정의의 두 역할판 전체','다른 화면비/항목수/긴 라벨 가독성','두 주체와 반대방향 관계/문구를 함께 보존. 단방향 절차/우열비교에 그대로 쓰면 의미가 달라짐.')
use('U-L2','RC-LAYOUT-002@v1','RC-CASE-002',172,['E2'],['C4','C5','C6','C7'],'첫 정의의 가로무대 전체','다른 출력환경/회사수·실제 산정식','수치단위·설명을 함께 보존. 회사별 배분차트로 전용할 근거 없음.')
cfg=[('001',1,['E1'],['C11'],'좌상2/TDC와 장문구','다른 장/동일픽셀·지속과정','장 번호/문구의 맥락 역할 보존'),('001',2,['E2'],['C11'],'E1과 같은 위치계열 외형반복','동일 자산/지속표시','장표식을 원본 표본과 연결'),('002',1,['e1_logos'],['C7'],'가로형2×4;5피티씨6HALLA','법인정식명/공식 자산/모션','로고식별성·명칭과 컨테이너를 구별'),('002',2,['e2_logos'],['C7'],'세로형원근8가로열;5HALLA6피티씨','일부 영문부속글자·같은타일자산·이동','E1전사를 E2독립판독으로 쓰지 않기'),('003',1,['E1','e1_roles'],['C11'],'좌청색건물/우녹색사람3명의 두 헤더','정확폰트·도상자산·모핑','역할명 주정보/설명 보조정보를 유지'),('004',1,['e1_arrows'],['C1'],'위파랑우향요청/아래녹색좌향지원 두 배치','이동·드로온/라벨시차','방향과 요청/지원주체를 함께 대조'),('005',2,['e2_building'],['C6'],'건물주변위/좌/우/앞4개;E1BIM원형과 외형차','완전한업무목록/동일부품/실제업무부위','명찰은008내부로흡수하지않고 독립연결'),('006',2,['e2_number','e2_value'],['C4'],'23.7억원 단일 사용처와 뒤윤곽/잎','숫자변화/효과원값·값치환시험','금액단위/산정설명을 같이보존'),('007',1,['e1_work','E1'],['C3','C12'],'오른쪽판하부전경;3모니터/책2묶음/화분2개','특정프로그램·독립자산·교체시험','업무묶음의 중앙강조/하위소품/헤더와관계 보존'),('008',2,['e2_building','E2'],['C5','C6'],'오른쪽중심대상;지원명찰별도;E1업무묶음과다른단위','실제사옥·창내부동작·동일자산/기관교체','기관표기와기단/조경관계 보존;명찰변수는별도')]
for n,(num,cas,evs,cs,dif,unv,co) in enumerate(cfg,1):use('U-C'+str(n),f'RC-COMP-{num}@v1',f'RC-CASE-00{cas}',134 if cas==1 else 172,evs,cs,dif,unv,co)
def link(u,c,rel,claims,reason):R['knowledge_links'].append({'id':'K'+str(len(R['knowledge_links'])+1),'unit_id':u,'concept_id':c,'relation':rel,'basis_kind':'inferred','claim_ids':claims,'rationale':reason})
for c,why in [('LAYOUT-SPLIT','좌우 영역이 요청/지원 주체의 서로 다른 역할을 담당한다. 판 두 개만으로 비교를 뜻하지 않는다.'),('LAYOUT-NETWORK','방향 화살표와 요청/지원 문구가 대응한다. 관계 연결을 수집하며 인과는 추정하지 않는다.')]:link('RC-LAYOUT-001@v1',c,'classified_as',['C1','C2','C9'],why)
link('RC-LAYOUT-001@v1','KNOW-LAYOUT-NETWORK','review_relevant',['C1'],'관련·방향 라벨과 연결 종류를 확인하는 질문. 관계선이 실제 인과를 입증하지 않는 반례를 적용.')
link('RC-LAYOUT-001@v1','KNOW-LAYOUT-SPLIT','review_relevant',['C2'],'역할 다른 두 영역에 적합; 공통 지표가 없어 분할비교는 제외.')
for u in ['RC-COMP-002@v1','RC-COMP-005@v1']:link(u,'REL-PARALLEL','classified_as',['C7'] if '002' in u else ['C6'],'한 화면의 회사/서비스 항목을 동등 범주로 읽는 조건부 해석. 동시 등장·순위의 증거 아님.')
link('RC-COMP-002@v1','LAYOUT-CARD-GROUP','classified_as',['C7'],'회사타일 구역의 카드형 집합만 분류; 전체화면이나 모션 범주가 아님.')
for u in ['RC-LAYOUT-002@v1','RC-COMP-008@v1','RC-COMP-005@v1']:link(u,'LAYOUT-SPACE-CALLOUT','classified_as',['C5','C6','C9'],'E2 건물 주변의 명칭/주석 부분에만 제한. 실제건물 부위 업무좌표로 확정하지 않는 개념주석 변형.')
for u in ['RC-LAYOUT-001@v1','RC-LAYOUT-002@v1','RC-COMP-007@v1','RC-COMP-008@v1']:link(u,'STYLE-3D','classified_as',['C8'],'유광/반사·겹침·원근/입체 외관의 표현 속성. 실제3D프로그램/AE레이어 구조는 미확인.')
for u in ['RC-COMP-005@v1','RC-COMP-008@v1']:link(u,'IP-04','review_relevant',['C5','C6'],'명찰 대응과 가림 검토에 참고. 근접배치 관측이 전달효과 입증은 아님.')
for u in ['RC-LAYOUT-001@v1','RC-LAYOUT-002@v1','RC-COMP-007@v1','RC-COMP-008@v1']:link(u,'SCREEN-GROUP','review_relevant',['C2'] if '001' in u or '007' in u else ['C5','C6'],'전체/부분의 묶음 경계와 하위구성/대상 대응의 근접·정렬 질문.')
link('RC-COMP-002@v1','MR-03','review_relevant',['C7'],'두 표본의 핵심로고 반복을 전환 연속성/동일자산으로 확대하지 않도록 확인.')
link('RC-COMP-006@v1','SCREEN-DATA','review_relevant',['C4'],'수치단위/설명은 보존하지만 실제산정데이터·회사별비례관계는 미확보.')
def comp(a,b,r,c):R['composition_links'].append({'from':a,'to':b,'relation':r,'basis_kind':'observed','claim_ids':c})
for a,ls,cs in [('RC-CASE-001','RC-LAYOUT-001@v1',['C1','C2']),('RC-CASE-002','RC-LAYOUT-002@v1',['C4','C5','C6'])]:comp(a,ls,'contains',cs)
for u in ['002','003','004','007']:comp('RC-LAYOUT-001@v1','RC-COMP-'+u+'@v1','contains',['C2','C3'])
for u in ['002','005','006','008']:comp('RC-LAYOUT-002@v1','RC-COMP-'+u+'@v1','contains',['C4','C5','C6','C7'])
comp('RC-COMP-005@v1','RC-COMP-008@v1','anchors_to',['C5','C6']);comp('RC-COMP-005@v1','RC-COMP-008@v1','overlaps',['C6'])
comp('RC-COMP-007@v1','RC-COMP-003@v1','accompanies',['C2','C3']);comp('RC-COMP-007@v1','RC-LAYOUT-001@v1','anchors_to',['C2','C3'])
for lay in ['001','002']:comp('RC-COMP-001@v1','RC-LAYOUT-'+lay+'@v1','accompanies',['C11'])
for i,cas,cs in [('Q-FLOW-001',1,['C1','C4']),('Q-MOTION-001',1,['C1']),('Q-MOTION-002',1,['C7']),('Q-MOTION-003',2,['C4','C5'])]:
    evs=['E1','E2'] if i in ['Q-FLOW-001','Q-MOTION-002'] else ['E1' if cas==1 else 'E2']
    use('U-'+i,i,'RC-CASE-00'+str(cas),134 if cas==1 else 172,evs,cs,'기존 조사 항목; 관측 모션 없음','진입/내부/주변/중간/동반/퇴장 및 경계 미검수','연속원본/인접표본을 확보한 다음 관찰; 현재조건은 미래시험을 검증하지 않음')
    R['events'].append({'id':'EV-'+i,'unit_id':i,'title':next(x['title'] for x in R['units'] if x['id']==i),'status':'unobserved','time':{'start':134 if cas==1 else 172,'end':172},'claim_ids':[],'time_meaning':'조사할 표본/경계 범위; 사건 발생·지속시간 아님'})
def review(u,c,st,reason,evs,cls,scope,nextp):
    r={'id':'RV'+str(len(R['reviews'])+1),'unit_id':u,'criterion_id':c,'status':st,'reason':reason,'evidence_ids':evs,'claim_ids':cls,'reviewer':'이번 실행 분석 에이전트(자기 재대조)','scope':scope,'next_probe':nextp}
    R['reviews'].append(r);link(u,c,'review_relevant',cls,'수집 기록의 해당 범위에 실제 확인 질문을 선정. 회사 의무기준이나 원칙 적용효과가 아님.');link(u,c,'evaluated_against',cls,'실제 검토행 '+r['id']+' 참조; status와 scope를 함께 읽는다.')
review('RC-LAYOUT-001@v1','Q-INFO-02','pass','화살촉 두 방향과 요청/지원 문구·역할 주체가 기존 상세에 일치.',['E1','e1_arrows','e1_roles'],['C1'],'PNG+원본크기ROI와 기록의 방향/문구 대응만. 음성/업무사실 검증 제외.','음성/시나리오가 제공되면 별도 내용 대응')
review('RC-COMP-007@v1','Q-SCREEN-01','pass','오른쪽 정보판 하부전경의 중앙큰모니터·양옆모니터/선반/책/화분, 역할헤더와의 관계를 원문/PNG에서 대조.',['E1','e1_work'],['C2','C3','C12'],'정적 수집 기록의 위계/묶음 대응만. 실제시청효과·다른표시환경 가독성 제외.','새환경 활용시 실제내용/해상도로 가독성 재검토')
review('RC-COMP-008@v1','Q-SCREEN-01','pass','건물/기단 묶음과 별도005명찰 4위치가 기록에 각각 보존되고 관계가 왕복됨.',['E2','e2_building'],['C5','C6'],'정적 원본-기록 조합/라벨 위치 대응만. 실공간 위치 정확성 제외.','기관교체 시 명찰/기관의 실제관계 확인')
review('RC-COMP-005@v1','IP-04','pass','이 표본에서 명찰은 건물을 둘러싸고 명칭을 읽을 수 있으며 별도 부품으로 보존. 주변광선/조경·기단과 일부겹침 기록.',['E2','e2_building'],['C6'],'수집 기록의 공간대응/가림 기술 대조. 이해도/최적거리/실부위업무 대응 효과 검증 아님.','시청환경/실제서비스 내용이 바뀌면 효과/가림을 별도 검수')
review('RC-COMP-006@v1','Q-INFO-02','pass','23.7억원 큰 수치와 설명의23.7억 원, 실제투입인력/비용 기준이라는 귀속을 재대조.',['e2_value','e2_number'],['C4'],'PNG 수치·단위 전사 대조만. 실제 산정 사실/음성 일치 검증 제외.','데이터와 음성이 있으면 별도 검증')
review('RC-LAYOUT-002@v1','SCREEN-DATA','hold','실제산정 상세·회사별 배분/비례·집계 데이터가 없어 데이터 사실성/산식은 확인 못함.',['E2','e2_value'],['C4','C7'],'화면전사는 확인했으나 실제 데이터타당성 판정 보류.','기술/데이터담당자의 산정표·집계기준·해당판본 확보')
review('RC-COMP-002@v1','MR-03','hold','같은8개 핵심로고와순서변화는 확인; 실제전환 구간이 없어 타일동일자산/연속이동은 보류.',['e1_logos','e2_logos'],['C7'],'정지표본2장 대조만. 전환/이동 미검수.','원본 전환창에서 타일/가림/로고를 추적')
review('RC-COMP-002@v1','Q-BRAND-01','not_reviewed','회사자료목록은 문맥만조회. 공식 원형/사용형·화면이미지와 자산의 픽셀/권한 대조는 수행하지 않음.',['e1_logos','e2_logos'],['C7'],'CI/공식자산 대조 미검수; 핵심명칭 관측은 유지.','R1/R5의 실제 자산버전·사용규칙과 화면로고 별도 대조')
for u,evs,cls in [('RC-CASE-001',['E1'],['C1','C2']),('RC-CASE-002',['E2'],['C4','C5','C6'])]:
    review(u,'Q-MOTION-01','hold','한시점 PNG는 완성시점/유지시간을 보여주지 않아 읽기 충분성을 판정할 수 없음.',evs,cls,'시간가독성 보류. 정적내용 누락 대조와 별도.','원본 연속구간·발화·표시환경 확보 후 등장/완성/가림/유지/퇴장 대조')
    review(u,'Q-TRUST-01','pass','현재PNG 파일해시/크롭원좌표/문서판본을 pin하고 주요주장을 해당PNG/ROI로 재대조.',evs,cls,'제공PNG-기록 대응과 이번크롭 변환/해시만. MP4진위/PTS추출로그는 미확인.','원본확보시 제공시각/메타데이터를 추출로그와 확인')
    review(u,'Q-TRUST-02','pass','관측/기능해석/미관측을 구분하고 정지2장을 모션/회사규칙/의도/동일자산으로 확대하지 않음.',evs,cls,'이번 기록의 주장범위 자기 점검; 회사승인·독립검수 아님.','새 근거가오면 영향받는 주장범위만 별도이력으로 보강')
for i,u,q,impact,nextp in [
('UN1','RC-CASE-001','실제 등장/전환/내부·주변 동작·퇴장 미관측','모션재사용/전편완료 판정불가','134초앞뒤 및172초사이 연속원본/경계표본'),
('UN2','RC-CASE-002','금액윤곽·빛·창내부 시간변화 미관측','카운트업/잔상/스케일/카메라/속도확정불가','수치/창/외곽/주변을 따로 전후비교'),
('UN3','RC-COMP-002@v1','같은 타일자산·편집프로젝트·로고정식사용형 미확인','반복외형을 동일자산/공식형으로 승격못함','편집자산과CI원본대조'),
('UN4','RC-COMP-008@v1','실제사옥인지·업무명찰과건물부위의대응 미확인','실제기관도면/공간정보로 활용불가','제작자/기관담당의출처확인'),
('UN5','RC-COMP-007@v1','특정소프트웨어·프로젝트정체·분리자산유무 미확인','실UI 튜토리얼/원자산재활용으로단정불가','원본화면자산/제작파일확보'),
('UN6','RC-LAYOUT-002@v1','산정표·회사별배분관계 미확인','데이터사실성/회사별기여차트로확정불가','산정원자료/내용담당확인'),
('UN7','RC-CASE-001','정확폰트·색상·재질/AE효과원값 미상','정확재현값제공 제한;외형/위계수집은 가능','원본프로젝트 또는 필요목적의실측'),
('UN8','RC-CASE-002','음성·시나리오·PTS추출로그 미제공','음성싱크/타임코드진위와산정사실은미검수','실제음성/원문/로그확보'),
('UN9','RC-COMP-002@v1','E2 작은부속영문 일부 흐림','법인풀네임 정밀전사제한;핵심8개대응은유지','더선명한해당프레임/자산원본'),
('UN10','RC-LAYOUT-001@v1','다른화면비·많은항목·긴문구의활용시험 없음','현재사례밖 적합성미검증','별도제작/응용요청시 실내용으로시험')]:R['unknowns'].append({'id':i,'unit_id':u,'question':q,'impact':impact,'next_probe':nextp})
R['limitations']=['실제관측: 제공7680×2160 PNG2장(전체보기2048×576)과 원본픽셀크롭8개를 original detail로 열람. OCR·원본MP4재생·재추출·음성청취 안함.','134/172초는 제공 메타데이터에 따른 시각. 자체PTS검증 아님. 38초를 연속관측시간으로 계산하지 않는다.','prior는 기존분석r2이며 이번실행의독립원본이아님. 기존상세/번호/근거원문은 바이트보존; 이번내용확인은 PNG/ROI 범위.','단일묶음후보/정지외형반복/동일원자산확인/정본등록/회사승인은 서로다름. 두레이아웃을 같은패턴으로 합치지않음.','모든모션조사는unobserved. 시간정지·이징·동시발생·퇴장·원제작의도/효과/회사규칙을 만들지않음.','Phase00지식은 분류/검토질문의 참고. 모든65원칙일괄적용안함. 스킬/정본/R4변경·등록/새화면/영상/PDF/외부스킬실행 없음.','일반화/다른원본/새스타일활용시험 아님. SHA/연결검사통과는 내용정확성·회사승인을대신하지않음.']
save('knowledge-links.json',R)
md('00_사례요약.md','''# 134·172초 — 지식과 사용처 수집

지정 스킬 draft.13으로 제공 PNG 두 장과 기존 수집 r2를 재대조한 로컬 초안이다. 읽는 순서: **이 요약 → [전체 상세](02_전체상세.md)·[정의/사용처](01_정의와사용처.md) → [근거/검토](03_근거와검토.md)**. [실제 조회 결과](05_조회안내.md)는 같은 구조의 JSON 색인으로 돌아간다. 기존 RC 번호/정의 v1을 유지했다.

## RC-CASE-001 · 134초

![E1](evidence/134.png)

좌 가족사 사업과 우 기술개발센터 전문인력 참여는 파랑 ‘프로젝트 요청’ 우향 / 녹색 ‘전문인력 지원’ 좌향으로 연결된다. 크림 공간의 두 흰 유광 역할판, 중앙의 넓은 여백, 청/녹 원형 헤더와 굵은 역할명·회색 설명, 좌 로고2×4와 우 BIM항목·업무 이미지의 층이 전체 구도를 만든다. 두 역할의 연결이라는 기능 해석이며 우열 비교/업무순서/실제 움직임을 뜻하지 않는다.

찾을 단위는 **RC-LAYOUT-001@v1 역할판 구성**, RC-COMP-003@v1 역할헤더, RC-COMP-004@v1 방향라벨, **RC-COMP-007@v1 업무 이미지 묶음**이다. 모니터3대·책2묶음·화분2개·선반은007의 하위다. 분할+연결 구성은 조건부 분류이고 2×4는 왼쪽 부분의 기하격자다. 등장/정착/퇴장과 실제 소프트웨어정체는 미관측/미확인이다.

## RC-CASE-002 · 172초

![E2](evidence/172.png)

실제 투입한 인력·비용 기준 **23.7억원을 가치창출성과로 산정했다**는 문구, 왼쪽 큰 금색입체값·중앙8회사 원근가로열·오른쪽 TDC 건물/기단의 가로무대다. 크림/금색 공간의 투명판·곡선받침·바닥반사·녹색유리·따뜻한 창빛이 깊이를 만든다. 기관 주변4명찰은 업무범주 주석이라는 해석이다. 실제부위별 업무/산정타당성/회사별기여비율은 확인하지 않았다.

**RC-LAYOUT-002@v1**, **RC-COMP-008@v1 건물/기단**, 별도 **RC-COMP-005@v1 지원명찰**, RC-COMP-006@v1 성과조형을 연결한다. 회사타일002는 E1과 핵심8로고가 반복되지만 2×4→원근가로열, HALLA/피티씨 순서가 다르다. 동일자산/이동/카운트업/빛·창내부변화는 미확인이다.

범위: 정지표본2장·ROI8개 및 번호/사용처/개념/검토의 왕복. 전편434.4초·134~172초연속검수·독립검수·회사승인·새자료 일반화시험은 아니다. 원본언어 유지/다른스타일 활용은 열어두되 현재 조건부후보의 의미·주체·단위를 보존한다.
''')
lines=['# 정의 → 현재 사용처 → 근거/차이','', '기존 정의·번호·조건의 보존 원문: [부품과조합](prior/01_부품과조합.md). 아래는 새 색인과 왕복하는 지역 사용처표이며 정본 등록이 아니다. 모니터·책·창·조경에 새 패턴번호를 발급하지 않았다.','', '| 정의/판본 | 구성·독립범위 | 현재 사용처·근거 | 현재 차이·미검증/조건 |','|---|---|---|---|']
for i,k,title,summary in defs:
    us=[u for u in R['uses'] if u['definition_id']==i]
    use_text='<br>'.join(f"{u['id']} · {u['case_unit_id']} {u['time']['start']}초 · "+', '.join(f"[{e}]({next(v['path'] for v in R['evidence'] if v['id']==e)})" for e in u['evidence_ids']) for u in us)
    diff='<br>'.join('차이: '+ '; '.join(u['differences'])+' / 미검증: '+'; '.join(u['unverified'])+' / 조건: '+u['conditions'][0]['text'] for u in us)
    lines.append(f'| {i} {title} | {summary} | {use_text} | {diff} |')
lines+=['','## 조합의 의미','', '역할판001 contains 회사타일002·헤더003·방향라벨004·업무묶음007. 업무묶음은 오른쪽판하부를 기준으로 배치되고 헤더와 동반한다. 무대002 contains 성과조형006·회사타일002·건물/기단008·명찰005. 명찰005 anchors_to/일부overlaps 건물008이며 내부자산으로 흡수하지 않는다. 장표식001은 두 전체배치에 동반한다. 이 관계는 **보이는 공간조합**이고 시간선후/중첩/AE parent가 아니다.','', '[JSON 정의·조합·사용처](knowledge-links.json) / [질문과 실제판정](03_근거와검토.md) / [기존 모션조사](prior/04_모션조사.md).']
md('01_정의와사용처.md','\n'.join(lines))
md('02_전체상세.md','''# 전체 상세와 이번 대조

**[기존 전체 상세 보존 원문](prior/02_전체상세.md)**의 두 사례 구역표·모든 문구·로고순서·배경층·도상·모니터/소품·반사·기단·라벨을 삭제/요약대체하지 않았다. [기존 부품/조합](prior/01_부품과조합.md), [기존 근거/검수](prior/03_근거와검수.md), [기존 미관측모션조사](prior/04_모션조사.md)도 바이트 그대로 보존했다. 원문의 과거 절대경로·original/collection.md·scratch 링크는 역사적 기록이며 이번 입력은 원기록/기존크롭 전체를 포함하지 않는다. 이번 활성 근거는 [E1](evidence/134.png), [E2](evidence/172.png), [새크롭좌표표](roi-manifest.json)다.

| 관점 | RC-CASE-001 / 134초 | RC-CASE-002 / 172초 |
|---|---|---|
| 정보·설명 | 가족사 사업→센터 전문인력: 프로젝트요청; 역방향 전문인력지원. 화살촉+라벨+주체를 함께 기록 | 실제투입 인력·비용 기준23.7억원 가치창출성과. 회사별분배/비교척도 없음. 기관·회사·서비스의 관련배치라는 해석 |
| 화면·격자 | 상부맥락/우상제목, 좌우역할판+중앙연결여백. 좌2열×4행은 하위격자, 우헤더/BIM항목/업무묶음의 세로위계 | 왼성과조형/중앙원근회사열/오른건물 가로3구역. 투명판·곡선받침·건물주변명찰의 공간층 |
| 타입·색·재질·깊이 | 굵은 짙은 역할명, 작은 회색설명, 고유로고글꼴. 흰유광판·청/녹 도상/모서리/화살표가 주체를 묶음. 선반·그림자·반사가 업무이미지를 전경화 | 설명2줄과 큰금속성수치가 주정보. 갈색명찰·흰판/기단·녹색유리·금빛곡선과 창빛·반사. 장표식은 상위맥락이라는 기능해석 |
| 시간·모션 | 134초한점의가시상태. 청/녹 화살표는 동시 보이나 동시등장/정지확인 아님 | 172초한점의가시상태. 숫자뒤윤곽/평행광선/창실루엣은 존재만확인. 카운트업·빛이동·정착 미관측 |
| 재사용 | 001역할판/003헤더/004방향라벨/007업무묶음. 보호후보: 주체·방향·라벨귀속, 가변후보: 문구/업무이미지/소품이나 시험없음 | 002무대/006성과조형/008건물기단/005명찰. 기관/수치/회사수 변경은 미시험; 실제부위관계·산식으로 사용불가 |
| 근거·판정 | 원문보존+E1 전체/ROI4개. 분류는추론, 정적대응판정만수행 | 원문보존+E2 전체/ROI4개. 데이터타당성·회사공식자산·모션은보류/미검수 |

이번 보강: 업무묶음 원본픽셀 ROI에서 왼평면도, 중앙와이어프레임, 오른세계지도+건축이미지2개, 책의 BIM/ENGINEERING/GLOBAL PROJECTS·DESIGN SOLUTIONS 문구가 보인다. 이는 하위구성 보강이며 새패턴번호/특정소프트웨어 식별로 만들지 않았다. 작은책장수·도면의 모든 글자를 정밀전사하지 않은 것은 관측범위삭제와 다르다.

핵심 재대조: 요청우향/지원좌향, 사람3명헤더와 BIM두도상, 23.7억원/산정설명, 건물 TDC/기술개발센터, 명찰4종/4위치, 로고8개대응과 HALLA/피티씨 순서를 각각 해당ROI로 확인했다. E2 작은부속영문 일부는 흐려 E1의 풀네임전사를 E2독립판독으로 복사하지 않았다. 의미를바꾸는 기존기록 정정사항은 이번한정범위에서 발견하지 않았으며, 기존의미에 대한 회사승인을 뜻하지 않는다.

[정의와현재차이](01_정의와사용처.md) → [근거·실제검토](03_근거와검토.md). [구조화편집원본](knowledge-links.json)의 facets/claims가 이 상세를 연결하고 prior 전체상세는 대체하지 않는다.
''')
review_lines=['# 근거·관측·실제 검토','', '원본 MP4·오디오·시나리오·추출로그는 미제공이다. MP4 SHA/434.4초/30fps는 입력값이며 독립 검증하지 않았다. 두 PNG는7680×2160, 화면비32:9. 제공시각134/172초는 자체PTS재계산이 아니다. 전체보기는2048×576축소, 원본픽셀크롭8개는 original 상세로 열람했다. 크롭은색/배율/회전변경없음. 좌상원점x우/y하 px, right/bottom 제외. [실제ROI표](roi-manifest.json).','', '| 근거 | 실제파일 SHA256 |','|---|---|']
for e in R['evidence']:review_lines.append(f"| [{e['id']}]({e['path']}) · {e['time']['start']}초 | {e['sha256']} |")
review_lines+=['','## 검토 관련 지식과 실제 결과','', 'review_relevant는 선정한 검토질문이다. evaluated_against는 아래 실제행과 같은단위/기준을 연결한다. pass는 아래scope의 원본-기록대응만을 뜻하며 회사/시안/영상전반 승인이나 원칙효과 증명이 아니다.','', '| 실제행/대상 | 기준/상태 | 결과/범위 | 다음 확인 |','|---|---|---|---|']
for r in R['reviews']:review_lines.append(f"| {r['id']} · {r['unit_id']} | {r['criterion_id']} · {r['status']} | {r['reason']} {r['scope']} | {r['next_probe']} |")
review_lines+=['','## 미상과 남은 범위','', '| 대상 | 미상/영향 | 다음 확인 |','|---|---|---|']
for r in R['unknowns']:review_lines.append(f"| {r['unit_id']} | {r['question']} / {r['impact']} | {r['next_probe']} |")
review_lines+=['','검토주체: 이번실행 분석에이전트의 자기재대조. 전체표본의 요소/관계누락은두프레임과기존상세를 대조했고 정밀미상·미관측을 별도보존했다. 새화면/영상/PDF·정본변경·회사등록/승인 수행없음.']
md('03_근거와검토.md','\n'.join(review_lines))
md('04_Phase00_지식선정.md','''# Phase 00 지식 조회와 분류 이유

카탈로그 [knowledge-catalog.json](knowledge-catalog.json)은 현재루트의75용어+폐기1개,65기본지식,26품질질문 합167개와11문맥의경로/해시를 pin했다. 카탈로그생성은 모든내용의의미전수검토가 아니다. [선택한원문항목](queries/selected-concept-source.json)은 이번실제로 읽은 정의/조건/반례다. 공통사전0.1.1(항목별0.1.0/0.1.1), 기본지식0.1.1, 레이아웃심화0.1.2, 판정정본은 catalog의source_pins/항목원문을 따른다.

| 범위 | 채택/제외·적합성 판단 | 현재 증거/사용처 |
|---|---|---|
| 역할판전체 | LAYOUT-SPLIT + LAYOUT-NETWORK 조건부태그. KNOW-LAYOUT-SPLIT/NETWORK의 역할분할·방향라벨 조건을 참고 | 001역할판, E1두판/요청지원라벨. 비교동등조건이없어 LAYOUT-SPLIT-COMPARE 제외 |
| 좌회사격자/중앙회사열 | REL-PARALLEL, LAYOUT-CARD-GROUP은 타일구역만 분류.2×4/원근가로열은 기하배치서술 | 002타일 E1/E2와 순서변화. 같은로고반복이 시간동시발생/동일자산은 아님 |
| 건물/명찰구역 | LAYOUT-SPACE-CALLOUT은 기관주변서비스범주주석으로제한한 변형. IP-04는 가까운라벨의대응/가림검토질문 | 008건물/기단과 별도005명찰 E2. 실제시설부위좌표/각층업무라고 주장하지 않음 |
| 표현언어 | STYLE-3D는 입체/유광/원근/반사 외관태그. 재질·빛·타입·색의역할조합을 기록 | 007업무묶음/008건물·두레이아웃. 실제3D도구·AE효과·CI토큰 확정안함. STYLE-ISOMETRIC은 투영근거없어 제외 |
| 시간·연속성 | MR-03는 회사타일반복을 이동모션으로 확대하지않는 질문. Q-MOTION-01/SCREEN-TIME-READ는 근거부족을 드러낼 관련지식 | 134/172정지2점만이라 관측모션/시간정지분류없음. 모든Q-FLOW/Q-MOTION 조사ID보존 |
| 정보/판정 | SCREEN-DATA/Q-INFO-02/Q-SCREEN-01/Q-TRUST-01/02를 필요한 범위에 선정 | 전사/정적관계대응 pass와 실제산정타당성 hold, CI미검수를 분리 |

부족한 사전 대응도 남겼다. 요청·지원의 양방향 업무관계는 사전의 일반 ‘관련’만으로 뜻을 충분히 설명하지 못하므로 문구/방향/주체를 자유기술하고 새정본용어를 만들지 않았다. ‘REL-SPACE’는 실제시설위치가아니라화면공간이므로 자동부여하지 않았다. 큰숫자가있다는이유로 LAYOUT-DATA-CHART로 분류하지 않았다.

R1자산목록은스키마/존재문맥만확인했고 공식CI자산대조는미실시. R2사전은정확ID/분류이유, R3기본·선택심화/편집디자인은관계·격자·타입/재질·검토질문, R4는미이관경계, R5는관측색/공식CI/선택역할분리, R6은원문해시/회신범위, R7은범위별pass/hold/미검수, R8은기본판/후보/실행경계를참고했다. 현재R8의2026-10-15당시 ‘01-A미시작’은최신2026-10-19연결안내와구별하고 현재실행의전면차단으로읽지않았다.

읽은문맥: R8_현재사용안내,01_진행현황,00_분석단계_지식연결_추가안내,재감사00_읽는순서와_현재상태/05_R1-R8_연결과_수집계약,편집디자인추가검토,회사CI화면역할연결규칙,판정운영기준; 심화는NETWORK/SPLIT/SPACE-CALLOUT와IP-04/MR-03만선택해전문확인. 외부스킬을실행/설치하거나 조사예시를현재관측근거로쓰지않았다. 재감사의134/172기존답안·실제사용색인/조회결과는읽지않았다.

[분류/검토연결원본](knowledge-links.json) → [사용처](01_정의와사용처.md) → [이번근거/판정](03_근거와검토.md). 65개전체의적용의무나원칙효과·회사승인을만들지않는다.
''')
for u in R['uses']:
    u['content_context']='가족사 프로젝트 지원: 가족사 사업의 프로젝트 요청과 기술개발센터 전문인력 지원' if u['case_unit_id']=='RC-CASE-001' else '실제 투입한 인력·비용 기준 23.7억원 가치창출성과와 관련 회사/기관 지원범주'
    u['detail_path']='02_전체상세.md'
    u['definition_path']='01_정의와사용처.md'
    u['composition_context']=[r for r in R['composition_links'] if r['from']==u['definition_id'] or r['to']==u['definition_id']]
for name in ['00_사례요약.md','01_정의와사용처.md','02_전체상세.md','03_근거와검토.md','04_Phase00_지식선정.md']:
    R['source_records'].append({'id':'CURRENT-'+name.split('_')[0],'path':name,'sha256':sha(O/name),'role':'current collection record, pinned; prior detailed records remain unchanged'})
save('knowledge-links.json',R)
commands=[]
def run(args,out):
    cmd=[sys.executable,'-B','-X','utf8',str(S/'scripts/knowledge_links.py')]+args
    proc=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    (O/out).write_text(proc.stdout or proc.stderr,encoding='utf-8');commands.append({'argv':cmd,'exit_code':proc.returncode,'result':out})
    if proc.returncode:raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)
cat=str(O/'knowledge-catalog.json');rec=str(O/'knowledge-links.json');idx=str(O/'knowledge-use-index.json')
run(['check','--catalog',cat,'--record',rec],'check-result.json')
run(['index','--catalog',cat,'--records',rec,'--out',idx],'index-result.json')
queries=[('work',['--query','업무 이미지']),('building',['--query','건물/기단']),('roleplate',['--query','역할판']),('space',['--id','LAYOUT-SPACE-CALLOUT']),('network',['--id','LAYOUT-NETWORK']),('tiles',['--query','RC-COMP-002@v1']),('group',['--id','SCREEN-GROUP']),('question',['--id','Q-SCREEN-01']),('observed-motion',['--query','조사','--motion-only']),('investigations',['--query','조사','--include-unobserved'])]
counts={}
for label,args in queries:counts[label]=len(run(['query','--catalog',cat,'--index',idx]+args,'queries/'+label+'.json')['uses'])
save('commands.json',commands)
md('run_queries.ps1',"$python = '"+sys.executable.replace('\\','/')+"'\n$tool = '"+str(S/'scripts/knowledge_links.py').replace('\\','/')+"'\n$catalog = Join-Path $PSScriptRoot 'knowledge-catalog.json'\n$index = Join-Path $PSScriptRoot 'knowledge-use-index.json'\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '업무 이미지'\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '건물/기단'\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '역할판'\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --id LAYOUT-SPACE-CALLOUT\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query 'RC-COMP-002@v1'\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '조사' --motion-only\n& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '조사' --include-unobserved\n")
query_lines=['# 실제 조회 명령과 결과','', '실행: PowerShell에서 `& ./run_queries.ps1`. 정확 실행인수/종료코드는 [commands.json](commands.json), 검사결과는 [check-result](check-result.json), 색인생성은 [index-result](index-result.json). 조회는 정확 개념ID 또는 명시 부분문자열이며 의미검색/추천/회사승인이 아니다.','', '| 검색 | 실제반환 사용처수 | 저장결과 |','|---|---:|---|']
for label,count in counts.items():query_lines.append(f'| {label} | {count} | [{label}.json](queries/{label}.json) |')
query_lines+=['','왕복실행: 업무이미지→007@v1→U-C9→134초/E1/e1_work→원문정의·현재차이·미검증. 건물/기단→008@v1→U-C10→172초/E2/e2_building→005명찰과anchors_to/overlaps. 역할판→LAYOUT001@v1→U-L1→134초전체→SPLIT/NETWORK와Q-INFO-02검토. [타일조회](queries/tiles.json)는같은정의002@v1의E1/E2두사용처와2×4/원근열·HALLA/피티씨차이를반환한다.','', 'LAYOUT-SPACE-CALLOUT→002무대/008건물/005명찰→각사용처/근거로역조회, SCREEN-GROUP→역할판/무대/업무묶음/건물의다른사용처로이동, Q-SCREEN-01→실제판정행/범위를조회했다. events/event_links는모션미관측이며 observed-motion은0건, include-unobserved조사는4건이다. 이0은실제모션없음을뜻하지않는다.','', '해시가바뀌면조회/검사가실패하도록pin한다. MD/sidecar를편집하면연결이유를검토하고 색인을다시생성해야한다. R4통합v0.2자동이관/등록·원본상세자동동기화는없다. prior의과거scratch/original링크는이력으로보존하고 활성경로를02/03문서에서별도제시했다.']
md('05_조회안내.md','\n'.join(query_lines))
checks={'copied_prior_byte_equal':all(sha(p)==sha(W/'knowledge-linked-skill-20261019/eval-inputs/static'/p.name) for p in (O/'prior').glob('*.md') if p.name!='input.md'),'png_hashes':{e['id']:e['sha256'] for e in R['evidence'][:2]},'unit_count':len(R['units']),'use_count':len(R['uses']),'knowledge_link_count':len(R['knowledge_links']),'review_count':len(R['reviews']),'query_use_counts':counts,'check_exit_codes':[x['exit_code'] for x in commands],'scope':'reference/hash/range plus this execution PNG/ROI self-readback; not independent semantic audit/company approval'}
save('verification.json',checks)
print(json.dumps(checks,ensure_ascii=False,indent=2))
