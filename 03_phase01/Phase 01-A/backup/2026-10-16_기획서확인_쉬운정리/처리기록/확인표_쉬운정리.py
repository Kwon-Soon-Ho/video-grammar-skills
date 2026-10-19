"""Update live preparation notes from human evidence; never open video contents."""
import pathlib,json,hashlib,os,re,shutil
from urllib.parse import quote,unquote
W=pathlib.Path(__file__).resolve().parent/'후속정리_20261016';W.mkdir(exist_ok=True)
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
D=P/'Phase 01-A';S=P/'한맥 영상';ST=W/'게시안';ST.mkdir(exist_ok=True)
M=json.loads((W.parent.parent/'phase01a-prep/게시구성_명세.json').read_text('utf-8'))
docs={x['id']:x for x in json.loads((W.parent/'문서목록과_읽기결과.json').read_text('utf-8'))['documents']}
rows={int(x['id'][2:]):x for x in M['registry']};targets=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dp(n):return P/docs[f'DOC{n:03}']['path']
def lk(p,fromp,label=None):return '['+(label or p.name)+']('+quote(os.path.relpath(p,fromp.parent).replace('\\','/'),safe='/._-')+')'
def stage(rel,text):
    target=D/rel;out=ST/rel;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(text if isinstance(text,str) else json.dumps(text,ensure_ascii=False,indent=2)+'\n','utf-8')
    targets.append({'relative':rel,'before':sha(target) if target.exists() else None,'after':sha(out)})
raw_answer='실제 제작 전 원고가 너무 복잡하게 되어 있어서 완성된 영상을 기준으로 필요한 내용을 초기 기획서와 함께 비교해가며 제작함'
userrecord={'id':'사용자확인_20261016_가족사재구성원고','date':'2026-10-16','source_type':'이 대화의 사용자 직접 답변','question_scope':'가족사 7곳의 초기기획서_*_2026년_경영보고_v4.docx 작성 성격','verbatim_answer':raw_answer,'interpretation':'복잡한 제작 전 원고를 보완하기 위해 완성 영상과 초기 기획서를 대조해 필요한 내용을 재구성한 자료','confirmed_scope':['문서 작성 성격과 사용한 비교 자료'],'not_confirmed':['어느 MP4가 최종 납품본인지','각 MP4와 문서의 모든 내용이 일치하는지','수치·레이아웃·모션의 독립 정답','회사 사용권한·외부 AI/API 처리 권한'],'documents':[]}
families={2:(30,26,[5,14,15,21]),3:(36,32,[17]),4:(41,37,[3,8,9,10,11,18]),5:(46,42,[1,4,19]),6:(51,47,[12,13,20]),7:(56,52,[6,16,22]),8:(61,57,[2,23,24])}
cards=[]
for k,row in rows.items():
    src=S/row['source_folder'];videos=sorted(p for p in src.iterdir() if p.is_file() and p.suffix.lower()=='.mp4')
    c={'id':row['id'],'number':k,'project':row['source_folder'],'videos':[p.relative_to(P).as_posix() for p in videos],'recommendation_status':'추천안 — 사용자 선택 전','primary_documents':[],'reference_documents':[],'final_delivery_confirmed':False,'video_document_match_confirmed':False,'video_content_opened':False}
    if k in families:
        n,ppt,initial=families[k];c.update(category='가족사 7곳',primary_documents=[dp(n).relative_to(P).as_posix()],reference_documents=[dp(ppt).relative_to(P).as_posix()]+[dp(x).relative_to(P).as_posix() for x in initial],recommendation='같은 회사 폴더의 MP4를 기준 영상 후보로, v4 Word를 내용 파악용 재구성 원고로 묶는다. v03 PPT와 초기 문서는 비교·수정 이력 참고로 둔다.',basis='같은 회사명·보고 주제·폴더의 자료이며, v4 작성 성격은 사용자 설명으로 확인됐다. 실제 영상 내용은 대조하지 않았다.',confirm='이 MP4를 앞으로 사용할 기준 영상으로 지정해도 되는지, 영상이 바뀌어야 하는 회사만 확인.',document_nature_confirmed=True)
        userrecord['documents'].append({'id':row['id'],'path':docs[f'DOC{n:03}']['path'],'sha256':sha(dp(n))})
    elif k in [9,11,12,17,18,19,20]:
        n={9:62,11:64,12:65,17:66,18:67,19:68}.get(k)
        primary=dp(n) if n else src/'가족사 소개 영상 기획서.png'
        c.update(category='같은 폴더의 1:1 후보',primary_documents=[primary.relative_to(P).as_posix()],recommendation='아래 영상 1개와 같은 폴더의 문서를 한 묶음의 작업 후보로 둔다.',basis='폴더·제목과 문서 주제가 대응하는 후보다. 이 사실만으로 최종본·실제 일치를 확정하지 않았다.',confirm='이 조합에서 바꿀 영상 또는 문서가 있는지 확인.')
        if k==9:c['confirm']='이 조합 유지 여부. PDF의 변경 전/후 중 실제 적용 원고가 따로 있다면 그 부분만 알려 주세요.'
        if k==12:
            c['recommendation']='MP4와 PDF 제작 의견을 같은 프로젝트 후보로 묶되 PDF는 확정 시나리오가 아닌 제작·수정 요청 자료로 표시한다.'
            c['confirm']='이 PDF가 최종 적용된 요구사항인지 확인. 실제 제작 규격은 PDF 수치가 서로 맞지 않아 이후 확인 대상으로 따로 둔다.'
        if k==20:c['confirm']='이 PNG와 영상의 프로젝트 대응 여부. 작은 원고·수정 표시가 반영된 최종 내용은 아직 확인하지 않았다.'
    elif k in range(13,17):
        c.update(category='홈페이지 클립',recommendation=f'폴더 안의 클립 {len(videos)}개를 모두 별도 원본으로 보존하고 같은 제품 묶음으로 등록한다. 이 중 하나만 최종본으로 고르지 않는다.',basis='번호와 제품 폴더 기준의 정리 제안이다. 기능·화면 내용이나 변형판 여부는 영상 미열람으로 미확인.',confirm='모두 쓸 자료인지, 제외할 파일만 있는지 확인. 없는 기획서는 다시 만들 필요 없이 “별도 문서 없음”으로 등록할 수 있다.')
    elif k==1:
        c.update(category='구분이 필요한 자료',reference_documents=[dp(x).relative_to(P).as_posix() for x in range(1,25)],recommendation='초기 폴더의 장헌·피티씨 MP4 2개는 비교 참고 후보로 남기고, 현재 작업 기준 후보는 각 회사 폴더의 자료005·자료002 MP4로 제안한다.',basis='초기 폴더라는 보관 위치와 동일 회사 자료의 별도 존재에 따른 정리 제안이다. 두 영상이 구본·중복인지 확인한 것은 아니다.',confirm='이 2개를 비교 참고로만 둘지, 별도 작업 대상으로도 쓸지 확인.')
    elif k==10:
        c.update(category='구분이 필요한 자료',primary_documents=[dp(63).relative_to(P).as_posix()],recommendation='크레인 영상에는 크레인 작업반경·인양 안정성 콘티를 대응 후보로 둔다. 기상 악화 영상은 다른 주제의 별도 자료로 유지하며 대응 기획서는 미확인으로 둔다.',basis='문서 제목과 추출 본문에서 크레인 설명을 확인했다. “기상 악화/해상풍” 제목의 별도 문서는 현재 목록에서 찾지 못했다.',confirm='크레인-콘티 조합 유지 여부와 기상 악화용 별도 기획서가 있는지만 확인.')
    elif k==21:
        c.update(category='구분이 필요한 자료',primary_documents=[dp(69).relative_to(P).as_posix(),dp(70).relative_to(P).as_posix()],recommendation='HWP는 내용·한영 원고, Excel은 화면 설명·국문 원고 버전·변경 이력을 보는 자료로 역할을 나눈다. 둘 사이 충돌이 있으면 임의로 최신값을 고르지 않는다.',basis='문서 본문의 구성에 따른 역할 추천이다. 파일명 날짜로 우선순위를 확정하지 않았다.',confirm='HWP=내용 원고 / Excel=화면·이력이라는 역할 구분이 맞는지, 실제 적용 문서가 따로 있는지만 확인.')
    elif k==22:
        c.update(category='구분이 필요한 자료',primary_documents=[dp(71).relative_to(P).as_posix()],recommendation='싱글·듀얼 MP4를 서로 다른 상영 버전 후보로 보존한다. HWP는 두 버전의 공통 내용 참고 후보로 두고, 화면·편집이 동일하다고 합치지 않는다.',basis='파일명에는 싱글/듀얼 표시가 있고 문서 주제는 센터 비전이다. 두 파일의 실제 관계와 공통 원고 여부는 미확인.',confirm='두 버전 모두 사용할지와 HWP를 공통 원고로 연결해도 되는지 확인.')
    elif k==23:
        c.update(category='구분이 필요한 자료',primary_documents=[dp(72).relative_to(P).as_posix()],recommendation='제목이 직접 대응하는 “221031_한 번 생각해봅시다.mp4”와 HWP를 우선 조합 후보로 둔다. “새로운시대준비된우리_Full영상.mp4”는 별도 참고 후보로 둔다.',basis='시나리오는 “새로운 시대 준비된 우리” 중 “한번 생각해봅시다” 소개라고 명시한다. 전체/발췌 포함 관계를 영상으로 확인한 것은 아니다.',confirm='제안한 우선 조합이 맞는지, Full영상도 별도 대상으로 사용할지만 확인.')
    else:raise ValueError(k)
    cards.append(c)
cp=D/'00_진행안내/06_영상과기획서_추천조합.md'
intro='''# 영상과 기획서 — 제가 묶어 놓은 추천 조합

**파일명을 다시 찾거나 입력할 필요 없이, 바꿀 부분만 알려 주세요.**

예: `가족사 7곳은 추천 조합 그대로. 센터는 싱글만. 홈페이지 클립은 모두 보관. 대호지교 기상 악화는 문서 없음.`

이 표는 **향후 쓸 자료를 묶는 추천안**입니다. 영상 내용을 열어 확인한 결과나 최종 납품본 인증이 아닙니다. 승인을 받아도 실제 영상 분석·스킬 개발을 자동 시작하지 않습니다.

## 이미 확인된 내용

가족사 7곳의 v4 Word는 제작 전의 복잡한 원고를 보완하기 위해 **완성 영상과 초기 기획서를 비교하며 필요한 내용을 재구성한 자료**입니다. 사용자 설명으로 문서 성격을 확인했습니다. 앞으로는 `재구성 원고 v4`로 부르고 실제 파일명은 유지합니다. 영상에서 만든 자료이므로 독립 평가의 정답으로 자동 사용하지 않습니다.

## 1. 먼저 확인할 가족사 7곳

**추천: 아래 MP4 + 재구성 원고 v4를 작업 기준 후보로 묶고, 초기 문서·PPT는 참고 자료로 둡니다.** 지금은 이 7개 조합에서 바뀌어야 할 것만 확인하면 됩니다.

| 회사 | 기준 영상 후보 | 내용 파악용 재구성 원고 | 판단 상태 |
|---|---|---|---|
'''
family_names={2:'피티씨',3:'산하종합기술',4:'삼안',5:'㈜장헌',6:'장헌산업',7:'한라산업개발',8:'한맥기술'}
for c in cards:
    k=c['number']
    if k in families:intro+='| '+family_names[k]+' | '+lk(P/c['videos'][0],cp)+' | '+lk(P/c['primary_documents'][0],cp)+' | 조합 선택 대기; 원고 성격 확인됨 |\n'
intro+='\n### 회사별 보조 자료 — 선택할 필요 없이 제가 참고로 분리했습니다\n\n'
for c in cards:
    if c['number'] not in families:continue
    intro+='- **'+family_names[c['number']]+'**: '+' / '.join(lk(P/x,cp) for x in c['reference_documents'])+'\n'
intro+='\n이 보조 자료가 영상에 전부 적용됐다는 뜻은 아닙니다. 수정 전·후 원고와 화면 참고를 구분하기 위한 배치입니다.\n'
for category,title in [('같은 폴더의 1:1 후보','2. 영상과 문서가 한 개씩 있는 후보'),('구분이 필요한 자료','3. 제가 구분해 둔 예외 자료'),('홈페이지 클립','4. 홈페이지 클립 — 18개 모두 목록에 포함')]:
    intro+='\n## '+title+'\n\n'
    for c in cards:
        if c['category']!=category:continue
        intro+='### '+c['id']+' · '+c['project']+'\n\n**추천 정리:** '+c['recommendation']+'\n\n'
        intro+='**영상'+('들' if len(c['videos'])>1 else '')+'**\n\n'
        for v in c['videos']:intro+='- '+lk(P/v,cp)+'\n'
        intro+='\n**연결할 문서 후보**\n\n'
        if c['primary_documents']:
            for v in c['primary_documents']:intro+='- '+lk(P/v,cp)+'\n'
        else:intro+='- '+('혼합 초기 문서 24개. 회사별 관련 문서는 위 가족사 보조 자료로 구분했고, 06. 센터.pptx 등 나머지는 초기 폴더에 그대로 둡니다.' if c['number']==1 else '같은 폴더에서 별도 기획서 미확인. 다른 제품 홍보 문서를 임의 연결하지 않습니다.')+'\n'
        intro+='\n**이렇게 묶은 이유:** '+c['basis']+'\n\n**바꿀 부분만 알려 주세요:** '+c['confirm']+'\n\n'
intro+='''## 답변 방법

파일명 전체 대신 회사명·자료ID와 변경점만 답하면 됩니다. 추천을 받아들여도 ‘최종 납품본 확인’과 ‘영상-문서 내용 일치’는 따로 남깁니다.

- **A. 가족사 7곳을 추천 조합대로 작업 기준 후보로 정리 (추천)** — 원고 성격은 확인됐고, 영상의 실제 내용은 이후 별도 검수합니다.
- **B. 가족사 중 일부 영상만 교체** — 회사명과 대신 쓸 파일만 알려 주세요.
- **C. 영상은 두고 문서 역할·우선순위 수정** — 회사명과 변경점만 알려 주세요.
- **D. 가족사 기준 후보 선정 보류** — 현재 파일과 추천안을 그대로 보관합니다.

나머지 16개 묶음은 한 번에 답하지 않아도 됩니다. 필요한 프로젝트부터 ‘추천대로 / 변경점 / 모름’만 알려 주세요. 자료별 파일·근거 연결은 이미 제가 정리했습니다.

## 다음에 확인할 내용

실제 검수 담당자, 문서의 수치 충돌, PG 최종 송출 규격, 외부 AI/API 처리 범위는 [남은 확인 사항](04_사용자확인_모음.md)에 남겨 두었습니다. 지금 파일 조합을 확인할 때 전부 해결할 필요는 없습니다.
'''
stage('00_진행안내/06_영상과기획서_추천조합.md',intro)
stage('00_진행안내/06_영상과기획서_추천조합.json',{'date':'2026-10-16','status':'proposed_not_approved','video_file_count':41,'card_count':23,'video_analysis_started':False,'cards':cards})
stage('00_진행안내/07_재구성원고_사용자확인.json',userrecord)
stage('00_진행안내/07_재구성원고_사용자확인.md','# 가족사 재구성 원고의 작성 성격 확인\n\n2026-10-16 / 사용자 직접 설명\n\n> '+raw_answer+'\n\n확인한 의미: '+userrecord['interpretation']+'입니다. 가족사 7곳의 v4 Word에 적용하며 파일명은 바꾸지 않습니다.\n\n이 답변은 어느 MP4가 최종 납품본인지, 영상과 문서가 전부 일치하는지, 외부 AI/API에 올려도 되는지를 확인한 답변은 아닙니다. 영상에서 재구성한 원고를 독립 정답으로 자동 채택하지 않습니다.\n\n문서별 현재 버전 해시는 같은 이름의 JSON에 기록했습니다. 영상은 열지 않았습니다.\n')
oldrole='문서는 영상 생성용 TTS 본문과 비낭독 참조 데이터 표를 구분한다. 본문 설명상 최종 영상을 정리한 자료이며, 제작 전 시나리오인지·사후 재구성인지와 대응 영상은 사용자 확인 전이다.'
newrole='문서는 TTS 본문과 비낭독 참조 데이터 표를 구분한다. 사용자 설명에 따라, 복잡한 제작 전 원고를 보완하려고 완성 영상과 초기 기획서를 비교해 재구성한 원고로 기록한다. 문서 성격은 확인됐으며 특정 MP4와의 내용 일치는 별도 미확인이다.'
for c in cards:
    k=c['number'];folder=rows[k]['folder'];base=D/folder
    text=(base/'00_자료설명.md').read_text('utf-8')
    evid=(base/'03_기획서검토_근거.md').read_text('utf-8');record=json.loads((base/'03_기획서검토_근거.json').read_text('utf-8'))
    if k in families:
        assert oldrole in text and oldrole in evid
        text=text.replace(oldrole,newrole).replace('Q01, Q02, Q04, Q05','Q01, Q04, Q05')
        evid=evid.replace(oldrole,newrole)
        record['facts'][1]['text']=newrole;record['facts'][1]['status']='문서 성격: 사용자 설명으로 확인 / 영상 일치: 미확인';record['facts'][1]['human_confirmation_id']=userrecord['id']
        record['human_confirmations']=[{'id':userrecord['id'],'confirmed':'작성 성격: 완성 영상과 초기 기획서 대조 후 재구성','not_confirmed':'개별 MP4와 문서의 실제 일치·최종 납품본 여부'}]
        record['questions']=[q for q in record['questions'] if q!='Q02']
        evid+='\n## 사용자 설명으로 추가 확인 — 2026-10-16\n\n> '+raw_answer+'\n\n원고의 작성 성격만 확인했습니다. 특정 영상의 일치·최종성·사용권한을 자동 확인하지 않습니다. [확인 기록](../../../00_진행안내/07_재구성원고_사용자확인.md) 참조.\n'
    text+='\n## 영상·문서 추천 조합 — 선택 전\n\n'+c['recommendation']+'\n\n변경점 확인: '+c['confirm']+'\n\n파일명 전체와 링크를 [쉬운 확인표](../../../00_진행안내/06_영상과기획서_추천조합.md)에 함께 배치했습니다. 추천안은 최종본 승인이나 분석 착수 지시가 아닙니다.\n'
    record['proposed_pairing']=c
    stage(folder+'/00_자료설명.md',text);stage(folder+'/03_기획서검토_근거.md',evid);stage(folder+'/03_기획서검토_근거.json',record)
questions='''# 남은 확인 사항 — 파일 조합은 제가 정리했습니다

**파일명을 다시 찾고 문서ID를 대조할 필요가 없도록 [영상·기획서 추천 조합](06_영상과기획서_추천조합.md)을 만들었습니다.** 먼저 그 표에서 바뀔 부분만 알려 주세요.

## Q01. 앞으로 쓸 자료 선택 — 추천 조합으로 확인

영상 41개와 문서를 23개 프로젝트 묶음으로 나란히 배치했습니다. 가족사 7곳을 먼저 확인하고, 나머지는 필요한 프로젝트부터 확인하면 됩니다. 파일명 전체 대신 `삼안은 그대로 / 센터는 싱글만 / 자료010 기상 악화는 문서 없음`처럼 답하면 됩니다.

추천 조합의 승인과 최종 납품 여부·내용 일치 검수는 구분합니다. 자료 선택만으로 실제 분석을 시작하지 않습니다.

## Q02. 가족사 v4 원고의 성격 — 답변 반영 완료

사용자 답변: 실제 제작 전 원고가 복잡해서, 완성 영상과 초기 기획서를 비교하며 필요한 내용을 재구성했다.

따라서 가족사 7곳의 v4 Word는 `재구성 원고`로 기록했습니다. 더 이상 같은 질문을 반복하지 않습니다. [원문 답변과 확인 범위](07_재구성원고_사용자확인.md).

## Q03. 조합에서 실제로 다른 부분만 확인

- 초기 폴더(자료001): 장헌·PTC 영상 2개는 비교 참고로 두고, 각 회사 폴더의 MP4를 우선 후보로 제안했습니다. 다르게 쓸 때만 알려 주세요.
- 가치창출(자료009): 영상+PDF를 묶었습니다. PDF 변경 전/후 중 적용 원고가 다르면 그 부분만 확인하면 됩니다.
- 대호지교(자료010): 크레인 영상+크레인 콘티를 묶고 기상 악화 영상은 별도 문서 미확인으로 뒀습니다. 기상 악화용 문서가 있거나 연결이 다르면 알려 주세요.
- PG(자료012): PDF는 제작·수정 의견 자료로 표시했습니다. 최종 규격은 문서의 치수·해상도·화면비가 맞지 않아 이후 실제 송출 가이드로 확인해야 합니다.
- 홈페이지(자료013~016): 클립 18개를 모두 보존하고 기획서 미확인으로 뒀습니다. 빼야 할 클립이나 별도 원고가 있을 때만 알려 주세요.
- 가족사 소개(자료020): 영상+PNG 기획안을 묶었습니다. 작은 원고·수정 사항의 최종 반영 여부는 미검토입니다.
- 노듈러거더(자료021): HWP는 내용·한영 원고, Excel은 화면·수정 이력으로 구분했습니다. 실제 역할이나 적용 버전이 다르면 알려 주세요.
- 센터(자료022): 싱글·듀얼을 별도 영상으로 유지하고 HWP를 공통 내용 참고 후보로 뒀습니다. 한 버전만 쓰거나 원고가 다르면 알려 주세요.
- 한번 생각해 봅시다(자료023): 제목이 대응하는 221031 영상+HWP를 우선 후보로, Full영상은 별도 참고로 뒀습니다. 이 구분이 다르면 알려 주세요.

## Q04. 검수 담당·실제 시청 환경 — 해당 자료를 쓸 때 확인

실제 디자인/내용 확인 담당자와 시청자·행사·홈페이지·교육 등 사용처는 문서로 확정할 수 없는 부분만 남았습니다. 모든 자료를 한 번에 작성할 필요는 없습니다. 첫 작업 대상을 정한 뒤 그 자료의 담당·환경부터 확인하면 됩니다.

## Q05. 외부 AI/API 처리 범위 — 실제 외부 처리 전에 별도 확인

이번 작업은 로컬 문서 정리뿐이며 업로드하지 않았습니다. DOC022(초기 한라 보고서)의 ‘“1급” 대외비 문서’, 가치창출 PDF와 한번 생각해 봅시다 HWP의 ‘대외비(2등급)’ 표시는 해당 문서 단위로 기록했습니다. 표시가 없는 자료도 공개 가능으로 자동 판단하지 않습니다.

영상·기획서별 개인 구독 AI/API 가능 여부와 가림 범위는 실제 처리 대상을 정한 뒤 근거와 함께 확인합니다. 지금 자료 조합을 확인하는 답변을 외부 처리 허가로 확대하지 않습니다.
'''
stage('00_진행안내/04_사용자확인_모음.md',questions)
state=json.loads((D/'00_진행안내/기획서검토_현황.json').read_text('utf-8'));state.update({'human_document_nature_confirmations':{'family_reconstructed_v4':7,'record':'07_재구성원고_사용자확인.json'},'pairing_proposals_prepared':23,'video_candidates_in_proposals':41,'pairing_proposals_approved':False,'final_selection_complete':False,'pairing_complete':False,'analysis_started':False,'skill_development_started':False})
stage('00_진행안내/기획서검토_현황.json',state)
index=(D/'00_진행안내/05_기획서검토_색인.md').read_text('utf-8')
index=index.replace('# 기획서 사전 검토 색인 — 2026-10-16','# 기획서 사전 검토 색인 — 2026-10-16\n\n**확인은 [영상·기획서 추천 조합](06_영상과기획서_추천조합.md)에서 시작하세요. 가족사 7곳 v4는 사용자 설명을 반영해 재구성 원고로 구분했습니다.**')
stage('00_진행안내/05_기획서검토_색인.md',index)
guide=(D/'00_먼저읽기.md').read_text('utf-8')
guide=guide.replace('2. 해당 폴더의 00_자료설명.md에서 문서 기반 요약을 읽고, [사용자 확인 모음](00_진행안내/04_사용자확인_모음.md)에 최종 영상·대응 문서 등 남은 답변을 줍니다.','2. [영상·기획서 추천 조합](00_진행안내/06_영상과기획서_추천조합.md)에서 제가 묶은 파일을 확인하고 바뀔 부분만 알려 주세요. 파일명을 다시 찾아 적을 필요가 없습니다.')
guide+='\n가족사 7곳 v4 Word는 완성 영상과 초기 기획서를 비교해 만든 **재구성 원고**로 사용자 설명을 반영했습니다. 작성 성격 확인과 기준 영상 선택·실제 내용 일치 검수는 구분합니다.\n'
stage('00_먼저읽기.md',guide)
report='''# 자료 확인 부담을 줄인 후속 정리

2026-10-16

기존 표는 문서ID를 다시 찾아 파일 대응을 사용자가 직접 구성해야 했다. 이를 23개 추천 조합과 실제 파일명·링크로 바꿨다. 영상 41개 모두 누락 없이 포함했고, 가족사 7곳→1:1 후보→예외 자료→홈페이지 클립으로 나눴다. 사용자는 바꿀 부분만 답할 수 있다.

가족사 7곳의 v4 작성 성격은 사용자 설명을 반영해 완성 영상·초기 기획서 대조 후 재구성한 원고로 기록했다. 현재 파일 버전 해시와 직접 답변을 함께 남겼다. 영상에서 만든 원고를 독립 평가 정답으로 자동 사용하지 않는다.

추천 조합은 같은 폴더·제목·문서 내용으로 구성한 작업 후보이며 아직 선택·실제 일치가 확인된 것이 아니다. 홈페이지 제품 클립을 경쟁 최종본으로 하나만 고르지 않았고, 대호지교 기상 악화 영상을 크레인 콘티에 억지 연결하지 않았다. 싱글·듀얼과 전체·발췌 후보도 별개로 유지했다.

자체 반대 관점 점검에서 ‘추천’을 사실 승인으로 확대할 위험, 원고 작성 성격 확인을 영상 일치 확인으로 확대할 위험, 사후 원고를 독립 정답으로 사용할 위험을 검토했다. 추천 상태·사용자 확인 범위를 별도 필드로 보완했다. 독립 검토자를 새로 실행한 것은 아니다.

최종 납품 여부, 실제 영상 내용·규격, 사용권한은 확인되지 않았다. 영상 파일은 열거나 분석하지 않았고 새 스킬도 개발하지 않았다. 과거 검수 보고서와 백업은 이력으로 보존하며 이번 수정은 현재 안내·자료 설명에만 반영했다.
'''
stage('05_결과보고/02_사용자답변과_추천조합_보완.md',report)
(W/'게시명세.json').write_text(json.dumps({'targets':targets,'cards':cards,'human_record':userrecord},ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({'staged_files':len(targets),'groups':len(cards),'videos':sum(len(c['videos']) for c in cards),'human_document_type_confirmed':len(userrecord['documents'])},ensure_ascii=False))
