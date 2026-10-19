"""R1 자료 등록/회사 CI 기록 검사. 파일 진위·승인·영상 내용은 판정하지 않는다."""
from pathlib import Path, PurePosixPath
import argparse, json, hashlib, math, re
from jsonschema import Draft202012Validator, FormatChecker

BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def schema_check(data,name):
    schema=read('00_운영계약/'+name);Draft202012Validator.check_schema(schema)
    return [name+': '+ '/'.join(map(str,e.path))+': '+e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data)]
def local_path(value,base=BASE):
    if not isinstance(value,str) or not value.strip():raise ValueError('빈 경로')
    value=value.replace('\\','/')
    if ':' in value or value.startswith('/') or '..' in PurePosixPath(value).parts:raise ValueError('루트 밖/절대/상위 경로')
    p=(base/value).resolve()
    if not p.is_relative_to(base.resolve()):raise ValueError('연결점으로 루트 밖 경로')
    return p
def nonfinite(x):
    if isinstance(x,float):return not math.isfinite(x)
    if isinstance(x,dict):return any(nonfinite(v) for v in x.values())
    if isinstance(x,list):return any(nonfinite(v) for v in x)
    return False
def inspect(companies,assets,colors,base=BASE):
    errors=[];warnings=[]
    for data,name in [(companies,'회사목록_규격.json'),(assets,'자산목록_규격.json'),(colors,'CI색상목록_규격.json')]:errors+=schema_check(data,name)
    if any(nonfinite(d) for d in [companies,assets,colors]):errors.append('NaN/Infinity 기록 금지')
    if errors:return {'valid':False,'errors':errors,'warnings':warnings,'collection_complete':False}
    members=companies['companies'];cids=[x['company_id'] for x in members]
    if len(cids)!=len(set(cids)):errors.append('회사ID 중복')
    if len({x['name_ko'].strip().casefold() for x in members})!=len(members):errors.append('동일 회사명 중복; 자동 병합 대신 검토 필요')
    confirmed={x['company_id'] for x in members if x['status']!='candidate'}
    company_count=companies['expected_company_count']
    if companies['list_status']=='confirmed' and (len(members)!=company_count or len(confirmed)!=company_count):errors.append('확정 명단은 사용자 결정한 회사 수와 일치해야 함')
    if companies['list_status']!='confirmed':warnings.append('가족사 명단 확인 전')
    if assets['scope']!=colors['scope']:errors.append('자산/색상 actual·synthetic 범위 혼합')
    actual=assets['scope']=='actual_registry'
    if actual and any(c['membership_source']['kind']=='synthetic_example' for c in members):errors.append('실제 회사 목록에 설명용 명단 근거')
    records=assets['records'];keys=[(a['asset_id'],a['record_version']) for a in records]
    if len(keys)!=len(set(keys)):errors.append('동일 자산ID·버전 중복/충돌')
    by={(a['asset_id'],a['record_version']):a for a in records}
    current={}
    for a in records:
        if a['revision_state']=='current':
            if a['asset_id'] in current:errors.append('자산의 현재 버전이 여러 개: '+a['asset_id'])
            current[a['asset_id']]=a
    def target(ref,label,registered=False):
        a=by.get((ref['asset_id'],ref['record_version']))
        if not a:errors.append(label+' 대상 ID·버전 없음');return None
        if ref['sha256']!=a['file']['sha256']:errors.append(label+' 대상 파일해시 불일치')
        if registered and a['registration_state']!='registered':errors.append(label+' 실제 파일 등록 필요')
        return a
    graph={key:[] for key in by}
    for a in records:
        label=a['asset_id']+'@'+a['record_version']
        for cid in a['company_ids']:
            if cid not in confirmed:errors.append(label+' 미확인/없는 회사ID')
        if actual and (a['source_origin']=='synthetic_example' or a['source']['kind']=='synthetic_example'):errors.append(label+' 설명용 자산을 실제 목록에 등록')
        if a['source_origin']=='synthetic_example' and a['source']['kind']!='synthetic_example':errors.append(label+' 설명용 출처 혼동')
        file=a['file']
        if a['registration_state']=='registered':
            if not file['path'] or not file['sha256']:errors.append(label+' 등록 파일 경로·해시 누락')
            elif actual:
                try:
                    p=local_path(file['path'],base)
                    if not p.is_file():errors.append(label+' 등록 파일 없음')
                    elif sha(p)!=file['sha256']:errors.append(label+' 실제 파일해시 불일치')
                except ValueError as e:errors.append(label+' '+str(e))
        elif file['path'] is not None or file['sha256'] is not None:errors.append(label+' 파일없는 대기상태에 경로/해시 채움')
        for relation in a['relationships']:
            other=target(relation['target'],label+' 관계',a['registration_state']=='registered' and relation['relation']=='derived_from')
            if not other:continue
            source_key=(a['asset_id'],a['record_version']);target_key=(other['asset_id'],other['record_version'])
            if relation['relation'] in ['derived_from','variant_of','supersedes']:graph[source_key].append(target_key)
            if source_key==target_key:errors.append(label+' 자기참조')
            if relation['relation']=='scenario_for' and (a['kind']!='scenario' or other['kind']!='video'):errors.append(label+' 시나리오/영상 관계 종류 불일치')
            if relation['relation']=='supersedes' and a['asset_id']!=other['asset_id']:errors.append(label+' 다른자산을 이전버전으로 연결')
        if a['role'] in ['derived','generated_output']:
            if not any(x['relation']=='derived_from' for x in a['relationships']) or a['generation'] is None:errors.append(label+' 파생 입력·생성 방법 누락')
        elif a['generation'] is not None or any(x['relation']=='derived_from' for x in a['relationships']):errors.append(label+' 원본/참고를 파생처럼 기록')
        if a['kind'] in ['extracted_frame','proxy','transcript','reconstructed_image'] and a['role']!='derived':errors.append(label+' 파생자료의 원본 오인')
        if a['kind']=='analysis_output' and a['role']!='generated_output':errors.append(label+' 분석산출물 역할 오류')
        if a['usage']['state']=='permitted_for_context' and (not a['usage']['contexts'] or not a['usage']['evidence']):errors.append(label+' 사용맥락 허용의 근거 누락')
    visiting=set();done=set()
    def visit(k):
        if k in visiting:errors.append('원본/변형/버전 순환관계');return
        if k in done:return
        visiting.add(k)
        for nxt in graph[k]:visit(nxt)
        visiting.remove(k);done.add(k)
    for k in graph:visit(k)
    for c in members:
        for ref in c['ci_asset_refs']:
            a=target(ref,c['company_id']+' CI')
            if a and (a['kind'] not in ['logo','ci_guide'] or c['company_id'] not in a['company_ids']):errors.append('회사 CI 대상·소속 불일치')
    color_keys=[(x['company_id'],x['color_id'],x['record_version']) for x in colors['colors']]
    if len(color_keys)!=len(set(color_keys)):errors.append('동일 색상ID·버전 중복')
    color_current=set()
    for color in colors['colors']:
        label=color['color_id']+'@'+color['record_version'];cid=color['company_id']
        if cid not in confirmed:errors.append(label+' 미확인/없는 회사ID')
        if color['revision_state']=='current':
            key=(cid,color['color_id'])
            if key in color_current:errors.append(label+' 색상의 현재 버전 여러 개')
            color_current.add(key)
        checked=color['verification']['state']=='source_checked'
        ci=target(color['ci_asset_ref'],label+' CI',checked);evidence=target(color['evidence_asset_ref'],label+' 색상근거',checked)
        if ci and (ci['kind']!='logo' or cid not in ci['company_ids']):errors.append(label+' CI 소속·종류 불일치')
        if evidence and cid not in evidence['company_ids']:errors.append(label+' 색상근거 회사범위 불일치')
        if color['source_level']=='official_declared' and evidence and evidence['kind'] not in ['ci_guide','reference_document']:errors.append(label+' 관측 로고를 공식색 선언 근거로 사용')
        if checked and (not (color['verification']['checked_by'] or '').strip() or not color['verification']['checked_at']):errors.append(label+' 원문대조자·시각 누락')
        raw=color['raw_value'];value=raw['value'];notation=raw['notation'];screen=color['screen_value'];method=color['normalization']['method']
        if color['source_level']=='official_declared' and method in ['raster_sample','vector_value_read']:errors.append(label+' 관측 방법을 공식 선언으로 승격')
        if color['source_level']=='vector_literal' and method=='raster_sample':errors.append(label+' 벡터 원문과 픽셀 추출 방법 혼합')
        observation=color.get('observation')
        if color['source_level']=='raster_sample' or method=='raster_sample':
            if not observation or not all(observation.get(k) for k in ['region','alpha_handling','background_handling','profile_assumption']):errors.append(label+' 래스터 샘플 영역·알파·배경·프로필 가정 누락')
        if method=='documented_conversion' and not color['normalization']['source_profile']:errors.append(label+' 변환 출력조건 누락')
        if notation=='HEX' and (not isinstance(value,str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}',value)):errors.append(label+' HEX 표기 오류')
        if notation in ['RGB','CMYK']:
            expected=3 if notation=='RGB' else 4;limit=255 if notation=='RGB' else 100
            if not isinstance(value,list) or len(value)!=expected or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not 0<=v<=limit for v in value):errors.append(label+' 색 채널·범위 오류')
        if notation=='PANTONE' and not isinstance(value,str):errors.append(label+' 별색 원문 이름 필요')
        if screen:
            if method=='none':errors.append(label+' 화면값의 관측/변환 방법 없음')
            if notation in ['CMYK','PANTONE'] and (method!='documented_conversion' or not color['normalization']['source_profile']):errors.append(label+' 인쇄/별색 무조건 HEX 변환')
            space=(raw['declared_color_space'] or '').strip().casefold()
            if method=='exact_srgb_identity' or space=='srgb':
                if space!='srgb':errors.append(label+' 색공간 미확인 sRGB 단정')
                expected=None
                if notation=='HEX' and isinstance(value,str):expected=value.upper()
                if notation=='RGB' and isinstance(value,list) and len(value)==3 and all(isinstance(v,int) and not isinstance(v,bool) and 0<=v<=255 for v in value):expected='#'+''.join(f'{v:02X}' for v in value)
                if expected!=screen['hex'] or (screen['alpha']!=1 and (method=='exact_srgb_identity' or color['source_level']=='official_declared')):errors.append(label+' 원문 sRGB값 변경 또는 불투명 identity 위반')
            if color['source_level']=='raster_sample' and method!='raster_sample':errors.append(label+' 이미지 추출값 방법 혼동')
        elif method!='none':errors.append(label+' 화면값 없는 변환 표기')
    logo_companies=set()
    for c in members:
        for ref in c['ci_asset_refs']:
            a=by.get((ref['asset_id'],ref['record_version']))
            if a and a['kind']=='logo' and a['role']=='original' and a['registration_state']=='registered' and a['revision_state']=='current':logo_companies.add(c['company_id'])
    def current_ci(color):
        ref=color['ci_asset_ref'];a=by.get((ref['asset_id'],ref['record_version']))
        c=next((c for c in members if c['company_id']==color['company_id']),None)
        return a and c and a['revision_state']=='current' and ref in c['ci_asset_refs']
    colored={x['company_id'] for x in colors['colors'] if current_ci(x) and x['source_level']!='ui_proposal' and x['revision_state']=='current' and x['verification']['state']=='source_checked' and x['screen_value'] is not None}
    official={x['company_id'] for x in colors['colors'] if current_ci(x) and x['source_level']=='official_declared' and x['revision_state']=='current' and x['verification']['state']=='source_checked' and x['screen_value'] is not None}
    complete=not errors and actual and companies['list_status']=='confirmed' and len(confirmed)==company_count and confirmed<=logo_companies and confirmed<=colored
    official_complete=complete and confirmed<=official
    if not complete:warnings.append('회사별 원본 CI·관측색 자료 수집/검토 미완료')
    if not official_complete:warnings.append('공식 지정색 전체 확인 미완료; 관측색은 공식값 아님')
    return {'valid':not errors,'errors':errors,'warnings':warnings,'collection_complete':complete,'official_values_complete':official_complete,'counts':{'companies':len(members),'assets':len(records),'colors':len(colors['colors'])}}
def palette(company_id,companies,colors,include_observed=False,include_proposals=False,assets=None,base=BASE):
    if assets is None:assets=read('10_공용자산/자산목록.json')
    result=inspect(companies,assets,colors,base)
    if not result['valid'] or assets['scope']!='actual_registry':return {'company_id':company_id,'colors':[],'reason':'검증 실패 또는 실제 목록 아님','errors':result['errors']}
    if company_id not in {x['company_id'] for x in companies['companies'] if x['status']!='candidate'}:return {'company_id':company_id,'colors':[],'reason':'확인된 회사 없음'}
    allowed={'official_declared'}
    if include_observed:allowed|={'vector_literal','raster_sample'}
    if include_proposals:allowed.add('ui_proposal')
    c=next(x for x in companies['companies'] if x['company_id']==company_id)
    by={(a['asset_id'],a['record_version']):a for a in assets['records']}
    selected=[x for x in colors['colors'] if x['company_id']==company_id and x['revision_state']=='current' and x['source_level'] in allowed and x['verification']['state']=='source_checked' and x['screen_value'] is not None and x['ci_asset_ref'] in c['ci_asset_refs'] and by[(x['ci_asset_ref']['asset_id'],x['ci_asset_ref']['record_version'])]['revision_state']=='current']
    return {'company_id':company_id,'colors':selected,'reason':None if selected else '해당 조건의 확인된 화면색 없음','authority':'원문대조/관측/제안의 기록. 회사 필수화·페이지 품질 승인 아님.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--colors');p.add_argument('--include-observed',action='store_true');p.add_argument('--include-proposals',action='store_true');args=p.parse_args()
    companies=read('10_공용자산/회사목록.json');assets=read('10_공용자산/자산목록.json');colors=read('10_공용자산/CI색상목록.json')
    result=inspect(companies,assets,colors)
    if args.colors and result['valid']:result['palette']=palette(args.colors,companies,colors,args.include_observed,args.include_proposals)
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['valid'] else 1
if __name__=='__main__':raise SystemExit(main())
