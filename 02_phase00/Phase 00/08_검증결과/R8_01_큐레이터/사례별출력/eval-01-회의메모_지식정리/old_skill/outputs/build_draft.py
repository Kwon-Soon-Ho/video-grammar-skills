from pathlib import Path
import json, hashlib

RUN = Path(__file__).resolve().parents[1]
BASE = RUN / 'inputs/Phase00'
OUT = RUN / 'outputs'
def read(rel):
    return json.loads((BASE / rel).read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

# Fixed bytes only, including 06/08: no decoding or evaluation-result inspection.
fixed_dirs = ['01_공통용어','02_원칙과레이아웃','03_한맥디자인','04_기록규격','05_출처와검토','06_맞춤스킬','07_실행도구','08_검증결과','09_다음단계인계','13_품질검수','실행스킬']
before = {str(p.relative_to(BASE)).replace('\\','/'): sha(p)
          for d in fixed_dirs for p in (BASE/d).rglob('*') if p.is_file()}
before['입력메모.json'] = sha(BASE/'입력메모.json')
save('input_hashes_before.json', before)

paths = {
 'tax':'01_공통용어/공통용어사전.json',
 'classification':'01_공통용어/분류운영규칙.json',
 'principles':'02_원칙과레이아웃/모션과정보전달원칙.json',
 'motion_cards':'02_원칙과레이아웃/모션원칙_심화카드.json',
 'motion_conflicts':'02_원칙과레이아웃/모션원칙_충돌판단사례.json',
 'screen':'02_원칙과레이아웃/화면설계원칙.json',
 'layout_deep':'02_원칙과레이아웃/레이아웃_심화지식.json',
 'layout_candidates':'02_원칙과레이아웃/레이아웃_확장후보.json',
 'design':'03_한맥디자인/한맥디자인정본.json',
 'motion_sources':'05_출처와검토/R3_모션_조사기록.json',
 'layout_sources':'05_출처와검토/R3_레이아웃_조사기록.json',
 'decisions':'05_출처와검토/사용자결정.json',
 'color_policy':'05_출처와검토/R5_적용정책_결정.json',
 'ci_reply':'05_출처와검토/검수와사용범위/사람답변원문/2026-10-15_8회사CI_최신자료와산하AI부재.json',
 'ci_rules':'03_한맥디자인/07_회사CI와_화면역할_연결규칙.md',
 'contrast_note':'03_한맥디자인/11_관측색_대비참고.md',
}
data = {k:read(p) for k,p in paths.items() if p.endswith('.json')}
refs = []
def ref(key, collection=None, ident=None, field='id', note='해당 항목 확인'):
    obj = data.get(key)
    pointer = ''
    if collection:
        index = next(i for i,x in enumerate(obj[collection]) if x[field] == ident)
        pointer = '/'+collection+'/'+str(index)
        obj = obj[collection][index]
    rid = 'REF-'+str(len(refs)+1).zfill(2)
    refs.append({'ref_id':rid, 'path':paths[key], 'json_pointer':pointer or None,
                 'id':ident, 'version':obj.get('version') if isinstance(obj,dict) else None,
                 'sha256':sha(BASE/paths[key]), 'this_run_read_scope':note,
                 'authority':'기존 자료 참조. 이번 실행의 새 승인이 아님'})
    return rid

R = {}
for ident in ['PURPOSE-PROCESS','REL-ORDER','LAYOUT-CARD-GROUP','LAYOUT-PROCESS-LINE','LAYOUT-NETWORK','LAYOUT-SPLIT-COMPARE','CURVE-LINEAR']:
    R[ident]=ref('tax','terms',ident,note='정의·별칭·적용/제외·상태·대체·버전 확인')
for ident in ['IP-01','IP-02','IP-03','IP-07','IP-10','AP-06','MP-02']:
    R[ident]=ref('principles','principles',ident,note='원칙 정의·적용/제외·출처·권한 확인')
    R[ident+'-card']=ref('motion_cards','cards',ident,note='로컬 심화카드의 출처 요약/자체 해석·예/반례·검토 깊이 확인')
for ident in ['SCREEN-CHOICE','SCREEN-COLOR','SCREEN-DENSITY']:
    R[ident]=ref('layout_deep','screen_cards',ident,note='화면설계 적용 해석·예/반례 확인; 외부 원문 미열람')
for ident in ['LAYOUT-CAND-TABLE','LAYOUT-CAND-CYCLE','LAYOUT-CAND-BRANCH']:
    R[ident]=ref('layout_candidates','candidates',ident,field='candidate_id',note='후보 전체와 기존ID 연결/기권 규칙 확인; term_id가 아님')
for key in ['classification','decisions','color_policy','ci_reply','ci_rules','contrast_note']:
    R[key]=ref(key,note='로컬 규칙/결정/선언의 해당 범위 확인; 사람 신원·원본 자산·최종 디자인 검증 없음')
R['design']=ref('design',note='hanmac-video@0.1.0의 팔레트 범위·규칙·관측과 역할 분리·권한 경계 확인; 외부 웹 원문 미열람')

def rr(*ids):return [R[x] for x in ids]
def question(qid, question, options):
    return {'question_id':qid,'question':question,'options':[
        {'id':chr(65+i),'text':v,'recommended':i==0} for i,v in enumerate(options)],
        'status':'unanswered_recorded_only','selected':None}

records = [
 {'draft_id':'DRAFT-MEMO-01','input_note_index':0,'title':'단계 번호와 카드의 기능을 구분',
  'disposition':'reference_ready_with_conditions',
  'term_distinctions':{'purpose':'단계 설명 PURPOSE-PROCESS','information_relation':'순서가 의미를 가지면 REL-ORDER',
    'layout':'LAYOUT-CARD-GROUP과 LAYOUT-PROCESS-LINE은 복합 가능','style_claim':'AI처럼 보임은 이 메모의 인상이며 일반 금지 근거가 아님'},
  'confirmed_in_local_knowledge':'정보 표식은 핵심과 구조를 식별하게 돕는다. 카드 그룹은 독립 항목 묶음이며 단계 의미를 자동 부여하지 않는다. 내용 기반 구도는 일괄 카드 금지나 무작위 비대칭을 반례로 둔다.',
  'project_interpretation':'단계 순서를 전달하는 번호는 유지 후보로 두고, 불필요하게 반복된 카드 테두리·장식은 목적에 맞게 줄이는 초안으로 정리한다.',
  'apply_when':['작업 순서와 현재 위치를 식별할 필요가 있고 단계 근거가 제공될 때','동일 역할의 독립 항목에 카드 경계가 읽기를 도울 때'],
  'exclude_or_hold':['실제 화면·시나리오 없이 모든 번호의 필요성을 확정하지 않는다.','병렬 항목에 단계를 암시하는 번호를 강제하지 않는다.'],
  'positive_example':'가상 접수→검토→완료 절차에 1·2·3과 현재 단계를 표시하되 카드 외곽선은 줄인다.',
  'counterexample':'AI 느낌을 없애려고 번호를 모두 지워 절차 순서와 현재 위치를 알 수 없게 한다.',
  'held_claims':['회사 전체의 번호/카드 금지','시선·이해도 개선 효과 입증'],
  'reference_refs':rr('PURPOSE-PROCESS','REL-ORDER','LAYOUT-CARD-GROUP','LAYOUT-PROCESS-LINE','IP-02','IP-02-card','SCREEN-CHOICE'),
  'review_question_id':'Q1'},
 {'draft_id':'DRAFT-MEMO-02','input_note_index':1,'title':'표·순환·분기는 지원 지식 후보 유지',
  'disposition':'candidate_reference_ready_formal_taxonomy_change_held',
  'term_distinctions':{'taxonomy':'기존 layout 14개 유지','candidate_ids':['LAYOUT-CAND-TABLE','LAYOUT-CAND-CYCLE','LAYOUT-CAND-BRANCH'],
    'id_boundary':'candidate_id는 정식 taxonomy term_id가 아니다. 새 정식 ID를 발급하지 않았다.'},
  'confirmed_in_local_knowledge':'DECISION-R3-LAYOUT-SCOPE-A는 14분류 유지·후보와 예/반례 별도 정리·새 분류ID 없음이다. 분류운영규칙은 other_candidate에서 빈 term_ids와 이유·자유후보를 허용한다.',
  'project_interpretation':'정확한 값 대조는 표, 복귀가 확인된 흐름은 순환, 조건별 경로는 분기 후보를 참고한다. 맞는 범위에만 기존 ID를 연결하고 맞지 않으면 other_candidate로 남긴다.',
  'apply_when':['표: 대상·열·행·단위·기간과 빈칸/미제공/0의 뜻이 확인될 때','순환: 복귀·반복·재시작 또는 종료 조건이 확인될 때','분기: 조건·각 경로 라벨·결과/합류가 확인될 때'],
  'exclude_or_hold':['표를 카드 그룹에 자동 편입하지 않는다.','순환을 선형 프로세스로 강제하지 않는다.','노드·연결이 NETWORK 정의에 맞는 해당 범위만 연결한다.','마름모/화살표만으로 현실 조건·인과·절차 진실을 확정하지 않는다.'],
  'positive_example':'가상 공법 A/B 비용·공기를 같은 단위의 표로 대조한다. 점검→조치→재점검은 복귀 조건을, 승인/보완 분기는 각 조건 라벨을 붙인다.',
  'counterexample':'빈 셀을 0으로 채우거나 일회성 승인을 원형으로 그린 뒤 새 정식 ID 3개를 바로 등록한다.',
  'held_claims':['새 taxonomy ID 신설·기존 의미 병합은 범위 변경 검토가 필요하며 이번 작업에서 미수행'],
  'reference_refs':rr('classification','decisions','LAYOUT-CAND-TABLE','LAYOUT-CAND-CYCLE','LAYOUT-CAND-BRANCH','LAYOUT-NETWORK','LAYOUT-SPLIT-COMPARE'),
  'review_question_id':'Q2'},
 {'draft_id':'DRAFT-MEMO-03','input_note_index':2,'title':'시청자의 주제별 사전 지식에 맞춘 설명',
  'disposition':'conditional_reference_ready_audience_level_unknown',
  'term_distinctions':{'source_concept':'숙련도별 설명 지원 조정 IP-10','audience_claim':'기획실이라는 부서명만으로 초보자 판정 불가','explanation':'핵심 용어 소개 IP-07과 모든 용어의 반복 풀이를 구별'},
  'confirmed_in_local_knowledge':'IP-10은 2021 공식 Summary에 근거한 조건부 참고이며 현재 기본 조회 범위에 포함돼 있다. 해당 주제 사전 지식 근거가 없으면 unknown이다. 초보자에게 유효한 지원이 전문가에게 방해될 수 있다는 요약 수준이다.',
  'project_interpretation':'인터뷰·업무 경험·입력 문서 등으로 낯선 개념을 확인한 뒤 핵심 명칭/역할을 먼저 소개하고 숙련자에게는 짧은 요약을 비교 후보로 둔다.',
  'apply_when':['시청자의 해당 주제 사전 지식 근거가 있을 때','용어 이해가 본 설명을 따라가는 데 필요할 때'],
  'exclude_or_hold':['기획실 전체의 지식 수준은 unknown','필수 고지·정확한 기술 용어·접근성 자막·무음 시청 지원은 숙련도 이유로 자동 삭제하지 않는다.','학술 장 전체·진단도구·회사 영상 효과는 미검토'],
  'positive_example':'가상 입문 시청자에게 펌프·밸브 역할을 한 번 소개하고 도면에서 대응시킨다. 익숙한 시청자에게는 요약과 필요한 용어표를 제공한다.',
  'counterexample':'부서명만 보고 모든 용어를 매번 풀어 써 화면·음성·자막이 경쟁하게 만든다.',
  'held_claims':['시청자 사전 지식 판정','모든 용어 항상 풀이의 회사 필수화','학습 효과 보장'],
  'reference_refs':rr('IP-01','IP-03','IP-07','IP-10','IP-10-card','decisions'),
  'review_question_id':'Q3'},
 {'draft_id':'DRAFT-MEMO-04','input_note_index':3,'title':'등속 설비 설명에서는 선형 변화 허용',
  'disposition':'reference_ready_with_conditions',
  'term_distinctions':{'timing':'CURVE-LINEAR는 일정한 변화율','path':'직선 경로와 시간상 등속은 다른 속성. 직선 위에서도 가감속할 수 있다.','principles':'AP-06과 MP-02는 관련되지만 별도 ID를 병합하지 않는다.'},
  'confirmed_in_local_knowledge':'AP-06 적용 해석과 합성 충돌사례 MC-01은 등속 전달·기계 시뮬레이션에 선형이 적합할 수 있으며 측정 대상의 시간·경로를 보존하도록 한다. 이징 미사용 자체는 실패가 아니다.',
  'project_interpretation':'설명 대상 설비는 같은 시간 간격에 같은 이동량을 주는 계획 후보로 두고, 안내 패널의 등장·정착 이징은 별도 검토한다. 실제 설비 데이터라는 판정은 입력 시간·거리 근거가 필요하다.',
  'apply_when':['일정 속도의 운동을 설명하는 것이 목적이고 계획/측정의 범위를 명시할 때'],
  'exclude_or_hold':['실제 시작·정지가 가감속이면 해당 구간을 등속으로 바꾸지 않는다.','시간 표본 없이 실제 렌더의 등속 관측이나 원본 AE Bézier 핸들값을 확정하지 않는다.','MP-02는 공개 강의 항목명 확인 수준이므로 강사의 상세 정의는 needs_primary_definition_review로 보류'],
  'positive_example':'가상 컨베이어 설명의 등속 구간은 일정 변화율로 유지하고 옆 설명 패널만 감속 정착시킨다.',
  'counterexample':'부드럽게 보이게 하려고 실제 등속 운동의 끝에 감속을 넣어 속도 설명을 바꾼다.',
  'held_claims':['실제 설비의 측정값·시간 대응','원본 곡선/키프레임 복원','MP-02 강의 본문 상세 이론 정의'],
  'reference_refs':rr('CURVE-LINEAR','AP-06','AP-06-card','MP-02','MP-02-card'),
  'review_question_id':'Q4'},
 {'draft_id':'DRAFT-MEMO-05','input_note_index':4,'title':'최신 CI 선언·관측색·본문 역할 승인 분리',
  'disposition':'reference_policy_ready_automatic_official_text_color_held',
  'term_distinctions':{'latest_material':'로컬 답변 전사에서 사용자 제공 8회사 CI 최신 확인','observed_color':'로컬 관측/표시 가정이 있는 색값','official_text_role':'모든 본문색으로의 공식 지정은 별도 범위·가독성·권한 판단','common_library':'한맥 공통 컬러와 회사별 CI색은 다른 자격'},
  'confirmed_in_local_knowledge':'R6-REPLY-CI-20261015-001은 제공 CI 8회사 최신 및 산하 Illustrator 원본 부재를 선언한다. 회사 승인·공식 sRGB값·사용 가이드 전체·실제 화면 적합성은 확인하지 않았다. DECISION-R5-OBSERVED-COLOR A는 디자이너 명시 선택·출처·가정·이유·검수 상태를 갖춘 프로젝트 초안 역할 후보만 허용한다.',
  'project_interpretation':'대상 회사와 자산/색 버전을 정하고 현재·원문대조 완료·표시 sRGB가 있는 관측색을 역할 후보로 명시 선택한다. 본문은 실제 배경·크기/굵기·움직임·시청 조건에서 검수한다. 최신 선언으로 자동 기본색이나 공식 본문색으로 승격하지 않는다.',
  'apply_when':['선택자 선언·회사/색 ID·버전·해시·출처·표시 가정·선택 이유·검수 대기가 남아 있을 때','한맥 30색은 공통 라이브러리로 명시 선택한 범위에서 사용'],
  'exclude_or_hold':['이번 사본에는 CI 바이너리 전체가 없어 원본 대조를 재수행하지 않았다.','프로필 없는 CMYK/별색을 공식 sRGB로 환산하지 않는다.','로고의 대비 예외를 브랜드색 본문 전체에 적용하지 않는다.','CI 원색을 덮어쓰거나 한맥 공통색을 회사 CI색으로 바꾸지 않는다.'],
  'positive_example':'가상 프로젝트에서 회사별 관측색을 강조선 후보로 명시 선택하고 본문과 배경의 최종 조합을 검수 대기로 기록한다.',
  'counterexample':'최신 CI라는 말만으로 밝은 관측색을 모든 본문에 자동 지정하고 로고 예외를 이유로 대비 검수를 생략한다.',
  'held_claims':['공식 본문색 역할','선택자 신원 인증','최종 가독성·회사 승인'],
  'reference_refs':rr('ci_reply','color_policy','ci_rules','contrast_note','design','SCREEN-COLOR'),
  'review_question_id':'Q5'}
]
for record in records:
    record.update({'status':'draft','company_approved':False,'case_refs':[],
                   'case_kind':'synthetic_not_company_video','numeric_default':None,
                   'change_kind':'new_draft_annotation_only','canonical_mutation':False})

questions = [
 question('Q1','대상 화면에서 번호가 맡는 역할을 어떻게 검토할까?', ['실제 단계 순서를 확인하고 필요한 번호 유지·장식만 조정','번호 대신 방향/명칭으로 순서를 명확히 표현','번호는 유지하되 카드 경계 축소 후보 비교','화면·시나리오 확보 후 해당 판단 보류']),
 question('Q2','표·순환·분기를 적용할 자료의 관계 근거는 무엇인가?', ['행열/단위·복귀조건·분기조건을 확인하고 기존 후보 지식으로 기록','정확한 값 조회만 필요한 표로 범위 한정','일회성 순서라면 선형 후보 비교','관계 근거가 없으므로 other_candidate와 확인 필요 사유 유지']),
 question('Q3','시청자의 해당 주제 사전 지식은 어떻게 확인할까?', ['간단한 인터뷰·업무 경험 자료로 낯선 핵심 개념 확인','확인된 입문 집단에 핵심 명칭 사전 소개','확인된 숙련 집단에 요약 후보 제공','근거 확보 전 수준 unknown 유지']),
 question('Q4','일정 속도 설명의 시간·거리 근거는 어떤 범위인가?', ['제공 시간·경로와 등속 구간을 확인한 뒤 선형 계획','실측이 아닌 개념 설명임을 표시하고 선형 예시','시작/정지 가감속을 별도 구간으로 모델링','자료 부족으로 실제 운동 판정 보류']),
 question('Q5','CI 관측색을 어떤 화면 역할로 검토할까?', ['대상 회사·버전·표시 가정을 pin하고 역할별 명시 선택 후 검수','본문은 검수된 별도 중립색 후보와 조합','해당 관측색을 강조/구분 후보로만 사용','원본/가독성/사용 가이드 부족으로 색 역할 선택 보류'])
]

source_audit=[]
needed={'SRC-ADOBE-12','SRC-JORGE-10','SRC-CAM-EXTRANEOUS','SRC-CAM-ESSENTIAL','SRC-R3-EXPERTISE-SUMMARY','SRC-L2-CARBON-CHART','SRC-L2-NNG-VISUAL','SRC-L2-IMPECCABLE-LAYOUT','SRC-L2-W3C-COLOR','SRC-L2-W3C-CONTRAST'}
for key in ['motion_sources','layout_sources']:
    for s in data[key]['sources']:
        if s['id'] in needed:
            source_audit.append({'source_id':s['id'],'title':s['title'],'url_recorded_in_db':s.get('url'),
              'local_research_record':paths[key],'prior_recorded_read_depth':s['read_depth'],
              'prior_recorded_sections':s.get('sections'),'prior_recorded_limits':s.get('limits'),
              'this_run_verification':'로컬 지식·조사기록의 해당 항목 확인. 외부 원문·외부 스킬·웹 페이지 재열람 없음.',
              'primary_definition_status':'needs_primary_definition_review' if s['id']=='SRC-JORGE-10' else 'prior_record_depth_only_not_reverified',
              'remote_content_verified_this_run':False})

result = {
 'artifact_id':'meeting-note-common-knowledge-draft','version':'0.1.0','status':'draft',
 'authority':'project_draft_not_company_rule','company_approved':False,'operational_release':False,
 'input':{'path':'입력메모.json','sha256':sha(BASE/'입력메모.json'),'kind':read('입력메모.json')['kind'],'note_count':5},
 'scope':'회의 메모 5건의 기존 지식 대조와 신규 초안 주석. 정본/분류ID/회사 필수규칙 변경 없음.',
 'summary':{'new_draft_records':5,'modified_canonical_records':0,'new_taxonomy_ids':0,'ready_reference':'5건 모두 조건부 참고 내용을 제공. 각 메모의 일괄 규칙화·현실/승인 주장은 아래 항목별 보류.','pending_review_questions':5},
 'records':records,'review_questions':questions,'reference_registry':refs,'source_audit':source_audit,
 'existing_decision_handling':'기존 A 선택을 확인한 동일 범위를 다시 승인 요청하지 않았다. Q1~Q5는 구체 적용에 필요한 미확인 입력을 위한 기록용 질문이다. 새 분류ID 신설·의미 병합·회사 필수화·승인은 미수행이다.',
 'change_control':{'canonical_modified':False,'backup':'정본을 변경하지 않아 변경 전 backup 생성 비적용. 실행 전후 고정 바이트 해시를 별도 보존.','deprecation_or_merge':None,'retroactive_application':False},
 'validation':{'draft_check':'validation.json 참조: 이 결과물의 한정 구조/참조 검사','existing_motion_checker':'기존 R3_모션자료검사.py 실제 실행: exit_code 0, valid true, errors []. 기존 입력 모션 지식 구조 검사이며 신규 결과물/효과/승인 검증과 별개.',
 'not_run':['R6_통합조회 전체 원문·자산 검사','R3_레이아웃자료검사 전체 실행: 외부 스킬/원문 해시 조회 경로를 포함하여 실행하지 않음','자료검증.py --record: 본 결과는 v0.2 통합 영상기록이 아니므로 적용하지 않음','최종 영상·가독성·시청자 효과·실제 CI 바이너리 검사']},
 'limitations':['이번 실행은 로컬 사본만 확인했다. 조사기록에 적힌 과거 확인 깊이는 이번 원문 재검증과 다르다.','가상 메모·합성 예시는 실제 회사 영상 사례나 사람 승인 근거가 아니다.','06/08은 고정파일 바이트 해시 비교만 수행했으며 내용은 열람하지 않았다.','토큰 사용량과 전체 수행 시간은 측정하지 않았다.']
}
save('knowledge_draft.json', result)

# Narrow output check, not a substitute for the DB's unrelated video-record schema.
out=read('입력메모.json')
loaded=json.loads((OUT/'knowledge_draft.json').read_text(encoding='utf-8'))
errors=[]
if loaded['status']!='draft' or loaded['company_approved'] is not False:errors.append('draft authority')
if len(records)!=len(out['notes']) or [x['input_note_index'] for x in records]!=list(range(5)):errors.append('note coverage')
all_refs={x['ref_id'] for x in refs}
if len(all_refs)!=len(refs):errors.append('duplicate reference ids')
if len({x['draft_id'] for x in records})!=len(records):errors.append('duplicate draft ids')
for x in records:
    if not set(x['reference_refs'])<=all_refs:errors.append(x['draft_id']+' unresolved ref')
    if x['case_refs'] or x['company_approved'] or x['canonical_mutation']:errors.append(x['draft_id']+' authority')
    if not x['positive_example'] or x['positive_example']==x['counterexample']:errors.append(x['draft_id']+' example')
for x in refs:
    p=(BASE/x['path']).resolve()
    if not p.is_relative_to(BASE.resolve()) or sha(p)!=x['sha256']:errors.append(x['ref_id']+' file/hash')
    if x['json_pointer']:
        value=read(x['path'])
        for part in x['json_pointer'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
        if value.get('id',value.get('candidate_id'))!=x['id']:errors.append(x['ref_id']+' pointer')
for q in questions:
    if len(q['options'])<4 or sum(v['recommended'] for v in q['options'])!=1 or q['selected'] is not None:errors.append(q['question_id']+' review')
taxonomy_ids={t['id'] for t in data['tax']['terms']}
if len([t for t in data['tax']['terms'] if t['axis']=='layout'])!=14:errors.append('layout count')
if any(c['candidate_id'] in taxonomy_ids for c in data['layout_candidates']['candidates']):errors.append('candidate is taxonomy')
after={str(p.relative_to(BASE)).replace('\\','/'):sha(p)
       for d in fixed_dirs for p in (BASE/d).rglob('*') if p.is_file()}
after['입력메모.json']=sha(BASE/'입력메모.json')
save('input_hashes_after.json',after)
if before!=after:errors.append('input bytes changed')
validation={'valid':not errors,'errors':errors,'scope':'신규 초안 JSON 재파싱·5메모 대응·ID 중복·로컬 참조 포인터/해시·예/반례 비동일·draft권한·4선택지/추천·14분류/후보 분리·입력 바이트 불변 검사만',
            'input_files_hashed':len(before),'input_bytes_unchanged':before==after,
            'fact_verified':False,'human_identity_verified':False,'company_approved':False,'operational_release':False,
            'not_proven':'자연어 의미 정확성·실제 영상 효과·외부 원문/전체 자산 진위는 입증하지 않는다.'}
save('validation.json',validation)
print(json.dumps(validation,ensure_ascii=False))
raise SystemExit(1 if errors else 0)
