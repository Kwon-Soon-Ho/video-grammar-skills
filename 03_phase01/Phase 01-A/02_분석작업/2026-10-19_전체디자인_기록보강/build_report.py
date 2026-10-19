from pathlib import Path
from xml.sax.saxutils import escape
import json,hashlib
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PDF=ROOT/'output/pdf/20261019_design_density_draft9.pdf'
pdfmetrics.registerFont(TTFont('MG','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MGB','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('MG',normal='MG',bold='MGB')
INK=colors.HexColor('#1D3047');BLUE=colors.HexColor('#235CA8');MUTED=colors.HexColor('#52677D');LIGHT=colors.HexColor('#EAF0F7')
styles={k:ParagraphStyle(k,fontName='MGB' if k in ('title','h','th') else 'MG',fontSize=s,leading=l,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,wordWrap='CJK') for k,s,l in [('title',20,28),('h',12,19),('p',10,16),('small',8.5,13),('cell',9,14),('th',9,14)]}
c=canvas.Canvas(str(PDF),pagesize=(595.28,841.89));c.setTitle('전체 디자인 기록 보강과 분석 스킬 draft.9');y=0
def text(t,style='p',gap=9):
 global y
 q=Paragraph(escape(t),styles[style]);_,h=q.wrap(499,800);q.drawOn(c,48,y-h);y-=h+gap;assert y>=58,(t[:30],y)
def start(n,title):
 global y
 c.setFillColor(BLUE);c.rect(0,833,596,9,stroke=0,fill=1);c.setFillColor(MUTED);c.setFont('MG',8)
 c.drawString(48,810,'COMPANY VIDEO / DESIGN RECORD ENRICHMENT');c.drawRightString(547,810,'2026.10.19')
 c.setStrokeColor(LIGHT);c.line(48,42,547,42);c.drawString(48,27,'개발 관측 기록 · 패턴 분류 유지 · 원본 제작 설정 및 회사 승인 미확정');c.drawRightString(547,27,str(n))
 y=785;text(title,'title',12)
def image(p,w=499,h=None):
 global y
 size=PILImage.open(p).size;h=h or w*size[1]/size[0];c.drawImage(str(p),48,y-h,width=w,height=h);y-=h+8
def table(rows,widths=(128,371)):
 global y
 data=[[Paragraph(escape(str(v)),styles['cell']) for v in row] for row in rows]
 t=Table(data,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#CFDAE8')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));_,h=t.wrap(499,800);t.drawOn(c,48,y-h);y-=h+12;assert y>=58,y
inputs=json.loads((OUT/'inputs.json').read_text(encoding='utf-8'));frames={f['id']:f for f in inputs['evidence']}
start(1,'패턴 번호는 유지하고 디자인 기록을 보강했다')
text('사용자 선택 ①을 반영했다. 노듈러·PG 두 기준 사례의 영역 비율, 글자 크기 관계, 여백, 선틀·배경층을 보강하고 다음 분석에 적용할 스킬 지침을 draft.9 후보로 수정했다. 전체 스킬 제작 완료를 뜻하지 않는다.')
image(frames['N177']['path'])
text('노듈러 177초 / 원본 7680×2160, 32:9. 전체 모델 배치와 설명·자막을 함께 본 뒤 아래 수치를 기록했다.','small')
image(OUT/'inspection/N177-label_left.png')
table([
 ['글자 크기 관계','가시 글자 높이: 제목58px / 왼쪽 설명75px / 오른쪽76px / 자막92px. 제목 대비 약1:1.29:1.31:1.59. 폰트 크기 원값이 아니다.'],
 ['설명 띠와 여백','177초 두 띠 폭은 약1474/1473px로 유사. 왼쪽 문구 좌우 여백126/135px, 오른쪽240/244px. 문구 길이와 띠 폭을 구분했다.'],
 ['영역 비중','모델 투영 외접 폭: 왼쪽34.1%W / 오른쪽24.0%W, 사이 여백 약19.1%W. 불규칙 물체의 실제 점유 면적이 아니다.'],
 ['글자·배경층','설명 안의 굵은 문구/가는 문구, 점·망·곡선·발광점, 모델의 청록 강조와 바깥 녹색 화살표를 분리 기록했다.']])
text('수치 기준: 글자 높이는 원본 RGB의 밝고 중립적인 픽셀 외접 높이(임계값 오차 약±2px). 띠·모델 경계는 수동 추정(띠±3~4px, 모델±15~20px). 정밀도를 같은 수준으로 포장하지 않았다.','small')
c.showPage()
start(2,'PG: 프레임을 한 사각형으로 기록하지 않았다')
image(frames['P47']['path'],w=499)
text('PG 47초 / 원본3840×2160, 16:9. 지도·지역 강조·기관 묶음·자막의 겹침을 전체 구도로 기록했다.','small')
table([
 ['배치·정렬','두 패널의 바닥은y≈616px, 카드 윗선은y≈787px로 맞는다. 패널 상단은 경찰222px / 강원114px로 달라 같은 높이로 통일하지 않는다.'],
 ['폭과 간격','47초 경찰 패널/카드 폭≈1.35배, 강원≈1.23배. 패널-카드 간격≈171px(7.9%H). 강원 안쪽 판은 외곽보다 사방 약30px 안쪽.'],
 ['구조·재질 외관','외곽 가는 선+색 L자 모서리 / 안쪽 비치는 판+짧은 흰 표시 / 두 정책 띠+분리 꺾쇠·빛나는 윤곽 / 세로 무늬선+원형 접점 / 밝은 카드·로고.'],
 ['글자와 상태','경찰 선택 글자 높이34px. 강원은47초42/46px,53초36/36px. 강조 중 가시 크기·굵기가 달라지는 외관도 기록하고 원본 weight·font-size는 미상으로 둔다.']])
text('모든 좌표는 해당 시점 원본 화면의 보이는 경계다. 카드 로고를 일반 자막 폰트로 추정하거나, 지도 투과 외관을 원본 opacity 수치로 확정하지 않았다.','small')
c.showPage()
start(3,'디자인을 다시 보며 크기 변화 하나를 더 찾았다')
text('이전 기록은 강원 기관 묶음의 오른쪽 이동을 확인했다. 이번에는 패널·문구·카드 크기를 따로 대조해, 이동과 함께 정책 패널의 크기가 줄어드는 차이를 추가로 찾았다.')
for ident,box,x,label in [('P47',[1400,60,2440,1060],48,'47초 / 동일 배율 ROI'),('P53',[2640,60,3680,1060],303,'53초 / 동일 배율 ROI')]:
 im=PILImage.open(frames[ident]['path']).crop(box);p=OUT/'inspection'/f'{ident}-comparison-native.png';im.save(p)
 c.setFont('MGB',10);c.setFillColor(INK);c.drawString(x,y,label);c.drawImage(str(p),x,y-250,width=244,height=234.6)
y-=267
table([
 ['정책 패널 외곽','47초 약804×502px → 53초681×426px. 폭·높이 모두 약85%. 바닥y616 부근은 유사하다.'],
 ['기관 카드 외곽','약652×234px → 653×234px로 크기가 유사하다. 카드 중심은 오른쪽으로 약1241px(32.3%W) 옮겨간다.'],
 ['기록 보완','전체 묶음을 하나의 강체 이동/일괄 축소로 설명하면 부족하다. 기존 LAYOUT-0003 / FLOW-0003 / DETAIL-0006 번호에 현재 관측과 차이를 연결했다.'],
 ['새로 남긴 쟁점','정확한 축소 시작·중간 속도·정착과 제작 앵커는 아직 미확인. 두 시점 차이만으로 가감속 함수를 만들지 않았다.']])
text('이전 관측·패턴 정의는 고정 해시와 함께 보존했다. 새 기록 판본에 보강 주장과 열린 쟁점을 추가했으며, 이전 기록이 처음부터 이 변화를 포착한 것처럼 수정하지 않았다.','small')
c.showPage()
start(4,'이번 묶음의 반영 범위와 다음 판단')
table([
 ['스킬 변경','draft.8을 백업한 뒤 draft.9 개발 작업본으로 반영. 디자인 밀도 지침, 혼합 정밀도 보강 파일, 해시·좌표·비율 일관성 검사 추가. 기존 스키마0.4와 패턴 번호 유지.'],
 ['검증 결과','52개 구조·출처·수치 일관성·이전 판본 보존 검사 통과. 잘못된 좌표/비율/글자 높이/파일 해시/누락 차원/패턴 변경을 넣은 거부 검사 포함. 영상 정확도52회 평가라는 뜻이 아니다.'],
 ['보존','이전 공개415개 파일과 draft.8 원본17개 파일 보존 확인. 패턴 라이브러리18개와 사례 연결 번호 유지. 보강 수치는 새 판본과 별도 파일에 기록.'],
 ['분석 범위','상세 기록 창: 노듈러166~181초15초, PG40~53초13초, 총28초. 이번 작업은 창 안의 디자인 보강이며 새 연속 분석 시간을 늘린 것이 아니다. 창 밖602.272초(약10분2초)가 남음.'],
 ['남은 핵심','기존 노듈러 화살표 강도 곡선·원본 동기화 쟁점, 새 PG 패널 축소 타이밍/가감속. 원본 서체·효과 설정·다른 장면 적용·전문가 판단·편집 가능한 재제작 검증도 남음.']])
text('외부 스킬 전체 반영 상태는 바뀌지 않았다','h')
text('기존41개 정적 검토 항목의 상태(지침·형식10 / 코드 일부21 / 미구현4 / 직접 이식 제외·평가 참고6)는 이번 디자인 보강으로 전면 구현으로 승격하지 않았다. 저장소 전체 분해·원본 테스트 실행·전문가 판단 전체·재제작 성공은 아직 완료가 아니다.','small')
text('다음 묶음 선택안','h')
text('① 보강 기록을 사용자 검토 후 기준 확정(추천): 이 보고서1~3쪽에서 빠진 구성·관계와 기록 밀도를 확인한다. ② PG 축소 변화부터 보완:51~53초 패널·문구·카드를 분리 추적해 새 쟁점을 줄인다. ③ 다른 사내 장면2~3개로 적용성 검증: 한정된 두 사례 밖에서도 이 기록 기준이 작동하는지 본다. ④ 전문가 판단 설계 검토: 외부 스킬의 채택/보류·대안 비교·비평 기준을 큰 구조로 점검한다. 원본 전체 확장은 각 선택 뒤 별도 묶음이다.','small')
text('결과 위치: Phase 01-A/02_분석작업/2026-10-19_전체디자인_기록보강. 실제 작업본은03_분석스킬/company-video-grammar-analyzer. 지침 반영과 회사 승인·독립 평가를 구분한다.','small')
c.save()
reader=PdfReader(str(PDF));assert len(reader.pages)==4,len(reader.pages)
render=OUT/'pdf-preview';render.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(str(PDF))
for i in range(len(doc)):
 doc[i].render(scale=1.7).to_pil().save(render/f'page-{i+1}.png')
qa={'path':str(PDF),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'pages':len(reader.pages),'text_extracted':[len(p.extract_text()) for p in reader.pages],'visual_review':'pending'}
(OUT/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
