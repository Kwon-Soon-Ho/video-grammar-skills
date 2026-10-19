from pathlib import Path
from xml.sax.saxutils import escape
from hashlib import sha256
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium

HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_analyzer_draft4_milestone.pdf'
FONT='C:/Windows/Fonts/'
pdfmetrics.registerFont(TTFont('Malgun',FONT+'malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold',FONT+'malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#18273A');BLUE=colors.HexColor('#245ABA');MUTED=colors.HexColor('#56677D');LINE=colors.HexColor('#D5DFEB')
styles={
 'title':ParagraphStyle('title',fontName='MalgunBold',fontSize=24,leading=34,textColor=INK,spaceAfter=15,wordWrap='CJK'),
 'h':ParagraphStyle('h',fontName='MalgunBold',fontSize=13,leading=20,textColor=INK,spaceBefore=12,spaceAfter=7,wordWrap='CJK'),
 'p':ParagraphStyle('p',fontName='Malgun',fontSize=10,leading=17,textColor=INK,spaceAfter=8,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='Malgun',fontSize=8.2,leading=13,textColor=MUTED,spaceAfter=6,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='Malgun',fontSize=9,leading=15,textColor=INK,wordWrap='CJK'),
 'th':ParagraphStyle('th',fontName='MalgunBold',fontSize=9,leading=15,textColor=colors.white,wordWrap='CJK')}
story=[]
def p(text,style='p'):story.append(Paragraph(escape(text),styles[style]))
def heading(number,title):p(f'{number:02d}  {title}','title')
def table(headers,rows,widths):
    data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,8)])
def chrome(c,doc):
    c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0)
    c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'PROJECT MILESTONE / ANALYZER REVISION');c.drawRightString(547,810,'2026.10.19')
    c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'draft.4 개발 후보 · 사용자 선택 반영 · 실제 성능 합격과 구분');c.drawRightString(547,27,str(doc.page))

heading(1,'조사에서 스킬 수정으로')
p('분석 스킬 수정 후보와 검증 범위','h')
p('전문가 판단·역설계 조사에서 유용한 구조를 골라 회사 영상 분석 스킬의 새 후보를 작성했다. 이번 분기점은 “규칙을 더 읽히기”에서 “무엇을 봤고 무엇이 빠졌는지 확인할 수 있는 기록”으로 바꾸는 것이다.')
p('사용자가 정한 두 가지','h')
table(['선택','이번 작업에 반영한 내용'],[
 ['수정 범위 ①','분석 정확도·근거 기록을 먼저 보완하고 다음 전문가 판단·재제작에 넘길 형식까지 연결한다.'],
 ['기록 밀도 ① + 보완','레이아웃의 전체 디자인을 기록한다. 모션은 전체 흐름과 세부 동작을 나눈다. 첫 패턴은 상세 분석하고, 반복은 카테고리·번호로 인용한다.']],[112,387])
p('큰 작업 묶음','h')
table(['단계','이번에 만든 것'],[['분해와 근거','대상 식별, 속성별 관찰 행, 원자 주장, 실제 프레임·시각 연결 검사'],['판단과 재사용','전체 디자인·흐름/세부 기록, 패턴 번호·고정 스냅샷, 조건·반례·구현 제안 인계'],['검증과 정착','합성 오류 검사, 기존 H02 개발 기록, 수정 후보 보존, 제출 보고서']],[112,387])
p('현재 상태: 0.1.0-draft.4 개발 후보. 기존 draft.3과 A5b 중단·실패 기록은 보존했다. 이번 사용자 선택은 수정 방향에 대한 결정이며 내용 정확도·회사 공통 문법의 승인이 아니다.','small')

story.append(PageBreak());heading(2,'무엇을 어떻게 기록하나')
p('전체를 남기고, 반복 설명을 줄인다','h')
p('레이아웃의 전체 구도·그룹·위계·정렬·여백·타이포·색·배경·형태를 기록한다. 모션은 화면의 순서와 중첩을 설명하는 전체 흐름, 텍스트·카드·선·내부 상태·가감속 같은 세부 동작을 함께 기록한다. 작다는 이유만으로 생략하지 않는다.')
p('정확한 수치의 깊이는 목적에 따라 조절한다. 처음에는 관계·비율·형태를 기록하고 재사용에 필요한 값만 측정한다. 제작 의도가 확인되지 않으면 해석으로 표시한다. “정밀 수치를 줄인다”는 말이 “전체 디자인을 생략한다”는 뜻은 아니다.')
table(['기존 약점','새 후보의 기록 방식'],[['A를 4로 식별해도 형식 통과','보이는 형태와 식별 이름을 분리하고, 식별 주장·근거·내용 검수 상태를 연결'],['위치만 보고 크기 감속 누락','대상별 요구 속성과 시간 구간을 정하고, 속성마다 주장과 미해결을 연결'],['장황한 문장을 다시 전수 검수','중복을 줄인 주장 ID를 정본으로 두고 사람이 읽을 요약을 생성'],['반복 장면을 매번 처음부터 설명','첫 상세 패턴에 카테고리와 번호를 주고 현재 장면의 근거·차이만 연결']],[153,346])
p('카테고리와 번호','h')
p('TEXT: 텍스트 등장 / CARD: 카드·UI 등장 / TRANSITION: 전환 / FLOW: 전체 흐름 / DETAIL: 세부 효과 / LAYOUT: 레이아웃. 예: PAT-CARD-0001. 실제 사례가 생길 때만 등록하고 패턴은 초안 상태로 쌓는다.')
p('이후 장면에서는 같은 패턴인지 현재 프레임으로 대조한다. 문구·요소 수·화면비·타이밍·순서·가감속·내부 동작이 다르면 차이와 미검증 부분을 남긴다. 번호만 붙여 내용 확인을 생략하지 않는다. 고정 스냅샷과 해시로 어느 상세 기록을 썼는지 남긴다.','small')

story.append(PageBreak());heading(3,'실제 자료로 만든 첫 기록')
image_path=WORK/'phase01a-a5b/cases/A5-A/H02/f_00864_014.400.png'
story.append(Image(str(image_path),width=499,height=280.69));story.append(Spacer(1,6))
p('기존 H02 12~20초 중 14.4초 원본 프레임. 이미 답안·실패가 알려진 개발 자료다. 새 독립 시험이나 사용자의 내용 확인이 아니다.','small')
p('대상 11개 · 주장 30개 · 열린 쟁점 4개','h')
p('열차 배경, 대형 A, 영문, 주제 제목과 설명, 궤적·노드, 주요 지도 UI, 기존 작은 UI, 노란 테두리, 기능 표제와 본문을 목록화했다. 전체 디자인을 정성 기록하고 모션을 흐름·세부로 연결했다.')
table(['기록','예시'],[['전체 흐름','기존 예시 축소 → 새 지도창 이동·확대 → 테두리·표제·설명 → 유지 → 축소 퇴장'],['세부 동작','지도 UI 크기 감속, 노란 선의 전개 순서, 내부 표, 문구·노드 변화'],['첫 패턴','PAT-CARD-0001: 이동·확대 UI 기능 예시와 노란 강조. 원본 관측·조건·미해결에 연결된 초안']],[100,399])
p('남은 쟁점: 정확한 확대율·시간 경계, 겹친 작은 UI 각각의 정체, 노드·배경의 세부 변화, 문구별 경계·정확한 글꼴과 색 값. 전체 디자인 서술의 원자화와 고유 주장 분모 전수 확정도 완료하지 않았다.','small')

story.append(PageBreak());heading(4,'확인한 것과 다음 판단')
table(['확인 항목','결과와 의미'],[['스킬 형식','기본 검증기 통과. 이름·설명·참조 구조 확인이며 내용 성능 검증은 아님.'],['합성 오류 검사','38/38 통과. 빠진 속성, 구간 공백, 잘못된 참조·원본·시각, 거짓 검수 완료, 불완전 패턴 확정을 거부.'],['등록과 반복 사용','카테고리 번호 배정·이전 항목 보존·고정 스냅샷·현재 주장 연결을 시험. 합성 반복 시험이며 실제 반복 장면 효과는 미검증.'],['기존 실제 자료','H02의 새 기록과 근거 연결을 확인. 이미 노출된 자료를 본 AI 수동 개발 사례.'],['과거 자료 보존','C: 동결판·결과·중단 기록과 D: 기존 스킬의 17파일 해시 일치.'],['아직 미입증','새 자료 분석 정확도, 반복 일치, 전체 누락률, 사용/미사용 비교, 사람 공수 절감, 실제 제작 성공.']],[112,387])
p('검사기가 보장하지 않는 것','h')
p('실제 A를 “4”라고 적고 supported 표시까지 잘못 붙이면 구조 검사만으로는 거부할 수 없다. 이 반례도 확인했다. 해시·필수 칸·세 시각 조건은 연결을 검사할 뿐, 글자·개수·진행 중 감속의 정답은 원본 내용 대조가 필요하다.')
p('다음 판단','h')
p('먼저 이 실제 기록에서 전체 디자인의 범위와 흐름/세부 구분이 맞는지 확인할 수 있다. 이후 텍스트·카드·전환의 실제 반복 사례와, 새로 노출 범위를 고정한 자료에서 수정 후보를 비교해야 한다. 어떤 경로를 먼저 할지는 추천안을 포함한 사지선다로 결정한다.')
p('변경 근거: 2026-10-19 전문가 판단·역설계 조사와 고정 원본 근거표, 이 채팅의 사용자 선택 두 건. REA의 근거·미해결 구조, Superpowers의 실패별 기록, Trail of Bits의 가정 추적, Ponytail의 조건부 재사용을 자체 구현에 반영했다. 세부 출처는 기존 조사 보고서와 이번 작업의 adoption-map.md에 연결했다.','small')

OUT.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='전문가 판단·역설계 반영: 분석 스킬 수정 후보와 검증 범위',author='Company video skill project')
doc.build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==4,len(reader.pages)
pdf=pdfium.PdfDocument(str(OUT));renders=WORK/'tmp/pdfs/analyzer-draft4';renders.mkdir(parents=True,exist_ok=True)
for index,page in enumerate(pdf):page.render(scale=1.4).to_pil().save(renders/f'page-{index+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'rendered_pages':len(pdf),'sha256':sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>200 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
