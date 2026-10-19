from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
import json,hashlib
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_internal_video_scope_and_motion_correction.pdf'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'));pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#182A40');BLUE=colors.HexColor('#255DB5');MUTED=colors.HexColor('#52677F');LINE=colors.HexColor('#D7E1ED')
styles={k:ParagraphStyle(k,fontName='MalgunBold' if k in ('title','h','th') else 'Malgun',fontSize=s,leading=l,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,spaceAfter=a,wordWrap='CJK') for k,s,l,a in [('title',21,29,12),('h',12,19,7),('p',10,17,8),('small',8.4,13.5,6),('cell',9,15,0),('th',9,15,0)]}
story=[]
def p(t,style='p'):story.append(Paragraph(escape(t),styles[style]))
def table(headers,rows,widths):
    data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,8)])
def chrome(c,doc):
    c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0);c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'PROJECT MILESTONE / OBSERVATION AND SOURCE COVERAGE');c.drawRightString(547,810,'2026.10.19')
    c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'사내 영상 세부 검수 진행 중 · 전체 조사 스킬 반영 미완료');c.drawRightString(547,27,str(doc.page))

p('사내 영상의 남은 범위와 실제 오판 정정','title')
p('현재 큰 단계는 분석 정확도·근거 기록 보완이다. 사내 영상의 세부 검수를 먼저 충분히 하라는 사용자 결정에 따라, 패턴 검색 확대에 앞서 두 원본의 전체 구성을 훑고 기존 두 분석 창의 미해결을 다시 확인했다.')
table(['확인 범위','이번 결과'],[
 ['원본 전체 개요','노듈러거더 약 418.475초, PG 약 211.797초. 5초 간격과 끝부분 표본 총 129장을 실제 검토해 잠정 작업 묶음 18개 + 11개로 정리. 정확 컷 경계·모든 짧은 장면 발견은 아님.'],
 ['상세 기록 창','노듈러 166~174초, PG 40~48초의 기존 기록을 보강. 창 길이 합집합 16초이며 모든 속성의 정밀 검수 완료 시간이 아님.'],
 ['실제 오판 정정','PG의 “지도 구도가 넓어지는 듯”이라는 기존 줌 추정을 기각. 원래 문장은 rejected로 보존하고 떨어진 지도 지형·기존 카드의 좌표 비교를 새 근거로 연결.'],
 ['추가 관찰','노듈러 먼 끝 화살표의 출현·강약·소실, 배경 ROI의 밝기 변화 보강. PG 연결선은 위쪽 화살 모양과 실제 이동을 분리하고 연속 10프레임 대조.'],
 ['스킬 수정','draft.7을 별도 ZIP으로 보존하고 draft.8 개발 작업본으로 보완. 공통 변환·반복 무늬 검증 지침과 원본 범위 집계 도구 추가. 전역 설치·완성판 선언 없음.']
],[104,395])
p('구조 검사와 영상 내용 검수는 다른 결과다','h')
p('새 범위·수정 추적 검사 23개와 기존 핵심 38개·패턴 조합 34개가 통과했다. JSON·출처·구간 집계에 대한 검사이며 영상의 오류율이나 누락 완전성을 측정한 점수가 아니다. 동일 AI의 후속 검수이고 사람 또는 독립 AI 합격이 아니다.','small')
p('제한 추출기의 PG 개요 읽기 실패는 이전 실패 기록을 보존한 뒤 새 보조 어댑터에서 제한된 짧은 읽기로 재시도해 30장 추출에 성공했다. 정본 전체 디코더를 수리했다는 뜻은 아니다.','small')

story.append(PageBreak());p('지도 기준점 비교로 줌 추정을 정정했다','title')
p('40초와 48초의 같은 원본 좌표에서 지속해서 보이는 지형과 기존 경찰청 카드를 비교했다. 아래는 확대·정합을 적용하지 않은 같은 영역의 크롭이다.','small')
old=WORK/'analysis-reliability-20261019/fresh/cases/NEW-P/window'
paths=[old/'f_01200_040.000.png',old/'f_01440_048.000.png']
rows=[[Paragraph(x,styles['th']) for x in ['기준점 / native 좌표','40초','48초']]]
for label,box in [('지도 남서',(1400,1440,1760,1680)),('지도 남동',(2840,1560,3240,1820)),('경찰청 카드',(440,848,928,1008))]:
    ims=[]
    for path in paths:
        with PILImage.open(path) as im:
            bio=BytesIO();im.crop(box).save(bio,format='PNG');bio.seek(0)
        w=168;h=w*(box[3]-box[1])/(box[2]-box[0]);ims.append(Image(bio,width=w,height=h))
    coord=f'{escape(label)}<br/>{box[0]},{box[1]}<br/>~ {box[2]},{box[3]}'
    rows.append([Paragraph(coord,styles['small'])]+ims)
t=Table(rows,colWidths=[139,180,180]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.4,LINE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t);story.append(Spacer(1,8))
p('두 지도 ROI와 카드는 같은 위치에서 일치한다. 가려진 북쪽 지형과 강조가 바뀐 정책 패널의 낮은 정합 후보는 기각했다. 정합은 4px 해상도의 보조이며 실제 AE 카메라·부모 리그를 복원하지 않았다.','small')
p('화살표의 모양과 움직임도 나눠 확인한다','h')
story.append(Image(str(HERE/'probes/P-line-framewise.jpg'),width=499,height=108.12));story.append(Spacer(1,5))
p('44.000~44.300초의 30fps 연속 10프레임. 위를 향한 무늬가 같은 자리로 보인다. 해당 정착 구간을 위로 흐르는 모션이라고 기록하지 않는다. 초기 생성·다른 시간의 이동 여부는 여전히 열린 항목이다.','small')

story.append(PageBreak());p('지금 어디이며 얼마나 남았는가','title')
table(['두 원본의 범위','현재 상태'],[
 ['전체 길이 합계','630.272초, 약 10분 30초'],
 ['잠정 작업 묶음','29개 중 2개 묶음에 일부 구간 기록. 나머지 27개에는 상세 구간 기록이 없음. 묶음은 검수 계획용이며 실제 컷 수가 아님.'],
 ['기록 창 밖','614.272초, 약 10분 14초. 전체 개요 표본으로 훑었지만 상세 기록을 만들지 않은 시간.'],
 ['현재 창 안','16초에도 미해결 항목 5개. 정밀 검수 완료로 처리하지 않음. 원본 전체의 발견하지 못한 항목은 이 숫자에 포함되지 않음.']
],[123,376])
p('바로 다음: 현재 창의 미해결부터 닫는다','h')
table(['대상','다음 확인'],[
 ['노듈러 3항목','① 배경의 연속 미세 변화와 하단 영역 ② 앞·먼 끝 화살표의 주기·가감속·동기화 ③ 174초 경계에서 등장 중인 왼쪽 설명의 완성 상태·리빌'],
 ['PG 2항목','④ 연결선 초기 생성~정착~퇴장과 다른 시각의 무늬 이동 ⑤ 행별 강조 주기와 지역 패널 강조의 동기화']
],[92,407])
p('전체 스킬 수정의 남은 큰 범주','h')
table(['범주','상태와 다음 결과물'],[
 ['1. 분석 신뢰성','진행 중. 현재 창 보완 후 원본의 미기록 묶음으로 확장해 실제 관측·근거·미해결을 축적.'],
 ['2. 패턴 검색·재사용','일부 구현. 상세 관측을 근거로 동작 구조의 동일성, 조건·변형·차이를 실제 사례에서 확인해야 함.'],
 ['3. 전문가 판단','연결 형식·문서 중심. 대안 생성→선택 이유→비평→재평가의 실제 작동과 사용자 선택 검증이 남음.'],
 ['4. 재제작 검증','편집 가능한 재제작, 렌더 비교, 문구·배치 변경 후 재사용 검증은 미구현.']
],[105,394])
p('소요 시간과 완료율은 산정하지 않았다. 조사 저장소 수나 테스트 통과 수를 전체 스킬 반영률로 쓰지 않는다. 29개 묶음별 시각·근거·다음 확인은 동봉한 “00_현재위치와_다음작업.md”와 source-coverage.json에 있다.','small')

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='사내 영상 전체 범위 정리와 지도·화살표 검수 정정',author='Company video skill project').build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==3,len(reader.pages)
pdf=pdfium.PdfDocument(str(OUT));renders=WORK/'tmp/pdfs/internal-video-audit';renders.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(pdf):page.render(scale=1.5).to_pil().save(renders/f'page-{i+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>300 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
