import pathlib,json,hashlib,re,os,shutil
from urllib.parse import quote,unquote
ROOT=pathlib.Path(__file__).resolve().parent;W=ROOT/'제공자료일괄등록_20261016';W.mkdir(exist_ok=True);ST=W/'게시안';ST.mkdir(exist_ok=True)
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');D=P/'Phase 01-A'
M=json.loads((ROOT.parent/'phase01a-prep/게시구성_명세.json').read_text('utf-8'));idx=json.loads((D/'00_진행안내/06_영상과기획서_추천조합.json').read_text('utf-8'));original_cards=json.loads(json.dumps(idx['cards']))
rows={x['id']:x for x in M['registry']};targets=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lk(p,base,label=None):return '['+(label or p.name)+']('+quote(os.path.relpath(p,base.parent).replace('\\','/'),safe='/._-')+')'
def stage(rel,data):
    p=D/rel;s=ST/rel;s.parent.mkdir(parents=True,exist_ok=True);s.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8');targets.append({'relative':rel,'before':sha(p) if p.exists() else None,'after':sha(s)})
answer='아 지금 물어보는게 영상과 시나리오를 어떻게 묶을지 물어보는거야? 내가 준 시나리오대로 다 묶으면 돼. sw 영상 같은 경우엔 시나리오가 따로 없어서 안 넣어 놓은거야'
receipt={'id':'사용자지시_20261016_제공자료대로일괄묶음','date':'2026-10-16','source':'사용자 직접 지시','verbatim':answer,'policy':'함께 제공한 시나리오·기획자료를 해당 프로젝트 영상과 묶는다. 시나리오를 넣지 않은 SW 홈페이지 클립은 별도 시나리오 없음으로 정상 등록한다.','association_scope':'프로젝트/폴더 단위 입력자료 연결. 개별 장면의 실제 내용 일치나 최종 납품본 확인과 구분.','no_repeated_pairing_questions':True,'analysis_started':False,'skill_development_started':False,'external_upload_performed':False,'sw_scope_note':'시나리오가 없는 4개 SW 홈페이지 폴더에 없음 확인을 반영한다. 이미 제공된 SW 홍보 스토리보드 3개는 해당 프로젝트 기획자료로 보존·연결한다.'}
exts={'.pptx','.docx','.hwp','.pdf','.xlsx','.png'}
shared_folder=P/'한맥 영상/00_26년 가족사 경영보고 영상'
shared=sorted(p.relative_to(P).as_posix() for p in shared_folder.iterdir() if p.is_file() and p.suffix.lower() in exts)
for c in idx['cards']:
    folder=P/'한맥 영상'/c['project'];provided=sorted(p.relative_to(P).as_posix() for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts)
    c.update({'recommendation_status':'제공 자료대로 프로젝트 묶음 등록 완료','input_bundle_registered':True,'association_scope':'project_folder','registration_record_id':receipt['id'],'provided_planning_documents':provided,'scenario_status':'별도 시나리오 없음 — 사용자 설명 반영' if c['number'] in range(13,17) else '제공 기획자료를 해당 영상 프로젝트에 연결','requires_new_scenario_before_registration':False,'pairing_question_pending':False,'confirm':'입력자료 묶음 확인 완료. 같은 연결 질문을 반복하지 않음. 장면별 실제 일치는 분석 착수 후 별도 검수.'})
    c['recommendation']='제공된 폴더의 영상과 시나리오·기획자료를 프로젝트 단위로 함께 등록한다. 여러 영상은 서로 다른 파일로 보존한다.' if provided else '시나리오 없이 제공된 SW 홈페이지 클립을 영상 입력자료로 등록한다. 별도 원고를 요구하거나 다른 홍보영상의 원고를 가져와 붙이지 않는다.'
    c['basis']='사용자 직접 지시: 제공한 시나리오대로 모두 묶기. 시나리오 미첨부 SW 자료는 별도 시나리오 없음.'
    if c['number'] in range(1,9):c['shared_planning_documents']=shared
    row=rows[c['id']];base=D/row['folder'];desc=(base/'00_자료설명.md').read_text('utf-8')
    # Retain source candidate links but remove obsolete choice questions from current description.
    desc=re.sub(r'^3\. 대응 시나리오·콘티·기획서 파일명·버전:.*$', '3. 연결 기획자료: '+('별도 시나리오 없음(사용자 확인). 제공 영상만 등록.' if not provided else '같은 폴더에 제공한 기획자료를 이 프로젝트의 영상 묶음에 연결했습니다.'),desc,flags=re.M)
    desc=re.sub(r'^   - 영상과의 관계:.*$', '   - 영상과 문서의 관계: 입력자료 묶음 등록 완료. 장면별 내용 일치는 아직 분석하지 않았습니다.',desc,flags=re.M)
    desc=desc.replace('2. 사용할 최종 영상의 파일명·위치: 미정','2. 등록한 영상 입력자료: 위 같은 폴더의 영상 파일 전체. 각 파일은 별도로 보존합니다.')
    desc=re.sub(r'^   - 최종 납품·배포본 확인:.*Q01.*$', '   - 파일의 납품·배포 상태는 별도 메모이며 입력자료 묶음 등록을 막지 않습니다.',desc,flags=re.M)
    desc=re.sub(r'^(사용자 확인|남은 확인): Q.*$', '자료 묶음 연결은 사용자 지시로 등록 완료했습니다. 담당자·외부 처리 범위는 실제 착수 시 필요한 대상에 한해 확인합니다.',desc,flags=re.M)
    desc=desc.replace('문서 기반 필드는 미작성','문서 없음 상태로 접수')
    if c['number'] in range(13,17):
        desc=desc.replace('문서 부재와 확인 대기를 반영했습니다.','시나리오 없음 확인과 영상 입력자료 등록을 반영했습니다.')
        desc=desc.replace('기획 문서가 확인되지 않아 목적·원고·화면 계획을 채우지 않았습니다.','별도 시나리오가 없다는 사용자 설명을 반영했습니다. 원고·화면 계획을 임의로 만들지 않았습니다.')
        desc=desc.replace('동일 폴더에 기획·시나리오 문서를 찾지 못했다. 파일명과 폴더명만으로 목적·시청자·원고를 확정하지 않았다.','이 SW 홈페이지 영상에는 별도 시나리오가 없어 넣지 않았다는 사용자 설명을 반영했다. 파일명만으로 원고를 만들지 않았다.')
        desc=desc.replace('SW 홍보영상의 같은 제품 기획서는 자동 연결하지 않았다. 홈페이지용 개별 클립과의 관계를 확인해야 한다.','SW 홍보영상의 같은 제품 기획서를 가져와 붙이지 않는다. 제공된 홈페이지 클립 자체를 등록한다.')
    pos=desc.find('\n## 영상·문서 추천 조합 — 선택 전')
    if pos<0:pos=desc.find('\n## 영상·문서 작업 기준 후보 — 사용자 선택 반영')
    if pos>=0:desc=desc[:pos]
    desc+='\n## 현재 입력자료 묶음 — 사용자 지시 반영\n\n'+c['recommendation']+'\n\n'+('가족사 7곳의 기존 MP4 기준 후보·v4 재구성 원고·초기 문서/PPT 참고 역할은 유지합니다.\n\n' if c['number'] in range(2,9) else '')+'[현재 묶음 목록](../../../00_진행안내/09_제공자료_묶음목록.md)에서 영상과 문서의 실제 파일명을 볼 수 있습니다. 같은 연결 질문은 다시 받지 않습니다. 실제 영상 분석·스킬 개발은 아직 시작하지 않았습니다.\n'
    record=json.loads((base/'03_기획서검토_근거.json').read_text('utf-8'));record.pop('proposed_pairing',None);record['input_bundle']=c;record['input_bundle_registered']=True;record['pairing_question_pending']=False;record['questions']=[q for q in record['questions'] if q not in ['Q01','Q03']];record['registration_record_id']=receipt['id']
    if c['number'] in range(13,17):record['scenario_absence_user_confirmed']=True;record['notes']=['별도 시나리오가 없어 첨부하지 않았다는 사용자 설명 확인. 추가 원고를 등록 조건으로 요구하지 않음.','기존 SW 홍보영상의 스토리보드를 가져와 홈페이지 클립에 연결하지 않음.'];record['scope']='제공 파일 목록과 사용자 설명으로 시나리오 없음 확인. 영상 본문은 미분석.'
    ev=(base/'03_기획서검토_근거.md').read_text('utf-8')
    # Preserve the prior review as context, explicitly supersede the association questions.
    ev+='\n## 최신 사용자 지시: 제공한 자료대로 묶음 등록\n\n제공된 시나리오·기획자료를 해당 프로젝트 영상과 함께 등록합니다. 앞선 연결 확인 대기·추가 시나리오 유무 질문은 이 지시로 종료합니다. '+('별도 시나리오 없음이 확인됐으며 영상만 정상 등록합니다. ' if c['number'] in range(13,17) else '')+'실제 장면 일치 검수는 아직 수행하지 않았습니다. [현재 등록 목록과 사용자 지시](../../../00_진행안내/09_제공자료_묶음목록.md).\n'
    stage(row['folder']+'/00_자료설명.md',desc);stage(row['folder']+'/03_기획서검토_근거.json',record);stage(row['folder']+'/03_기획서검토_근거.md',ev)
idx.update({'status':'registered_as_supplied_project_bundles','registered_input_group_count':23,'registered_video_file_count':41,'remaining_unregistered_groups':0,'association_scope':'project_folder','registration_record_id':receipt['id'],'pairing_questions_pending':False,'family_report_shared_planning_documents':shared});idx.pop('remaining_unselected_groups',None)
stage('00_진행안내/06_영상과기획서_추천조합.json',idx)
newpath=D/'00_진행안내/09_제공자료_묶음목록.md'
out='# 제공 자료 기준 영상·기획서 묶음\n\n2026-10-16 / 사용자 지시 반영 완료\n\n**넣어주신 시나리오·기획자료를 해당 프로젝트 영상에 연결했습니다. 같은 연결 질문을 다시 받지 않습니다.** 시나리오를 넣지 않은 SW 홈페이지 클립 4개 묶음은 ‘별도 시나리오 없음’으로 등록했습니다. 이미 첨부된 SW 홍보 스토리보드는 해당 프로젝트에 연결해 보존했습니다.\n\n가족사 7곳은 앞서 선택한 MP4·v4 재구성 원고·초기/PPT 비교 참고 역할을 유지합니다. 여러 영상이 있는 폴더는 프로젝트 묶음 안에서 각 파일을 따로 보존하며 억지로 일대일 대응을 만들지 않습니다. 영상 내용 분석·스킬 개발은 미시작입니다.\n\n'
out+='## 가족사 경영보고 공용 참고 자료\n\n'
for rel in shared:out+='- '+lk(P/rel,newpath)+'\n'
out+='\n공용 자료는 가족사 경영보고 프로젝트의 참고로 연결합니다. 공유 검증표의 과거 주장을 이번 분석 결과로 재사용하지 않습니다.\n'
for c in idx['cards']:
    out+='## '+c['id']+' · '+c['project']+'\n\n영상\n\n'
    for rel in c['videos']:out+='- '+lk(P/rel,newpath)+'\n'
    out+='\n제공 기획자료\n\n'
    if c['provided_planning_documents']:
        for rel in c['provided_planning_documents']:out+='- '+lk(P/rel,newpath)+'\n'
    else:out+='- **별도 시나리오 없음 — 사용자 확인. 추가 제출 필요 없음.**\n'
    supplementary=[x for x in c['reference_documents'] if x not in c['provided_planning_documents']]
    if supplementary:
        out+='\n추가 비교 참고(기존 등록 유지)\n\n'
        for rel in supplementary:out+='- '+lk(P/rel,newpath)+'\n'
    if c['number']==1:out+='\n회사별 초기 자료가 섞인 폴더이므로 프로젝트 참고 묶음으로 보존합니다. 모든 문서가 두 영상 각각에 전부 대응한다고 간주하지 않습니다.\n'
    if c['number']==10:out+='\n제공 콘티 본문의 확인 범위는 크레인 설명입니다. 기상 악화 영상을 포함한 폴더 자료로 보존하며 각 장면 대응은 이후 분석에서 검수합니다. 별도 시나리오 제출을 다시 요구하지 않습니다.\n'
    if c['number']==22:out+='\n싱글·듀얼은 각각의 영상 파일로 보존하고 제공 원고를 같은 프로젝트에 연결합니다.\n'
    if c['number']==23:out+='\n제공한 두 영상과 원고를 같은 프로젝트로 묶되 전체/발췌 관계를 확인했다고 기록하지 않습니다.\n'
out+='\n## 등록 범위\n\n이번 완료는 입력자료의 프로젝트 연결입니다. 최종 납품본 인증·장면별 실제 일치 판정·API 업로드·분석 착수로 확대하지 않습니다. 원본은 이동하거나 변경하지 않았습니다.\n'
stage('00_진행안내/09_제공자료_묶음목록.md',out);stage('00_진행안내/09_제공자료_묶음목록.json',{'date':'2026-10-16','receipt':receipt,'cards':idx['cards']})
stage('00_진행안내/09_제공자료_등록지시.json',receipt)
stage('00_진행안내/06_영상과기획서_추천조합.md','# 영상과 기획서 자료 연결 — 등록 완료\n\n사용자 지시에 따라 제공된 시나리오·기획자료를 프로젝트별 영상과 묶었습니다. 시나리오가 없는 SW 홈페이지 클립은 별도 시나리오 없음으로 등록했습니다.\n\n[현재 영상·기획서 묶음 목록](09_제공자료_묶음목록.md)에서 전체 파일을 확인할 수 있습니다. 기존 추천안·질문은 변경 전 백업으로 보존했습니다. 같은 묶음 선택을 다시 요청하지 않습니다.\n\n실제 영상 분석·스킬 개발은 미시작입니다.\n')
stage('00_진행안내/04_사용자확인_모음.md','# 자료 연결 확인 — 사용자 지시 반영 완료\n\n영상과 시나리오를 어떻게 묶을지에 관한 질문은 종료했습니다. 제공된 자료대로 프로젝트별로 연결했고, 시나리오 미첨부 SW 홈페이지 영상은 별도 시나리오 없음으로 등록했습니다. [현재 묶음 목록](09_제공자료_묶음목록.md).\n\n가족사 7곳 v4는 완성 영상과 초기 기획서를 대조해 재구성한 원고라는 사용자 설명을 유지했습니다. 이미 제공된 SW 홍보 스토리보드도 그대로 보존했습니다.\n\n## 실제 작업을 시작한 뒤 필요한 경우에만 확인\n\n- 내용 검수 담당·실제 시청 환경: 사용할 자료의 판단에 필요한 범위에서 확인\n- 문서 수치·PG 규격·수정 전후 차이: 이후 분석에서 실제 충돌이 확인된 항목만 검수\n- 외부 AI/API 처리 범위: 외부 처리를 요청한 시점에 해당 자료와 필요한 범위로 확인\n\n이 항목들은 현재 입력자료 묶음 등록을 막지 않습니다. 실제 영상 분석·스킬 개발·외부 업로드는 아직 시작하지 않았습니다.\n')
s=json.loads((D/'00_진행안내/기획서검토_현황.json').read_text('utf-8'))
for key in ['pairing_proposals_approved','pairing_proposals_partially_selected','remaining_unselected_group_count','pairing_proposals_approved_scope_note']:s.pop(key,None)
s.update({'input_bundle_registration_complete':True,'registered_input_group_count':23,'registered_video_file_count':41,'pairing_complete':True,'pairing_complete_scope':'제공 자료의 프로젝트/폴더 단위 연결 완료. 실제 영상-문서 의미 일치 판정은 아님.','semantic_video_document_match_verified':False,'pairing_questions_pending':False,'scenario_absence_confirmed_group_ids':['자료013','자료014','자료015','자료016'],'scenario_absence_blocks_registration':False,'human_answers_pending':False,'future_human_review_when_needed':['내용 판단에 필요한 검수 담당·환경','분석 후 확인된 충돌','외부 처리 요청 시 자료별 범위'],'current_bundle_index':'09_제공자료_묶음목록.json','analysis_started':False,'skill_development_started':False})
stage('00_진행안내/기획서검토_현황.json',s)
g=(D/'00_먼저읽기.md').read_text('utf-8');g=g.replace('최종본·대응 문서·첫 시험 대상은 미정입니다.','제공된 영상·문서의 프로젝트 연결은 완료했습니다. 최종 납품 상태·첫 시험 대상은 별도이며 분석은 미시작입니다.')
g=g.replace('같은 폴더의 후보를 적어 두었으니 이번에 사용할 버전만 표시하면 됩니다. 모르면 미정, 자료가 없으면 없음입니다.','같은 폴더에 넣어주신 영상·기획자료를 묶었습니다. 시나리오 미첨부 SW 홈페이지 영상은 별도 시나리오 없음으로 등록했습니다.')
g=g.replace('홈페이지용 4개 묶음은 같은 폴더 문서가 없어 확인 대기로 표시했습니다.','홈페이지용 4개 묶음은 사용자 설명에 따라 별도 시나리오 없음으로 등록했습니다.')
g=g.replace('나머지 16개 묶음은 추천안 상태이며 실제 영상 분석·스킬 개발은 미실행입니다.','나머지 자료도 제공 폴더 기준으로 묶음 등록을 완료했으며 실제 영상 분석·스킬 개발은 미실행입니다.')
g=re.sub(r'^2\. .*$', '2. [등록된 영상·기획서 묶음](00_진행안내/09_제공자료_묶음목록.md)을 봅니다. 추가 연결 확인이나 시나리오 재작성은 필요 없습니다.',g,flags=re.M)
g+='\n## 최신 상태: 제공한 자료대로 프로젝트 묶음 등록 완료\n\n영상 41개를 23개 폴더 묶음으로 등록했습니다. 시나리오 미첨부 SW 홈페이지 클립 18개는 별도 시나리오 없음이며 정상 접수된 자료입니다. 기존 홍보영상 스토리보드는 보존했습니다. 이전의 ‘나머지 16개 추천안/확인 대기’ 상태는 이번 사용자 지시로 종료했습니다. [현재 목록](00_진행안내/09_제공자료_묶음목록.md). 영상 분석·스킬 개발은 아직 시작하지 않았습니다.\n';stage('00_먼저읽기.md',g)
i=(D/'00_진행안내/05_기획서검토_색인.md').read_text('utf-8');i=re.sub(r'^\*\*확인은 .*?\*\*$', '**제공자료의 연결 확인은 완료했습니다. [현재 묶음 목록](09_제공자료_묶음목록.md)을 보세요. 시나리오 미첨부 SW 홈페이지 영상은 별도 시나리오 없음입니다.**',i,flags=re.M);i=i.replace('미작성·확인 대기','시나리오 없음 확인·영상 등록');stage('00_진행안내/05_기획서검토_색인.md',i)
stage('05_결과보고/04_제공자료대로_일괄연결.md','# 제공 자료대로 영상·기획자료 일괄 연결\n\n2026-10-16\n\n사용자가 제공한 시나리오대로 묶으라고 명시했고 SW 영상의 시나리오 미첨부 이유를 설명했다. 23개 프로젝트 폴더의 영상 41개를 제공 기획자료와 연결하고, 시나리오가 없는 SW 홈페이지 4개 묶음은 없음으로 정상 등록했다. 이미 제공된 SW 홍보 스토리보드 3개는 보존했다.\n\n자료 설명·근거 기록·현재 목록·질문·진행 상태를 같은 기준으로 수정했다. 프로젝트 단위 연결과 영상의 장면별 실제 내용 일치를 구분했고, 동일 연결 질문을 다시 하지 않도록 표시했다. 기존 가족사 7곳의 기준 후보와 재구성 원고 역할은 유지했다.\n\n반대 관점 자체 점검: 문서가 있는 SW 홍보 자료를 지우거나, 혼합 초기 폴더의 모든 문서를 모든 영상에 일대일 대응시키거나, 등록 완료를 실제 분석 완료로 오인하는 위험을 확인하고 범위를 명시했다. 실제 영상 파일은 열지 않았으며 분석·스킬 개발·외부 업로드는 하지 않았다. 이전 문서는 백업하고 원본은 보존했다.\n')
vids=[v for c in idx['cards'] for v in c['videos']];assert len(vids)==len(set(vids))==41;assert len(idx['cards'])==23
for old,new in zip(original_cards,idx['cards']):assert old['videos']==new['videos'] and old['primary_documents']==new['primary_documents'] and old['reference_documents']==new['reference_documents']
assert sum(not c['provided_planning_documents'] for c in idx['cards'])==4
for x in targets:
    p=D/x['relative'];assert sha(p)==x['before'] if x['before'] else not p.exists()
    t=(ST/x['relative']).read_text('utf-8');assert '\ufffd' not in t
    if x['relative'].endswith('.md'):
        for u in re.findall(r'\]\(([^)\n]+)\)',t):
            if '://' in u:continue
            to=(p.parent/unquote(u)).resolve()
            try:staged=ST/to.relative_to(D.resolve())
            except ValueError:staged=None
            assert to.exists() or (staged and staged.exists()),(p,u)
for name in ['02_분석작업','03_분석스킬','04_검증자료']:assert sorted(p.name for p in (D/name).rglob('*') if p.is_file())==['00_예약폴더_안내.md']
(W/'게시명세.json').write_text(json.dumps({'targets':targets,'receipt':receipt},ensure_ascii=False,indent=2),'utf-8')
if os.environ.get('DOC_REVIEW_PUBLISH')=='1':
    B=D/'backup/2026-10-16_제공자료대로_일괄연결';assert not B.exists();B.mkdir(parents=True)
    for x in targets:
        p=D/x['relative'];assert sha(p)==x['before'] if x['before'] else not p.exists()
        if x['before']:
            b=B/'변경전'/x['relative'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b);assert sha(b)==x['before']
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ST/x['relative']).read_bytes());assert sha(p)==x['after']
    result={'date':'2026-10-16','updated_files':len(targets),'groups_registered':23,'video_files':41,'provided_local_planning_files':sum(len(c['provided_planning_documents']) for c in idx['cards']),'scenario_absence_confirmed_groups':4,'same_file_lists_preserved':True,'pairing_questions_pending':False,'analysis_started':False,'skill_development_started':False,'video_content_opened':False,'external_upload_performed':False}
    (W/'검증결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8');shutil.copy2(__file__,B/'제공자료_일괄묶음_반영.py');shutil.copy2(W/'게시명세.json',B/'게시명세.json');shutil.copy2(W/'검증결과.json',B/'검증결과.json')
    R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_제공자료대로_일괄연결';R.mkdir(exist_ok=False)
    shutil.copy2(D/'05_결과보고/04_제공자료대로_일괄연결.md',R/'01_연결정리_결과.md');shutil.copy2(D/'00_진행안내/09_제공자료_등록지시.json',R/'02_사용자지시_기록.json');shutil.copy2(W/'검증결과.json',R/'03_등록범위_검증결과.json')
    print(json.dumps(result,ensure_ascii=False))
else:print(json.dumps({'mode':'preflight','files':len(targets),'groups':23,'videos':41,'scenario_absence_groups':4},ensure_ascii=False))
