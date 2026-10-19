from pathlib import Path
import argparse
import contextlib
import hashlib
import io
import json
import sys
import traceback

OUT = Path(__file__).resolve().parent
CASE = OUT.parent
DB = CASE / 'inputs' / 'Phase00'
OUT.mkdir(exist_ok=True)

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path, scope='full_file'):
    if not path.is_file():
        item = {'path': str(path), 'exists': False, 'scope': scope}
        with (OUT / 'read_evidence.jsonl').open('a', encoding='utf-8') as fp:
            fp.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(json.dumps(item, ensure_ascii=False))
        return None
    data = path.read_bytes()
    text = data.decode('utf-8-sig')
    item = {'path': str(path), 'exists': True, 'scope': scope, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'lines': len(text.splitlines()), 'read_range': 'entire file'}
    with (OUT / 'read_evidence.jsonl').open('a', encoding='utf-8') as fp:
        fp.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(json.dumps(item, ensure_ascii=False))
    print(text)
    return json.loads(text) if path.suffix == '.json' else text

def snapshot():
    return [{'path': str(p.relative_to(CASE)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted((CASE/'inputs').rglob('*')) if p.is_file()]

def prepare():
    dump(OUT/'inputs_before.json', snapshot())
    read(CASE/'task.txt')
    for rel in [
        '실행스킬/video-guidance-reviewer/SKILL.md',
        '실행스킬/video-guidance-reviewer/references/근거찾기와적용조건.md',
        '실행스킬/video-guidance-reviewer/references/판정과사람검수.md',
        '13_품질검수/03_판정운영기준.md',
        '13_품질검수/품질항목_정본.json',
    ]:
        read(DB/rel)

def criteria_details():
    p=DB/'13_품질검수/품질항목_정본.json'
    j=json.loads(p.read_text(encoding='utf-8-sig'))
    ids=['Q-INFO-01','Q-INFO-02','Q-SCREEN-02','Q-BRAND-02','Q-TRUST-01','Q-TRUST-02']
    print(json.dumps({k:v for k,v in j.items() if k!='cards'},ensure_ascii=False,indent=2))
    selected=[c for c in j['cards'] if c['id'] in ids]
    print(json.dumps(selected,ensure_ascii=False,indent=2))
    with (OUT/'read_evidence.jsonl').open('a',encoding='utf-8') as fp:
        fp.write(json.dumps({'path':str(p),'exists':True,'sha256':sha(p),'scope':'semantic_selected_json_pointers','read_range':['/cards[id='+i+']' for i in ids],'note':'prepare stdout was truncated in UI; these selected cards are displayed in full separately.'},ensure_ascii=False)+'\n')

def preselect():
    p=DB/'13_품질검수/품질항목_정본.json'
    j=json.loads(p.read_text(encoding='utf-8-sig'))
    reasons={
        'Q-INFO-01':('전문용어를 풀어 쓴 3카드의 목적·대상·설명수준을 문서로 점검','문서 의미·초보 이해용 범위에 한정. 실제 시청자 이해도는 미검수'),
        'Q-INFO-02':('쉬운설명의 부정어·의미·조건이 제공 원문과 같은지 직접 대조','문서 전사/의미/조건·반례. 영상 음성·자막 검수 아님'),
        'Q-SCREEN-02':('선형 프로세스의 정보관계·가로/세로·선택조건·반례를 확인','레이아웃 설명카드의 조건부 지식만. 실제 화면 밀도·가독성은 미검수'),
        'Q-BRAND-02':('연결목록의 디자인 참조를 회사 규칙/공식색/실제 시안 승인으로 승격하지 않았는지 확인','출처·역할 분리만 적용. 실제 색/시안 적용 적합성은 이번 대상에 비적용'),
        'Q-TRUST-01':('상류 파일·원문·연결판본·SHA와 문장 지지범위를 직접 검증','문서 비공간 주장. PTS/OCR/좌표/프레임을 요구하거나 만들지 않음'),
        'Q-TRUST-02':('주목 이동 기능과 실제 시선효과, 가시성 관측과 제작원인, 미검수와 승인 경계를 확인','효과/구현/회사일반화의 주장범위 검토. 실제 효과·제작자 의도 확정 아님'),
    }
    selection={'id':'eval-03-preselection','before_target_content_read':True,'target':'작업초안/쉬운말_지식카드.json 3카드 + 연결목록.json','criteria_path':str(p),'criteria_version':j.get('version'),'criteria_sha256':sha(p),'selection_basis':'task.txt + 실행 SKILL 및 두 references + 품질항목_정본의 선정 카드. 아직 카드/연결목록/상류결과 내용 미열람.','items':[{'id':i,'required':True,'reason':r,'scope':s} for i,(r,s) in reasons.items()],'not_required_groups':'수치/SI/그래프, 실제 글리프·줄바꿈·대비·크롭·자막·음향·지속·섬광·이징·동작 연속성·로고 원형 등 실제 산출물을 전제로 하는 항목은 문서 설명카드라는 목적에 강제하지 않음. 문서에 관련 주장이 새로 발견되면 이유를 기록해 범위 추가.','all_26_mandatory':False,'single_total_score':None,'selection_changes':[],'elapsed_seconds':None,'tokens':None}
    dump(OUT/'검수항목_사전선정.json',selection)
    print(json.dumps(selection,ensure_ascii=False,indent=2))

def review_read():
    if not (OUT/'검수항목_사전선정.json').is_file():
        raise RuntimeError('사전 선정 기록이 없으므로 결과 열람을 진행하지 않습니다.')
    for rel in [
        '00_운영계약/01_보존과버전_계약.md',
        '00_운영계약/정본과표시_연결목록.json',
        '01_공통용어/공통용어사전.json',
        '01_공통용어/분류운영규칙.json',
        '01_공통용어/용어판정기준.json',
        '01_공통용어/02_기록단위와분류축.md',
        '02_원칙과레이아웃/레이아웃지식.json',
        '02_원칙과레이아웃/레이아웃_심화지식.json',
        '02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md',
        '14_스킬재구성/R8_현재사용안내.md',
        '14_스킬재구성/현재상태_정정표.json',
        '작업초안/쉬운말_지식카드.json',
        '작업초안/연결목록.json',
        '상류결과/01/결과.json',
        '상류결과/01/결과.md',
        '상류결과/02/결과.json',
        '상류결과/02/결과.md',
        'backup/이번작업/큐레이터_소량시범_20261016/쉬운말_지식카드_v0.1.0.json',
        'backup/이번작업/기록관리자_소량시범_20261016/연결목록_v0.1.0.json',
        '03_한맥디자인/회사별_디자인연결_현황.json',
        '05_출처와검토/검수와사용범위/07_한맥디자인과_CI_확인현황.md',
        '14_스킬재구성/사람피드백/R8-3_적용성검토자_검토답변.json',
    ]:
        read(DB/rel)
    for rel in ['입력고정.json', '상류_인계증거.json', 'eval_metadata.json']:
        read(CASE/rel)

def focus_targets():
    for rel in ['작업초안/쉬운말_지식카드.json','작업초안/연결목록.json','상류결과/01/결과.md','상류결과/02/결과.md']:
        read(DB/rel, 'semantic_full_target_or_report')

def focus_sources():
    for rel in ['01_공통용어/공통용어사전.json','01_공통용어/분류운영규칙.json','01_공통용어/용어판정기준.json','02_원칙과레이아웃/레이아웃지식.json','02_원칙과레이아웃/레이아웃_심화지식.json']:
        p=DB/rel;j=json.loads(p.read_text(encoding='utf-8-sig'))
        print('SOURCE_TOP',rel,json.dumps({k:v for k,v in j.items() if not isinstance(v,(list,dict))},ensure_ascii=False))
        def walk(value, pointer=''):
            if isinstance(value,dict):
                small=json.dumps(value,ensure_ascii=False)
                if len(small)<18000 and any(t in small for t in ['선형 프로세스','주목 이동','가시성','opacity','오퍼시티']):
                    print(pointer,json.dumps(value,ensure_ascii=False,indent=2));return
                for k,v in value.items():walk(v,pointer+'/'+str(k))
            elif isinstance(value,list):
                for i,v in enumerate(value):walk(v,pointer+'/'+str(i))
        walk(j)
        with (OUT/'read_evidence.jsonl').open('a',encoding='utf-8') as fp:
            fp.write(json.dumps({'path':str(p),'exists':True,'sha256':sha(p),'scope':'semantic_keyword_selected_json_subtrees','read_range':'Top scalar metadata and smallest matching subtrees <=18000 characters for 선형 프로세스, 주목 이동, 가시성, opacity, 오퍼시티'},ensure_ascii=False)+'\n')
    read(DB/'02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md','semantic_full_file')

def focus_exact():
    wanted={'LAYOUT-PROCESS-LINE','FUNCTION-FOCUS','PROPERTY-VISIBILITY','PROPERTY-OPACITY'}
    for rel in ['01_공통용어/공통용어사전.json','01_공통용어/용어판정기준.json','02_원칙과레이아웃/레이아웃지식.json','02_원칙과레이아웃/레이아웃_심화지식.json']:
        p=DB/rel;j=json.loads(p.read_text(encoding='utf-8-sig'))
        def walk(v,ptr=''):
            if isinstance(v,dict):
                if any(v.get(k) in wanted for k in ['id','term_id']):
                    print(rel,ptr,json.dumps(v,ensure_ascii=False,indent=2));return
                for k,x in v.items():walk(x,ptr+'/'+k)
            elif isinstance(v,list):
                for n,x in enumerate(v):walk(x,ptr+'/'+str(n))
        walk(j)
    p=DB/'02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md'
    lines=p.read_text(encoding='utf-8-sig').splitlines()
    selected=[(n+1,l) for n,l in enumerate(lines[:16])]
    start=next(n for n,l in enumerate(lines) if l.startswith('## ') and 'LAYOUT-PROCESS-LINE' in l)
    end=next((n for n in range(start+1,len(lines)) if lines[n].startswith('## ')),len(lines))
    selected += [(n+1,lines[n]) for n in range(start,end)]
    print(str(p));print('\n'.join(str(n)+': '+l for n,l in selected))
    for rel in ['03_한맥디자인/회사별_디자인연결_현황.json','05_출처와검토/검수와사용범위/07_한맥디자인과_CI_확인현황.md','14_스킬재구성/사람피드백/R8-3_적용성검토자_검토답변.json']:
        read(DB/rel,'semantic_full_file')

def local_audit():
    def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
    cards=load(DB/'작업초안/쉬운말_지식카드.json');index=load(DB/'작업초안/연결목록.json')
    terms=load(DB/'01_공통용어/공통용어사전.json');catalog=load(DB/'00_운영계약/정본과표시_연결목록.json')
    termmap={r['id']:r for r in terms['terms']};cardmap={r['id']:r for r in cards['records']}
    audits=[]
    for item in index['items']:
        c=cardmap[item['id']];original=termmap[c['term_ref']['id']];ref=item['draft_ref']
        audits.append({'card_id':c['id'],'term_id':original['id'],'source_snapshot_equal':c['source_snapshot']==original,'source_sha_match':c['source_file']['sha256']==sha(DB/c['source_file']['path']),'term_version_match':c['term_ref']['version']==original['version'],'axis':original['axis'],'link_id_match':item['id']==c['id'],'link_term_ref_match':item['term_ref']==c['term_ref'],'document_version_match':ref['document_version']==cards['document_version'],'record_version_match':ref['record_version']==c['version'],'draft_file_sha_match':ref['file_sha256']==sha(DB/ref['path']),'source_status_preserved':c['source_snapshot']['status']==original['status'],'state':c['state'],'company_approved':c['company_approved']})
    design=index['design_reference'];actual=load(DB/design['path'])
    designcheck={'profile_id_actual':actual.get('profile_id'),'reference_id':design['id'],'id_match':actual.get('profile_id')==design['id'],'version_match':actual.get('version')==design['version'],'sha_match':sha(DB/design['path'])==design['sha256'],'usage':design['usage']}
    backup_paths=['backup/이번작업/큐레이터_소량시범_20261016/쉬운말_지식카드_v0.1.0.json','backup/이번작업/기록관리자_소량시범_20261016/연결목록_v0.1.0.json']
    backups=[{'path':s,'sha256':sha(DB/s)} for s in backup_paths]
    metadata={}
    for s in ['입력고정.json','상류_인계증거.json']:
        j=load(CASE/s);metadata[s]={'top_keys':list(j),'value':j}
    checks=[]
    def inspect(v,ptr=''):
        if isinstance(v,dict):
            dest=v.get('destination')
            expected=v.get('sha256')
            if dest and expected:
                target=DB/dest
                checks.append({'destination':dest,'exists':target.is_file(),'expected_sha256':expected,'actual_sha256':sha(target) if target.is_file() else None,'match':target.is_file() and expected==sha(target)})
            for k,x in v.items():inspect(x,ptr+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):inspect(x,ptr+'/'+str(i))
    for x in metadata.values():inspect(x['value'])
    missing=[]
    for s in ['01_진행현황.md','08_검증결과/R8_04_통합검증/00_최종보고.md','07_실행도구/R6_통합조회.py','07_실행도구/R7_연결확인.py','13_품질검수/판정방식_사용자결정.json','05_출처와검토/R7_02_품질항목_조사기록.json','13_품질검수/항목별기준']:
        p=DB/s;missing.append({'path':str(p),'exists':p.exists()})
    result={'target_document':{'id':cards['id'],'version':cards['document_version'],'sha256':sha(DB/'작업초안/쉬운말_지식카드.json'),'human_review':cards['human_review'],'company_approved':cards['company_approved']},'index':{'id':index['id'],'version':index['version'],'sha256':sha(DB/'작업초안/연결목록.json'),'human_review':index['human_review'],'company_approved':index['company_approved']},'card_count':len(cardmap),'index_count':len(index['items']),'same_card_set':set(cardmap)=={x['id'] for x in index['items']},'card_checks':audits,'design_reference':designcheck,'backup_hashes':backups,'transfer_checks':checks,'path_scope_checks':missing,'canonical_registration_for_working_draft':[x for x in catalog['canonical_entries'] if x.get('path','').startswith('작업초안/')]}
    dump(OUT/'local_audit.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

def context_excerpt():
    terms=['기본','후보','screen_state','related_state','배타','미채택','회신','아직','별도','01-A','units']
    paths=['04_기록규격/06_통합최소기록_규격_v0.2.md','08_검증결과/R4_04_보완결과와레드팀.md','01_공통용어/02_기록단위와분류축.md','09_다음단계인계/R7_01-A_구현전_인계.md','09_다음단계인계/R7_R8_스킬재구성_인계.md']
    for rel in paths:
        p=DB/rel;lines=p.read_text(encoding='utf-8-sig').splitlines()
        picked=[(i+1,l) for i,l in enumerate(lines) if any(t in l for t in terms)]
        print(rel,sha(p));print('\n'.join(str(n)+': '+l for n,l in picked))
        with (OUT/'read_evidence.jsonl').open('a',encoding='utf-8') as fp:
            fp.write(json.dumps({'path':str(p),'sha256':sha(p),'scope':'semantic_errata_relevant_lines','read_range':[n for n,l in picked]},ensure_ascii=False)+'\n')
    p=DB/'03_한맥디자인/한맥디자인정본.json';j=json.loads(p.read_text(encoding='utf-8-sig'))
    print(str(p),sha(p));print(json.dumps({k:v for k,v in j.items() if not isinstance(v,(list,dict))},ensure_ascii=False,indent=2))
    print('DESIGN_ROOT_KEYS',list(j))
    for key in ['source','sources','notes','policy','usage_policy','scope','typography','motion']:
        if key in j:print(key,json.dumps(j[key],ensure_ascii=False,indent=2))

def errata_check():
    doc = read(DB/'14_스킬재구성/현재상태_정정표.json')
    checks=[]
    for row in doc['records']:
        references=[]
        for role, refs in [('source', [row['source']]), ('basis', row['basis'])]:
            for ref in refs:
                p=DB/ref['path']
                actual = sha(p) if p.is_file() else None
                references.append({'role': role, 'path': ref['path'], 'exists': p.is_file(), 'expected_sha256': ref['sha256'], 'actual_sha256': actual, 'match': actual == ref['sha256']})
                if p.is_file():
                    read(p, 'errata_source_or_basis_full_file')
        checks.append({'id': row['id'], 'all_hashes_match': all(x['match'] for x in references), 'references': references})
    dump(OUT/'errata_hash_checks.json', checks)
    print(json.dumps(checks, ensure_ascii=False, indent=2))

def verify_unchanged():
    before=json.loads((OUT/'inputs_before.json').read_text(encoding='utf-8'))
    after=snapshot()
    dump(OUT/'inputs_after.json', after)
    result={'files_before': len(before), 'files_after': len(after), 'inputs_unchanged': before == after, 'changed_paths': []}
    b={r['path']:r for r in before};a={r['path']:r for r in after}
    result['changed_paths']=[p for p in sorted(set(b)|set(a)) if b.get(p)!=a.get(p)]
    dump(OUT/'readonly_verification.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result['inputs_unchanged']:
        raise RuntimeError('inputs changed')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('stage', choices=['prepare','criteria_details','preselect','review_read','focus_targets','focus_sources','focus_exact','local_audit','context_excerpt','errata_check','verify_unchanged'])
    args=parser.parse_args()
    stage=args.stage
    stdout=io.StringIO();stderr=io.StringIO();exit_code=0
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            globals()[stage]()
        except Exception:
            exit_code=1
            traceback.print_exc()
    (OUT/(stage+'.stdout.txt')).write_text(stdout.getvalue(),encoding='utf-8')
    (OUT/(stage+'.stderr.txt')).write_text(stderr.getvalue(),encoding='utf-8')
    execution={'stage':stage,'executable':sys.executable,'argv':sys.argv,'python_flags':['-B','-X','utf8'],'exit_code':exit_code,'stdout_file':stage+'.stdout.txt','stderr_file':stage+'.stderr.txt','elapsed_seconds':None,'tokens':None}
    dump(OUT/(stage+'.execution.json'),execution)
    print(stdout.getvalue(),end='')
    print(stderr.getvalue(),end='',file=sys.stderr)
    print(json.dumps(execution,ensure_ascii=False))
    return exit_code

if __name__=='__main__':
    raise SystemExit(main())
