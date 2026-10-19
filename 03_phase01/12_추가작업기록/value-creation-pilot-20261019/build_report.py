from pathlib import Path
import json, hashlib
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from PIL import Image
import pypdfium2 as pdfium

O=Path(__file__).resolve().parent;R=O.parent
P=R/'output/pdf/20261019_value_creation_knowledge_and_design_pilot.pdf';P.parent.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('K','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('KB','C:/Windows/Fonts/malgunbd.ttf'))
W,H=595.28,841.89
C=canvas.Canvas(str(P),pagesize=(W,H));C.setTitle('가치창출 영상 - 새 지식 기록과 화면·모션 시범');C.setAuthor('사내 영상 생성기 프로젝트')
INK='#17383D';ACC='#087F72';MUT='#53676A';BG='#F1F5F3'
sty=ParagraphStyle('body',fontName='K',fontSize=10,leading=16,textColor=HexColor(INK),wordWrap='CJK')
page=0
def para(text,y,x=38,w=519,size=10,bold=False):
 s=ParagraphStyle('p',parent=sty,fontSize=size,leading=size*1.6,fontName='KB' if bold else 'K')
 p=Paragraph(text,s);a,h=p.wrap(w,720);assert y+h<801,(page,text[:50],y,h)
 p.drawOn(C,x,H-y-h);return y+h
def title(k,t,sub):
 global page
 page+=1;C.setFillColor(HexColor(ACC));C.rect(0,H-9,W,9,fill=1,stroke=0)
 para(k,28,size=9,bold=True);para(t,49,size=22,bold=True);para(sub,87,size=9)
 C.setStrokeColor(HexColor('#D4DFDC'));C.line(38,H-113,W-38,H-113)
def heading(t,y):return para(t,y,size=13,bold=True)+8
def bullet(t,y):return para('• '+t,y)+7
def img(p,x,y,w=None,h=None):
 im=Image.open(p);iw,ih=im.size
 if w is None:w=h*iw/ih
 if h is None:h=w*ih/iw
 assert y+h<798
 C.drawImage(str(p),x,H-y-h,w,h);return y+h
def end():
 C.setFillColor(HexColor(MUT));C.setFont('K',8);C.drawString(38,25,'2026-10-19 · 개발 시범 · 실제 모션/사용자 이해도 미검증')
 C.drawRightString(W-38,25,str(page));C.showPage()

title('01 / 적용 기준','검토 영상을 교체한 새 시범','목표: 복제 가능한 좌표 목록에서, 새 내용에 적용할 디자인·모션 지식으로')
y=heading('현재 한 묶음에서 만든 것',131)
y=bullet('가치창출 영상의 계약·프로젝트 지원 두 사례 기록, 조건이 있는 패턴 후보 6개, 새 화면안 2종과 각 6단계 정지 스토리보드.',y)
y=bullet('계약은 16:9 요약, 프로젝트 지원은 9:16 분류 설명으로 변형했다. 원본 전체 시퀀스 대체본이나 회사 최종 시안은 아니다.',y)
y=heading('변경 시나리오를 읽은 기준',y+8)
y=para('6쪽을 모두 화면으로 확인했다. 2~4쪽은 우측 푸른 변경안을 사용하고, 1·5·6쪽의 “변경없음”은 좌측 원문을 유지했다. 1쪽의 푸른 작업시간 메모는 내레이션과 분리했다.',y)
y=heading('영상의 숫자와 변경안의 숫자를 분리',y+18)
for line in ['계약 수주: 영상 17.5 → 변경안 17.6억원 / 매출: 12.9 → 12.9억원','계약 비용: 영상 8.7 → 변경안 8.4억원','프로젝트 지원: 영상 23.7억원·26건 → 변경안 22.2억원·27건','전체 합계: 영상 55.5 → 유지 시나리오 55.7억원']:
 y=bullet(line,y)
y=para('영상은 디자인·모션의 근거이고 새 화면의 내용은 변경안 기준이다. 숫자 차이를 오독으로 처리하거나 원본 관측 기록을 바꾸지 않았다.',y+6)
y=heading('먼저 남겨둔 입력 쟁점',y+18)
y=para('계약 매출 세부 6.2+6.5는 12.7이지만 본문 총액은 12.9억원이다. 0.2억원을 임의의 “기타”로 만들지 않았다. 총액 요약은 유지하고 매출 구성비 차트는 확정을 유보했다.',y)
para('원본: 가치창출성과 영상_260923_v3.mp4 / 7분14.4초 / 7680×2160 / 30fps<br/>기준 문서: 가치창출 시나리오_v1(260916).pdf / 6쪽',y+18,size=9)
end()

title('02 / 원본을 지식으로 읽기','전체 디자인을 먼저 보존','아래 화면은 원본 표본이다. 새 시안의 수치·배치와 혼동하지 않는다.')
img(O/'extraction/cases/VALUE/contract/f_03360_112.000.png',38,130,w=519)
para('계약 112초 표본: 수주 구성·비용·실제 매출이 가로로 배열된 상태',282,size=9)
img(O/'extraction/cases/VALUE/project/f_04500_150.000.png',38,312,w=519)
para('프로젝트 지원 150초 표본: 업무 실경과 유형별 성과 정보의 분할',464,size=9)
y=heading('원본의 전체 언어와 역할',495)
y=para('밝은 여백, 상단 장 제목, 장별 강조색, 가는 정보 프레임, 입체적으로 보이는 기술·경제 아이콘, 실적 사진을 결합한다. 큰 숫자가 주장을 맡고 사진은 업무 맥락, 정보면은 분류와 근거를 맡는다.',y)
y=heading('전체 흐름과 독립 동작을 따로 연결',y+14)
y=para('계약: 수주/매출 → 수주 구성 → 비용 추가 → 실제 매출과 중복 제외.<br/>지원: 요청/지원 관계 → 총액/건수 → 업무 구성 → 비용절감 의미 → 요약.<br/>숫자 변화, 정보 패널 추가, 분류 행 등장은 흐름과 연결하되 별도 재사용 후보로 남겼다.',y)
para('관측 범위: 전편 12초 간격 개괄 37표본 + 계약 78~116초 20표본 + 지원 126~174초 25표본(각 2초 간격). 연속 재생·음성 청취·전편 정밀 검수는 하지 않았다. 가감속·정확한 시작 프레임은 확정하지 않는다.',y+15,size=9)
end()

title('03 / 계약 새 화면안','산정값과 참고값을 위계로 구분','16:9 · 변경안의 매출 12.9 / 수주 17.6 / 비용 8.4억원 적용')
img(O/'proofs/A-state-5.png',38,132,w=519)
y=heading('옮긴 것은 숫자의 역할과 정보의 관계',444)
y=para('실제 매출을 가장 크게 두고 수주는 참고, 비용은 별도로 표시했다. 원본의 녹색 계열·밝은 정보면을 변형하고, 이번 요약에서 입체 장식·실경·구성 도넛은 유보했다. 원본 디자인 요소는 지식 기록에 남아 있다.',y)
y=heading('보호할 것 / 바꿀 수 있는 것',y+16)
y=para('<b>보호</b>: 매출을 산정에 반영한다는 기준, 수주·비용과의 의미 차이, 기간·단위, 합산이나 순이익으로 보이지 않는 관계.<br/><b>가변</b>: 색·재질, 가로/세로 구역, 아이콘·사진, 수치를 보조하는 표현과 세부 항목 수.',y)
y=heading('선택하지 않은 대안도 기록',y+16)
y=para('동급 3카드는 같은 성과 세 개처럼 보일 수 있다. 수주→비용→매출 화살표는 산식·차감 관계를 암시할 수 있다. 이번에는 매출 중심 구성을 골랐으며, 실제 오해 감소는 사용자 검토가 필요하다.',y)
end()

title('04 / 계약 모션 스토리보드','주장은 남기고 보조 정보를 더하기','각 시간은 새 설계의 제안이다. 원본 측정값·음성 동기화 시간이 아니다.')
img(O/'proofs/A-storyboard.png',60,126,w=475)
y=heading('전체 흐름과 세부 동작 제안',643)
y=para('맥락 → 매출 → 참고 수주 → 별도 비용 → 산정 한계 → 유지. 매출의 위치를 고정하고 카드·라벨·금액을 한 묶음으로 추가한다. 숫자는 확정값을 제시하는 안을 우선하며 튀는 반동은 유보했다.',y)
para('14초는 이 요약 화면의 잠정 길이이다. 계약 변경 시나리오 전체를 14초에 낭독하는 계획이 아니다. 실제 모션·읽기 시간·오디오 싱크는 다음 검증 대상이다.',y+10,size=9)
end()

title('05 / 프로젝트 지원 새 화면안','같은 총액, 분류 기준만 교체','9:16 · 왼쪽 가족사별 / 오른쪽 업무유형별 · 서로 더하는 값이 아니다.')
img(O/'proofs/B-state-2.png',38,130,h=430)
img(O/'proofs/B-state-5.png',310,130,h=430)
y=heading('축소 대신 정보 구조를 다시 배치',615)
y=para('총액 22.2억원·27건·기간·산정 관점은 같은 위치에 남긴다. 아래에서 가족사별(15.5+6.7)과 유형별(18.2+1.5+1.2+1.3)을 순서대로 보여준다. 각 분류는 같은 22.2억원을 설명한다.',y)
para('원본 구리색 장 분위기와 큰 수치 위계는 유지했지만, 사진·3D 느낌의 장식은 이 정보 전달 시범에서 유보했다. 완성 영상의 미감 방향까지 확정한 선택은 아니다. 유형별 막대는 총금액을 기준으로 하며 건수는 별도 표시한다.',y+10,size=9)
end()

title('06 / 지원 모션 스토리보드','분류가 바뀌어도 총액은 같은 값','모션을 통해 관계를 전달하는 제안. 분류 전환의 명료함은 실제 재생에서 확인해야 한다.')
img(O/'proofs/B-storyboard.png',82,125,w=430)
y=heading('독립 동작 후보: 분류 제목과 행의 동시 교체',700)
para('총액·기간·단위는 고정하고 분류 제목과 해당 행을 함께 바꾼다. 20초는 잠정 길이이며, 행별 등장 간격·가감속·오디오 싱크는 미확정이다.',y,size=9)
end()

title('07 / DB 기록과 전문가 판단','패턴 이름보다 적용 조건을 남기기','이번 6개 ID는 로컬 후보이다. 기존 정본 DB와 스킬 draft.9는 수정하지 않았다.')
y=heading('사례 → 배치 → 전체 흐름 → 세부 동작',133)
for line in ['VC-CASE-A/B: 원본 전체 언어·요소·상태·프레임·해석과 새 브리프를 보존한다.','VC-LAY-01: 주 산정값/참고값 분리. VC-LAY-02: 총액 고정+분류 교체(새 변형).','VC-FLOW-01: 맥락→주장→근거/구성→한계 설명. 필요한 장면에만 사용한다.','VC-MOTION-01: 수치·차트의 의미 상태 일치. 02: 핵심 유지+정보 추가. 03: 분류 묶음 교체(새 제안).']:
 y=bullet(line,y)
y=heading('구체적인 반례 입력을 넣어 판단',y+10)
for line in ['입력 “계약번호 0017”: 중간 숫자가 거짓 정보를 만들므로 금액 카운트업을 적용하지 않는다.','입력 “한맥 1~6월 / 삼안 1~9월”: 기간이 달라 같은 총액의 분류로 묶지 않는다.','입력 “매출-비용=순이익 설명”: 현재 산정값/참고값 배치로는 산식을 숨길 수 있어 별도 관계 구조를 고른다.']:
 y=bullet(line,y)
y=para('위 반례는 실제 입력을 작성해 논리적으로 판단한 예시이다. 모델 반복시험·실제 영상시험·사용자 시험을 통과한 결과는 아니다.',y,size=9)
y=heading('조사한 스킬에서 이번에 가져온 판단 방식',y+17)
y=para('Ponytail: 기존 표현·작은 변형·새 표현을 비교하고 불필요한 구조를 늘리지 않기.<br/>REA: 관측/해석/제안과 근거·미상을 구분하고 미상이 막는 사용을 한정하기.<br/>Impeccable·gstack: 전체 위계와 전달 실패를 비평하고 대안의 제외 이유 남기기.<br/>도메인 모델링·평가 지침: 사례/패턴/연결/조건/검토의 역할과 검증 범위를 분리하기.',y)
para('연결한 상류 파일·커밋·해시와 적용 결과는 research-application.json에 있다. 이번에 모든 조사 스킬을 구현·실행하거나 전수 검증한 것은 아니다. 전역 훅·코드맵·바이너리 절차·웹 고정 시간 규칙은 직접 이식하지 않았다.',y+12,size=9)
end()

title('08 / 현재 위치와 다음 선택','시범 결과를 보고 기준을 결정할 단계','자동 검사 통과를 디자인 품질이나 사용자 이해도 통과로 확대하지 않는다.')
y=heading('확인한 것과 남은 것',132)
y=para('시나리오 6쪽의 열/색 기준, 새 화면의 금액·단위와 합계 관계, 원본/변경안 수치 분리, 12개 정지 상태의 화면 구성, 기존 스킬 파일 보존을 확인했다. 프로젝트 유형 4개는 22.2억원·27건으로 맞는다.',y)
y=para('현재 결과는 같은 영상에서 고른 두 사례의 개발 시범이다. 다른 주제의 새 브리프에서도 통하는지, 실제 움직임과 음성에서 잘 읽히는지, 사용자 판단과 회사의 브랜드 기준에 맞는지는 아직 확인하지 않았다. 전편 정밀 분석도 남아 있다.',y+12)
y=heading('다음 큰 작업 - 한 가지 선택',y+20)
options=[
 ('① 원본 기록과 새 화면을 함께 검토 (추천)','두 사례에서 보존할 디자인 언어·빠진 역할·허용할 변형을 정한다. 기록과 결과를 비교해 기준을 보정하며 실제 영상 제작은 뒤로 둔다.'),
 ('② 한 장면을 짧은 모션으로 검증','계약 또는 지원의 정지안을 실제 재생 가능한 시범으로 만든다. 등장·전환·유지의 이해도를 확인하며 DB 확장은 유보한다.'),
 ('③ 다른 주제로 재사용 시험','같은 정보 관계를 가진 다른 내용의 브리프를 만들고 이 기록으로 선택·변형해본다. 주제 전이가 가능한지 보되 브랜드 마감·실모션은 유보한다.'),
 ('④ 원본 디자인 자산 기록부터 보강','입체 아이콘·실경·프레임·차트 등 재사용할 표현의 역할과 조합을 더 기록한다. 원본 스타일 보존을 우선하며 새 화면 제작은 늘리지 않는다.')]
for h,t in options:
 y=para(h,y,size=11,bold=True)+5;y=para(t,y,size=9)+14
para('보관 상태는 별도 publication-receipt.json으로 확인한다. D: 보관이 실행 전 차단되면 로컬 완성본을 제시하고 미보관 사실을 보고한다. 이번 PDF는 기존 보고서·원본·실패 기록을 대체하지 않는다.',y+4,size=9)
end();C.save()
prev=O/'report-preview';prev.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(str(P))
for i in range(len(doc)):doc[i].render(scale=1.5).to_pil().save(prev/f'page-{i+1}.png')
(O/'report-build.json').write_text(json.dumps({'path':str(P),'pages':len(doc),'sha256':hashlib.sha256(P.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print(str(P));print('pages',len(doc))
