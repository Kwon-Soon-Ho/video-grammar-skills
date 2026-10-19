"""R3-2 설명용 지식의 권한·원문 참조·조회 계약 검사. 영상 분류·효과 판정기가 아니다."""
from pathlib import Path
import json,hashlib,importlib.util
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(k,log,cases,ext):
    errors=[]
    def err(s):errors.append(s)
    def schema(obj,props,label):
        before=len(errors)
        for e in Draft202012Validator({'type':'object','properties':props,'required':list(props),'additionalProperties':False}).iter_errors(obj):err(label+' 형식: '+e.message)
        return len(errors)==before
    text={'type':'string','minLength':1};refs={'type':'array','minItems':1,'uniqueItems':True,'items':text}
    expected_depths={'SRC-L2-KLREQ':'group_note_draft_selected_sections','SRC-L2-CARBON-GRID':'product_guideline_selected_sections','SRC-L2-CARBON-TYPE':'product_guideline_selected_sections','SRC-L2-CARBON-CHART':'archived_guideline_selected_sections','SRC-L2-CARBON-AXIS':'archived_guideline_selected_sections','SRC-L2-NNG-VISUAL':'author_guidance_selected_sections','SRC-L2-NNG-PROXIMITY':'author_guidance_selected_sections','SRC-L2-NNG-REGION':'author_guidance_selected_sections','SRC-L2-W3C-COLOR':'understanding_selected_sections','SRC-L2-W3C-CONTRAST':'understanding_selected_sections','SRC-L2-ADOBE-SAFE':'official_tool_article_sections','SRC-L2-BIPM-SI':'primary_pdf_selected_text','SRC-L2-IMPECCABLE-LAYOUT':'local_reference_text_only','SRC-L2-IMPECCABLE-TYPE':'local_reference_text_only','SRC-L2-SHOT-COMPOSITION':'local_entrypoint_text_only'}
    if set(s['id'] for s in log['sources'])!=set(expected_depths) or len(log['sources'])!=15:err('조사 출처 누락·중복·확장 검토 필요')
    if log.get('skill_execution') is not False or log.get('existing_layout_taxonomy_changed') is not False:err('스킬 실행·분류 변경 위장')
    expected_urls={
    'SRC-L2-KLREQ':'https://www.w3.org/TR/klreq/',
    'SRC-L2-CARBON-GRID':'https://www.carbondesignsystem.com/building-blocks/foundations/2x-grid/guidelines',
    'SRC-L2-CARBON-TYPE':'https://www.carbondesignsystem.com/building-blocks/foundations/typography/overview',
    'SRC-L2-CARBON-CHART':'https://v10.carbondesignsystem.com/data-visualization/chart-types/',
    'SRC-L2-CARBON-AXIS':'https://v10.carbondesignsystem.com/data-visualization/axes-and-labels/',
    'SRC-L2-NNG-VISUAL':'https://www.nngroup.com/articles/principles-visual-design/',
    'SRC-L2-NNG-PROXIMITY':'https://www.nngroup.com/articles/gestalt-proximity/',
    'SRC-L2-NNG-REGION':'https://www.nngroup.com/articles/common-region/',
    'SRC-L2-W3C-COLOR':'https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html',
    'SRC-L2-W3C-CONTRAST':'https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html',
    'SRC-L2-ADOBE-SAFE':'https://helpx.adobe.com/premiere/desktop/get-started/source-and-program-monitor-adjustments/view-safe-zones-in-the-monitors.html',
    'SRC-L2-BIPM-SI':'https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf/fcf090b2-04e6-88cc-1149-c3e029ad8232',
    'SRC-L2-IMPECCABLE-LAYOUT':'https://github.com/pbakaus/impeccable/blob/2f98774f86bc05563876643db37e6c37c322850f/skill/reference/layout.md',
    'SRC-L2-IMPECCABLE-TYPE':'https://github.com/pbakaus/impeccable/blob/2f98774f86bc05563876643db37e6c37c322850f/skill/reference/typeset.md',
    'SRC-L2-SHOT-COMPOSITION':None}
    for s in log['sources']:
        if s.get('read_depth')!=expected_depths.get(s['id']):err(s['id']+' 검토 깊이 무단 변경')
        if s.get('url')!=expected_urls.get(s['id']):err(s['id']+' 확인한 출처 URL 교체')
        if not s.get('sections') or not s.get('limits') or s.get('remote_content_sha256') is not None:err(s['id']+' 읽은 절·한계·원격 스냅샷 표기')
    local_files={'SRC-L2-IMPECCABLE-LAYOUT':'backup/2026-10-14_R3_추가조사/스킬원본/impeccable/skill/reference/layout.md','SRC-L2-IMPECCABLE-TYPE':'backup/2026-10-14_R3_추가조사/스킬원본/impeccable/skill/reference/typeset.md','SRC-L2-SHOT-COMPOSITION':r'C:\Users\User\.codex\skills\shot-composition\SKILL.md'}
    for s in log['sources']:
        if s['id'] in local_files:
            if s['local_path']!=local_files[s['id']]:err(s['id']+' 원문 경로 교체');continue
            p=Path(s['local_path']) if ':' in s['local_path'] else BASE/s['local_path']
            if not p.exists() or s['local_sha256']!=sha(p):err(s['id']+' 로컬 원문 해시 불일치')
            if s['id'].startswith('SRC-L2-IMPECCABLE') and s['commit']!='2f98774f86bc05563876643db37e6c37c322850f':err(s['id']+' 커밋 교체')
    for r in log.get('reused_prior_sources',[]):
        p=BASE/r['prior_research_path']
        if r['prior_research_path']!='05_출처와검토/R3_모션_조사기록.json' or not p.exists() or sha(p)!=r['prior_research_sha256']:err('선행 조사 참조·해시 불일치')
    source_ids={s['id'] for s in log['sources']}|{s['id'] for s in read('05_출처와검토/출처목록.json')['sources']}
    core=read('02_원칙과레이아웃/레이아웃지식.json');screen=read('02_원칙과레이아웃/화면설계원칙.json');tax=read('01_공통용어/공통용어사전.json')
    core_by={r['id']:r for r in core['layouts']};screen_by={r['id']:r for r in screen['principles']};relations={r['id'] for r in tax['terms'] if r['axis']=='information_relation'};layout_ids={r['id'] for r in tax['terms'] if r['axis']=='layout'}
    if k.get('authority')!='project_draft_not_company_rule' or k.get('company_approved') is not False or k.get('actual_video_test') is not False or k.get('automatic_selection') is not False or k.get('universal_numeric_defaults') is not None:err('상위 참고 권한 위장')
    if set(k)!={'id','version','authority','company_approved','actual_video_test','core_refs','design_reference','layout_cards','screen_cards','universal_numeric_defaults','automatic_selection','text_edit_policy'}:err('심화지식 상위 계약 필드 누락·추가')
    if not k.get('text_edit_policy'):err('원문 보존·표기 제안 구분 없음')
    expected_core=['02_원칙과레이아웃/레이아웃지식.json','01_공통용어/공통용어사전.json','02_원칙과레이아웃/화면설계원칙.json']
    if [r['path'] for r in k['core_refs']]!=expected_core:err('정본 참조 경로 불일치')
    for r in k['core_refs']:
        p=BASE/r['path']
        if not p.exists() or sha(p)!=r['sha256'] or read(r['path'])['version']!=r['version']:err('정본 참조 버전·해시 불일치')
    dr=k['design_reference'];d=read('03_한맥디자인/한맥디자인정본.json')
    if dr['path']!='03_한맥디자인/한맥디자인정본.json' or dr['sha256']!=sha(BASE/dr['path']) or dr['profile_ref']!=d['profile_id']+'@'+d['version']:err('한맥 참조 계약 불일치')
    if dr['authority']!='영상 레이아웃·폰트 크기·간격·안전영역의 승인 규칙 아님':err('한맥 참조를 회사 영상 의무 규칙으로 승격')
    fields=['id','term_id','name_ko','definition_origin','definition','application_origin','relation_policy','fit_when','reading_order','composition_decisions','positive_example','counterexample','acceptable_variation','alternative_when','korean_text_adjustment','landscape_adjustment','portrait_adjustment','square_adjustment','temporal_conditions','abstain_when']
    props={f:text for f in fields};props.update({'status':{'const':'draft'},'company_approved':{'const':False},'fit_relation_ids':{'type':'array','uniqueItems':True,'items':text},'minimum_inputs':refs,'source_refs':refs,'source_locator_refs':{'type':'array','minItems':1,'items':{'type':'object','properties':{'source_id':text,'locator':text},'required':['source_id','locator'],'additionalProperties':False}},'numeric_default':{'const':None},'case_kind':{'const':'synthetic_not_company_video'},'auto_relation_assignment':{'const':False}})
    ids=[r['id'] for r in k['layout_cards']]
    if len(ids)!=14 or len(set(ids))!=14 or set(ids)!=set(core_by):err('기존14개 layout ID 누락·중복·신규')
    for r in k['layout_cards']:
        if not schema(r,props,r.get('id','?')):continue
        old=core_by.get(r['id'])
        if old and any(r[f]!=old[f] for f in ['id','term_id','name_ko','definition']):err(r['id']+' 기존 의미·이름 불일치')
        if any(i not in relations for i in r['fit_relation_ids']):err(r['id']+' 없는 관계ID 또는 축 혼동')
        if any(i not in source_ids for i in r['source_refs']):err(r['id']+' 없는 출처')
        if [x['source_id'] for x in r['source_locator_refs']]!=r['source_refs']:err(r['id']+' 출처 위치 누락·중복·순서 불일치')
        if r['positive_example']==r['counterexample']:err(r['id']+' 예/반례 동일')
    sp={f:text for f in ['id','name_ko','project_interpretation','positive_example','counterexample','abstain_when']};sp.update({'status':{'const':'draft'},'company_approved':{'const':False},'source_refs':refs,'numeric_default':{'const':None},'case_kind':{'const':'synthetic_not_company_video'}})
    ids=[r['id'] for r in k['screen_cards']]
    if len(ids)!=8 or len(set(ids))!=8 or set(ids)!=set(screen_by):err('화면설계8개 ID 누락·중복')
    for r in k['screen_cards']:
        if not schema(r,sp,r['id']):continue
        if r['id'] in screen_by and r['name_ko']!=screen_by[r['id']]['name_ko']:err(r['id']+' 기존 화면기준 명칭 불일치')
        if any(i not in source_ids for i in r['source_refs']):err(r['id']+' 화면설계 출처 없음')
    cp={f:text for f in ['id','name_ko','input_description','project_decision','counterexample','abstain_when']};cp.update({'layout_refs':refs,'screen_refs':refs,'case_kind':{'const':'synthetic_not_company_video'},'numeric_values_role':{'const':'illustration_only_not_company_default'}})
    if cases.get('status')!='draft' or cases.get('company_approved') is not False or cases.get('actual_video_test') is not False:err('스트레스 사례 권한 위장')
    ids=[r['id'] for r in cases['cases']]
    if len(ids)!=12 or len(set(ids))!=12:err('12사례 누락·중복')
    for r in cases['cases']:
        if not schema(r,cp,r['id']):continue
        if any(i not in layout_ids for i in r['layout_refs']) or any(i not in screen_by for i in r['screen_refs']):err(r['id']+' 사례 참조 없음')
    if ext.get('status')!='proposal_not_new_taxonomy' or ext.get('company_approved') is not False or ext.get('decision_ref')!='DECISION-R3-LAYOUT-SCOPE-A' or ext.get('case_kind')!='synthetic_not_company_video':err('확장후보 권한·결정근거 위장')
    if set(ext)!={'id','version','status','company_approved','decision_ref','case_kind','source_origin','candidates'}:err('확장후보 상위 계약 필드 누락·추가')
    decisions=read('05_출처와검토/사용자결정.json')['decisions'];decision=next((r for r in decisions if r['id']==ext.get('decision_ref')),None)
    if not decision or decision['selected']!='A' or decision['company_rule_approval'] is not False:err('사용자 A범위 결정 기록 불일치')
    ids=[r['candidate_id'] for r in ext['candidates']]
    if set(ids)!={'LAYOUT-CAND-TABLE','LAYOUT-CAND-CYCLE','LAYOUT-CAND-BRANCH'} or len(ids)!=3 or any(i in layout_ids for i in ids):err('후보3개 누락·중복·분류ID침범')
    ep={f:text for f in ['candidate_id','name_ko','fit_when','reading_order','composition_decisions','positive_example','counterexample','alternative_when','existing_id_connection_rule','unclassified_policy','abstain_when']}
    for r in ext['candidates']:schema(r,ep,r['candidate_id'])
    return errors
def main():
    k=read('02_원칙과레이아웃/레이아웃_심화지식.json');l=read('05_출처와검토/R3_레이아웃_조사기록.json');c=read('02_원칙과레이아웃/레이아웃_문구와화면비사례.json');e=read('02_원칙과레이아웃/레이아웃_확장후보.json')
    errors=inspect(k,l,c,e)
    spec=importlib.util.spec_from_file_location('gen',BASE/'07_실행도구/R3_레이아웃조회문서생성.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    for path,value in gen.views(k,l,c,e).items():
        if (BASE/path).read_text(encoding='utf-8')!=value.rstrip()+'\n':errors.append('조회문서 불일치 '+path)
    if (BASE/'02_원칙과레이아웃/11_레이아웃_설명도.html').read_text(encoding='utf-8')!=gen.html_view(k).rstrip()+'\n':errors.append('설명도 소스 불일치')
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'형식·권한·참조·출처 깊이·조회 동기화 검사. 자연어 의미·시선·가독성·실영상 효과는 별도.'},ensure_ascii=True));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
