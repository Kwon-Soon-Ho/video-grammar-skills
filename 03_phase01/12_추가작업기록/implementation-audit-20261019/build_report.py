from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_research_implementation_scope_audit.pdf'
audit=json.loads((HERE/'implementation-audit.json').read_text(encoding='utf-8'))
manifest=json.loads((WORK/'research/ponytail-rea-20261019/research-manifest.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#1C2B40');BLUE=colors.HexColor('#245ABA');MUTED=colors.HexColor('#52657B');LINE=colors.HexColor('#D8E0EC')
styles={k:ParagraphStyle(k,fontName='MalgunBold' if k in ('title','h','th') else 'Malgun',fontSize=s,leading=l,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,spaceAfter=a,wordWrap='CJK') for k,s,l,a in [('title',22,31,13),('h',12,19,7),('p',10,17,8),('small',8.3,13.2,6),('cell',9,14.8,0),('th',9,15,0)]}
story=[]
def p(t,style='p'):story.append(Paragraph(escape(t),styles[style]))
def table(headers,rows,widths):
 data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,8)])
def chrome(c,doc):
 c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0);c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'PROJECT MILESTONE / SCOPE AND IMPLEMENTATION');c.drawRightString(547,810,'2026.10.19')
 c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'전체 반영 미완료 · 기본 교체 보류 · 기존 결과와 실패 보존');c.drawRightString(547,27,str(doc.page))

p('조사는 넓게 진행했고,\n구현은 일부만 진행했다'.replace('\n',' '),'title')
p('사용자 확인: “조사한 스킬이 많은데 벌써 다 반영하고 수정했다고?” 이 질문을 계기로 조사, 지침 작성, 실행 코드, 실제 품질 검증을 다시 구분했다. 전체 반영 완료로 읽히는 진행 보고는 부정확했다.')
p('지금까지 바꾼 것은 분석 기록·근거 검사와 패턴 등록·연결의 일부다. 전문가 판단 과정과 실제 영상 재제작까지 끝난 상태가 아니다. 기존 기본 스킬은 교체하지 않았으며 새 판본은 개발 후보로 보관한다.')
p('큰 카테고리별 현재 위치','h')
table(['범주','실제로 있는 것','남은 핵심'],[
 ['1. 분석 신뢰성·근거·기록','대상·속성·시간·원자 주장, 파일·프레임 근거 연결, 미해결 기록과 검사','내용 오답·누락 보완, 실제 자료에서의 행동 검증. 현재 진행 중'],
 ['2. 사례 검색·패턴 재사용','카테고리·번호·고정 사본, 전체 사례와 레이아웃·흐름·세부 연결, 단순 단어 검색','조건에 맞는 후보 선택, 현재 장면 대조, 차이와 재사용 적합성 검증'],
 ['3. 전문가 판단·기획','목적·조건·반례·구현 제안을 적는 지침과 인계 칸','복수 대안 → 선택 근거 → 비평 → 수정 → 재평가를 실제 기획에서 수행'],
 ['4. 역설계·제작 검증','관측 기록을 제작에 넘길 연결 형식 일부','편집 가능한 재제작, 실제 렌더 대조, 문구·내용을 바꾼 재사용 시험. 이번 후보에 미구현']
],[101,191,207])
p('사용자가 앞서 선택한 “분석 정확도·근거 기록 우선”을 유지한다. 네 범주를 큰 작업 묶음으로 진행하며, 기록 형식의 완성을 전체 파이프라인의 완성으로 보고하지 않는다.','small')

story.append(PageBreak());p('조사한 원칙과\n반영한 기능은 다르다'.replace('\n',' '),'title')
p('조사 이력에는 이전 11개 저장소와 이번 10개 저장소가 있다. 두 저장소가 겹쳐 고유 저장소는 19개다. 이전 선택 파일 379개와 이번 소스 검토 기록 41개는 조사 범위이며, 스킬 수·구현 기능 수·완성률이 아니다. 기존에 참고한 로컬 전문 스킬 7개도 별도다.','small')
table(['조사 묶음','가져온 부분','아직 해야 할 부분'],[
 ['Ponytail','기존 지식 우선 조회, 불필요한 반복 축소, 생략 조건을 판단 인계에 일부 반영','검색 결과와 새 목적을 비교해 실제로 무엇을 생략할지 판단·검증'],
 ['REA','관측/추론 구분, 미해결 질문, 증거 연결과 해소 조건의 일부 검사','상충 판정·개정 관리, 재구성 의무 → 구현 → 렌더 검증 연결'],
 ['Impeccable · gstack','디자인 차원, 목적·조건·반례·구현 제안의 형식','구체 산출물에 대한 전문가 비평, 대안 비교와 수정 후 재평가'],
 ['Trail of Bits · Superpowers · Anthropic','원자 주장, 확인 범위, 형식 검사와 내용 검수 분리, 일부 오류 시험','독립 검토와 새 자료 비교, 의미 오답·누락 및 평가기 자체의 한계 검증'],
 ['Matt Pocock · ECC · Vercel','용어·결정 기록, 초안 규칙, 조건·반례를 남기는 형식','공통 용어·변형 관리, 반복 사례에서 규칙 도출과 반례 시험']
],[126,182,191])
p('41개 소스 검토 포인트를 후보 코드와 대조한 결과','h')
p('draft.5 기준: 코드 일부 반영 21개 / 지침·형식 반영 10개 / 미구현 4개 / 직접 이식 제외·평가 참고 6개. 서로 크기가 다른 조사 포인트의 분류라서 21/41 같은 구현 완성률로 계산할 수 없다. 새 draft.6의 추가 변경은 다음 쪽에 별도로 기록했다.','small')
p('원본 스킬 전체를 설치하는 것이 목표는 아니다. 영상 목적에 맞는 원칙·기능·평가 방식을 선택해 옮긴다. 다만 문서에 칸을 만든 것, 도구가 형식을 통과한 것, 실제 결과가 좋아진 것은 각각 증거가 필요하다.','small')
p('추적 자료','h')
p('implementation-audit.json: 이번 41개 포인트별 GitHub 고정 커밋·파일·발견·후보 파일 해시·남은 범위. current-progress.json: 네 범주와 최신 후보 상태. 이전 11개 저장소는 조사 이력을 연결했으며, 기존 Phase 00 완료 상태 전체를 이번 감사에서 다시 판정한 것은 아니다.','small')

story.append(PageBreak());p('실제 사용에서도\n아직 고칠 점이 나왔다'.replace('\n',' '),'title')
p('기존에 노출된 K-GEO H03·H04 두 구간을 개발 자료로 분석해 62개 주장을 기록했다. 새 홀드아웃이나 독립 비교가 아니다. 첫 기록을 보존하고 구조 검사와 내용 대조 결과를 나눴다.')
table(['확인 항목','결과와 의미'],[
 ['실제 검사기 오류','H03에서 같은 표의 서로 다른 셀·이름표를 중복으로 거부했다. 셀·필드를 구분하는 dimension을 추가해 사실을 삭제하지 않고 통과하도록 수정했다. 같은 구분·속성·시간의 중복은 계속 거부한다.'],
 ['검색 추가의 범위','번호·이름·정의·조건에서 단어와 카테고리를 찾는 기능을 추가했다. 의미 유사도 검색이나 현재 장면의 적합성 판정은 아니다.'],
 ['구조 검사 통과 후 내용 문제','강조의 반복, 아래 문구와 상단 표제의 선후 관계, 표제 전환의 중간 형태, 인셋 내부 이동 방향, 주변 원형 빛과 작은 붉은 빛 등 보완할 발견 7개를 열어 두었다. 전체 오류 수나 정확도는 산출하지 않았다.'],
 ['코드 검증과 보존','추가 경계 검사 18개, 기존 핵심 38개·조합 34개가 통과했다. 형식·출처·중복·검색의 검사이며 시각 정확도 시험이 아니다. 보호 파일 223개의 해시를 확인했고 기존 A5b 중단 상태를 유지한다.']
],[111,388])
p('다음 큰 작업과 완료를 판단할 결과물','h')
p('① 분석 신뢰성: 실제 누락과 오답을 수정하고 대상·속성·시간·근거를 재검토한다. 이미 본 자료의 수정 결과와 새 자료의 검증 결과를 구분한다. 이 범주를 먼저 진행한다.')
p('② 재사용: 조건으로 후보를 찾고 반복 장면의 현재 근거·차이·미확정을 남긴다. ③ 전문가 판단: 복수 대안과 선택·비평·재평가가 들어 있는 실제 기획 사례를 만든다. ④ 역설계: 편집 가능한 제작물과 원본 대조 렌더, 내용 변경 시험을 남긴다.','small')
p('사용자 판단이 필요한 지점에서는 추천안을 포함한 사지선다로 묻는다. 이미 정한 기록 밀도와 분류는 다시 묻지 않는다. 기본 적용·전체 반영 완료 여부는 위 결과물의 확인 범위를 근거로 별도 보고한다.','small')
p('보관 판본: draft.4·draft.5 기존 후보 보존 / draft.6은 이번 검사기 보완의 별도 후보. 실제 제작 품질·분석 정확도 개선·회사 공통 규칙의 승인은 아직 주장하지 않는다.','small')

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='조사 대비 구현 범위 재정리와 실제 사용 검증 현황',author='Company video skill project').build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==3,len(reader.pages)
pdf=pdfium.PdfDocument(str(OUT));renders=WORK/'tmp/pdfs/implementation-audit';renders.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(pdf):page.render(scale=1.5).to_pil().save(renders/f'page-{i+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'sha256':sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>500 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
