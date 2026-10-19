"""R5 프로젝트 디자인 초안의 참조 연결 검사. 화면 생성·승인·영상 분석 없음."""
from pathlib import Path, PurePosixPath
import argparse,copy,hashlib,importlib.util,json,re
from jsonschema import Draft202012Validator,FormatChecker
BASE=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('중복 JSON 키: '+ascii(k))
            out[k]=v
        return out
    def nonfinite(s):raise ValueError('비유한 JSON 수: '+s)
    return json.loads(Path(p).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=nonfinite)
def local(value,base):
    if not isinstance(value,str) or not value.strip():raise ValueError('빈 경로')
    value=value.replace('\\','/')
    if ':' in value or value.startswith('/') or '..' in PurePosixPath(value).parts:raise ValueError('루트 밖 경로')
    p=(base/value).resolve()
    if not p.is_relative_to(base.resolve()):raise ValueError('루트 밖 연결점')
    return p

def inspect(data,base=BASE):
    """입력 변경/파일 쓰기 없음. valid는 구조와 참조만 뜻한다."""
    base=Path(base).resolve();errors=[];pending=[];resolved=[]
    def err(s):errors.append(s)
    try:
        json.dumps(data,ensure_ascii=False,allow_nan=False).encode('utf-8')
        schema=read(base/'03_한맥디자인/디자인적용_기록규격.json');Draft202012Validator.check_schema(schema)
        errors += [str(list(e.path))+': '+e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data)]
        if errors:return result(errors,pending,resolved)
        expected={
          'companies':('10_공용자산/회사목록.json','record_version'),
          'assets':('10_공용자산/자산목록.json','record_version'),
          'colors':('10_공용자산/CI색상목록.json','record_version'),
          'hanmac':('03_한맥디자인/한맥디자인정본.json','version'),
          'policy':('05_출처와검토/R5_적용정책_결정.json',None)}
        docs={}
        for key,(rel,vkey) in expected.items():
            d=read(base/rel);docs[key]=d;p=data['source_pins'][key]
            if p['path']!=rel or p['sha256']!=sha(base/rel) or p['version']!=(d[vkey] if vkey else 'A@2026-10-15'):err(key+' 정본 경로·버전·hash 불일치')
        if errors:return result(errors,pending,resolved)
        c,a,k,h=docs['companies'],docs['assets'],docs['colors'],docs['hanmac']
        spec=importlib.util.spec_from_file_location('r5_link_r1',base/'07_실행도구/R1_자산검사.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        check=m.inspect(c,a,k,base=base)
        if not check['valid']:errors+=['R1 '+e for e in check['errors']];return result(errors,pending,resolved)
        if docs['policy']['selected']!='A' or docs['policy']['state']!='user_directed':err('사용자 A 정책 필요')
        members={x['company_id']:x for x in c['companies'] if x['status']!='candidate'}
        targets=data['company_ids']
        if any(cid not in members for cid in targets):err('확인되지 않은 대상 회사')
        if (data['ownership']=='single_company')!=(len(targets)==1):err('단독/공동 회사 범위 불일치')
        if data['ownership']=='multi_company':pending.append('공동주체·대표색·로고 크기/순서/동등성은 사람이 결정. 회사순서에서 자동 추정 금지')
        amap={(x['asset_id'],x['record_version']):x for x in a['records']}
        cmap={(x['company_id'],x['color_id'],x['record_version']):x for x in k['colors']}
        tokens={x['id']:x for x in h['color_tokens']}
        rolekeys=[];logokeys=[]
        for logo in data['logos']:
            cid=logo['company_id'];ref=logo['asset_ref'];key=(cid,ref['asset_id'],ref['record_version']);logokeys.append(key)
            asset=amap.get(key[1:])
            if cid not in targets or asset is None or cid not in asset['company_ids'] or asset['kind']!='logo' or asset['revision_state']!='current' or asset['registration_state']!='registered' or ref['sha256']!=asset['file']['sha256']:err('선택 로고 소속·현재 버전·hash 불일치')
            pending.append(cid+' 로고: 공식 최신판/언어·가로세로·반전/단색형·보호공간·최소크기·배경/배포 범위 검수. 선택 메모만으로 증명 안 됨')
        if len(logokeys)!=len(set(logokeys)):err('같은 회사·로고 중복 선택')
        if data['logo_intent']=='selected' and not data['logos']:err('로고 선택 의도에 자산 없음')
        if data['logo_intent']!='selected' and data['logos']:err('로고 의도와 선택 목록 모순')
        if data['logo_intent']=='undecided':pending.append('로고 필요 여부·선택 미정')
        for role in data['color_roles']:
            rolekeys.append((role['company_id'],role['role']))
            cid=role['company_id'];source=role['source'];sel=role['selection']
            if cid is not None and cid not in targets:err('색 역할이 대상 회사 밖에 있음')
            if data['data_scope']=='spec_example' and sel['kind']!='synthetic_example':err('설명용 역할을 실제 디자이너 선택으로 표시')
            if data['data_scope']=='actual_project_draft' and sel['kind']!='designer_declaration':err('실제 초안에 합성 선택 근거')
            hexvalue=None;origin=source['kind']
            if origin=='ci_color':
                color=cmap.get((cid,source['color_id'],source['record_version']))
                if not color:err('없는 회사·CI색 버전')
                else:
                    if cid not in members or color['ci_asset_ref'] not in members[cid]['ci_asset_refs']:err('현재 회사 CI 참조 밖의 색')
                    asset=amap.get((color['ci_asset_ref']['asset_id'],color['ci_asset_ref']['record_version']))
                    if not asset or asset['revision_state']!='current':err('현재 CI가 아닌 색')
                    if color['revision_state']!='current' or color['verification']['state']!='source_checked' or color['screen_value'] is None:err('미확인/변환 미정/과거 CI색 역할 지정')
                    elif color['screen_value']['color_space']!='srgb' or color['screen_value']['alpha']!=1:err('이 초안 계약은 불투명 sRGB 역할만 지원')
                    else:hexvalue=color['screen_value']['hex']
                    if source['source_level']!=color['source_level']:err('CI색의 관측/선언 자격 변경')
                    pending.append(str(cid)+' '+role['role']+': 관측색의 가정·역할 적합성·선택자/실제 선택 확인')
            elif origin=='hanmac_token':
                t=tokens.get(source['token_id'])
                if not data['use_hanmac_library'] or cid is not None:err('한맥 공통색의 명시 선택 또는 공통 자격 누락')
                if not t or t['scope']!='global_color_library' or t['type']!='color':err('없는 전역 한맥 색 토큰')
                else:hexvalue=t['value']
            else:
                hexvalue=source['hex'];pending.append('프로젝트 새 색: CI 원색/한맥 정본색이 아님. 선택 목적·조합 검수')
            if hexvalue:resolved.append({'company_id':cid,'role':role['role'],'hex':hexvalue,'origin':origin,'use':'project_draft_candidate','review_status':'pending'})
        if len(rolekeys)!=len(set(rolekeys)):err('회사·역할 중복; 명시 대안은 별도 초안으로 비교')
        globalroles={role for cid,role in rolekeys if cid is None}
        if any(cid is not None and role in globalroles for cid,role in rolekeys):err('공통·회사 역할 우선순위 모호함; 범위별 별도 초안으로 분리')
        styles={x['id'] for x in h['references']+h['gradients']}
        for ref in data['optional_style_refs']:
            if ref not in styles or not data['use_hanmac_library']:err('선택 스타일 ID/공통 참고 선택 불일치')
            pending.append(ref+': 선택 참고의 목적/시점/표면·타입·UI 적용성 검수. 필수 UI/영상 수치로 승격 금지')
        r=data['linked_r4_record']
        if r is not None:
            p=local(r['path'],base)
            if p.relative_to(base).parts[0] not in ['04_기록규격','12_통합기록']:err('R4 연결은 현재 규격 예시 또는 통합기록만 허용')
            elif not p.is_file() or sha(p)!=r['sha256']:err('R4 파일 hash 불일치')
            else:
                d=read(p)
                if not isinstance(d,dict):err('R4 링크 JSON은 객체여야 함');return result(errors,pending,resolved)
                if d.get('schema_version')!='0.2.0' or d.get('record_id')!=r['record_id'] or d.get('version')!=r['version']:err('R4 기록 ID·버전 불일치')
                if data['data_scope']=='actual_project_draft' and p.relative_to(base).parts[0]!='12_통합기록':err('규격 예시를 실제 프로젝트 원본으로 연결')
                if data['data_scope']=='actual_project_draft':
                    spatial=d.get('spatial_contract');evidence=spatial.get('evidence_contract') if isinstance(spatial,dict) else None
                    time=evidence.get('time_contract') if isinstance(evidence,dict) else None
                    if not isinstance(evidence,dict) or evidence.get('record_purpose')!='draft_record' or not isinstance(time,dict) or time.get('source_type') not in ['internal','external']:err('실제 초안에 합성/미상 R4 범위 연결 금지')
                pending.append('R4 연결은 참조만 확인. 동영상 관측값 변경·가족사 토큰을 R4 한맥 필드에 삽입·품질 승인 안 됨')
        if data['output_context']['width'] is None:pending.append('출력 해상도·최종 표시 크기 미정')
        if data['output_context']['background_condition']=='unknown':pending.append('로고/글자의 최종 배경 미정')
        pending+=['최종 프레임·한국어/숫자·단위·자막·시청환경·움직이는 배경 검수','로컬 해시는 원문 무결성이다. 최신성/공식성/디자이너 identity·회사/운영 승인 증명 안 됨']
        return result(errors,pending,resolved)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as e:
        return result(errors+['검사 입력/필수 참조 오류: '+ascii(str(e))],pending,resolved)

def result(errors,pending,resolved):
    return {'valid':not errors,'scope':'구조/현재 참조·정책 검수. 실제 디자인 품질·선택자 인증/회사 승인 아님.','errors':errors,'human_review_queue':list(dict.fromkeys(pending)),'resolved_draft_candidates':resolved,'company_approved':False,'fact_verified':False,'human_selection_verified':False,'operational_release':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('record');args=p.parse_args()
    try:r=inspect(read(Path(args.record)))
    except (OSError,ValueError,RecursionError) as e:r=result(['JSON/파일 읽기 오류: '+ascii(str(e))],[],[])
    print(json.dumps(r,ensure_ascii=True,allow_nan=False,indent=2));return 0 if r['valid'] else 1
if __name__=='__main__':raise SystemExit(main())
