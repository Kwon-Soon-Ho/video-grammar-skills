import pathlib,json,hashlib,re,os,shutil
from urllib.parse import quote,unquote
ROOT=pathlib.Path(__file__).resolve().parent;W=ROOT/'가족사후보선택_20261016';W.mkdir(exist_ok=True);ST=W/'게시안';ST.mkdir(exist_ok=True)
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');D=P/'Phase 01-A'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lk(p,base):return '['+p.name+']('+quote(os.path.relpath(p,base.parent).replace('\\','/'),safe='/._-')+')'
targets=[]
def stage(rel,data):
    p=D/rel;s=ST/rel;s.parent.mkdir(parents=True,exist_ok=True);s.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8');targets.append({'relative':rel,'before':sha(p) if p.exists() else None,'after':sha(s)})
m=json.loads((D/'00_진행안내/06_영상과기획서_추천조합.json').read_text('utf-8'));before_cards=json.loads(json.dumps(m['cards']))
selection={'id':'사용자선택_20261016_가족사7곳_기준후보_A','date':'2026-10-16','source':'이 대화의 사용자 직접 답변','answer':'A. 추천 조합대로 작업 기준 후보를 정리하기 (추천)','selected_scope':'자료002~008: 회사별 제시한 MP4를 작업 기준 영상 후보, 각 v4 Word를 재구성 원고, PPT·초기 문서를 비교 참고로 등록','not_authorized_or_confirmed':['실제 영상 분석 착수','분석 스킬 개발','스킬 기본 전환','외부 업로드','최종 납품본 여부나 모든 영상 내용의 일치'],'other_groups_status':'나머지 16개 묶음은 추천안 상태 유지','items':[]}
for c in m['cards']:
    if c['number'] not in range(2,9):continue
    assert len(c['videos'])==len(c['primary_documents'])==1 and not c.get('working_candidate_selected',False)
    c.update({'recommendation_status':'작업 기준 후보 등록 완료 — 사용자 A안 선택','working_candidate_selected':True,'selection_record_id':selection['id'],'confirm':'작업 기준 후보 선택 완료. 실제 영상 내용 일치와 최종 납품 여부는 미확인 상태로 보존.'})
    v=P/c['videos'][0];doc=P/c['primary_documents'][0]
    selection['items'].append({'id':c['id'],'project':c['project'],'video':c['videos'][0],'video_identification':{'bytes':v.stat().st_size,'mtime_ns':v.stat().st_mtime_ns,'content_opened':False},'reconstructed_script':c['primary_documents'][0],'script_sha256':sha(doc),'reference_documents':c['reference_documents'],'working_candidate_selected':True,'final_delivery_confirmed':False,'video_document_match_confirmed':False})
    folder=next((D/'01_입력자료/01_기존자료_등록').glob(c['id']+'_*'));rel=folder.relative_to(D).as_posix()
    desc=(folder/'00_자료설명.md').read_text('utf-8')
    assert '2. 사용할 최종 영상의 파일명·위치: 미정' in desc
    desc=desc.replace('2. 사용할 최종 영상의 파일명·위치: 미정','2. 작업 기준 영상 후보(사용자 선택): '+lk(v,folder/'00_자료설명.md'))
    desc=desc.replace('   - 최종 납품·배포본 확인: 미확인 — Q01 답변 대기','   - 최종 납품·배포본 확인: 미확인 — 작업 기준 후보 선택과 별도이며 영상 내용은 미검토')
    desc=desc.replace(' — 주 문서·대응 버전은 사용자 확인 대기',' — v4는 재구성 원고, PPT는 비교 참고로 역할 등록 완료. 실제 내용 일치는 별도 미확인')
    desc=desc.replace('사용자 확인: Q01, Q04, Q05','남은 확인: Q04, Q05').replace('아직 어떤 항목도 자동 승인하지 않았습니다.','작업 기준 후보는 사용자 A안 선택을 반영했고, 검수 담당·외부 처리 범위는 미정입니다.')
    desc=desc.replace('## 영상·문서 추천 조합 — 선택 전','## 영상·문서 작업 기준 후보 — 사용자 선택 반영')
    desc=desc.replace('변경점 확인: 이 MP4를 앞으로 사용할 기준 영상으로 지정해도 되는지, 영상이 바뀌어야 하는 회사만 확인.','사용자 선택: 제시한 MP4 + v4 재구성 원고 + 초기 문서·PPT 참고의 조합으로 작업 기준 후보 등록 완료.')
    desc=desc.replace('추천안은 최종본 승인이나 분석 착수 지시가 아닙니다.','이번 등록은 작업 기준 후보 선택입니다. 최종 납품 확인이나 실제 분석 착수로 확대하지 않습니다.')
    desc+='\n선택 근거: [가족사 7곳 A안 선택 기록](../../../00_진행안내/08_가족사7곳_작업기준후보_선택기록.md).\n'
    record=json.loads((folder/'03_기획서검토_근거.json').read_text('utf-8'));record['proposed_pairing']=c;record['working_pairing_selected']=True;record['selection_record_id']=selection['id'];record['questions']=[q for q in record['questions'] if q!='Q01'];record.setdefault('human_confirmations',[]).append({'id':selection['id'],'confirmed':'작업 기준 후보와 문서 역할 선택','not_confirmed':'최종 납품 여부·영상 내용 일치·외부 처리 권한·분석 착수'})
    ev=(folder/'03_기획서검토_근거.md').read_text('utf-8')+'\n## 작업 기준 후보 선택 — 2026-10-16\n\n사용자 A안 선택으로 위 MP4·v4 Word·PPT/초기 문서의 조합을 등록했습니다. 역할은 영상 후보·재구성 원고·비교 참고입니다. 실제 일치 검수나 최종 납품 확인은 별도 상태로 유지합니다. [선택 기록](../../../00_진행안내/08_가족사7곳_작업기준후보_선택기록.md).\n'
    stage(rel+'/00_자료설명.md',desc);stage(rel+'/03_기획서검토_근거.json',record);stage(rel+'/03_기획서검토_근거.md',ev)
m['status']='partially_selected_as_working_candidates';m['selected_working_candidates']=7;m['remaining_unselected_groups']=16;m['selection_record_id']=selection['id'];stage('00_진행안내/06_영상과기획서_추천조합.json',m)
table='# 가족사 7곳 작업 기준 후보 선택 기록\n\n2026-10-16 / 사용자 직접 선택\n\n> '+selection['answer']+'\n\n등록 범위: 회사별 MP4 = 작업 기준 영상 후보 / v4 Word = 재구성 원고 / 초기 기획서·PPT = 비교 참고.\n\n| 자료 | 기준 영상 후보 | 재구성 원고 |\n|---|---|---|\n'
path=D/'00_진행안내/08_가족사7곳_작업기준후보_선택기록.md'
for x in selection['items']:table+='| '+x['id']+' '+x['project'].split('/')[-1]+' | '+lk(P/x['video'],path)+' | '+lk(P/x['reconstructed_script'],path)+' |\n'
table+='\n선택이 반영된 현재 기준 후보 7건입니다. 나머지 16개 묶음은 아직 추천안입니다. 원본 파일은 이동·복사·변경하지 않았습니다. 영상은 열거나 분석하지 않았으며, 분석 스킬 개발·스킬 기본 전환·외부 업로드도 하지 않았습니다. 최종 납품본 여부와 실제 영상-문서 내용 일치는 이 답변으로 확인한 사항이 아닙니다.\n'
stage('00_진행안내/08_가족사7곳_작업기준후보_선택기록.md',table);stage('00_진행안내/08_가족사7곳_작업기준후보_선택기록.json',selection)
t=(D/'00_진행안내/06_영상과기획서_추천조합.md').read_text('utf-8')
t=t.replace('이 표는 **향후 쓸 자료를 묶는 추천안**입니다.','이 표는 **가족사 7곳은 작업 기준 후보 등록 완료, 나머지 16곳은 추천안**입니다.')
t=t.replace('## 1. 먼저 확인할 가족사 7곳','## 1. 작업 기준 후보 등록 완료 — 가족사 7곳')
t=t.replace('**추천: 아래 MP4 + 재구성 원고 v4를 작업 기준 후보로 묶고, 초기 문서·PPT는 참고 자료로 둡니다.** 지금은 이 7개 조합에서 바뀌어야 할 것만 확인하면 됩니다.','**사용자 A안 선택을 반영했습니다. 아래 MP4 + 재구성 원고 v4를 작업 기준 후보로 묶고 초기 문서·PPT는 참고 자료로 등록했습니다.** [선택 기록](08_가족사7곳_작업기준후보_선택기록.md).')
t=t.replace('조합 선택 대기; 원고 성격 확인됨','기준 후보 등록 완료; 원고 성격 확인됨')
a=t.index('- **A. 가족사 7곳');b=t.index('\n나머지 16개 묶음',a)
t=t[:a]+'가족사 7곳은 A안 선택이 반영돼 같은 선택을 다시 받을 필요가 없습니다. 변경이 생기면 회사명과 변경점만 알려 주세요.\n'+t[b:]
stage('00_진행안내/06_영상과기획서_추천조합.md',t)
q=(D/'00_진행안내/04_사용자확인_모음.md').read_text('utf-8')
q=q.replace('## Q01. 앞으로 쓸 자료 선택 — 추천 조합으로 확인','## Q01. 가족사 7곳 선택 반영 완료 / 나머지 자료는 추천안')
q=q.replace('영상 41개와 문서를 23개 프로젝트 묶음으로 나란히 배치했습니다. 가족사 7곳을 먼저 확인하고, 나머지는 필요한 프로젝트부터 확인하면 됩니다.','영상 41개와 문서를 23개 프로젝트 묶음으로 배치했습니다. 가족사 7곳은 사용자 A안으로 작업 기준 후보 등록을 완료했습니다. 나머지 16개 묶음은 필요한 프로젝트부터 확인하면 됩니다.')
q+='\n가족사 7곳 작업 기준 후보 등록 근거: [사용자 A안 선택 기록](08_가족사7곳_작업기준후보_선택기록.md).\n'
stage('00_진행안내/04_사용자확인_모음.md',q)
s=json.loads((D/'00_진행안내/기획서검토_현황.json').read_text('utf-8'));s.update({'pairing_proposals_partially_selected':True,'selected_working_candidate_count':7,'selected_working_candidate_ids':[x['id'] for x in selection['items']],'remaining_unselected_group_count':16,'selection_record':'08_가족사7곳_작업기준후보_선택기록.json','final_selection_complete':False,'pairing_complete':False,'analysis_started':False,'skill_development_started':False});s['pairing_proposals_approved']=False;s['pairing_proposals_approved_scope_note']='전체 23개 승인 여부는 false. 자료002~008의 7개 작업 기준 후보 선택만 완료.'
stage('00_진행안내/기획서검토_현황.json',s)
g=(D/'00_먼저읽기.md').read_text('utf-8')+'\n## 가족사 7곳 작업 기준 후보 등록\n\n사용자 A안 선택에 따라 자료002~008의 MP4·v4 재구성 원고·PPT/초기 문서 참고 조합을 등록했습니다. [등록된 7건](00_진행안내/08_가족사7곳_작업기준후보_선택기록.md). 나머지 16개 묶음은 추천안 상태이며 실제 영상 분석·스킬 개발은 미실행입니다.\n'
stage('00_먼저읽기.md',g)
i=(D/'00_진행안내/05_기획서검토_색인.md').read_text('utf-8');i+='\n가족사 7곳은 [사용자 A안 선택](08_가족사7곳_작업기준후보_선택기록.md)을 반영해 작업 기준 후보로 등록했습니다. 실제 영상 내용 일치 검수와 구분합니다.\n';stage('00_진행안내/05_기획서검토_색인.md',i)
stage('05_결과보고/03_가족사7곳_작업기준후보_등록.md','# 가족사 7곳 작업 기준 후보 등록\n\n2026-10-16 / 사용자 A안 선택 반영\n\n자료002~008의 MP4 7개와 회사별 v4 재구성 원고를 기준 후보로 등록하고, PPT·초기 문서는 비교 참고로 구분했다. 자료 설명·현재 조합 목록·확인 항목·현황을 함께 갱신했다. [등록 내역과 선택 근거](../00_진행안내/08_가족사7곳_작업기준후보_선택기록.md).\n\n나머지 16개 프로젝트 추천안과 기존 원본을 유지했다. 영상은 열지 않았고 실제 분석·스킬 개발·기본 전환·외부 업로드는 진행하지 않았다. 작업 기준 후보 선택과 최종 납품/실제 일치 검수를 구분해 기록했다. 변경 전 파일은 별도 백업했으며 이전 보고서는 당시 기록으로 보존한다.\n')
assert len(selection['items'])==7
assert [c for c in m['cards'] if c['number'] not in range(2,9)]==[c for c in before_cards if c['number'] not in range(2,9)]
for x in targets:
    p=D/x['relative'];assert (sha(p)==x['before']) if x['before'] else not p.exists()
    t=(ST/x['relative']).read_text('utf-8');assert '\ufffd' not in t
    if x['relative'].endswith('.md'):
        for u in re.findall(r'\]\(([^)\n]+)\)',t):
            if '://' in u:continue
            to=(p.parent/unquote(u)).resolve()
            try:staged=ST/to.relative_to(D.resolve())
            except ValueError:staged=None
            assert to.exists() or (staged and staged.exists()),(p,u)
for name in ['02_분석작업','03_분석스킬','04_검증자료']:assert sorted(p.name for p in (D/name).rglob('*') if p.is_file())==['00_예약폴더_안내.md']
(W/'게시명세.json').write_text(json.dumps({'targets':targets,'selection':selection},ensure_ascii=False,indent=2),'utf-8')
if os.environ.get('DOC_REVIEW_PUBLISH')=='1':
    B=D/'backup/2026-10-16_가족사7곳_기준후보선택';assert not B.exists();B.mkdir(parents=True)
    for x in targets:
        p=D/x['relative'];assert sha(p)==x['before'] if x['before'] else not p.exists()
        if x['before']:
            b=B/'변경전'/x['relative'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b);assert sha(b)==x['before']
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ST/x['relative']).read_bytes());assert sha(p)==x['after']
    result={'date':'2026-10-16','saved_files':len(targets),'previous_files_backed_up':sum(bool(x['before']) for x in targets),'working_candidates_registered':7,'other_16_card_records_unchanged':True,'video_content_opened':False,'analysis_started':False,'skill_development_started':False,'default_skill_promotion':False,'external_upload_performed':False,'final_delivery_confirmation':False,'semantic_video_document_match_confirmation':False}
    (W/'검증결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    shutil.copy2(__file__,B/'가족사후보_선택반영.py');shutil.copy2(W/'게시명세.json',B/'게시명세.json');shutil.copy2(W/'검증결과.json',B/'검증결과.json')
    R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_가족사7곳_기준후보선택';R.mkdir(exist_ok=False)
    shutil.copy2(D/'00_진행안내/08_가족사7곳_작업기준후보_선택기록.json',R/'01_사용자선택_기록.json');shutil.copy2(W/'검증결과.json',R/'02_등록검증_결과.json')
    (R/'00_읽는순서.md').write_text('# 가족사 7곳 기준 후보 등록 기록\n\n사용자 A안 선택과 등록 범위를 보존한다.\n\n- 01_사용자선택_기록.json: 선택한 7개 영상·원고·참고 자료와 확인 범위\n- 02_등록검증_결과.json: 등록·백업·범위 점검\n\n실제 분석은 미시작이다. 현재 안내는 Phase 01-A/00_진행안내/08_가족사7곳_작업기준후보_선택기록.md에서 확인한다.\n','utf-8')
    print(json.dumps(result,ensure_ascii=False))
else:print(json.dumps({'mode':'preflight','files':len(targets),'selected_working_candidates':7,'other_groups_unchanged':16},ensure_ascii=False))
