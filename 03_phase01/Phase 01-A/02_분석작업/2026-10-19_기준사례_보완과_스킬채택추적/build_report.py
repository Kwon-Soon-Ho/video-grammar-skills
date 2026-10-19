from pathlib import Path
from xml.sax.saxutils import escape
import json,hashlib
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_two_reference_cases_and_adoption_trace.pdf'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'));pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#182A40');BLUE=colors.HexColor('#255DB5');MUTED=colors.HexColor('#52677F');LINE=colors.HexColor('#D7E1ED')
styles={k:ParagraphStyle(k,fontName='MalgunBold' if k in ('title','h','th') else 'Malgun',fontSize=s,leading=l,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,spaceAfter=a,wordWrap='CJK') for k,s,l,a in [('title',21,29,12),('h',12,19,7),('p',10,17,8),('small',8.3,13,6),('cell',9,15,0),('th',9,15,0)]}
story=[]
def p(t,style='p'):story.append(Paragraph(escape(t),styles[style]))
def table(headers,rows,widths):
 data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,8)])
def chrome(c,doc):
 c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0);c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'REFERENCE CASE DRAFT / OBSERVATION AND ADOPTION TRACE');c.drawRightString(547,810,'2026.10.19')
 c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'분석 사례 보완 · 동일 AI 검토 · 전체 스킬 적용 및 독립 평가 미완료');c.drawRightString(547,27,str(doc.page))

p('두 장면을 기준 사례 후보로 보완했다','title')
p('사용자 선택 ①에 따라 기존 미해결 5개와 전후 구간을 확인했다. 현재 스킬 본체는 draft.8을 유지하고, 이번에는 실제 관측 사례·분리된 패턴 정의·조사 반영 대조표를 추가했다. 전체 스킬 제작을 끝낸 상태는 아니다.')
table(['기존 쟁점','보완 결과','현재 판단'],[
 ['노듈러 배경','세 ROI에서 도입 밝아짐과 이후 무늬 위치 유사·유지 확인. 별도 빛 이동은 확인되지 않음.','범위 한정 답변'],
 ['노듈러 회전 강조','한 번의 화살표 강조와 구조물 왕복 기울임을 분리. 오른쪽 원호는 좌측보다 오래 남음.','부분 보완'],
 ['노듈러 왼쪽 설명','문구 판독·외곽 폭 정착·가감속을 나눠 확인. 화면 표기 문자도 정정.','범위 한정 답변'],
 ['PG 연결선','생성 중 위쪽으로 차오르는 유색 영역, 정착 뒤 무늬 위치, 후속 묶음 이동을 분리.','범위 한정 답변'],
 ['PG 정책 행 강조','기존 노란 행의 유사 상태와 새 분홍 행별 한 차례 강조를 대조. 반복 주기 전제를 채택하지 않음.','범위 한정 답변']
],[102,292,105])
p('미해결 하나를 완료로 닫지 않았다','h')
p('화살표의 정확한 강도 곡선과 원본 동기화 설정은 남는다. 구조물 투영 경사의 가감속을 측정했더라도 그것을 화살표 밝기의 가감속이나 원본 AE 설정으로 옮기지 않는다. 최종 퇴장·폰트명·효과 설정 등 범위 밖 항목도 각 정의의 미상 파라미터와 한계로 보존한다.','small')
table(['이번 기록','확인 범위'],[
 ['노듈러 166~181초 / PG 40~53초','합계28초. 이전16초보다 전후12초 확장. 원본 전체 약630.272초 중 기록 창 밖602.272초가 남음.'],
 ['전체 디자인과 모션 연결','각 사례3개 화면 상태. 총25개 대상·113개 주장, 새 패턴 정의12개. 개수는 정확도·완성률 점수가 아님.'],
 ['검증의 성격','출처·시각·범위·참조·선별 추출 검사와 같은 AI의 시각 대조. 독립 정답·전수 발견·새 문구 재제작·회사 승인은 아님.']
],[177,322])

story.append(PageBreak());p('노듈러: 문구 판독과 폭 정착을 나눴다','title')
p('아래는 왼쪽 설명 띠의 원본 ROI를 시간순으로 놓은 것이다. 하나의 선에서 빈 띠, 부분 문구, 전체 문구, 폭 정착으로 구분해 기록했다.','small')
story.append(Image(str(HERE/'inspection/N-left-label.jpg'),width=499,height=236.56));story.append(Spacer(1,7))
table(['시각 / 관측량','기록한 사실'],[
 ['173.0 → 173.6초','청록 선 간격 약21 → 733 native px. 빈 띠가 열리며 일부 글자가 드러남.'],
 ['174.0 → 174.8초','전체 문구는174초에 읽히지만 선 간격은1272 → 1473px로 더 넓어져 정착.'],
 ['가감속 근거','0.2초 간격의 폭 증가량32→189→491→354→185→105→58→30→8px. 초반 가속·후반 감속 성격. 실제 마스크/폭 속성 원값 아님.'],
 ['문자 판독 정정','영상 표기는 “켄틸레버 바닥판 시공시 동바리 역할 수행”. 과거의 “캔틸레버” 판독은 기각으로 보존. 하단 자막의 “시공 시”, “역할도 수행”은 별도 문구.']
],[133,366])
p('같은 화면 안의 동작도 각각 다르다','h')
p('앞 단면 검은 구멍 상단의 화면 투영 경사는170.6초 약+17.8°,171.5초 약-6.3°,172.4초 약+17.9°로 왕복한다. 반주기에서 극점 부근 느리고 중간이 빠른 성격을 확인했다. 이 값은 실제3D 회전각이 아니다. 전면·먼 끝 화살표는174초 소실하지만 오른쪽 곡선은 이후에도 남는다.176초 뒤의 형상 밀착 강조와179.5초 뒤 마감 판은 새 대상으로 나눴다.','small')
p('같은 PAT-TEXT-0002로 연결하되 오른쪽 설명의 문구·길이·등장 시각과 미확인 가감속은 차이로 남겼다. 왼쪽에서 측정한 곡선을 오른쪽의 원본 값으로 복사하지 않았다.','small')

story.append(PageBreak());p('PG: 선의 성장과 무늬 흐름을 구분했다','title')
p('42.4~43.5초의 연결선 ROI. 아래 기관 카드 위에서 분홍 무늬의 드러나는 범위가 위로 자라고, 위 접점이 선명해진다. 정착 뒤 무늬가 계속 위로 흐른다는 근거로 사용하지 않는다.','small')
story.append(Image(str(HERE/'inspection/P-line-birth.jpg'),width=499,height=285.4));story.append(Spacer(1,7))
table(['대상','새 관측'],[
 ['연결선 생성','42.8/43.0/43.2/43.4초의 유색 위 경계 y=772/748/704/642px. 같은0.2초의 진행량24→44→62px로 생성 전반 가속 경향. 실제 글리프 이동속도·정확 감속 함수는 미확정.'],
 ['행별 강조','첫 분홍 행은44~46초 밝고46.5~47.5초 약화. 둘째 행은46.5초 이후 진입,47.5~50초 강조 후 약화. 기존 노란 행과 공통 점멸 주기를 만들지 않음.'],
 ['후속 배치','51.5~53초 분홍 카드·연결선·프레임·문구는 함께 오른쪽으로 이동. 지도와 경찰청 카드의 같은 ROI는48초와49~53초 비교에서 픽셀이 일치.']
],[95,404])
p('번호를 재사용하되 현재 근거를 남긴다','h')
p('두 정책 행은 PAT-TEXT-0003을 함께 인용하고 각 문구·등장·강조 시간을 따로 연결했다. 로고 선등장/카드 면은 PAT-CARD-0003, 연결선 채움은 PAT-DETAIL-0005, 기관 묶음 재배치는 PAT-DETAIL-0006으로 나눴다. 같은 사례 안의 연결이며 새 제작에서의 재사용 성공은 미검증이다.','small')

story.append(PageBreak());p('외부 스킬은 선별·구현·검증을 추적 중이다','title')
p('사용자 질문에 따라 기존 draft.5 조사 대조표를 현재 draft.8 파일과 다시 연결했다. 추가 조사41개 항목 중17개는 해당 파일 전체,24개는 관련 구간을 정적으로 검토했다. 파일 전체 검토도 저장소 전체 분해나 원본 테스트 실행을 뜻하지 않는다.')
table(['현재 상태','해석'],[
 ['지침·형식10 / 코드 일부21','기록 칸·근거 자격·패턴 등록/조합/검색·수정/범위 검사 등 부분 반영. 전문가 판단 전체 기능의 완성이 아님.'],
 ['미구현4 / 직접 이식 제외·평가 참고6','상충 판정·재현 검증·전문 분석 배치/지표 집계 등이 남음. 코드용 전역 훅, 점수 기반 회사 규칙 자동 승격 등은 직접 이식 제외. 서로 크기가 다른 항목의 합계로 완료율을 만들지 않음.'],
 ['아직 실제 검증하지 않은 핵심','목적별 설계 대안 생성→선택 이유→독립 비평→수정·재평가, 편집 가능한 재제작→렌더 대조→내용 변경 재사용. 외부 프로젝트 테스트·벤치마크도 직접 실행하지 않음.']
],[165,334])
p('사례와 패턴의 현재 분류','h')
table(['분류 / 새 번호','역할'],[
 ['LAYOUT-0002/0003','각 사례 전체 디자인.3개 화면 상태와 영역·위계·문구·색·배경·형태.'],
 ['FLOW-0002/0003','조립/설명/강조/마감 또는 기관 추가/행 강조/재배치의 전체 전개.'],
 ['TEXT-0002/0003 · CARD-0003','설명 띠 리빌, 정책 행 전개/강조, 로고 선등장과 카드 면.'],
 ['DETAIL-0002~0006','기울임, 주변 화살표 강조, 형상 밀착 강조, 연결선 채움, 기관 묶음 재배치.']
],[178,321])
p('전체 사례를 보존하고14개 패턴 인용을 연결했다. 기존6개 정의는 바이트를 보존하고 새12개는 모두 draft/candidate로 두었다. 문구·색·속도 차이만으로 번호를 더 쪼개지 않았다.','small')
p('현재 위치와 다음 사용자 판단','h')
p('분석 신뢰성 보완 중이며, 기록 창 밖 약10분2초와 등록한 미해결1개가 남는다. 원본 전체에는 아직 발견하지 못한 대상·오류가 있을 수 있다. 다음 묶음에서는 사용자가 사례의 밀도·분류를 검토하거나, 다른 장면으로 확장하거나, 한 영상 전체를 분석하거나, 남은 정밀 수치의 필요 범위를 선택할 수 있다.','small')

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='두 기준 사례 보완과 외부 스킬 반영 추적',author='Company video skill project').build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==4,len(reader.pages)
renders=WORK/'tmp/pdfs/case-benchmarks';renders.mkdir(parents=True,exist_ok=True);pdf=pdfium.PdfDocument(str(OUT))
for i,page in enumerate(pdf):page.render(scale=1.5).to_pil().save(renders/f'page-{i+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>300 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
