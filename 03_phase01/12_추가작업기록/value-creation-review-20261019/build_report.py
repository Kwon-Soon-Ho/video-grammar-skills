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
O=Path(__file__).resolve().parent;R=O.parent;S=R/'value-creation-pilot-20261019'
P=R/'output/pdf/20261019_value_creation_source_language_review.pdf'
pdfmetrics.registerFont(TTFont('K','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('KB','C:/Windows/Fonts/malgunbd.ttf'))
W,H=595.28,841.89;C=canvas.Canvas(str(P),pagesize=(W,H));C.setTitle('가치창출 영상 - DB 수집 범위 정리와 원본 비교 기록');C.setAuthor('사내 영상 생성기 프로젝트')
style=ParagraphStyle('p',fontName='K',fontSize=10,leading=16,wordWrap='CJK',textColor=HexColor('#17383D'))
page=0
def para(t,y,x=38,w=519,size=10,b=False):
 s=ParagraphStyle('x',parent=style,fontSize=size,leading=size*1.6,fontName='KB' if b else 'K');p=Paragraph(t,s);_,h=p.wrap(w,730)
 assert y+h<798,(page,y,h,t[:40]);p.drawOn(C,x,H-y-h);return y+h
def title(t,sub):
 global page
 page+=1;C.setFillColor(HexColor('#087F72'));C.rect(0,H-9,W,9,fill=1,stroke=0)
 para('원본 기록 검토 / 사용자 ①+③ 혼합 결정 반영',30,size=9,b=True);para(t,51,size=21,b=True);para(sub,88,size=9)
def img(p,x,y,w=None,h=None):
 a,b=Image.open(p).size
 if w is None:w=h*a/b
 if h is None:h=w*b/a
 assert x+w<=W-30 and y+h<795
 C.drawImage(str(p),x,H-y-h,w,h);return y+h
def end():
 C.setFillColor(HexColor('#53676A'));C.setFont('K',8);C.drawString(38,25,'2026-10-19 · 비교 검토 · 새 시안/모션 제작 및 스킬 수정 보류');C.drawRightString(W-38,25,str(page));C.showPage()

title('계약: 원본에도 위계가 있다','원본과 새 시안의 차이를 찾는 비교이다. 가독성 우열을 검증한 실험은 아니다.')
para('원본 112초 / 32:9 / 원본 수치',121,size=9,b=True)
img(S/'extraction/cases/VALUE/contract/f_03360_112.000.png',38,143,w=519)
para('현재 시범 / 16:9 / 변경안 수치 / 정보 구조 검토용',301,size=9,b=True)
img(S/'proofs/A-state-5.png',94,324,w=407)
y=para('고칠 설명',568,size=13,b=True)+7
y=para('원본을 “동급 3패널”로 단순화한 설명은 부정확했다. 실제 매출은 주황색 큰 금액과 상승 아이콘으로 강조되고, 패널 너비와 정보량도 다르다. 새 시안은 위계를 처음 만든 것이 아니라 다른 방식으로 바꾼 것이다.',y)
y=para('아직 옮기지 못한 디자인',y+12,size=13,b=True)+7
para('상단 장 배지·제목 띠, 도시 배경과 정보면의 층, 프레임·숫자의 재질감, 업무 도상의 조합은 새 시안에서 빠졌다. 현재 시안은 산정값/참고값 관계 검토에는 쓰되 원본 디자인의 응용 검증 완료로 취급하지 않는다.',y)
end()

title('지원: 핵심 강조가 약해졌다','같은 총액의 분류를 구분한 것은 새 구조 제안이며, 원본의 시각 언어 이식과는 별개다.')
para('원본 150초 / 32:9 / BIM 설계 큰 구획 + 약82% 강조',122,size=9,b=True)
img(S/'extraction/cases/VALUE/project/f_04500_150.000.png',38,145,w=519)
para('현재 시범 / 9:16',305,size=9,b=True)
img(S/'proofs/B-state-5.png',38,327,h=353)
y=para('남은 관계 / 빠진 강조',324,x=258,w=299,size=13,b=True)+9
y=para('총액 22.2억원·27건과 가족사별/유형별 분류를 구분한 것은 유지할 수 있는 구조 제안이다. 다만 원본은 BIM 설계가 대부분이라는 메시지를 큰 구획·도넛·82%로 반복한다.',y,x=258,w=299)
y=para('새 안은 4개 행에 비슷한 면적을 주고 82%를 직접 말하지 않는다. 막대 길이 차이는 있지만 핵심 강조 전이가 충분한지 확인되지 않았다.',y+11,x=258,w=299)
y=para('함께 기록할 디자인 조합',y+15,x=258,w=299,size=13,b=True)+9
y=para('실적 영상/지도와 정보판의 분할, 따뜻한 프레임과 점무늬·도시 실루엣, 주항목 1개+보조 3개의 비대칭 구성. 세로화할 때 삭제·축소만 하지 않고 역할을 유지하는 재배치가 필요하다.',y,x=258,w=299)
para('비교 한계: 화면비·숫자·정보량·표현이 함께 바뀌었다. 이 비교만으로 평면형이 더 낫다고 단정하지 않는다. 사용자 결정은 원본 언어를 충실히 수집하되 이후 다른 스타일로의 활용도 열어두는 것이다.',706,size=9)
end()

title('DB 수집은 재구축 없이 끝낼 수 있다','사용자 결정: ① 원본 언어를 충실히 기록 + ③ 이후 활용에서는 스타일 변형 허용')
y=para('현재 무엇을 하고 있었나',129,size=13,b=True)+8
y=para('스킬 draft.9를 그대로 둔 채 에이전트가 원본 표본을 관찰하고 기록 구조·판단 기준을 보정한 개발 작업이다. 새 화면은 별도 시범으로 그렸다. 완성 스킬을 독립적으로 실행한 성능 평가나 정본 DB 등록 완료는 아니다.',y)
y=para('왜 새 화면까지 만들었나',y+17,size=13,b=True)+8
y=para('앞서 선택된 “두 사례의 새 기록+새 브리프 시범”에 따라 응용 가능성을 확인하려고 만들었다. 그러나 이를 DB 수집의 필수 종료 조건으로 확대하고 디자인 방향 선택을 계속 앞세울 필요는 없었다. 추가 화면 재구축·모션 제작은 현재 수집 범위에서 제외한다.',y)
y=para('수집 단계에서 확인할 것',y+17,size=13,b=True)+8
y=para('전체 사례와 레이아웃·디자인 언어·부품·전체 흐름·세부 동작을 연결한다. 요소의 존재뿐 아니라 배치·역할·강조·동반 조합을 기록한다. 반복 표현은 번호와 현재 근거·차이로 연결한다. 관측/기능 해석/새 제안과 미상·미검수 범위를 구별한다.',y)
y=para('이번 기록에서 고친 것',y+17,size=13,b=True)+8
y=para('원본 계약의 위계 설명을 정정하고 장 배지·실경/정보면·재질·핵심 강조·도상의 조합 후보를 보완했다. 원본 패널 재배치와 새 안의 핵심 위치 고정을 구별했다. 2초 표본의 모션 후보를 제작용 타이밍 템플릿으로 승격하지 않는다.',y)
y=para('다음 범위',y+17,size=13,b=True)+8
para('두 사례의 수집 기록에서 누락·미상과 재사용에 필요한 관측 보강점을 정리한다. 원본의 모든 표현을 공통 규칙으로 강제하지 않는다. 실제 제작·다른 주제 적용은 별도 요청 시 진행한다. 기존 시범·스킬 draft.9·정본 패턴은 보존했다.',y)
end();C.save()
doc=pdfium.PdfDocument(str(P));preview=O/'report-preview';preview.mkdir(exist_ok=True)
for i in range(len(doc)):doc[i].render(scale=1.5).to_pil().save(preview/f'page-{i+1}.png')
(O/'report-build.json').write_text(json.dumps({'path':str(P),'pages':len(doc),'sha256':hashlib.sha256(P.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print('3-page review report rendered:',P)
