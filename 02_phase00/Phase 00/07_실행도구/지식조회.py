"""Phase 00 지식 조회. 관측·창작·자동 승인 수행하지 않음."""
from 자료검증 import catalogs, BASE
import argparse,json
def lookup(query,axis=None,include_pending=False):
    t,s,p,q,l,d=catalogs();query=query.casefold().strip();out=[]
    if not query:return out
    for r in t['terms']:
        if r['status']=='deprecated' or (axis and r['axis']!=axis):continue
        keys=[r['id'],r['name_ko'],r['name_en'],*r['aliases']]
        if any(query in x.casefold() for x in keys):
            directions={'페이드인':'enter','fade in':'enter','페이드아웃':'exit','fade out':'exit','확대':'increase','축소':'decrease'}
            out.append({'kind':'term','matched_query':query,'qualifiers':{'direction':directions.get(query,'unknown')},'data':r})
    if axis:return out
    for r in p['principles']+q['principles']+l['layouts']:
        if r['status']=='deprecated' or (not include_pending and r['status']=='needs_primary_definition_review'):continue
        if query in (r['id']+' '+r['name_ko']+' '+r['definition']).casefold():out.append({'kind':'reference_knowledge','data':r})
    return out
def palette(include_optional=False):
    d=catalogs()[-1]
    return {'profile_ref':d['profile_id']+'@'+d['version'],'colors':[x for x in d['color_tokens'] if include_optional or x['scope']=='global_color_library'],'optional_styles':d['references']+d['gradients'] if include_optional else [],'authority':'출처 선택 확인·사용 가능 컬러. 회사 문법 승인과 별개.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('query',nargs='?');p.add_argument('--axis');p.add_argument('--palette',action='store_true');p.add_argument('--include-optional',action='store_true');p.add_argument('--include-pending',action='store_true');a=p.parse_args()
    result=palette(a.include_optional) if a.palette else lookup(a.query or '',a.axis,a.include_pending)
    print(json.dumps(result,ensure_ascii=False,indent=2))
