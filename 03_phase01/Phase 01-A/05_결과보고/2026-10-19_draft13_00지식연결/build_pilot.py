from pathlib import Path
import json,hashlib,shutil,importlib.util,os
R=Path(__file__).resolve().parent;W=R.parent;P=R/'pilot';P.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copytree(W/'collection-skill-structure-20261019/records',P/'preserved/static',dirs_exist_ok=True)
shutil.copytree(W/'value-creation-collection-20261019',P/'preserved/motion',dirs_exist_ok=True)
def srcrows(folder):return [dict(id='S'+str(i+1),path=f.relative_to(P).as_posix(),sha256=sha(f),role='preserved_observation') for i,f in enumerate(sorted(folder.glob('*.md')))]
def evidence(key,path,a,b=None):return dict(id=key,path=path.relative_to(P).as_posix(),sha256=sha(path),time={'start':a,'end':a if b is None else b},kind='still_frame' if b is None else 'contact_sheet')
def base(key):return dict(schema_version='video-knowledge-links-0.1',record_id=key,version='r1',source={'name':'가치창출성과 영상_260923_v3.mp4','sha256':'be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa','duration_seconds':434.4},source_records=[],evidence=[],claims=[],units=[],facets=[],knowledge_links=[],uses=[],composition_links=[],events=[],event_links=[],reviews=[],unknowns=[],limitations=['기존 관측 기록과 지식의 연결 작업. 새 원본 연속 재생/재추출·새 픽셀 검수 아님.','정확 AE 속성·폰트·색 원값/실제 청취/원제작 의도·다른 내용/화면비 적용은 미검증.','정본 등록/회사 승인 아님. source record와 연결 구조는 별도이며 자동 동기화 없음.'],company_approved=False,canonical_registered=False)
def claim(d,key,text,evs,basis='observed'):
    d['claims'].append(dict(id=key,text=text,basis_kind=basis,evidence_ids=evs,source_record_ids=[x['id'] for x in d['source_records']]))
def unit(d,key,kind,title,summary,status='observed_static',version='v1'):
    d['units'].append(dict(id=key,kind=kind,title=title,summary=summary,observation_status=status,definition_version=version))
def facet(d,target,domain,name,description,claims,basis='inferred'):
    d['facets'].append(dict(id='F'+str(len(d['facets'])+1),unit_id=target,domain=domain,name=name,description=description,basis_kind=basis,claim_ids=claims))
def knowledge(d,target,key,relation,claims,why):
    d['knowledge_links'].append(dict(id='K'+str(len(d['knowledge_links'])+1),unit_id=target,concept_id=key,relation=relation,basis_kind='inferred',claim_ids=claims,rationale=why))
def use(d,key,target,case,a,b,evs,claims,diffs=None,condition=None):
    d['uses'].append(dict(id=key,definition_id=target,case_unit_id=case,time={'start':a,'end':b},evidence_ids=evs,claim_ids=claims,differences=diffs or [],unverified=['동일 원본 자산/회사 표준 및 다른 주제·화면비 적용 미검증'],conditions=[{'text':condition or '현재 정보 역할·관계를 보존하는 범위의 후보. 새 내용의 의미·문구·읽기 시간은 재검토한다.','validation':'untested'}]))
def compose(d,a,b,rel,claims,basis='inferred'):
    d['composition_links'].append({'from':a,'to':b,'relation':rel,'basis_kind':basis,'claim_ids':claims})
def review(d,target,key,status,reason,evs,claims,probe=None):
    d['reviews'].append(dict(id='R'+str(len(d['reviews'])+1),unit_id=target,criterion_id=key,status=status,reason=reason,evidence_ids=evs,claim_ids=claims,reviewer='AI: 기존 기록-새 연결 구조 대조',scope='기존 관측 기록의 의미/연결 검토. 새 원본 시각·가독성/효과 검사 아님.',next_probe=probe))
    knowledge(d,target,key,'evaluated_against',claims,reason)

titles={'RC-COMP-001@v1':('장 번호/제목 표식','장 번호와 장 제목을 묶는 표식. 본문 전체 디자인과 구분.'),
'RC-COMP-002@v1':('가족사 로고 타일 묶음','같은 회사 목록을 담은 타일 가족 후보. 동일 파일/연속 모핑은 미확인.'),
'RC-COMP-003@v1':('역할 헤더','역할판 상부의 헤더/구분선/문구 묶음.'),
'RC-COMP-004@v1':('요청·지원 방향 라벨','주체와 방향별 문구를 함께 전달하는 표식. 실제 모션은 미관측.'),
'RC-COMP-005@v1':('지원 명찰','건물 주변 네 지원 항목 표식. 건물/기단과 별도 부품.'),
'RC-COMP-006@v1':('성과 수치 조형','큰 금액+단위와 받침/강조 조합. 정량 차트와 구분.'),
'RC-COMP-007@v1':('업무 이미지 묶음','모니터3대+선반+책/화분을 묶은 업무 이미지. 소품은 하위 구성.'),
'RC-COMP-008@v1':('건물/기단 묶음','건물과 원형 기단을 묶은 기관 대상. 주변 명찰과 별도.')}
conditions={1:'장 구분이 필요한 경우 번호/제목 역할을 보존한다. 표식의 색·장 번호·제목은 가변 후보이며 회사 표준은 미확인.',
 2:'같은 소속 목록을 묶어 보여줄 때 회사명/로고 식별·비율을 보호한다. 개수·격자/가로열은 가변 후보이나 순서·읽기와 공식 자산을 다시 검토한다.',
 3:'역할 영역의 상위 제목과 하위 정보를 구분할 때 사용. 헤더 문구/폭은 가변이지만 본문과 구분되는 위계·경계는 검토한다.',
 4:'두 주체 사이 요청/지원의 방향과 문구를 함께 보호한다. 색·길이/배치는 변형 후보이며 방향이 다른데 같은 의미로 복제하지 않는다.',
 5:'주변에 배치할 지원 항목과 중심 대상의 의미 대응을 보호한다. 항목수/문구/위치는 가변 후보이며 건물 일부라는 오해·가림을 검토한다.',
 6:'같은 집계/단위를 가진 하나의 성과를 크게 강조할 때 후보. 값/단위/산정 맥락은 보호하고 단순 ID/날짜를 값 변화나 성과 척도로 쓰지 않는다.',
 7:'전문 업무를 상징하는 장면 묶음이 필요할 때 후보. 모니터/선반/소품의 그룹 역할은 보호하며 개수·소품은 가변 후보. 실제 제품 UI/기능을 증명하지 않는다.',
 8:'기관을 대표하는 대상+받침을 함께 쓸 때 후보. 건물과 기단의 지지·공간 관계는 보호하며 명찰은 별도. 실제 사옥/정확 투영·규정은 별도 확인.'}
profile='PROFILE-VC-CREAM-SPACE@v1'
for second in [134,172]:
    d=base('LINK-VC-'+str(second));d['source_records']=srcrows(P/'preserved/static')
    d['evidence']=[evidence('E134',P/'preserved/static/evidence/134.png',134),evidence('E172',P/'preserved/static/evidence/172.png',172)]
    case='RC-CASE-001' if second==134 else 'RC-CASE-002';layout='RC-LAYOUT-001@v1' if second==134 else 'RC-LAYOUT-002@v1';ev='E'+str(second)
    if second==134:
        claim(d,'C1','가족사 사업→기술개발센터 전문인력 참여: 파랑 프로젝트 요청. 반대 방향 초록 전문인력 지원.',[ev])
        claim(d,'C2','흰 역할판 두 개, 왼쪽 회사8개 2열×4행, 오른쪽 역할 헤더/BIM/모니터 업무 묶음. 중앙 관계 여백.',[ev])
        claim(d,'C3','크림 공간·흰 유광처럼 보이는 판·모서리 색 강조·원형 도상·가는 선·바닥 반사가 함께 보임.',[ev])
        claim(d,'C4','업무 묶음은 모니터3대+선반+책·화분. 별도 방향 라벨은 두 역할판의 문구/방향과 대응.',[ev])
        members=[1,2,3,4,7];title='두 조직의 요청·지원 역할판';information='두 주체의 방향 있는 요청/지원 교환. 비교 지표나 데이터 상관으로 강제하지 않음. 관계 세부 어휘는 미분류 후보.';grid='전체는 두 역할 영역과 중앙 연결 여백, 왼쪽 내부는2열×4행 모듈. 정보 유형과 기하 배치를 별도로 기록.'
        type_roles='장 표식/본문 제목→역할 헤더→BIM 항목/회사명→방향별 요청·지원 문구. 글꼴명/정확 척도는 미상.'
        variant='흰 판/가는 구분선·파랑 요청/초록 지원을 관계에 대응. 역할색을 회사CI 원색/규정으로 확정하지 않음.'
    else:
        claim(d,'C1','실제 투입 인력·비용 기준 성과 23.7억원으로 설명. 회사별 배분/산정 타당성은 미검증.',[ev])
        claim(d,'C2','왼쪽 거대 금색 입체 수치–중앙 원근 회사열–오른쪽 건물/원형 기단의 공간 배치.',[ev])
        claim(d,'C3','크림·금색 공간·곡선 받침·투명 판·짙은 녹색 유리처럼 보이는 면·바닥 반사/금빛 곡선.',[ev])
        claim(d,'C4','BIM지원 위, BIM설계 좌아래, 디자인지원 오른쪽, 해외사업지원 전면 아래. 명찰과 건물/기단은 별도.',[ev])
        members=[1,2,5,6,8];title='성과값·회사열·센터의 공간 무대';information='성과 수치·관련 회사·센터 지원 범위의 병렬 제시. 회사열을 금액의 분할/합산 증거로 해석하지 않음.';grid='좌 수치/중앙 회사열/우 기관 대상의 비대칭 세 영역. 회사 타일의 기하 배열은 원근 가로열이며 134초 모듈과 다름.'
        type_roles='23.7억원은 주수치+단위, 상부 설명문은 산정 맥락, 명찰은 지원 항목. 숫자 크기가 정량 척도를 뜻하지 않음.'
        variant='금색 입체 수치를 주강조하고 건물 녹색 면/투명 명찰·원형 기단으로 공간을 구성. 실제3D 제작도구/공식CI색은 미상.'
    claim(d,'C5','두 화면의 동일 회사 목록은 2×4와 원근 가로열의 배치 차이, HALLA/피티씨 순서 차이를 가진 가족 후보. 동일 파일/이동은 미확인.',['E134','E172'])
    claim(d,'C6','좌상 장 표식은 금갈색 육각형 배지의 2/TDC와 프로젝트 지원을 통한 가치 창출 제목을 묶는다. 본문 제목과 구별된다.',[ev])
    unit(d,case,'case',title,' '.join(x['text'] for x in d['claims'][:3])+' 모션은 두 정지 표본에서 미관측. 전체 문구/디테일은 보존 MD에 연결.')
    unit(d,layout,'layout',title+' 구성',grid)
    unit(d,profile,'visual_profile','크림 공간의 입체 정보 무대','크림색 공간+입체 정보 대상+받침/프레임·반사의 조합 가족 후보. 개별 색·대상·재질 처리 차이는 사용처에 보존.')
    facet(d,layout,'information','관계/내용',information,['C1','C2'])
    facet(d,layout,'screen','전체/하위 격자',grid,['C2','C5'])
    facet(d,profile,'visual','타입의 역할',type_roles,['C1','C2','C4'])
    facet(d,profile,'visual','역할색/형태/재질/층',variant,['C3'])
    facet(d,profile,'visual','공통 표현 조합','크림 배경과 입체 대상·프레임/기단·반사를 공간 기준으로 함께 기록. 고급스럽다는 평가/시청자 효과는 확정하지 않음.',['C3'])
    facet(d,layout,'motion','관측 상태','이번 근거는 정지 두 점. 등장·이동·정착·퇴장/오디오·이징은 미관측.',['C2'])
    for n in members:
        key=f'RC-COMP-{n:03}@v1';unit(d,key,'component',*titles[key]);compose(d,layout,key,'contains',['C2','C4'])
        use(d,'U'+str(n),key,case,second,second,[ev],['C6'] if n==1 else (['C4'] if n in [4,5,7,8] else ['C2']),['2×4 vs 원근 가로열, HALLA/피티씨 순서 차이'] if n==2 else [],conditions[n])
        if n==2:
            d['uses'][-1]['claim_ids']=['C2','C5'];d['uses'][-1]['evidence_ids']=['E134','E172']
            d['uses'][-1]['evidence_roles']={eid:('current' if eid==ev else 'context_variant') for eid in ['E134','E172']}
    for key in [layout,profile]:use(d,'U-'+('LAYOUT' if key==layout else 'PROFILE'),key,case,second,second,[ev],['C1','C2','C3'],[variant],condition=('주체/방향/내용 관계와 읽는 구역을 보호한다. 판 개수·격자·원근·여백은 내용량/화면비에 맞춘 변형 후보.' if key==layout else '크림 공간+입체 정보대상+지지면/반사의 조합을 참고한다. 소재/역할색/대상은 가변 후보이며 정보 관계·필수 문구/회사CI를 훼손하지 않는다.'))
    compose(d,case,layout,'contains',['C2']);compose(d,layout,profile,'accompanies',['C3'])
    if second==172:compose(d,'RC-COMP-005@v1','RC-COMP-008@v1','anchors_to',['C4'])
    knowledge(d,layout,'LAYOUT-SPLIT','classified_as',['C2'],grid)
    if second==134:knowledge(d,layout,'LAYOUT-NETWORK','classified_as',['C1','C2'],'표식과 방향으로 두 집단을 연결한다. 인과/동작은 미확정.')
    else:knowledge(d,'RC-COMP-008@v1','LAYOUT-SPACE-CALLOUT','classified_as',['C4'],'기관 대상 주변 위치에 라벨을 대응한다. 실제 공간 좌표/등각 도면은 아님.')
    knowledge(d,profile,'STYLE-3D','classified_as',['C3'],'입체·공간 표현의 외관 분류. 실제 모델/카메라 도구 증거 아님.')
    knowledge(d,layout,'SCREEN-HIERARCHY','review_relevant',['C1','C2'],'주/보조/맥락 역할 보존을 검토할 지식. 효과 승인 아님.')
    review(d,layout,'Q-INFO-03','pass','관계/금액을 근거 없는 비교·인과·분할로 확대하지 않고 원래 의미/한계를 기록했다.',[ev],['C1','C2'])
    review(d,profile,'Q-BRAND-02','hold','관측색/재질과 공식CI 원형/역할 토큰의 연결은 미확인.',[ev],['C3'],'선택할 회사/프로젝트 역할·공식CI 사용 근거를 확인')
    review(d,layout,'Q-MOTION-01','not_reviewed','정지 입력만으로 정보 완성/읽기 유지 시간을 검토하지 못함.',[],['C2'],'해당 장면의 실제 모션/읽기 유지 구간을 확보')
    d['unknowns']=[dict(id='UNKNOWN-MOTION',unit_id=layout,question='대상별 등장/내부 변화/정착/퇴장은 어떠한가?',impact='동작 패턴/읽기 시간 재사용 제한',next_probe='해당 구간 연속 근거/경계 표본 확보')]
    for c in d['claims']:
        names=['01_부품과조합.md','02_전체상세.md'] if c['id'] in ['C4','C5'] else ['02_전체상세.md']
        c['source_record_ids']=[x['id'] for x in d['source_records'] if Path(x['path']).name in names]
    save(P/f'case-{second}.json',d)

old=json.loads((W/'grammar-usage-index-20261019/data/uses.json').read_text(encoding='utf-8'))
d=base('LINK-VC-MOTION');d['source_records']=srcrows(P/'preserved/motion')
unit(d,'VC-CASE-A','case','계약 성과 전개','기존 계약 수집의 선택 모션 창만 연결','observed_sampled')
unit(d,'VC-CASE-B','case','지원 성과 전개','기존 지원 수집의 선택 모션 창만 연결','observed_sampled')
for j,row in enumerate(old[5:11],1):
    a,b=row['seconds'];eid='E'+str(j);cl='C'+str(j);target=row['local_units'][0];case='VC-CASE-'+('A' if j<4 else 'B')
    sheet=Path(row['evidence'][-1]).name;d['evidence'].append(evidence(eid,P/'preserved/motion/evidence'/sheet,a,b))
    claim(d,cl,row['content']+' '+row['limits'],[eid]);unit(d,target,'flow',row['title'],row['content'],'observed_sampled')
    d['claims'][-1]['source_record_ids']=[x['id'] for x in d['source_records'] if Path(x['path']).name in [('01_계약_수집기록.md' if j<4 else '02_프로젝트지원_수집기록.md'),'05_근거와_실행기록.md']]
    facet(d,target,'information','사용한 내용',row['content'],[cl]);facet(d,target,'motion','전체 흐름/겹침/미상',row['limits'],[cl])
    flow_conditions={1:'설명을 누적하면서 이전 구역을 보존할 때 후보. 공간이 이미 찼다면 같은 판 추가를 강제하지 않는다.',2:'기존 두 지표와 새 지표의 비교 맥락을 유지할 때 후보. 기간/집계가 바뀌면 이전 수치를 그대로 남기지 않는다.',3:'연속 양을 나타내는 성과 강조에 후보. 날짜/식별번호는 카운트업 제외, 변화 중 보간값은 실측 데이터가 아니다.',4:'관계 맥락에서 총량 요약으로 넘길 때 후보. 기존 방향 문구를 읽어야 한다면 퇴장 시점을 다시 검토한다.',5:'여러 업무의 실제 사례 영상을 함께 소개할 때 후보. 기간/범위가 다른 자료를 동등 비교로 오해시키지 않도록 라벨을 검토한다.',6:'실제로 우세한 구성비와 나머지 항목을 설명할 때 후보. 분모/단위를 보호하며 네 항목이라는 이유만으로 주1+보조3을 강제하지 않는다.'}
    use(d,'U'+str(j),target,case,a,b,[eid],[cl],condition=flow_conditions[j])
    compose(d,case,target,'contains',[cl])
    for tag in row['grammar_tags']:knowledge(d,target,tag,'classified_as',[cl],'기존 표본 기록의 해당 역할/속성/관계 해석. 정확 구현/정보 효과 검증 아님.')
    for tag in row['review_knowledge_refs']:knowledge(d,target,tag,'review_relevant',[cl],'이 기록에서 검토할 관련 지식. 원제작자의 원칙 사용/효과를 입증하지 않음.')
    d['events'].append(dict(id='EVENT'+str(j),unit_id=target,title=row['title'],status='observed_sampled',time={'start':a,'end':b},claim_ids=[cl]))
    review(d,target,'Q-MOTION-02','pass','기존 기록의 대상·변화·유지/중첩과 확인 범위를 연결했다. 가시성 변화를 원본 속성/AE 구현으로 확정하지 않았다.',[eid],[cl])
    review(d,target,'Q-CAP-02','not_reviewed','실제 음성/자막 싱크를 청취하지 않았다.',[],[cl],'실제 오디오/자막과 해당 원본 시각을 확보')
    d['unknowns'].append(dict(id='UNKNOWN'+str(j),unit_id=target,question='정확 경계·속도곡선·원본 구현은?',impact='정밀 동작/구현 템플릿으로 직접 사용 제한',next_probe='쟁점 경계/대상의 추가 원본 표본 또는 프로젝트를 확인'))
for suffix,parent,title,summary,eid,cl,a,b in [
 ('A-NUM','VC-CASE-A/A-M3','매출 수치 변화','0.8→10.8→12.9억원. 끝값 가시 경계(110,110.5]초. 중간값은 실적 시계열 아님.','E3','C3',108,112),
 ('A-ICON','VC-CASE-A/A-M3','상승 도상 후속 조립','수치가 끝값을 보인 뒤에도 111/112초의 상승 도상 상태가 다름. 정확 완료 미상.','E3','C3',108,112),
 ('B-NUM','VC-CASE-B/B-M3','비중 수치 공개','약44→64→82%, 끝값 가시 경계(148.5,149]초.','E6','C6',147,150),
 ('B-CARDS','VC-CASE-B/B-M3','보조 카드/차트 후속 보강','149.5초 세번째 카드·도넛색·막대 후속. 모든 요소 동시 완료 아님.','E6','C6',147,150)]:
    key='MOTION-VC-'+suffix+'@v1';unit(d,key,'detail',title,summary,'observed_sampled');facet(d,key,'motion','독립 세부 동작',summary,[cl]);case='VC-CASE-'+suffix[0]
    use(d,'U-'+suffix,key,case,a,b,[eid],[cl],condition=('수치/단위/끝값의 의미를 보호하고 보간값을 실측으로 쓰지 않는다. 속도/유지는 새 문구와 시청 조건에서 검토한다.' if suffix.endswith('NUM') else '주수치와 관련된 보조 동작이지만 동시 완료를 전제하지 않는다. 장식의 후속 때문에 실제 정보가 언제 완성되는지 가려지지 않는지 검토한다.'));compose(d,parent,key,'contains',[cl]);knowledge(d,key,'FUNCTION-REVEAL','classified_as',[cl],'관측 단계의 공개 역할을 분류한 해석.')
    start=110.5 if suffix=='A-NUM' else (111 if suffix=='A-ICON' else (149 if suffix=='B-NUM' else 149.5))
    event={'id':'EVENT-'+suffix,'unit_id':key,'title':title+('의 끝값이 보이는 첫 표본' if suffix.endswith('NUM') else '의 관측된 후반 변화 상태'),'status':'observed_sampled','time':{'start':start,'end':start if suffix.endswith('NUM') else b},'claim_ids':[cl]}
    if suffix in ['A-NUM','B-NUM']:event['start_bounds']=[110,110.5] if suffix=='A-NUM' else [148.5,149]
    d['events'].append(event)
for group,cl in [('A','C3'),('B','C6')]:
    d['event_links'].append({'from':'EVENT-'+group+('-ICON' if group=='A' else '-CARDS'),'to':'EVENT-'+group+'-NUM','relation':'continues_after','basis_kind':'observed','claim_ids':[cl]})
    review(d,'VC-CASE-'+group+('/A-M3' if group=='A' else '/B-M3'),'Q-MOTION-01','hold','수치 끝값과 보조 도상/카드의 후속 상태는 구분했지만 정보 전체 완성/읽기 유지 시간은 미확인.',['E3' if group=='A' else 'E6'],[cl],'전체 대상의 마지막 변화와 읽기 유지 구간을 실제 원본에서 확인')
save(P/'motion-windows.json',d)

spec=importlib.util.spec_from_file_location('kl',R/'candidate/company-video-grammar-analyzer/scripts/knowledge_links.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cat=m.catalog_read(R/'knowledge/catalog.json');files=[P/'case-134.json',P/'case-172.json',P/'motion-windows.json']
for f in files:m.check_record(cat,f)
index=m.make_index(cat,R/'knowledge/catalog.json',files)
index['catalog_pin']['path']=os.path.relpath(R/'knowledge/catalog.json',P).replace('\\','/')
for row in index['records']:row['path']=os.path.relpath(row['path'],P).replace('\\','/')
save(P/'usage-index.json',index)

for f in files:
    d=json.loads(f.read_text(encoding='utf-8'));lines=[f"# {d['record_id']} — 지식과 사용처 연결",'',
    '이번 결과는 기존 관측의 연결 재편집이다. 읽는 순서: 사례 요약 → 아래의 연결 상세 → 보존 원문과 근거. 새 원본 관측/회사 승인 아님.','']
    for u in d['units']:
        if u['kind']=='case':lines += [f"## 사례 요약 — {u['title']}",'',u['summary'],'']
    if d['record_id'] in ['LINK-VC-134','LINK-VC-172']:
        second=d['record_id'].split('-')[-1];lines += [f'![{second}초 원본](preserved/static/evidence/{second}.png)','']
    lines += ['## 상세 — 정보/화면/표현/모션의 역할','','| 단위 | 관점 | 기록 |','|---|---|---|']
    for x in d['facets']:lines.append('| '+x['unit_id']+' | '+x['domain']+' / '+x['name']+' | '+x['description'].replace('|','／')+' |')
    lines += ['','## 재사용 정의와 사용처','','| 정의/판본 | 내용·시각 | 현재 차이/미검증 | 재사용 조건(미시험) |','|---|---|---|---|']
    for x in d['uses']:
        u=next(u for u in d['units'] if u['id']==x['definition_id']);tm=x['time'];t=str(tm['start'])+'초' if tm['start']==tm['end'] else f"{tm['start']}~{tm['end']}초";lines.append(f"| {u['id']} / {u['definition_version']} — {u['title']} | {x['case_unit_id']} {t} | {' / '.join(x['differences']+x['unverified'])} | {' / '.join(c['text'] for c in x['conditions'])} |")
    lines += ['','## 실제 검토와 보류','','| 항목/대상 | 결과 | 이유와 다음 확인 |','|---|---|---|']
    for x in d['reviews']:lines.append(f"| {x['criterion_id']} / {x['unit_id']} | {x['status']} | {x['reason']} {x.get('next_probe') or ''} |")
    lines += ['','관련 지식 분류/검토 연결과 근거 ID는 [부속 색인]('+f.name+')을 따른다. 위 pass는 기존 기록과 새 연결의 일관성 검토이며 새 원본 가독성/효과 판정이 아니다.','','## 보존 원문과 근거','']
    for x in d['source_records']:lines.append(f"- [{Path(x['path']).name}](<{Path(x['path']).as_posix()}>)")
    lines += ['','한계: '+' / '.join(d['limitations'])]
    f.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('pilot: 2 still cases, 6 prior motion flows + 4 linked detail units; 3 sidecars validated')
