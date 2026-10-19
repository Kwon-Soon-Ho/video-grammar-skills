"""Read-only exact concept / explicit-string lookup. No DB writes or approval."""
from pathlib import Path
import argparse,json,hashlib
BASE=Path(__file__).resolve().parent
def read(name):return json.loads((BASE/name).read_text(encoding='utf-8-sig'))
def lookup(concept=None,query=None,motion_only=False,include_unobserved=False,include_proposals=False):
    catalog=read('data/catalog.json');uses=read('data/uses.json')
    stale=[]
    for pin in read('data/catalog-source-pins.json'):
        p=Path(pin['path'])
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin['sha256']:stale.append(pin['path'])
    if stale:raise ValueError('catalog_source_changed_or_missing: '+repr(stale))
    if concept:
        matches=[x for x in catalog if x['id']==concept]
        if not matches:raise ValueError('unknown_exact_concept: '+concept)
    else:
        q=query.casefold()
        matches=[x for x in catalog if any(q in str(x.get(k,'')).casefold() for k in ['id','name_ko','name_en','title','aliases'])]
    ids={x['id'] for x in matches}
    # 원칙 연결은 검토 관련성으로 반환하며 실제 적용/승인을 추론하지 않는다.
    results=[]
    for u in uses:
        classification=sorted(ids.intersection(u['grammar_tags']))
        review=sorted(ids.intersection(u['review_knowledge_refs']))
        text_hit=not concept and any(query.casefold() in str(u.get(k,'')).casefold() for k in ['title','aliases','content'])
        if not(classification or review or text_hit):continue
        if motion_only and u['kind']!='prior_sampled_motion':continue
        if u['kind']=='unobserved_motion' and not include_unobserved:continue
        if u['kind']=='excluded_proposal' and not include_proposals:continue
        results.append({**u,'match_explanation':{'classification_inference':classification,'review_relevance':review,'explicit_text':text_hit}})
    return dict(request={'concept':concept,'query':query,'motion_only':motion_only},
      method='exact ID or explicit text; not semantic search',
      warning='분류는 기록에 대한 해석, 원칙은 검토 관련성. 원제작 의도/적용 효과/회사 승인을 추론하지 않음.',
      matched_catalog=[{k:x[k] for k in ['id','kind','axis','name_ko','title','status','replaced_by','source_path'] if k in x} for x in matches],
      results=results,scope='색인13행 한정; 결과 없음은 전체 영상의 부재 증거가 아님')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--concept');g.add_argument('--query')
    p.add_argument('--motion-only',action='store_true');p.add_argument('--include-unobserved',action='store_true');p.add_argument('--include-proposals',action='store_true')
    a=p.parse_args()
    try:print(json.dumps(lookup(a.concept,a.query,a.motion_only,a.include_unobserved,a.include_proposals),ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
