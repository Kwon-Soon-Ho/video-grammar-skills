"""출처 깊이·초안 권한·참조·조회 정합성 검사. 자연어 정답과 실영상 효과는 검사하지 않는다."""
from pathlib import Path
import json,hashlib,importlib.util
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(data,log,candidates,core,core_hash):
    errors=[]
    def err(msg):errors.append(msg)
    core_ids={p['id'] for p in core['principles']};sources={s['id']:s for s in log['sources']}
    expected_depths={'SRC-ADOBE-12':'public_article_sections','SRC-JORGE-10':'public_course_outline','SRC-R3-POLYUM':'secondary_article_sections','SRC-CAM-EXTRANEOUS':'publisher_summary','SRC-CAM-ESSENTIAL':'publisher_summary','SRC-CAM-TRANSIENT':'publisher_summary','SRC-R3-EXPERTISE-SUMMARY':'publisher_summary','SRC-CARBON-CHOREO':'archived_ui_guideline_sections','SRC-CARBON-OVERVIEW':'archived_ui_guideline_sections','SRC-FLUENT':'ui_guideline_sections','SRC-UX-MOTION':'author_article_sections','SRC-W3C-FLASH':'w3c_understanding_sections','SRC-W3C-PAUSE':'w3c_understanding_sections','SRC-W3C-INTERACTION':'w3c_understanding_sections','SRC-R3-MATERIAL2':'search_extract_only','SRC-R3-APM':'publisher_summary','SRC-R3-CHANGE-STUDY':'article_selected_sections'}
    if set(sources)!=set(expected_depths):err('이번 조사 출처 누락·신규 출처 검토 필요')
    for ident,s in sources.items():
        if s.get('read_depth')!=expected_depths.get(ident):err(ident+' 검토 깊이 승인 없이 변경')
        if not s.get('sections') or not s.get('limits') or not s.get('url','').startswith('https://'):err(ident+' 출처 위치·한계·URL 없음')
        if s.get('remote_content_sha256') is not None:err(ident+' 원격 원문 스냅샷 미실행 위장')
    if set(data)!={'id','version','core_ref','authority','default_company_requirement','actual_video_test','decision_ref','cards'}:err('심화카드 상위 누락·허용되지 않은 필드')
    if data.get('decision_ref')!='DECISION-R3-MOTION-SCOPE-A':err('조건부 참고 선택 근거 없음')
    strings=['id','name_ko','family','status','source_locator','source_read_depth','interpretation_origin','project_interpretation','positive_example','counterexample','abstain_when','case_kind','observables','review_question','duplicate_failure_policy','limitations']
    props={k:{'type':'string','minLength':1} for k in strings}
    props.update({'status':{'const':'draft'},'company_approved':{'const':False},'case_kind':{'const':'synthetic_not_company_video'},'source_refs':{'type':'array','minItems':1,'uniqueItems':True,'items':{'type':'string','minLength':1}},'related_ids':{'type':'array','uniqueItems':True,'items':{'type':'string'}},'source_summary_ko':{'type':['string','null']},'numeric_default':{'const':None},'recommendation_enabled':{'type':'boolean'}})
    schema={'type':'object','properties':props,'required':list(props),'additionalProperties':False}
    if data.get('authority')!='project_draft_not_company_rule' or data.get('default_company_requirement') is not False or data.get('actual_video_test') is not False:err('상위 초안 권한 위장')
    if data.get('core_ref')!={'path':'02_원칙과레이아웃/모션과정보전달원칙.json','version':core['version'],'sha256':core_hash}:err('정본 버전·해시 불일치')
    ids=[c.get('id') for c in data.get('cards',[])];
    if len(ids)!=len(set(ids)) or set(ids)!=core_ids:err('원칙 누락·중복·신규ID')
    for c in data.get('cards',[]):
        ident=c.get('id','?')
        for e in Draft202012Validator(schema).iter_errors(c):err(ident+' 형식: '+e.message)
        p=next((p for p in core['principles'] if p['id']==ident),None)
        if p and any(c.get(k)!=p[k] for k in ['name_ko','family','related_ids']):err(ident+' 기존 의미/관계 불일치')
        for ref in c.get('source_refs',[]):
            if ref not in sources:err(ident+' 없는 출처')
            elif c.get('source_read_depth')!=sources[ref]['read_depth']:err(ident+' 출처 깊이 위장')
        if ident.startswith('MP-') and (c.get('source_summary_ko') is not None or c.get('source_read_depth')!='public_course_outline' or c.get('interpretation_origin')!='public_outline_only_project_interpretation'):err(ident+' 강의 본문 확인 위장')
        if ident=='IP-10' and (c.get('recommendation_enabled') is not True or c.get('source_refs')!=['SRC-R3-EXPERTISE-SUMMARY'] or p['status']!='reference'):err('IP-10 조건부 참고 계약 불일치')
        if any(x not in core_ids for x in c.get('related_ids',[])):err(ident+' 관계 참조 없음')
        if c.get('positive_example')==c.get('counterexample'):err(ident+' 예/반례 동일')
    source_ids=[s['id'] for s in log['sources']]
    if len(source_ids)!=len(set(source_ids)):err('출처ID 중복')
    if log.get('original_core_changed') is not True or not log.get('approved_change','').startswith('사용자 A에 따라 IP-10만'):err('사용자 선택에 따른 좁은 정본 개정 기록 없음')
    if candidates.get('status')!='proposal_not_new_taxonomy' or candidates.get('company_approved') is not False or candidates.get('source_read_depth')!='author_article_sections':err('추가 후보 권한·깊이')
    if candidates.get('source_ref')!='SRC-UX-MOTION':err('UX 후보 출처 변경')
    ux_ids=[r['candidate_id'] for r in candidates.get('rows',[])]
    if len(ux_ids)!=12 or len(set(ux_ids))!=12:err('UX 후보 누락·중복')
    for r in candidates.get('rows',[]):
        if r.get('case_kind')!='synthetic_not_company_video' or not r.get('existing_connections') or any(x not in core_ids for x in r.get('existing_connections',[])):err('UX 참조·실사례 위장')
    return errors
def main():
    data=read('02_원칙과레이아웃/모션원칙_심화카드.json');log=read('05_출처와검토/R3_모션_조사기록.json');c=read('02_원칙과레이아웃/추가모션체계_연결후보.json');core=read('02_원칙과레이아웃/모션과정보전달원칙.json')
    errors=inspect(data,log,c,core,sha(BASE/'02_원칙과레이아웃/모션과정보전달원칙.json'))
    spec=importlib.util.spec_from_file_location('gen',BASE/'07_실행도구/R3_모션조회문서생성.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    expected=gen.render_cards(data,log,sha(BASE/'02_원칙과레이아웃/모션원칙_심화카드.json'))
    if (BASE/'02_원칙과레이아웃/03_모션원칙_적용예와반례.md').read_text(encoding='utf-8')!=expected:errors.append('심화카드 조회본 불일치')
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'설명용 지식의 구조·출처 깊이·권한·연결만 검사. 영상 효과·자연어 의미·학술 원문 진위는 별도 검토.'},ensure_ascii=False));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
