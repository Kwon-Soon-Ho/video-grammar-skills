from pathlib import Path
from hashlib import sha256
from xml.sax.saxutils import escape
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
OUT=WORK/'output/pdf/20261019_backup_analysis_reliability_detail_review.pdf'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'));pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold')
INK=colors.HexColor('#182A40');BLUE=colors.HexColor('#255DB5');MUTED=colors.HexColor('#52677F');LINE=colors.HexColor('#D7E1ED')
styles={k:ParagraphStyle(k,fontName='MalgunBold' if k in ('title','h','th') else 'Malgun',fontSize=s,leading=l,textColor=colors.white if k=='th' else MUTED if k=='small' else INK,spaceAfter=a,wordWrap='CJK') for k,s,l,a in [('title',22,31,13),('h',12,19,7),('p',10,17,8),('small',8.4,13.5,6),('cell',9,15,0),('th',9,15,0)]}
story=[]
def p(t,style='p'):story.append(Paragraph(escape(t),styles[style]))
def table(headers,rows,widths):
 data=[[Paragraph(escape(x),styles['th']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EFF4FA'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]));story.extend([t,Spacer(1,8)])
def chrome(c,doc):
 c.setFillColor(BLUE);c.rect(0,832.89,595.28,9,fill=1,stroke=0);c.setFont('Malgun',8);c.setFillColor(MUTED);c.drawString(48,810,'PROJECT MILESTONE / BACKUP AND DETAIL REVIEW');c.drawRightString(547,810,'2026.10.19')
 c.setStrokeColor(LINE);c.line(48,42,547,42);c.drawString(48,27,'분석 신뢰성 보완 · 사내 영상 정밀 검수 우선 · 전체 반영 미완료');c.drawRightString(547,27,str(doc.page))

p('기존 스킬을 백업하고\n분석 작업본을 수정했다'.replace('\n',' '),'title')
p('사용자 지시 “기존 스킬은 백업하고 수정 작업 계속 진행하자”에 따라 백업을 확인한 뒤 D: 프로젝트 분석 스킬 본체를 draft.7 개발 작업본으로 갱신했다. 기존 실패·관측·과거 후보는 보존했다.')
table(['보존·적용','확인한 내용'],[
 ['백업 210파일','D: 분석스킬 디렉터리 전체와 C: 동결 A5b·최신 draft.6 후보를 ZIP으로 백업. 압축 내부 파일별 SHA-256 및 D: 사본 일치 확인.'],
 ['기존 본체 원본','draft.3 본체 7파일은 99_백업의 원본폴더에도 그대로 보존. 사용자 수정 지시에 따라 기존 작업 경로에는 draft.7을 배치.'],
 ['수정 작업본','Phase 01-A / 03_분석스킬 / company-video-grammar-analyzer. 같은 내용의 draft.7 스냅샷을 수정후보에 별도 보관.'],
 ['변경 범위','모션 관찰의 반복·주변 효과·중간 상태·사건 관계 지침, 수정 전후·지적·보완 주장·근거를 연결하는 검사 도구.'],
 ['보호 이력','기존 보호 경로 347개 중 본체 7개는 원본을 백업으로 보존하고, 나머지 340개는 원래 경로에서 바이트 일치. 기존 A5b 중단·실패 상태 유지.']
],[107,392])
p('이번에 수정한 판단 방식','h')
p('“등장했다”로 끝내지 않고, 반복하는 강약·밝기·면적, 전환 중간에 남은 선·면, 글자와 바탕의 서로 다른 등장 시점, 주 대상 주변의 작은 빛을 따로 살핀다. 미확인 속성을 제외해 검수가 끝난 것처럼 보이지 않도록 열린 항목으로 남긴다.')
p('도입 원칙: Ponytail의 반복 축소는 충분히 확인한 지식을 재사용하는 데 적용한다. REA의 증거·미해결·판정 연결은 수정 검수에 일부 적용했다. 두 원본 시스템 전체를 구현하거나 조사한 모든 스킬의 반영을 끝낸 것은 아니다.','small')

story.append(PageBreak());p('한 장면도\n등장 순서를 더 나눠 본다'.replace('\n',' '),'title')
p('새 PG 영상의 첫 관측을 보존한 뒤, 40~48초 구간에 0.1초 간격 81개 표본을 추가했다. 지역 카드·설명 프레임 ROI를 시간순으로 재대조하니 다음처럼 나눠 기록할 수 있었다. 표본 사이의 실제 시작은 더 좁은 프레임 검수 없이 확정하지 않는다.')
table(['표본 시각','직접 보인 상태','기록 단위'],[
 ['41.3 → 41.6초','로고가 뚜렷하지 않음 → 얇게 드러난 부분 → 일부 글자 → 강원 로고 형태','로고 글자의 가시성'],
 ['42.3 → 42.8초','이미 보이는 로고 뒤에 좁은 세로 면이 생겨 밝은 가로 카드 면으로 넓어짐','로고와 배경 면을 별도 대상·순서로 연결'],
 ['42.7 → 43.3초','위쪽의 좁은 프레임·빈 붉은 띠가 가로로 전개되고 첫 문구가 읽힘','설명 프레임·띠·글자 구분'],
 ['46.0 → 46.4초','둘째 줄이 뚜렷하지 않음 → 작은 어두운 띠 → 가로로 넓어짐','둘째 줄 띠의 등장과 범위'],
 ['46.5 → 47.2초','옅은 둘째 줄 글자 → 판독 가능 문구 → 강한 분홍 강조','글자 등장과 강조를 구분']
],[90,239,170])
p('기존 K-GEO 지적도 수정 전후를 연결했다','h')
p('기존 지적 7개와 추가 발견·경계 보완 2개를 합쳐 9개에 대한 보완 관측을 남겼다. 수신기 강조의 반복, 아래 문구와 위 표제의 선후, 인셋 내부 이동 방향, 표제 중간 형태, 원형 빛과 붉은 광점 등이 포함된다. 이 9개는 전체 영상의 오류 총수나 정확도 분모가 아니다.','small')
p('수정 검수 장부는 다른 대상의 주장, 요구와 다른 근거 유형, 바뀌지 않은 이전 주장으로 지적을 닫는 것을 거부한다. addressed는 지적에 답하는 보완 기록이 있다는 뜻이며 자동 시각 진실성 판정이나 독립 검수 합격을 뜻하지 않는다.','small')
p('개발 과정에서 새 속성의 시간 범위 누락과, 남아 있는 헤더를 해당 없음으로 잘못 처리한 작성기 오류도 발견해 보완했다. 첫 실패와 중간 기록은 별도 보존했다.','small')

story.append(PageBreak());p('새 사내 영상 두 구간에서\n실제로 기록했다'.replace('\n',' '),'title')
p('① 노듈러거더 166~174초: 7680x2160 전체와 좌우 도해를 구분','h')
story.append(Image(str(HERE/'fresh/cases/NEW-N/window/f_05100_170.000.png'),width=499,height=140.34));story.append(Spacer(1,7))
p('긴 구조물과 상판 조립, 앞 단면·먼 끝·오른쪽 단면의 화살표, 설명 띠와 공통 자막을 구분했다. 오른쪽 설명은 167.3초 옅은 단일 선, 167.9초 두 선, 168.2초 부분 글자, 168.6~168.7초 전체 문구로 보이는 단계를 기록했다.','small')
p('② PG 자율주행 40~48초: 지도 위 기관별 설명과 자막을 구분','h')
story.append(Image(str(HERE/'fresh/cases/NEW-P/window/f_01410_047.000.png'),width=419,height=235.69));story.append(Spacer(1,7))
p('경찰청의 노랑 묶음과 지역 기관의 분홍 묶음, 연결선, 횡성의 청록 강조, 하단 진행 자막을 나눴다. 자막은 문구 교체와 글자가 왼쪽부터 밝아지는 변화를 따로 기록했고, 오디오를 듣지 않아 발화 싱크로 확정하지 않았다.','small')
p('두 구간 첫 출력: 대상 22개·주장 69개를 보존. 세부 보완판은 밝은 카드 면을 별도 대상으로 더해 총 23개·72개 주장이다. 각 구간의 구조·프레임 출처 연결 검사는 통과했다. 이 개수는 완전성·품질 점수가 아니다.','small')

story.append(PageBreak());p('사내 영상은\n세부 검수를 우선한다'.replace('\n',' '),'title')
p('사용자 추가 결정: 동작 구조를 중심으로 같은 패턴을 묶고 정보 역할·배치·색·속도는 조건과 변형으로 관리한다. 다만 과거 사용자가 누락을 추가 발견해 같은 영상을 두세 번 검수했던 부담을 줄이도록 사내 영상의 세부 분해와 검수를 먼저 충분히 진행한다.')
table(['확인한 것','아직 확인하지 않은 것'],[
 ['백업과 프로젝트 작업본 갱신, 변경 코드·상대 링크 확인','전체 조사 스킬 반영, 회사 공통 규칙 승인, 전역 설치'],
 ['수정 장부 오류 검사 18개, 기존 핵심 38개·조합 34개 통과','새 자료의 독립 내용 검수, 오류·누락의 전수 분모와 정확도'],
 ['새 두 구간 각각 0.5초 17개 + 보강 0.1초 81개 표본 추출. 지정 ROI를 상세 대조','추출한 모든 프레임의 전체 화면 native 검수, 원본 두 영상 전체의 세부 분석'],
 ['노듈러 배경 미세 변화와 PG 연결선 내부 변화는 요구 속성으로 올리고 열린 검수로 유지','배경의 연속 변화, 연결선 무늬 방향, 정확 강조 주기·가감속·좌표 수치']
],[249,250])
p('확인 범위는 각각 8초다','h')
p('노듈러거더 원본은 약 6분 58초, PG 원본은 약 3분 32초다. 이번 작업은 선택한 두 구간의 개발 분석·보완이다. 두 원본 전체를 분석 완료했다고 표시하지 않는다. 첫 관측·구조 통과·등록 지적 보완과 정밀 검수 완료를 구분한다.','small')
p('다음 큰 작업','h')
p('우선 사내 영상의 대상별 확인 범위와 열린 검수부터 정리한다. 작은 효과·내부 상태·동시 사건·중간 형태가 실제 근거에 연결되는지 확인한 뒤 패턴 검색·재사용을 확장한다. 그 후 전문가의 대안·선택·비평·재평가, 편집 가능한 재제작·렌더 비교로 이어간다.','small')
p('사용자 결정을 프로젝트 지침에도 기록했다. 불확실성을 적는 것은 관찰을 생략할 이유가 아니며, 필요한 근거를 보강한 뒤에도 남는 한계를 뜻한다. 조사·문서·코드·실제 시각 검증의 진행 상태를 나눠 보고한다.','small')

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=57,title='백업 후 분석스킬 수정과 사내 영상 세부 검수',author='Company video skill project').build(story,onFirstPage=chrome,onLaterPages=chrome)
reader=PdfReader(OUT);assert len(reader.pages)==4,len(reader.pages)
pdf=pdfium.PdfDocument(str(OUT));renders=WORK/'tmp/pdfs/analysis-reliability';renders.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(pdf):page.render(scale=1.5).to_pil().save(renders/f'page-{i+1:02d}.png')
qa={'pdf':str(OUT),'pages':len(reader.pages),'sha256':sha256(OUT.read_bytes()).hexdigest(),'all_pages_have_text':all(len(p.extract_text())>300 for p in reader.pages),'visual_review':'pending'}
(HERE/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
