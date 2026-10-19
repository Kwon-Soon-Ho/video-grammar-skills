EXPECTED_PATHS = ('01_공통용어/분류운영규칙.json', '02_원칙과레이아웃/00_지식안내.md', '02_원칙과레이아웃/01_R3_단계별진행안내.md', '02_원칙과레이아웃/02_모션원칙_읽는순서.md', '02_원칙과레이아웃/03_모션원칙_적용예와반례.md', '02_원칙과레이아웃/04_모션원칙_충돌과예외.md', '02_원칙과레이아웃/05_추가모션체계_연결검토.md', '02_원칙과레이아웃/06_레이아웃지식_읽는순서.md', '02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md', '02_원칙과레이아웃/08_화면설계_적용기준과반례.md', '02_원칙과레이아웃/09_문구와화면비_검토사례.md', '02_원칙과레이아웃/10_확장레이아웃_후보와반례.md', '02_원칙과레이아웃/레이아웃_문구와화면비사례.json', '02_원칙과레이아웃/레이아웃_심화지식.json', '02_원칙과레이아웃/레이아웃_확장후보.json', '02_원칙과레이아웃/레이아웃지식.json', '02_원칙과레이아웃/모션과정보전달원칙.json', '02_원칙과레이아웃/모션원칙_심화카드.json', '02_원칙과레이아웃/모션원칙_충돌판단사례.json', '02_원칙과레이아웃/지식목록.md', '02_원칙과레이아웃/추가모션체계_연결후보.json', '02_원칙과레이아웃/화면설계원칙.json', '03_한맥디자인/08_영상적용_예와반례.md', '03_한맥디자인/R5_표시_입력목록.json', '03_한맥디자인/디자인적용_기록규격.json', '03_한맥디자인/디자인적용_설명용예시.json', '03_한맥디자인/영상적용_예와반례.json', '03_한맥디자인/영상전용_미정항목.json', '03_한맥디자인/한맥디자인정본.json', '03_한맥디자인/회사별_디자인연결_현황.json', '04_기록규격/03_근거와주장_기록규격.md', '04_기록규격/06_통합최소기록_규격_v0.2.md', '04_기록규격/근거주장_스키마.json', '04_기록규격/시간프레임_스키마.json', '04_기록규격/좌표변환_스키마.json', '04_기록규격/통합최소기록_설명용_v0.2.json', '04_기록규격/통합최소기록_스키마_v0.2.json', '05_출처와검토/R2_조사기록.json', '05_출처와검토/R3_레이아웃_조사기록.json', '05_출처와검토/R3_모션_조사기록.json', '05_출처와검토/R4_근거주장_조사기록.json', '05_출처와검토/R4_시간프레임_조사기록.json', '05_출처와검토/R4_좌표변환_조사기록.json', '05_출처와검토/R4_통합이관_정책검토안.md', '05_출처와검토/R4_통합이관_조사기록.json', '05_출처와검토/R5_적용정책_결정.json', '05_출처와검토/R5_조사기록.json', '05_출처와검토/R7_02_품질항목_조사기록.json', '05_출처와검토/R7_03_평가계획_조사기록.json', '05_출처와검토/검수결정.json', '05_출처와검토/검수와사용범위/07_한맥디자인과_CI_확인현황.md', '05_출처와검토/검수와사용범위/R6_조사기록.json', '05_출처와검토/검수와사용범위/사람검수_요청목록.json', '05_출처와검토/검수와사용범위/사람검수_접수규격.json', '05_출처와검토/검수와사용범위/사람검수_접수대장.json', '05_출처와검토/검수와사용범위/사람검수_접수정책.json', '05_출처와검토/검수와사용범위/사람답변원문/2026-10-15_8회사CI_최신자료와산하AI부재.json', '05_출처와검토/검수와사용범위/원문경로_복구연결.json', '05_출처와검토/검수와사용범위/작업정책_연결목록.json', '05_출처와검토/검수와사용범위/출처와사용범위_연결규격.json', '05_출처와검토/검수와사용범위/출처와사용범위_연결목록.json', '05_출처와검토/검수와사용범위/통합검수_입력규격.json', '05_출처와검토/검수와사용범위/한맥디자인_대화근거.json', '05_출처와검토/사용자결정.json', '05_출처와검토/스킬심층검토/검토파일목록.json', '05_출처와검토/스킬심층검토/스킬심층검토정본.json', '05_출처와검토/출처목록.json', '06_맞춤스킬/00_스킬안내.md', '06_맞춤스킬/01_시범사용안내.md', '06_맞춤스킬/video-guidance-reviewer/SKILL.md', '06_맞춤스킬/video-guidance-reviewer/evals/evals.json', '06_맞춤스킬/video-guidance-reviewer/references/작업기준.md', '06_맞춤스킬/video-knowledge-curator/SKILL.md', '06_맞춤스킬/video-knowledge-curator/evals/evals.json', '06_맞춤스킬/video-knowledge-curator/references/작업기준.md', '06_맞춤스킬/video-record-steward/SKILL.md', '06_맞춤스킬/video-record-steward/evals/evals.json', '06_맞춤스킬/video-record-steward/evals/files/검사입력.json', '06_맞춤스킬/video-record-steward/references/작업기준.md', '06_맞춤스킬/자료목록.json', '06_맞춤스킬/평가계획.json', '07_실행도구/R5_디자인적용검사.py', '07_실행도구/R6_사람검수.py', '07_실행도구/R6_출처사용검사.py', '07_실행도구/R6_통합조회.py', '07_실행도구/R7_연결확인.py', '07_실행도구/근거주장_규격검사.py', '07_실행도구/시간프레임_규격검사.py', '07_실행도구/좌표변환_규격검사.py', '07_실행도구/통합기록_규격검사.py', '08_검증결과/Phase00_종료재감사.md', '08_검증결과/R6_R7_최종레드팀.md', '08_검증결과/R7_03_마무리확인.json', '08_검증결과/R7_최종반례검사.json', '09_다음단계인계/R6_검수연결_인계.md', '10_공용자산/CI색상목록.json', '10_공용자산/자산목록.json', '10_공용자산/회사목록.json', '13_품질검수/01_기존자료와_보완목록.md', '13_품질검수/02_품질판정방식_검토안.md', '13_품질검수/03_판정운영기준.md', '13_품질검수/05_사람검수_준비목록.md', '13_품질검수/사람검수_준비목록.json', '13_품질검수/연결과인계/03_검수와보류_연결규칙.md', '13_품질검수/연결과인계/기존기록_연결표.json', '13_품질검수/연결과인계/연결방식_사용자결정.json', '13_품질검수/연결과인계/품질검수_작성양식.json', '13_품질검수/판정방식_사용자결정.json', '13_품질검수/평가계획/00_진행방식_검토안.md', '13_품질검수/평가계획/01_정답과_판정단위.md', '13_품질검수/평가계획/02_표본과_유출방지.md', '13_품질검수/평가계획/03_지표와_분모.md', '13_품질검수/평가계획/04_판단보류와_미채점.md', '13_품질검수/평가계획/05_사람의견차이와_중재.md', '13_품질검수/평가계획/06_재시험과_비교.md', '13_품질검수/평가계획/07_실행전_검토목록.md', '13_품질검수/평가계획/08_정리된_판정예.md', '13_품질검수/평가계획/지표정의_정본.json', '13_품질검수/평가계획/진행방식_사용자결정.json', '13_품질검수/평가계획/평가설계_정본.json', '13_품질검수/평가계획/항목별_평가준비표.json', '13_품질검수/품질항목_정본.json', '13_품질검수/항목별기준/01_정보와데이터.md', '13_품질검수/항목별기준/02_한국어와단위.md', '13_품질검수/항목별기준/03_자막과전달경로.md', '13_품질검수/항목별기준/04_화면과도표.md', '13_품질검수/항목별기준/05_모션과시간.md', '13_품질검수/항목별기준/06_브랜드와출처.md', '13_품질검수/항목별기준/07_분석신뢰도.md', 'backup/2026-10-15_R6_03_초안/검토전사본/05_출처와검토/검수와사용범위/사람검수_요청목록.json')

"""R7 기반 참조 읽기 확인. 영상/실제 기록/사람 내용/승인을 검사하지 않는다."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, math, re

MANIFEST='13_품질검수/연결과인계/현재연결_입력고정.json'
MAP='13_품질검수/연결과인계/기존기록_연결표.json'
FORM='13_품질검수/연결과인계/품질검수_작성양식.json'
MODE='13_품질검수/연결과인계/연결방식_사용자결정.json'
QUALITY='13_품질검수/품질항목_정본.json'
PLAN='13_품질검수/평가계획/평가설계_정본.json'
COVERAGE='13_품질검수/평가계획/항목별_평가준비표.json'
R4='04_기록규격/통합최소기록_설명용_v0.2.json'
R5='03_한맥디자인/디자인적용_설명용예시.json'
R6='05_출처와검토/검수와사용범위/사람검수_접수대장.json'
MAX_BYTES=8*1024*1024

def local(base,rel):
    if not isinstance(rel,str) or not rel or '\\' in rel or ':' in rel:
        raise ValueError('invalid_relative_path')
    p=PurePosixPath(rel)
    if p.is_absolute() or any(v in ('','.','..') for v in rel.split('/')):
        raise ValueError('unsafe_path')
    result=(base/Path(*p.parts)).resolve()
    if not result.is_relative_to(base):raise ValueError('path_outside_base')
    return result

def bytes_at(base,path):
    with local(base,path).open('rb') as f:raw=f.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise ValueError('file_size_limit')
    return raw

def digest(raw):return hashlib.sha256(raw).hexdigest()

def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate_json_key')
        d[k]=v
    return d

def integer(s):
    if len(s.lstrip('-'))>128:raise ValueError('integer_size_limit')
    return int(s)

def floating(s):
    v=float(s)
    if not math.isfinite(v):raise ValueError('nonfinite_json_number')
    return v

def reject_constant(s):raise ValueError('nonfinite_json_constant')

def parse(raw):
    d=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_int=integer,parse_float=floating,parse_constant=reject_constant)
    todo=[(d,0)]
    while todo:
        value,depth=todo.pop()
        if depth>100:raise ValueError('json_depth_limit')
        if isinstance(value,str) and any(0xD800<=ord(c)<=0xDFFF for c in value):raise ValueError('json_surrogate')
        if isinstance(value,dict):todo.extend((v,depth+1) for pair in value.items() for v in pair)
        elif isinstance(value,list):todo.extend((v,depth+1) for v in value)
    return d

def identity(d):
    if not isinstance(d,dict):return None,None
    return next((d[k] for k in ['id','$id','record_id','application_id'] if k in d),None),d.get('version',d.get('schema_version'))

def checked_ref(ref,files):
    if not isinstance(ref,dict) or not isinstance(ref.get('path'),str) or ref['path'] not in files:raise ValueError('reference_not_in_fixed_files')
    if ref.get('sha256')!=files[ref['path']]['sha256']:raise ValueError('reference_hash_mismatch')
    if 'version' in ref and ref['version']!=files[ref['path']]['version']:raise ValueError('reference_version_mismatch')

def inspect(base):
    out={'valid':False,'scope':'fixed_foundation_files_and_mapping_structure_only','errors':[],
         'file_pin_count':0,'criteria_mapping_count':0,'field_location_count':0,
         'r6_fixed_files_current':False,'r6_live_query_executed':False,'r6_declaration_context_validated':False,
         'actual_R4_R5_records_validated':False,'actual_R7_review_records_validated':False,
         'actual_video_analyzed':False,'content_verified':False,'human_identity_authenticated':False,
         'company_approved':False,'permission_granted':False,'operational_release':False,
         'readiness_proposal':'not_evaluated','requires_separate_r6_and_actual_record_and_content_checks':True}
    try:
        base=Path(base).resolve()
        manifest_raw=bytes_at(base,MANIFEST);m=parse(manifest_raw)
        if not isinstance(m,dict) or set(m)!={'id','version','scope','pins'}:raise ValueError('manifest_shape')
        if (m['id'],m['version'],m['scope'])!=('r7-foundation-link-context','0.1.0','fixed_foundation_references_only'):raise ValueError('manifest_identity_scope')
        if not isinstance(m['pins'],list) or len(m['pins'])!=len(EXPECTED_PATHS):raise ValueError('pin_count')
        files={};loaded={};snapshots={}
        for pin in m['pins']:
            if not isinstance(pin,dict) or set(pin)!={'path','sha256','id','version'}:raise ValueError('pin_shape')
            path=pin['path']
            if not isinstance(path,str) or path not in EXPECTED_PATHS or path in files:raise ValueError('unexpected_or_duplicate_path')
            if not isinstance(pin['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',pin['sha256']):raise ValueError('invalid_hash')
            raw=bytes_at(base,path)
            if digest(raw)!=pin['sha256']:raise ValueError('fixed_file_changed:'+path)
            snapshots[path]=digest(raw);files[path]=pin
            if path.endswith('.json'):
                loaded[path]=parse(raw)
                if identity(loaded[path])!=(pin['id'],pin['version']):raise ValueError('file_identity_version_changed:'+path)
            elif pin['id'] is not None or pin['version'] is not None:raise ValueError('nonjson_identity')
        if set(files)!=set(EXPECTED_PATHS):raise ValueError('missing_fixed_path')
        quality=loaded[QUALITY];plan=loaded[PLAN];fieldmap=loaded[MAP];form=loaded[FORM]
        if loaded[MODE].get('selected')!='A' or loaded[MODE].get('actual_content_review') is not False:raise ValueError('mode_not_supported')
        for key in ['outcome_policy_ref','operation_ref','source_catalog_ref']:checked_ref(quality[key],files)
        for key in ['policy_ref','outcome_policy_ref','metrics_ref','coverage_ref','research_ref']:checked_ref(plan[key],files)
        for ref in plan['document_refs']:checked_ref(ref,files)
        checked_ref(fieldmap['criteria_ref'],files)
        checked_ref(loaded[COVERAGE]['criteria_ref'],files)
        cards=quality['cards']
        if not isinstance(cards,list) or len(cards)!=26:raise ValueError('quality_card_count')
        cids=[c['id'] for c in cards]
        if len(cids)!=len(set(cids)):raise ValueError('duplicate_criterion_id')
        cards_by_id={c['id']:c for c in cards}
        bids=[]
        for binding in fieldmap['bindings']:
            if binding['id'] in bids:raise ValueError('duplicate_binding_id')
            bids.append(binding['id'])
            path=binding['structure_reference']
            if path not in (R4,R5,R6) or path not in files:raise ValueError('unknown_structure_source')
            if binding['structure_reference_sha256']!=files[path]['sha256'] or binding['actual_evidence'] is not False:raise ValueError('structure_source_scope')
            keys=binding['key_path']
            if not isinstance(keys,list) or not keys or not all(isinstance(k,str) and k for k in keys):raise ValueError('invalid_key_path')
            value=loaded[path]
            for key in keys:
                if not isinstance(value,dict) or key not in value:raise ValueError('structure_key_missing')
                value=value[key]
        rows=fieldmap['criteria_links']
        if len(rows)!=26 or {r['criterion_ref'] for r in rows}!=set(cids):raise ValueError('criterion_map_coverage')
        for row in rows:
            c=cards_by_id[row['criterion_ref']]
            if (row['group'],row['required_evidence'],row['hold_when'],row['human_role'])!=(c['group'],c['required_evidence'],c['hold_when'],c['human_review']['role']):raise ValueError('criterion_map_drift')
            for key in ['binding_candidates','human_context_candidates']:
                ids=row[key]
                if not isinstance(ids,list) or len(ids)!=len(set(ids)) or not set(ids)<=set(bids):raise ValueError('binding_reference_invalid')
            if row['actual_target_ref'] is not None or row['actual_evidence_refs']!=[] or row['actual_review_result'] is not None:raise ValueError('mapping_cannot_claim_actual_review')
        if fieldmap['actual_R7_record_links']!=0 or fieldmap['structure_examples_are_not_real_evidence'] is not True or fieldmap['R6_context_is_not_R7_approval'] is not True:raise ValueError('mapping_scope')
        if form['kind']!='unfilled_template_not_actual_review_or_R4_record' or form['actual_review_count']!=0 or form['actual_target_count']!=0:raise ValueError('form_scope')
        if any(v is not None and v!=[] for v in form['blank_fields'].values()):raise ValueError('form_not_blank')
        if any(form[k] is not False for k in ['company_approved','permission_granted','operational_release']):raise ValueError('form_approval_forbidden')
        if digest(bytes_at(base,MANIFEST))!=digest(manifest_raw):raise ValueError('manifest_changed_during_check')
        for path,old in snapshots.items():
            if digest(bytes_at(base,path))!=old:raise ValueError('input_changed_during_check:'+path)
        out.update(valid=True,file_pin_count=len(files),criteria_mapping_count=len(rows),field_location_count=len(bids),r6_fixed_files_current=True)
    except Exception as e:
        out['errors'].append({'code':type(e).__name__,'detail':str(e)[:500]})
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(description='R7 기반 파일/참조 연결 읽기 확인. 내용/실제 기록/승인 검사 아님.')
    ap.add_argument('--base',required=True);args=ap.parse_args()
    result=inspect(args.base);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['valid'] else 1)
