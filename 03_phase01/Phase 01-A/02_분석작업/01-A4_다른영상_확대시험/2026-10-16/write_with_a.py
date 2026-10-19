from pathlib import Path
from fractions import Fraction
import json

R=Path(__file__).parent
plan=json.loads((R/'case-plan.json').read_text(encoding='utf-8'))
rois=json.loads((R/'with_a_rois/manifest.json').read_text(encoding='utf-8'))
common=['case-plan.json','output-format.md','skill-draft2/SKILL.md','skill-draft2/references/evidence-and-records.md','skill-draft2/references/motion-review.md','skill-draft2/references/output-contract.md','skill-draft2/scripts/evidence_catalog.py','skill-draft2/scripts/check_observations.py','extract.py','with_a_rois/manifest.json']

def base(c):
    p=next(x for x in plan['cases'] if x['case_id']==c)
    return dict(schema_version='a3-observation-0.1',case_id=c,source=p['source'],window_seconds=p['window_seconds'],method='개요 보드는 탐색에만 사용. 실제 PNG 선택 프레임을 view_image로 열람하고 작은 글자·경계는 native raster ROI를 별도 열람. 시간순 관찰 뒤 완성 상태에서 역추적. 연속 재생/전 프레임 검사는 하지 않음.',document_mode='none' if c=='V05' else 'storyboard_text_chronology_unverified',audio_reviewed=False,evidence=[],objects=[],coverage={},hypotheses=[],limitations=['선택 표본 사이의 정확한 시작/종료 프레임 및 짧은 사건은 미확정.','가감속은 명시한 대상/속성의 시각 추정이며 원본 보간함수·키프레임 값은 미상.','RGB 변환 색 범위 정확도 미검증; 픽셀색을 공식 CI색으로 해석하지 않음.','오디오 디코딩·청취·전사 없음. 음성/자막 싱크 미검수.','회사 공통 규칙이나 제작 의도, 실제 안전성 인증으로 승격하지 않은 AI 관측 초안.','Phase 00 정본 용어 정의가 별도 제공되지 않아 분류 ID를 임의 부여하지 않음.'],files_read=[str(R/x) for x in common])

def frames(d,aid,case,inds,prefix):
    lp=R/'cases'/aid/case/'실행기록.json';log=json.loads(lp.read_text(encoding='utf-8'));d['files_read'].append(str(lp))
    d.setdefault('extraction_context',[]).append({k:log.get(k) for k in ['phase','timing_status','timing_mapping','sar_status','orientation','input_sha256','input_sha256_after']})
    for i in inds:
        f=log['frames'][i];d['evidence'].append(dict(id=prefix+str(i),path=f['path'],actual_seconds=f['actual_playback_seconds'],role='context_after' if Fraction(f['actual_playback_seconds'])>=Fraction(str(d['window_seconds'][1])) else 'within',sha256=f['sha256'],raster=f['raster'],transforms=f['transforms'],extraction_log=str(lp)));d['files_read'].append(f['path'])

def crops(d,names,prefix):
    for name in names:
        r=next(x for x in rois if Path(x['path']).stem==name)
        e=dict(id=prefix+name.split('_')[-1],path=r['path'],actual_seconds=r['actual_seconds'],role='within',sha256=r['sha256'],parent_path=r['parent_path'],transforms=[dict(op='crop',xyxy=r['crop_xyxy'],coordinate_system='native 3840x2160 raster',resize=None)])
        d['evidence'].append(e);d['files_read'].append(r['path'])

def event(desc,props,t,refs,order='',kind='unknown',basis='이동/리빌은 관찰했으나 표본의 블러·가림 또는 변화량 미계측으로 정확한 가감속을 분류하지 않음.',status='observed',lim=None):
    return dict(description=desc,properties=props,time_seconds=t,evidence_ids=refs,direction_order=order,easing=dict(property=props[0],classification=kind,basis=basis),status=status,limitations=lim or [])

def obj(d,id,name,events,parent=None):d['objects'].append(dict(id=id,name=name,parent=parent,events=events))

def save(d):
    d['files_read']=list(dict.fromkeys(d['files_read']))
    out=R/'company-video-grammar-analyzer-workspace/iteration-1'/('eval-'+d['case_id'])/'with_skill/outputs';out.mkdir(parents=True,exist_ok=True)
    (out/'observations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=[f"# {d['case_id']} 관찰 초안",'',f"범위: {d['window_seconds']}초, 시작 포함/끝 제외. 오디오는 미검수.",'',d['coverage']['overview'],'']
    for o in d['objects']:
        lines.append('## '+o['name']);lines.append('')
        for e in o['events']:lines.append(f"- {e['time_seconds'][0]}–{e['time_seconds'][1]}초: {e['description']} (근거 {', '.join(e['evidence_ids'])}; 가감속 {e['easing']['classification']}: {e['easing']['basis']})")
        lines.append('')
    if d.get('document_comparison'):
        lines+=['## 문서 대응','']
        for x in d['document_comparison']:lines.append('- '+x['finding']+' — '+', '.join(x['locators']))
    lines+=['','## 검사 범위와 남은 한계','',d['coverage']['secondary_details'],d['coverage']['internal_content'],'']
    lines += ['- '+x for x in d['coverage']['unresolved']+d['limitations']]
    lines+=['','근거 파일·실제 표시시각·해시·ROI 변환은 observations.json에 연결했습니다. 구조 검사는 내용 정답이나 회사 승인을 뜻하지 않습니다.']
    (out/'observations.md').write_text('\n'.join(lines),encoding='utf-8')
    print(out)

d=base('V01');frames(d,'A4-D','V01',[0,3,4,6,8,12,16,19,20],'f');frames(d,'A4-D','V01_with_more',[],'x')
crops(d,['V01_with_more_title_'+str(i) for i in range(8)],'t')
d['files_read'] += [str(R/x) for x in ['documents/DOC063.txt','documents/DOC063.json','with_a_catalog_D.json','with_a_catalog_more.json','cases/A4-D/V01/board-1.jpg','cases/A4-D/V01/board-2.jpg']]
obj(d,'scene','가교 전경·카메라',[
 event('수면을 넓게 두고 육지에서 두 작업대로 이어지는 가교를 대각선으로 본다. 앞쪽 작업대에는 노란 크롤라크레인, 아래쪽 수면 가까이에는 프레임과 수직 파일/장비가 보인다. 뒤쪽에는 지게차 모양 장비·자재·콘·난간이 있다. 초기 전경에서 점차 크레인과 앞 작업대가 커지고 육지/뒤 작업대는 좌상 방향으로 밀려난다. 컷 없이 접근하는 화면 변화이다.',['apparent_scale','position'],[0,8],['f0','f3','f6','f8','f12','f16','f19','f20'],'전경 → 앞 작업대/크레인에 접근',basis='0~1.2초 변화가 작고 3.2/4.8/6.4/8초에서 확대가 진행된다. 원근 변화와 카메라 이동이 혼합되어 동일 특징의 속도를 계측하지 않았으므로 가속 여부는 보류. 8초는 context_after이다.')])
obj(d,'title_bg','좌상 제목 배경',[
 event('1.2초에 밝은 짧은 수평 막대가 나타나고 1.3→1.5초 오른쪽으로 뻗으면서 높이도 커져 둥근 사각형이 된다. 1.7초의 큰 살구색 배경은 이후 폭·높이를 줄여 어두운 갈색/회색 배경으로 정착한다.',['scale','reveal','color'],[1.2,2.4],['f3','t0','t1','t2','f4','t3','t4','t5','t6','t7','f6'],'짧은 막대 → 가로 확장·두꺼워짐 → 큰 둥근 배경 → 축소·어두워짐',basis='초기 확장과 후반 축소는 방향이 다르다. 1.7/1.8/1.9/2.1/2.2 표본에서 후반 축소가 줄어드는 경향이지만 블러와 비균일 표본 때문에 전체를 단일 곡선으로 분류하지 않음.')])
obj(d,'title_text','제목 문구',[
 event('“1.크레인 작업 반경 및 물류인양 안정성 검토”가 왼쪽부터 선명해진다. 앞 구절은 주황, “안정성 검토”는 흰색이다. 배경이 만들어지는 동안 문구는 아직 일부만 보여 배경 리빌과 글자 리빌이 중첩된다. 1.7→2.2초 이미 읽히는 “1.크레인” 글자의 크기도 조금 줄어든다.',['reveal','scale'],[1.5,2.4],['t2','t3','t4','t5','t6','t7','f6'],'왼쪽 문구부터 오른쪽 “안정성 검토”까지',basis='각 글자 선명화와 크기 변화가 중첩되어 글자별 속도/불투명도 곡선을 분리 계측하지 않음.')])
obj(d,'title_outline','제목의 얇은 외곽 테두리',[
 event('배경 바깥의 가는 밝은 둥근 선이 별도로 나타난다. 1.7초에는 상단 선이 우측 끝까지 닫히지 않았고 1.8/1.9초에 더 오른쪽으로 이어진다. 2.1/2.2초에는 제목 외곽을 감싼다. 배경 면이 이미 넓게 있어도 선의 완성은 뒤따른다.',['reveal'],[1.5,2.4],['t2','t3','t4','t5','t6','t7','f6'],'왼쪽 둥근 가장자리에서 위·아래 수평선이 우측으로 연결',basis='얇은 선 끝을 ROI로 확인했으나 밝기/블러 때문에 픽셀 단위 궤적과 속도는 미계측.')],parent='title_bg')
obj(d,'subtitle','“대호지교 가교” 보조 문구',[
 event('제목 아래에 회색 보조 문구가 흐리게 나타난 후 “대호지교 가교”로 읽히게 된다. 1.7~1.9초 글자마다 기울고 흐린 상태가 보이고 2.1~2.4초 수평 줄로 정돈된다. 제목보다 늦게 완성된다.',['visibility','shape'],[1.7,2.4],['t3','t4','t5','t6','t7','f6'],'제목 리빌 중 시작 → 제목 아래 정착',basis='흐린 중간 글자에서 변형/회전 성격은 보이나 축이나 글자별 순서는 부족한 표본으로 확정하지 않음.')])
obj(d,'environment','수면·크레인 내부/주변',[
 event('전경이 확대되는 동안 수면의 밝고 어두운 물결·반사 패턴도 바뀐다. 크레인 붐, 검은 와이어, 매달린 장비와 수직 파일은 계속 보이나 이 표본들만으로 크레인의 독립 주행이나 하중 인양을 확정하지 않는다.',['internal_content','luminance'],[0,8],['f0','f6','f12','f16','f19','f20'],'수면 변화는 카메라 접근과 동시',basis='수면 패턴은 비강체이고 카메라도 움직이므로 단일 방향/속도는 미상.')])
d['document_comparison']=[dict(document_id='DOC063',document_sha256='879959f784ee8fa6cca088056305249aaef8fa6a9a4e58bf365a52fd20818c36',locators=['slide[2]/p[5]','slide[2]/p[6]'],quote='멀리서 대호지교 가교 공사 환경을 줌인 한다.',evidence_ids=['f0','f6','f12','f19'],finding='문서 Scene 1 (00:00~00:10)의 전경→크레인 포커싱 줌인과 화면 접근 방향이 대응한다. “1-2초간” 전경 유지의 정확한 길이는 미계측이고, “자재를 들고 이동하는 크레인”의 독립 이동은 선택 표본에서 확인하지 못했다. 분석창은 8초에서 끝나므로 문서 10초까지의 수행 여부를 판단하지 않았다.'),dict(locators=['slide[2]/p[1]','slide[2]/p[8]'],quote='1. 크레인 작업 반경, 물류·인양 안정성 검토',evidence_ids=['f6'],finding='영상 제목은 문서의 주제와 대응하지만 쉼표/가운뎃점 대신 “및”, “물류인양” 표기를 사용한다. 화면 대사 문장은 이 구간에 본문 자막으로 보이지 않으며 오디오 대응은 미검수이다.')]
d['coverage']=dict(overview='0~8초 전경·제목 생성·접근 화면을 검사했다. 8초 경계는 문맥 프레임이다.',secondary_details='제목의 면, 문구, 얇은 외곽선, 보조 문구를 별개로 추적했고 크레인 와이어/후크/수면도 대조했다.',internal_content='실제 소프트웨어 UI는 이 창에 보이지 않는다. 3D 장면 내부 수면 변화와 장비 배치를 검사했다.',unresolved=['독립적인 크레인 주행/인양 동작, 접근의 정확한 속도곡선은 미확정.','문서가 제작 전 의도인지 사후 수정 콘티인지 텍스트 추출만으로 확정하지 못함. 원본 PPT 레이아웃·그림은 미열람.'])
save(d)

d=base('V02');frames(d,'A4-D','V02',[0,3,6,10,14,19],'f')
for label,inds,prefix in [('radius',[0,1,2,3],'r'),('row',[5,6,7],'w'),('load',[8,9,10,11,12,13,14],'l')]:crops(d,['V02_'+label+'_'+str(i) for i in inds],prefix)
d['files_read'] += [str(R/x) for x in ['documents/DOC063.txt','documents/DOC063.json','with_a_catalog_D.json','cases/A4-D/V02/board-1.jpg','cases/A4-D/V02/board-2.jpg']]
obj(d,'layout','크레인과 제조사 표의 좌우 대응',[
 event('좌측에는 작업대 위 크레인과 붐 끝에서 내려오는 와이어/장비, 우측에는 “크롤라크레인 제조사 정격하중표”가 배치된다. 좌상 제목/대호지교 가교는 유지된다. 표는 Boom length, Working radius, Rated load의 JIS/BS/PCSA 열로 구성되어 있다.',['layout'],[130,138],['f0','f6','f14','f19'],'3D 모델 왼쪽, 수치 근거 표 오른쪽',kind='not_applicable',basis='배치/정보관계 기술. 모델의 독립 이동을 관측한 것이 아님.')])
obj(d,'column','붐길이 열 강조',[
 event('130초에는 Boom length 열 전체를 청록·파랑 윤곽이 감싸고 45.0 (147′8″)가 밝게 강조된다. 131.2초에는 윤곽이 사라지고 일반 표 셀 상태로 돌아간다.',['visibility','color'],[130,131.2],['f0','f3'],'붐길이 열 강조 종료 → 첫 반경 행 강조',basis='강조 소실의 중간 속도 표본 부족.')])
obj(d,'radius','작업 반경 도형·문구',[
 event('크레인 밑에 반투명 청록 타원이 생겨 좌우로 커진다. 130.4초 작은 타원, 130.8초 큰 타원, 131.2초 거의 정착 크기로 보인다. 초록 화살표가 중심에서 화면 좌하 쪽으로 뻗으며 131.2초부터 아래에 “작업 반경 R=9.7m” 글자가 흐리게 만들어지고 132.4초 선명하다.',['scale','reveal','position'],[130,132.4],['r0','r1','r2','r3','f6'],'타원 확장/방향 화살표 → 반경 라벨',kind='decelerate',basis='타원 우측 가시 경계의 확장량은 같은 0.4초 간격 130.4→130.8에서 크고 130.8→131.2에서 작다. 타원 크기의 시각적 감속 판정이며 텍스트나 다른 도형의 곡선에 적용하지 않음.',lim=['크레인에 가려진 타원 중심·좌측 전체 경계는 미측정. 픽셀 오차 미상.'])])
obj(d,'crane_label','크롤라크레인 라벨·점선 보조선',[
 event('131.2초 붐 근처 주황 글자가 일부 나타나고 132.4초 “크롤라크레인” 라벨과 아래쪽 작은 꺾인 표지가 보인다. 이때 붐 방향을 연장한 옅은 청록 점선과 수직 와이어 부근 보조선도 보인다.',['reveal'],[131.2,132.4],['f3','f6'],'라벨 부분 노출 → 선명한 라벨/점선',basis='점선의 정확한 그리기 순서는 1.2초 간격 두 표본으로 확정하지 않음.')])
obj(d,'row','9.7m 행의 확대 강조',[
 event('9.7 / 31′10″ / 69,000 / 64,400 / 142,000 / 69,900 / 152,100 첫 행이 분홍 바탕·파란 글씨로 강조된다. 132초 내부에 작은 둥근 테두리가 생기고 132.4초 기존 글자와 확대 글자가 겹쳐 보인다. 132.8초 확대 행은 좌우로 넓어져 원래 표 밖까지 약간 돌출되고 이후 유지된다.',['scale','internal_content'],[130,134],['f0','f3','w5','w6','w7','f10'],'첫 행 색 강조 → 복제/겹침처럼 보이는 확대 → 독립 띠 형태 정착',kind='decelerate',basis='132/132.4/132.8의 같은 간격에서 둥근 행 윤곽 폭 증가가 뒤 구간에 줄어드는 시각적 경향. 실제 복제 레이어 사용 여부는 미상.',lim=['중첩 글자를 하나의 글자 연속 이동으로 단정하지 않았다. 정확한 폭/오차 수치는 미계측.'])])
obj(d,'load_label','정격하중 화살표·카드·숫자',[
 event('133.2초 “정격…” 글자와 얇은 수평선이 나타나고 133.6초 파란 상향 화살표와 “정격하중”이 보인다. 134초까지 화살표/카드가 커져 정착한다. 134.8초 카드 안에 흐린 숫자 6이 먼저 보이고 135.2초 69와 t, 135.6초 69 ton이 읽힌다.',['reveal','scale','visibility'],[133.2,135.6],['l8','l9','l10','l11','l12','l13','l14'],'제목/선 → 위쪽 화살표·카드 → 숫자 69 → ton',basis='화살표 크기는 133.6→134에서 커지고 134→134.4 거의 유지되어 감속 정착과 양립한다. 글자 리빌/숫자 선명화는 별도 변화이며 정확한 가감속은 미계측. 숫자는 카운트업으로 단정하지 않음.')])
obj(d,'load_highlight','JIS 값·와이어/인양장비 강조',[
 event('134초에는 JIS rating 제목이 밝고 수직 와이어·아래 장비 윤곽에 파란 강조가 더해진다. 135.6초에는 첫 행 JIS 69,000 셀이 짙은 파란 바탕·흰 글자로 강조된다. 137.6초에도 카드 69 ton과 셀 69,000이 함께 유지된다.',['color','luminance','internal_content'],[132.4,137.6],['f6','f10','f14','f19'],'행 강조 뒤 JIS/장비 강조 → 69,000 셀과 69 ton 카드 연결',basis='색/광량 변화의 세부 시작과 세기 곡선은 미측정. 빛 강조를 실제 장비 이동으로 기록하지 않음.')])
obj(d,'water','배경 수면',[
 event('크레인과 표 외곽은 대체로 같은 배치인데 바다 표면의 물결 무늬는 표본 사이에 변한다. 화면을 완전 정지 화면으로 취급하지 않았다.',['internal_content'],[130,138],['f0','f6','f14','f19'],basis='비강체 물결 패턴의 단일 이동 방향/가감속은 미상.')])
d['document_comparison']=[dict(document_id='DOC063',document_sha256='879959f784ee8fa6cca088056305249aaef8fa6a9a4e58bf365a52fd20818c36',locators=['slide[9]/p[14]','slide[9]/p[15]','slide[9]/p[16]','slide[9]/p[17]'],quote='크레인 도해에는 작업반경 R=9.7m, 정격하중 69.0Ton 문구를 표시한다.',evidence_ids=['f6','f14','f19'],finding='내용은 slide[9]의 좌측 크레인/우측 제조사 표, R=9.7m, JIS 69,000kg 및 69.0Ton과 대응한다. 실제 카드에는 “69 ton”으로 표시되어 소수 .0이 생략된다. 문서 타임코드는 01:25~01:40(85~100초)인데 실제 지정창은 130~138초이다. 내용 대응과 시간 대응을 분리해야 한다.'),dict(locators=['slide[12]/p[7]','slide[12]/p[8]','slide[12]/p[13]'],quote='평면도에 크레인 위치를 중심으로 작업반경 R=24m 원을 표시한다.',evidence_ids=['f0','f6','f19'],finding='실제 02:10~02:18은 문서 같은 시간대 slide[12]의 평면 배치/R=24m 화면과 다르다. 현재 창은 사선 3D 크레인과 제조사 표의 R=9.7m 조건이다. 문서의 실제 안전성 판단과 대사는 영상 시각만으로 검증하지 않았다.')]
d['coverage']=dict(overview='130~138초에서 표의 수치 관계와 반경/하중 그래픽의 중첩 순서를 검사했다.',secondary_details='타원, 초록 화살표, 주황 장비 라벨, 청록 점선, 파란 와이어/장비 강조, 카드의 얇은 상하 선을 별도로 확인했다.',internal_content='우측은 소프트웨어 인터랙션이 아닌 정격하중표 시각물이다. 열→첫 행→확대 행→JIS 셀 강조 상태 변화를 추적했다.',unresolved=['정확한 원형/화살표 시작 프레임 및 빛 강조의 속도곡선은 미확정.','문서 버전의 실제 제작 순서·시간표 차이 원인은 미상. 문서 레이아웃/삽입 이미지는 미열람.'])
save(d)

d=base('V05');frames(d,'A4-G','V05',[0,2,4,6,8,10,12,14,16,18,20,22,28],'f');frames(d,'A4-G','V05_with_more',[7,8],'x')
crops(d,['V05_title_'+str(i) for i in range(6)],'t');crops(d,['V05_panels_'+str(i) for i in range(9,22)],'p')
d['files_read'] += [str(R/x) for x in ['with_a_catalog_more.json','with_a_catalog_G_extra.json','cases/A4-G/V05/board-1.jpg','cases/A4-G/V05/board-2.jpg','cases/A4-G/V05/board-3.jpg']]
d['limitations']+=['원본 SAR 미상. 관측 방향/크기는 native raster 기준이며 디스플레이 실치수/비율로 확정하지 않는다.','마지막 열람 프레임은 10.933333초(164/15)로 창 끝 10.9666666667초보다 이르다. 이 창에 context_after 프레임은 확보하지 않았다.']
obj(d,'background','어두운 업무 책상·듀얼 모니터 배경',[
 event('야경을 배경으로 책상, 키보드, 마우스, 좌우 대형 모니터와 아래 보조 기기가 배치된다. 시작에는 어둡고 크게 보이는 배경이 0.8~1.6초 쪽으로 작아지고 밝아져 자리잡는다. 좌 모니터는 CAD 도면, 우 모니터는 목록과 도면 썸네일이다. 이후에는 배경 구도가 대체로 유지된다.',['apparent_scale','luminance'],[0,3.2],['f0','f2','f4','f6','f8'],'초기 어두운 확대 상태 → 밝아지며 약간 줌아웃',basis='0/0.8/1.6초 모니터 모서리 변화를 비교했으나 크기와 밝기 각각의 곡선은 미계측.')])
obj(d,'korean','한글 제목 “인터페이스”',[
 event('0.2초부터 일부 글자 조각이 보이고 0.6/0.8/1초에는 글자별 선명도가 서로 다르다. 글자 사이 간격이 줄어드는 방향으로 모여 1.4초에 “인터페이스” 한 줄로 읽힌다. 완성 제목은 우측 중앙에 흰색으로 유지된다.',['position','visibility'],[0,1.6],['f0','t0','t1','f2','t2','t3','f4'],'흩어진/부분적인 글자 → 좁아진 자간의 완성 제목',basis='글자별 등장 순서가 단순 좌→우가 아니고 크기/선명화가 겹친다. 각 글자의 동일 특징을 충분히 추적하지 않아 이징 미확정.',lim=['0.2초 ROI는 첫 글자 일부가 왼쪽으로 잘려 있어 최초 전체 자형을 판독하지 않음.'])])
obj(d,'english','Interface 영문·녹색 사각형·점선',[
 event('한글 제목 위에 짙은 녹색 작은 사각형과 영문 일부가 1.4초 보인다. 1.6초 “Interfa…”가 잘려 보이고 1.8~2.4초 오른쪽으로 넓어진 사각형 안에 “Interface”가 드러난다. 흰 점선 외곽과 우측 끝의 빨강/초록 교차선도 함께 진행한다. 이후 3.2초에는 녹색 면/점선이 사라지고 영문은 투명한 회색 큰 글자로 남는다.',['reveal','visibility'],[1.4,3.2],['t3','f4','t4','f6','t5','f8'],'작은 프레임 → 우측으로 리빌 확장 → 배경 면/점선 퇴장·영문 흐림',basis='면의 폭·높이가 변하고 글자가 잘려 드러나는 관측이며 영문 전체 확대만으로 설명하지 않았다. 1.4/1.6/1.8/2.4 폭 변화는 감속 가능성이 있으나 리빌 경계와 프레임 변환이 섞여 정확한 곡선은 미확정.')])
obj(d,'body','인터페이스 설명 본문',[
 event('3.2초 한글 제목 아래 세 줄 본문이 나타나며 마지막 줄은 아직 흐리다. 4초에는 “사용자 경험을 바탕으로 사용자의 편의성을 최우선적으로 고려하여 / 기존의 복잡한 인터페이스에서 벗어나 메뉴를 단순화하고, / 듀얼모니터기능을 활용한 새로운 작업공간을 제공합니다.”가 읽힌다. 메뉴 단순화·듀얼모니터·새로운 작업공간 구절이 굵게 강조된다.',['visibility','reveal'],[2.4,4],['f6','f8','f10'],'상단 줄 → 하단 줄까지 선명화',basis='본문 각 줄의 불투명도/위치 변화를 촘촘히 추적하지 않아 곡선 미상.')])
obj(d,'g','대형 녹색 G',[
 event('4초에 가는 원호/점선이 넓은 좌측 영역에 보이고 4.4초부터 큰 G 면이 반투명하게 나타난다. 4.8/5.2초 더 진해지고 5.6초 왼쪽 대부분을 차지하는 G와 가는 밝은 외곽이 분명해진다. G 면은 이후 패널의 뒤쪽에 남는다.',['visibility','luminance'],[3.2,5.6],['f8','f10','x7','f12','x8','f14'],'선/원호 → G 면의 가시성 증가 → 외곽 강조',basis='4.4/4.8/5.2초 같은 형상에서 면 농도가 증가하는 것이 보이나 광량 측정이 없어 선형/가감속은 미확정. 커지는 물체 이동으로 단정하지 않음.')])
obj(d,'guides','G 주변 원호·점선·좌표 표식',[
 event('G 주변에 흰 실선/점선 원호와 직선이 겹쳐 나타나고 일부가 사라진다. 5.6초 위쪽에 빨간 원형 십자 표식, 6.4초에는 위쪽 표식에서 왼쪽을 따라 오는 노란 점선과 아래로 이어진 흰 원호 및 빨강/초록 십자 표식이 보인다. 아래 표식은 6.4→7.2→8→8.8초 오른쪽·아래로 이동하며 원호 끝이 따라가고 이후 거의 정착한다.',['position','reveal'],[4,9.6],['f10','x7','f12','x8','f14','f16','f18','f20','f22','p21'],'다수 원호 등장/정리 → 상단 표식·점선 → 아래 원호 끝 표식 우하 이동',kind='decelerate',basis='6.4/7.2/8/8.8초의 같은 0.8초 간격에서 아래 빨강/초록 교차점 이동이 크게 줄어든다. 화면 전체에서 교차점을 독립 추적한 시각적 감속이며 패널의 속도 근거와 분리했다.',lim=['원호와 점선 전체의 생성 방향·길이 곡선은 미계측. G의 형태를 실제 CAD 편집 도구로 조작했다고 추정하지 않음.'])])
obj(d,'panel1','첫 CAD 패널 외곽',[
 event('5.8초에는 패널이 이 ROI에 없고 6초 작고 흐린 노란 테두리 CAD 패널이 좌상 영역에 나타난다. 6.2~6.4초 빠르게 커진 뒤 크기 변화가 작아진다. 이후 프레임은 우하로 이동해 7.2~7.4초 정착한다. 7.4초 뒤쪽 두 번째 패널의 테두리가 오른쪽에서 나타나도 첫 패널의 지속적으로 보이는 모서리와 제목줄은 유지된다.',['scale','position'],[5.8,7.6],['p9','p10','p11','f16','p12','p13','p14','f18','p15','p16'],'작은 패널 → 확대 → 우하 이동·정착 → 뒤 패널의 우측 노출',kind='decelerate',basis='scale은 6.0→6.2 증가가 크고 6.2→6.4 증가가 작으며 이후 거의 일정. 위치는 6.6/6.8/7.0/7.2의 동일 간격에서 같은 외곽 모서리의 우하 변위가 줄어듦. 픽셀 자동 측정은 하지 않았고 시각적 오차는 미상.')])
obj(d,'glint','첫 패널의 노란 빛',[
 event('작은 패널의 상단에 노란 발광이 생기고 6.2초 패널 위쪽 왼편으로, 6.4~6.8초 좌상 모서리 부근으로 모인다. 7.4초 이후 같은 모서리에 밝은 별 모양 빛과 상단 테두리 빛이 남아 있다.',['position','luminance'],[6,9.6],['p10','p11','f16','p12','p13','p15','p21'],'상단 부근 → 좌상 모서리 부근 → 유지',basis='프레임 자체도 이동/확대하므로 프레임 기준 발광 위치와 밝기 변화를 분리해 관찰했다. 중심 추적 및 광량 곡선은 미상.')],parent='panel1')
obj(d,'panel1text','첫 패널의 노란 라벨·본문',[
 event('6.8초 “단순한 메뉴…”가 노란 띠 위에서 왼쪽부터 드러나며 7.4초 “단순한 메뉴구성 / 넓은 작업공간”이 완성된다. 그 아래 첫 줄, 이어 두 번째 줄이 보이며 7.6초에는 “꼭 필요한 기능으로만 단순화한 메뉴구성 / 메뉴의 효율적인 공간배치로 넓은 작업공간 확보” 두 줄이 읽힌다.',['reveal'],[6.8,7.6],['p13','p14','f18','p15','p16'],'왼쪽부터 노란 제목 리빌 → 아래 본문 첫 줄 → 둘째 줄',basis='리빌 중간 표본에서 단어가 오른쪽 경계에서 잘려 보임. 같은 글자 이동 속도는 측정하지 않음.')],parent='panel1')
obj(d,'panel2','두 번째 CAD 패널 외곽·내부 UI',[
 event('7.4초 첫 패널 뒤에 노란 테두리가 겹쳐 보이고 7.6/7.8초 우측으로 빠져나오면서 넓은 빈 검정 내부가 보인다. 8~8.4초 외곽은 오른쪽으로 이동해 첫 패널 옆에 정렬되고 감속 정착한다. 앞의 첫 패널이 좁아진 것으로 해석하지 않았다.',['position','visibility'],[7.4,8.6],['p15','p16','p17','f20','p18','p19','p20'],'뒤쪽 겹침 → 오른쪽 이동·가림 해소 → 좌우 두 패널 정착',kind='decelerate',basis='8.0/8.2/8.4초 우측 외곽 모서리의 같은 0.2초 간격 변위가 줄고 8.6초 거의 같음. 초기 7.4~7.8초는 속도가 커지는 경향이 있지만 가림 때문에 전체 in_out을 확정하지 않음.'),
 event('외곽 노출과 별도로 두 번째 패널 내부는 처음 빈 검정이 넓고 7.8초 왼쪽에서 도면 일부가 들어온다. 8초에는 도면이 더 넓어지고 8.2초 흰 속성 패널 일부가, 8.4초 전체가 보인다. 흰 패널에는 레이어·색상·선 관련 설정과 원형 도형/수치가 보이며 8.6/9.6/10.933초 대체로 유지된다. 커서 이동이나 실제 클릭은 관측되지 않았다.',['internal_content','reveal'],[7.6,10.933333333333334],['p16','p17','f20','p18','p19','p20','p21','f28'],'검정 여백 → 도면 리빌 → 흰 속성 UI 리빌 → 유지',basis='내용이 프레임 안에서 좌→우로 드러나는 변화는 확인. 녹화 UI 조작인지 별도 이미지/마스크 연출인지 렌더만으로 확정 불가; 리빌 가감속은 미계측.',lim=['속성 UI의 모든 작은 수치를 전사하지 않았으며 작업 기능이 실제 실행되었다고 주장하지 않음.'])])
obj(d,'panel2text','두 번째 패널의 노란 라벨·본문',[
 event('7.6초 우측 아래에 짧은 노란 세로 막대가 보이고 7.8초 “모니터” 일부, 8초 “듀얼모니터”가 읽힌다. 라벨은 오른쪽 끝을 기준으로 왼쪽으로 드러나는 방향이다. 8.2초 아래 첫 줄, 8.4~8.6초 둘째 줄이 나타나 “듀얼모니터의 화면 분리 및 연동기능으로 / 더욱 넓어진 작업공간 제공”이 완성된다.',['reveal'],[7.6,8.6],['p16','p17','f20','p18','p19','p20'],'우측 노란 막대 → 우→좌 제목 리빌 → 아래 두 줄 설명',basis='라벨의 드러나는 방향을 글자 잘림으로 확인했으며 이동/가감속은 미계측.')],parent='panel2')
obj(d,'internal_hold','정착 후 화면 속 UI·정보 관계',[
 event('두 패널은 왼쪽 단순한 메뉴/넓은 공간, 오른쪽 화면 분리·연동이라는 설명을 한글 제목 “인터페이스”의 사례로 보여준다. 8.8/9.6/10.933초 전경 패널의 도면 구성과 흰 속성 UI는 대체로 유지되며 뒤쪽 물리 모니터의 도면/썸네일도 유지되어 보인다. 외곽 정착만으로 내부 정지를 가정하지 않고 세 시점을 대조했다.',['internal_content'],[8.8,10.933333333333334],['f22','p21','f28'],'두 기능 예시와 우측 총괄 설명 동시 유지',kind='not_applicable',basis='선택 표본 사이 UI 상태 유지 관측. 전 프레임 불변 또는 실제 연동 기능 검증을 의미하지 않는다.')])
d['coverage']=dict(overview='0~10.9666666667초 범위의 시작·리빌·중첩·정착 상태를 검사했다. 마지막 실제 열람은 10.933333초이다.',secondary_details='영문 점선 테두리, 빨강/초록 십자, G 실선/점선 원호, 노란 발광과 패널 외곽, 양쪽 라벨의 반대 리빌 방향을 별도로 확인했다.',internal_content='배경 모니터와 전경 패널을 구분해 검사. 두 번째 패널의 빈 내부→도면→흰 속성 UI를 외곽 이동과 분리했으며 정착 뒤 3시점도 비교했다.',unresolved=['글자별 정확한 가감속, G 광량·테두리 생성의 세부 곡선, UI가 실제 실행 녹화인지 정적 자료 연출인지는 미확정.','배경 UI의 모든 작은 텍스트와 내부 CAD 수치의 완전한 전사는 하지 않음.','SAR 미상으로 실제 디스플레이 비율을 확정하지 않음.'])
save(d)
