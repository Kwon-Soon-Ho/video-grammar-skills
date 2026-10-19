from pathlib import Path
import json,hashlib,importlib.util,re,tempfile,shutil
R=Path(__file__).resolve().parent;I=R/'문법색인';W=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('grammar_lookup',I/'조회.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
checks=[]
def check(name,condition,detail=None):
    checks.append({'name':name,'passed':bool(condition),'detail':detail})
def ids(r):return {x['id'] for x in r['results']}

catalog=read(I/'data/catalog.json');uses=read(I/'data/uses.json')
check('unique_catalog_and_usage_ids',len({x['id'] for x in catalog})==len(catalog) and len({x['id'] for x in uses})==len(uses))
known={x['id'] for x in catalog}
check('all_classification_and_review_refs_resolve',all(set(u['grammar_tags']+u['review_knowledge_refs'])<=known for u in uses))
check('exact_split_does_not_match_split_compare', {x['id'] for x in q.lookup(concept='LAYOUT-SPLIT')['matched_catalog']}=={'LAYOUT-SPLIT'})
check('split_retrieves_134_case','USE-001' in ids(q.lookup(concept='LAYOUT-SPLIT')))
check('work_ensemble_retrievable','USE-003' in ids(q.lookup(query='업무 이미지 묶음')))
check('building_ensemble_retrievable','USE-004' in ids(q.lookup(query='건물 기단')))
check('number_motion_retrievable', 'USE-008' in ids(q.lookup(query='숫자 도상 시차',motion_only=True)))
check('still_arrow_not_returned_as_motion',not q.lookup(query='134초 화살표 모션',motion_only=True)['results'])
check('unobserved_stays_separate',ids(q.lookup(query='134초 화살표 모션',include_unobserved=True))=={'USE-012'})
check('new_design_not_source_pattern',not q.lookup(query='가족사별→업무별')['results'])
check('proposal_explicitly_retrievable',ids(q.lookup(query='가족사별→업무별',include_proposals=True))=={'USE-013'})
check('principle_match_labeled_review_not_effect',all(x['match_explanation']['review_relevance'] and not x['company_rule'] for x in q.lookup(concept='MR-08')['results']))
check('unused_layout_reports_no_usage',not q.lookup(concept='LAYOUT-TIMELINE')['results'])
check('deprecated_id_retained_without_silent_merge',q.lookup(concept='STYLE-PIP')['matched_catalog'][0]['status']=='deprecated')
try:q.lookup(concept='NO-SUCH-ID');unknown=False
except ValueError:unknown=True
check('unknown_exact_id_rejected',unknown)
check('65_items_and_40_cards_covered',len(read(R/'data/65-item-review.json'))==65 and len(read(R/'data/40-source-card-crosswalk.json'))==40)
check('all_544_integrity_rows_resolve',len(read(R/'data/source-file-integrity.json'))==544 and all(x['resolved_match'] for x in read(R/'data/source-file-integrity.json')))
check('protected_files_unchanged',all(Path(p['path']).exists() and sha(Path(p['path']))==p['sha256'] for p in read(R/'data/protected-source-pins.json')))
check('record_originals_preserved',sha(I/'records/original/collection.md')==sha(W/'collection-skill-structure-20261019/records/original/collection.md'))

missing=[]
for u in uses:
    for e in u['evidence']:
        p=(I/e.split('#')[0])
        if not p.exists():missing.append(e)
check('all_usage_evidence_links_exist',not missing,missing)

# 작업 폴더의 별도 오류 주입 사본만 변경하고 정본/실제 pin은 건드리지 않는다.
temp=R/'data/stale-source-fixture';shutil.copytree(I/'data',temp/'data',dirs_exist_ok=True)
pins=read(temp/'data/catalog-source-pins.json');pins[0]['sha256']='0'*64
(temp/'data/catalog-source-pins.json').write_text(json.dumps(pins),encoding='utf-8')
old=q.BASE;q.BASE=temp
try:q.lookup(concept='LAYOUT-SPLIT');stale=False
except ValueError:stale=True
finally:q.BASE=old
check('stale_catalog_source_blocks_query',stale)

# 새 안내/목차/사용처의 링크만 검증. 복사된 역사 원문은 내용·절대경로를 보존한다.
broken=[];n=0
files=list(R.glob('*.md'))+list(I.glob('*.md'))
for f in files:
    for raw in re.findall(r'\]\(([^\n]+?)\)',f.read_text(encoding='utf-8')):
        raw=raw.strip().strip('<>')
        if re.match(r'^(https?://|thread://|#)',raw):continue
        raw=raw.split('#')[0];raw=re.sub(r':\d+$','',raw)
        p=Path(raw) if Path(raw).is_absolute() else f.parent/raw;n+=1
        if not p.exists():broken.append({'file':str(f),'target':raw})
check('new_markdown_local_links_exist',not broken,{'checked':n,'broken':broken})
result={'scope':'구조/참조/조회 경계 테스트. 의미 정확도/시청자 효과/스킬 우월성 시험 아님','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)}
(R/'data/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['passed']==result['total'] else 1)
