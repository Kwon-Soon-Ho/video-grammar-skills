from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
HERE=Path(__file__).resolve().parent;OUT=HERE/'proofs';OUT.mkdir(exist_ok=True)
BG='#F5F7F4';INK='#163A3D';MUTED='#5A7071';GREEN='#087F72';PALE='#E2EEE8';LINE='#CADAD4';WHITE='#FFFFFF';GOLD='#B8773F';CREAM='#F8F4EC'
FONTS={}
def font(size,bold=False):
 key=(size,bold)
 if key not in FONTS:FONTS[key]=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf',size)
 return FONTS[key]
def txt(d,xy,s,size=30,color=INK,bold=False,maxwidth=None):
 f=font(size,bold);x,y=xy
 lines=[]
 for raw in s.split('\n'):
  if maxwidth is None:lines.append(raw);continue
  line=''
  for char in raw:
   if line and d.textlength(line+char,font=f)>maxwidth:lines.append(line.rstrip());line=char.lstrip()
   else:line+=char
  lines.append(line)
 for line in lines:d.text((x,y),line,font=f,fill=color,anchor='lt');y+=int(size*1.45)
 return y
def box(d,b,fill=WHITE,outline=None,r=16):d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=2)
def footer(d,w,h):
 d.line((64,h-54,w-64,h-54),fill=LINE,width=2)
 txt(d,(64,h-36),'디자인·모션 시범안  |  시나리오 변경안 기준  |  실제 제작·음성 싱크 미검증',16,MUTED)
def amount(d,x,y,value,size=150,color=GREEN,unit='억원'):
 txt(d,(x,y),value,size,color,True)
 width=d.textlength(value,font=font(size,True));txt(d,(x+width+18,y+size-48),unit,36,color,True)
def contract(stage=5):
 im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1600,12),fill=GREEN)
 txt(d,(80,63),'계약 부문의 가치창출',46,INK,True)
 txt(d,(82,135),'2026년 1~9월  ·  기준이 다른 지표는 구분해서 읽습니다',25,MUTED)
 d.line((80,195,1520,195),fill=LINE,width=2)
 txt(d,(80,248),'가치창출금액에 반영한 매출',31,GREEN,True)
 if stage>=1:
  amount(d,80,315,'12.9',180)
  txt(d,(87,552),'실제로 발생한 매출을 반영했습니다.',30,INK)
 else:txt(d,(85,370),'매출 기준으로\n성과를 보여줍니다.',60,INK,True)
 d.line((965,250,965,655),fill=LINE,width=2)
 if stage>=2:
  box(d,(1020,245,1520,425),WHITE,None,18)
  txt(d,(1050,273),'수주  /  참고지표',27,MUTED,True)
  amount(d,1050,322,'17.6',72,INK)
 if stage>=3:
  box(d,(1020,452,1520,632),'#EAEDEA',None,18)
  txt(d,(1050,480),'계약 수행 투입비용  /  별도 표시',23,MUTED,True)
  amount(d,1050,529,'8.4',72,INK)
 if stage>=4:
  box(d,(80,695,1520,795),PALE,None,9)
  txt(d,(108,721),'수주와 매출은 중복 합산하지 않습니다.',28,INK,True)
  txt(d,(109,760),'이 화면은 손익이나 순이익을 산출한 결과가 아닙니다.',22,MUTED)
 footer(d,1600,900);return im
def project(mode='types',stage=5):
 im=Image.new('RGB',(900,1600),CREAM);d=ImageDraw.Draw(im)
 d.rectangle((0,0,900,12),fill=GOLD)
 txt(d,(64,62),'프로젝트 지원',48,INK,True)
 txt(d,(65,133),'2026년 1~9월  ·  외부 대체비용 관점',25,MUTED)
 d.line((64,192,836,192),fill=LINE,width=2)
 txt(d,(64,230),'실제 투입비용 기준의 가치',30,GOLD,True)
 if stage>=1:
  amount(d,60,292,'22.2',145,GOLD)
  txt(d,(67,470),'총 27건의 전문업무 지원',32,INK,True)
  txt(d,(68,527),'직접 매출과는 구분합니다.',25,MUTED)
 else:txt(d,(65,300),'전문인력 지원을\n가치로 기록합니다.',57,INK,True)
 if stage>=2:
  d.line((64,602,836,602),fill=LINE,width=2)
  title='가족사별로 본 지원' if mode=='families' else '업무유형별로 본 지원'
  txt(d,(64,648),title,33,INK,True)
  txt(d,(65,708),'같은 22.2억원의 분류 기준을 바꿔 봅니다.',23,MUTED)
  if mode=='families':
   totalw=772;leftw=totalw*15.5/22.2
   d.rectangle((64,785,64+leftw,855),fill=GREEN);d.rectangle((64+leftw,785,836,855),fill=GOLD)
   txt(d,(64,904),'한맥기술',32,GREEN,True);txt(d,(555,904),'15.5억원',38,GREEN,True)
   txt(d,(65,962),'전체 지원금액의 약 70%',25,MUTED)
   d.line((64,1035,836,1035),fill=LINE,width=2)
   txt(d,(64,1085),'삼안',32,GOLD,True);txt(d,(585,1085),'6.7억원',38,GOLD,True)
  else:
   rows=[('BIM 설계','18.2','5',GREEN),('BIM 지원','1.5','7','#4B8B9A'),('해외사업 지원','1.2','1','#527CA0'),('디자인 지원','1.3','14',GOLD)]
   visible=1 if stage==3 else 4
   for i,(name,val,count,col) in enumerate(rows[:visible]):
    yy=783+i*139
    txt(d,(64,yy),name,30,INK,True)
    txt(d,(477,yy),val+'억원',34,col,True)
    txt(d,(714,yy+3),count+'건',26,MUTED)
    d.rounded_rectangle((64,yy+62,836,yy+81),radius=9,fill='#E4E3DA')
    d.rounded_rectangle((64,yy+62,64+772*float(val)/22.2,yy+81),radius=9,fill=col)
 if stage>=5:
  box(d,(64,1390,836,1498),'#EEE8DB',None,12)
  txt(d,(88,1412),'가족사별·업무유형별 금액은',24,INK,True)
  txt(d,(88,1450),'같은 총액의 다른 분류이며 더하지 않습니다.',23,MUTED)
 footer(d,900,1600);return im
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 frames=[]
 a_specs=[(0,'0~1초','분류 기준 먼저 제시'),(1,'1~3.5초','매출12.9를 먼저 정착'),(2,'3.5~5.5초','수주17.6은 참고로 추가'),(3,'5.5~8초','비용8.4는 별도 추가'),(4,'8~10초','중복합산 금지 설명'),(5,'10~14초','최종 상태 유지')]
 b_specs=[('families',0,'0~1초','프로젝트 지원 맥락'),('families',1,'1~3초','22.2억원·27건 정착'),('families',2,'3~7초','가족사별 분류 제시'),('types',3,'7~10초','총액 유지·분류 기준 변경'),('types',4,'10~15초','업무유형별 행 추가'),('types',5,'15~20초','동일 총액·중복합산 금지')]
 for i,(stage,t,desc) in enumerate(a_specs):
  p=OUT/f'A-state-{i}.png';contract(stage).save(p);frames.append({'case':'A','index':i,'path':str(p),'sha256':sha(p),'time_proposed':t,'description':desc,'status':'static storyboard frame; motion not rendered'})
 for i,(mode,stage,t,desc) in enumerate(b_specs):
  p=OUT/f'B-state-{i}.png';project(mode,stage).save(p);frames.append({'case':'B','index':i,'path':str(p),'sha256':sha(p),'time_proposed':t,'description':desc,'status':'static storyboard frame; motion not rendered'})
 for case in ['A','B']:
  subset=[f for f in frames if f['case']==case];portrait=case=='B';tw,th=(600,338) if not portrait else (310,551);cols=2 if not portrait else 3
  sh=Image.new('RGB',(cols*(tw+24)+24,((len(subset)+cols-1)//cols)*(th+90)+24),'#E8EFED');d=ImageDraw.Draw(sh)
  for i,f in enumerate(subset):
   x=24+(i%cols)*(tw+24);y=24+(i//cols)*(th+90)
   sh.paste(Image.open(f['path']).resize((tw,th)),(x,y));txt(d,(x,y+th+10),f['time_proposed'],20,INK,True)
   txt(d,(x,y+th+42),f['description'],18,MUTED,maxwidth=tw)
  sh.save(OUT/f'{case}-storyboard.png')
 (HERE/'proof-index.json').write_text(json.dumps({'frames':frames,'actual_motion_rendered':False,'numbers_basis':'effective scenario PDF; not source video values','readability_or_comprehension_user_test':'not performed'},ensure_ascii=False,indent=2),encoding='utf-8')
 print('12 storyboard frames and2 contact sheets created')
if __name__=='__main__':main()
