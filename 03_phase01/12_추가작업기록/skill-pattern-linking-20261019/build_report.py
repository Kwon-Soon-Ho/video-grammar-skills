from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_pattern_composition_decision.pdf'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#18273A');BLUE=colors.HexColor('#245ABA');MUTED=colors.HexColor('#56677D');LINE=colors.HexColor('#D5DFEB')
styles={k:ParagraphStyle(k,fontName='MalgunBold' if k in ('title','h','th') else 'Malgun',fontSize=size,leading=leading,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,spaceAfter=space,wordWrap='CJK') for k,size,leading,space in [('title',23,32,13),('h',12,19,7),('p',10,17,8),('small',8.3,13,6),('cell',9,15,0),('th',9,15,0)]}
story=[]
def p(text,style='p'):story.append(Paragraph(escape(text),styles[style]))
def table(headers,rows,widths):
    data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,9)])
class Composition(Flowable):
    def __init__(self):super().__init__();self.width=499;self.height=152
    def draw(self):
        c=self.canv
        def box(x,y,w,h,title,subtitle):
            c.setFillColor(colors.HexColor('#EDF3FC'));c.setStrokeColor(LINE);c.roundRect(x,y,w,h,6,fill=1,stroke=1)
            c.setFillColor(INK);c.setFont('MalgunBold',10);c.drawCentredString(x+w/2,y+h-18,title)
            c.setFont('Malgun',8.3);c.drawCentredString(x+w/2,y+12,subtitle)
        box(131,101,237,43,'전체 사례: 원본과 분석 기록 보존','새 번호들을 조합해 전체 화면과 흐름 조회')
        c.setStrokeColor(BLUE);c.setLineWidth(1)
        c.line(249.5,101,249.5,82);c.line(79,82,420,82)
        for x in (79,249.5,420):c.line(x,82,x,65)
        box(0,12,158,53,'LAYOUT','전체 디자인과 정보 관계')
        box(170.5,12,158,53,'FLOW','순서·유지·중첩')
        box(341,12,158,53,'CARD / DETAIL / TEXT','독립적으로 다시 쓸 동작')
        c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawCentredString(249.5,0,'각 정의는 최초 상세 관측·근거·미해결로 연결')
def chrome(c,doc):
    c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0)
    c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'PROJECT MILESTONE / PATTERN COMPOSITION');c.drawRightString(547,810,'2026.10.19')
    c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'사용자 분류 결정 반영 · draft.5 개발 후보 · 기존 기록 보존');c.drawRightString(547,27,str(doc.page))

p('전체 사례를 보존하고\n패턴을 나눠 연결한다'.replace('\n',' '),'title')
p('사용자가 선택한 ① “전체 사례 + 레이아웃·전체 흐름·독립 세부 번호 연결”을 스킬과 기록·조회 도구에 반영했다. 전체 장면을 찾는 기능과 필요한 동작만 꺼내 쓰는 기능을 함께 갖추는 방향이다.')
story.extend([Composition(),Spacer(1,14)])
p('기존 H02 사례에서 분리한 다섯 단위','h')
table(['번호','담는 내용'],[['PAT-LAYOUT-0001','상위 주제와 기능 UI의 전체 배치·위계·정렬·타이포·색·배경·형태'],['PAT-FLOW-0001','기존 예시 축소 → 새 UI 제시 → 강조·설명 → 유지·회수. 일부 과정의 중첩도 기록'],['PAT-CARD-0002','UI의 이동·확대·정착과 축소 회수. 위치와 크기 변화는 따로 연결'],['PAT-DETAIL-0001','노란 외곽 테두리의 전개·유지·회수'],['PAT-TEXT-0001','기능 표제와 본문의 등장 순서·회수. 정확 리빌 방식은 미확정']],[145,354])
p('기존 PAT-CARD-0001은 장면 전체를 묶었던 이력으로 보존했다. 새 CARD-0002와 뜻을 바꿔치기하지 않았다. 문구·색·시간이 조금 다르다는 이유만으로 무조건 새 번호를 만들지 않는다.','small')
p('전체 사례에는 번호뿐 아니라 어느 패턴이 어디에 배치되고 무엇과 겹치거나 함께 쓰이는지를 연결했다. 관측된 관계와 설계상 해석은 분리해 기록한다.','small')

story.append(PageBreak());p('부분 조회를 확인했다','title')
p('노란 테두리 동작만 선택하면','h')
table(['조회 결과','포함 범위'],[['선택 정의','PAT-DETAIL-0001 한 개. 전체 레이아웃과 전체 흐름 정의는 따라오지 않음.'],['원본 주장 3개','c022: 테두리 대상 식별 / c023: 왼쪽·상단부터 둘레 전개 / c024: 강조 유지와 회수'],['근거 8개','위 세 주장에 연결한 시점의 프레임만 포함. 관련 미해결도 함께 전달.'],['다른 장면에 적용','색·선폭·대상 외곽·시간을 새 장면에서 검토해야 함. 조회 성공은 제작 성공이 아님.']],[118,381])
p('검사 결과','h')
table(['검사','결과'],[['새 조합 검사','34/34 통과. 잘못된 역할, 빠진 흐름, 순환하는 선후·포함 관계, 다른 대상의 주장, 변조된 스냅샷, 거짓 확정을 거부.'],['기존 핵심 회귀','38/38 통과. 과거 출처 읽기와 현재 기록 검사를 구분해 시험. 형식 변경에 맞춘 시험 입력 보완 이력도 남김.'],['스킬 형식·사례 연결','기본 검증기 통과. 새 사례의 구조·카탈로그 근거 연결 통과. 상대 참조 10개 확인.'],['보존','이전 후보·관측·패턴·공개 기록 등 보호 파일 97개 해시 일치. 기존 A5b 중단 상태 유지.']],[118,381])
p('확인 범위와 남은 작업','h')
p('이번 작업은 이미 알고 있던 H02 개발 기록을 분리·연결한 것이다. 원래의 전체 디자인·모션 관측을 보존하고 근거 참조 범위를 좁혔으며, 새 영상 분석이나 독립 내용 검수를 수행한 것은 아니다.')
p('작은 UI의 개별 정체, 노드·배경의 세부 변화, 정확한 시간·수치·글꼴·색 값 등 기존 미해결은 남아 있다. 새 장면에서의 정확도·누락·반복 매칭·검수 부담·실제 제작 효과는 후속 검증 대상이다. 사용자 선택은 기록 구조의 결정이며 관측 내용이나 회사 공통 규칙의 승인이 아니다.','small')
p('보관: Phase 01-A의 별도 draft.5 수정 후보와 패턴 색인·개발 기록. 제출 보고서는 작업 보고서(pdf) / 01_제출보고서 / Phase 01-A에 저장한다. 기존 기본 스킬을 교체하거나 새 후보를 운영판으로 승격하지 않았다.','small')
OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='전체 사례와 독립 패턴 연결: 사용자 결정과 draft.5 반영 결과',author='Company video skill project').build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==2,len(reader.pages)
pdf=pdfium.PdfDocument(str(OUT));renders=WORK/'tmp/pdfs/pattern-composition';renders.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(pdf):page.render(scale=1.5).to_pil().save(renders/f'page-{i+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'rendered_pages':len(pdf),'sha256':sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>200 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
