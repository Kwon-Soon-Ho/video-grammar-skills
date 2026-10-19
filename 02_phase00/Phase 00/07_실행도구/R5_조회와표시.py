"""R5 읽기 전용 조회·표시 생성. 새 로고/화면/명암색을 만들지 않는다."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
BASE=Path(__file__).resolve().parents[1]
INPUTS=('10_공용자산/회사목록.json','10_공용자산/자산목록.json','10_공용자산/CI색상목록.json','03_한맥디자인/한맥디자인정본.json','03_한맥디자인/자료목록.json','03_한맥디자인/문서생성.cjs','03_한맥디자인/회사별_디자인연결_현황.json','03_한맥디자인/디자인적용_기록규격.json','03_한맥디자인/영상적용_예와반례.json','03_한맥디자인/영상전용_미정항목.json','05_출처와검토/R5_적용정책_결정.json','07_실행도구/R5_디자인적용검사.py','07_실행도구/R5_조회와표시.py','07_실행도구/R1_자산검사.py','00_운영계약/회사목록_규격.json','00_운영계약/자산목록_규격.json','00_운영계약/CI색상목록_규격.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(base,rel):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('중복 JSON 키')
            out[k]=v
        return out
    def invalid(s):raise ValueError('비유한 값')
    d=json.loads((base/rel).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid);json.dumps(d,ensure_ascii=False,allow_nan=False).encode('utf-8');return d
def guard(base=BASE):
    base=Path(base).resolve();errors=[]
    try:
        d=read(base,'03_한맥디자인/R5_표시_입력목록.json')
        if d['version']!='0.1.0' or len(d['files'])!=len(INPUTS) or {x['path'] for x in d['files']}!=set(INPUTS):raise ValueError('필수 표시 입력목록 불일치')
        for x in d['files']:
            p=(base/x['path']).resolve()
            if not p.is_relative_to(base) or not p.is_file() or sha(p)!=x['sha256']:errors.append('검토된 정본/생성입력 변경: '+x['path'])
        manifest=read(base,'03_한맥디자인/자료목록.json')
        for x in manifest['files']:
            p=(base/'03_한맥디자인'/x['path']).resolve()
            if not p.is_relative_to((base/'03_한맥디자인').resolve()) or not p.is_file() or sha(p)!=x['sha256']:errors.append('기존 한맥 표시 manifest 불일치: '+x['path'])
        knowledge=read(base,'03_한맥디자인/영상적용_예와반례.json');pins=knowledge['basis_pins']
        localrefs={ref for case in knowledge['cases'] for ref in case['basis'] if not ref.startswith('http')};externalrefs={ref for case in knowledge['cases'] for ref in case['basis'] if ref.startswith('http')}
        if len(pins['local'])!=len(localrefs) or {x['path'] for x in pins['local']}!=localrefs:errors.append('사례 로컬 근거pin 누락/중복')
        if len(pins['external'])!=len(externalrefs) or {x['url'] for x in pins['external']}!=externalrefs:errors.append('사례 외부 조사pin 누락/중복')
        for x in pins['local']:
            p=(base/x['path']).resolve()
            if not p.is_relative_to(base) or not p.is_file() or sha(p)!=x['sha256']:errors.append('사례 근거 판본 변경: '+x['path']);continue
            if p.suffix=='.json':
                value=read(base,x['path']);version=value.get('version',value.get('record_version',value.get('schema_version')))
                if version!=x['version_if_declared']:errors.append('사례 근거 버전 불일치: '+x['path'])
        for x in pins['external']:
            ref=x['research_record_ref'];p=(base/ref['path']).resolve()
            if not p.is_relative_to(base) or not p.is_file() or sha(p)!=ref['sha256']:errors.append('외부 조사기록 판본 변경: '+ref['path']);continue
            source=read(base,ref['path']);entry=next((s for s in source['sources'] if s['id']==x['research_entry_id']),None)
            if source['version']!=ref['version'] or not entry or entry['url']!=x['url'] or entry['depth']!=x['depth']:errors.append('외부 근거 조사판본/URL/깊이 불일치')
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as e:errors.append('필수 표시 입력 오류: '+ascii(str(e)))
    return {'valid':not errors,'errors':errors,'boundary':'로컬 변경 감지. 회사 공식성/최신성/승인 검증 아님.'}
def _query(company_id,include_observed=False,include_hanmac=False,include_styles=False,base=BASE):
    if not isinstance(company_id,str) or not company_id.strip() or any(type(v) is not bool for v in [include_observed,include_hanmac,include_styles]):return {'valid':False,'errors':['회사ID 문자열과 명시 boolean 옵션 필요'],'colors':[]}
    base=Path(base).resolve();check=guard(base)
    if not check['valid']:return {'valid':False,'errors':check['errors'],'colors':[]}
    c=read(base,'10_공용자산/회사목록.json');a=read(base,'10_공용자산/자산목록.json');k=read(base,'10_공용자산/CI색상목록.json');h=read(base,'03_한맥디자인/한맥디자인정본.json')
    spec=importlib.util.spec_from_file_location('r5_query_r1',base/'07_실행도구/R1_자산검사.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    palette=m.palette(company_id,c,k,include_observed=include_observed,assets=a,base=base)
    company=next((x for x in c['companies'] if x['company_id']==company_id),None)
    if not company or palette.get('errors'):return {'valid':False,'errors':palette.get('errors') or ['확인된 회사ID 없음'],'colors':[]}
    final=guard(base)
    if not final['valid']:return {'valid':False,'errors':final['errors'],'colors':[]}
    return {'valid':True,'company_id':company_id,'name_ko':company['name_ko'],'logos':company['ci_asset_refs'],'colors':palette['colors'],'hanmac_common_colors':[x for x in h['color_tokens'] if x['scope']=='global_color_library'] if include_hanmac else [],'optional_style_refs':[x['id'] for x in h['references']+h['gradients']] if include_styles else [],'selected_roles':{},'selected_logo':None,'company_approved':False,'operational_release':False,'boundary':'자료 조회. 색/로고/스타일 역할 자동선택·공식CI/디자인 승인 아님. 관측색/한맥/스타일은 각각 명시 옵션 필요.'}
def query(company_id,include_observed=False,include_hanmac=False,include_styles=False,base=BASE):
    try:return _query(company_id,include_observed,include_hanmac,include_styles,base)
    except (OSError,ValueError,KeyError,TypeError,RecursionError,AttributeError) as e:return {'valid':False,'errors':['조회 입력/참조 읽기 오류: '+ascii(str(e))],'colors':[]}
def contrast(a,b):
    def lum(h):
        v=[int(h[i:i+2],16)/255 for i in [1,3,5]];v=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in v]
        return sum(x*y for x,y in zip(v,[0.2126,0.7152,0.0722]))
    v=sorted([lum(a),lum(b)]);return (v[1]+0.05)/(v[0]+0.05)
def views(base=BASE):
    base=Path(base).resolve();check=guard(base)
    if not check['valid']:raise ValueError('; '.join(check['errors']))
    links=read(base,'03_한맥디자인/회사별_디자인연결_현황.json');colors=read(base,'10_공용자산/CI색상목록.json')
    md='# 8회사 디자인 자료 연결 현황\n\n정본에서 생성한 자료 조회표. 역할·로고는 자동 선택하지 않는다. 공식/최신 CI·개별 시안 승인 아님. 공유 AI 자산은 여러 회사에 참조된다.\n\n| 회사 | CI자산 참조 | 색기록 | 역할/로고 선택 |\n|---|---|---|---|\n'
    for c in links['companies']:
        folder='주식회사장헌' if c['company_id']=='jangheon' else c['name_ko'];target='../10_공용자산/04_조회용자료/'+folder+'/00_CI와심볼_안내.md'
        md+=f"| [{c['name_ko']}]({target}) / {c['company_id']} | {len(c['ci_asset_refs'])} | {len(c['color_refs'])} | 미선택 |\n"
    md+='\n현재 공식 화면색 기본 조회 조건을 만족하는 색은 없다. 관측값은 명시 조회의 후보 자료이며 공식색/권고역할로 승격하지 않는다. 한맥 웹색은 별도 공통 참고다.\n\n[회사별 연결 정본](회사별_디자인연결_현황.json) · [화면 역할 연결 규칙](07_회사CI와_화면역할_연결규칙.md) · [영상 적용 예·반례](08_영상적용_예와반례.md)\n'
    ratios=[]
    for c in colors['colors']:
        if c['source_level']!='raster_sample' or c['screen_value'] is None:continue
        h=c['screen_value']['hex'];ratios.append({'company_id':c['company_id'],'color_id':c['color_id'],'record_version':c['record_version'],'hex':h,'source_level':c['source_level'],'assumption':c['normalization']['notes'],'contrast_with_white':contrast(h,'#FFFFFF'),'contrast_with_black':contrast(h,'#000000'),'interpreted_role':None,'design_approved':False})
    spec={'scope':'불투명 sRGB로 표시한다고 가정한 관측색 대 흰색/검정의 단색 대비. 로고 자체 합격/불합격·글자역할추천·최종영상 품질/WCAG인증 아님.','source':'https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html','pairs':ratios}
    t='# 관측색의 단색 대비 참고\n\nsRGB 표시를 가정한 불투명 관측색과 흰색/검정의 수치다. CI 자체를 합격/불합격으로 판정하거나 글자색 역할을 자동 추천하지 않는다. 영상 배경·알파·글자 굵기/크기·움직임·최종 시청 환경은 별도 검수한다. 표시는 소수 둘째 자리지만 판단 시 원수치를 사용한다.\n\n| 회사 / 색ID | 관측값 | 흰색 대비 | 검정 대비 |\n|---|---|---|---|\n'
    for x in ratios:t+=f"| {x['company_id']} / {x['color_id']} | {x['hex']} | {x['contrast_with_white']:.2f}:1 | {x['contrast_with_black']:.2f}:1 |\n"
    t+='\n[계산값과 가정](관측색_단색대비_참고.json) · [W3C 대비 설명](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)\n'
    final=guard(base)
    if not final['valid']:raise ValueError('; '.join(final['errors']))
    return {'10_회사별_연결현황.md':md,'11_관측색_대비참고.md':t,'관측색_단색대비_참고.json':json.dumps(spec,ensure_ascii=False,indent=2)+'\n'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--company');p.add_argument('--include-observed',action='store_true');p.add_argument('--include-hanmac',action='store_true');p.add_argument('--include-styles',action='store_true');args=p.parse_args()
    if args.company is None and any([args.include_observed,args.include_hanmac,args.include_styles]):r={'valid':False,'errors':['옵션 조회에는 --company 필요'],'colors':[]}
    else:r=query(args.company,args.include_observed,args.include_hanmac,args.include_styles) if args.company is not None else guard()
    print(json.dumps(r,ensure_ascii=True,allow_nan=False,indent=2));return 0 if r['valid'] else 1
if __name__=='__main__':raise SystemExit(main())
