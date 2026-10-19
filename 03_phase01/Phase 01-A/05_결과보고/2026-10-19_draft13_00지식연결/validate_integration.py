from pathlib import Path
import json,hashlib,copy,importlib.util,subprocess,re,sys
R=Path(__file__).resolve().parent;W=R.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S=R/'candidate/company-video-grammar-analyzer';spec=importlib.util.spec_from_file_location('knowledge_links',S/'scripts/knowledge_links.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
catalog=R/'knowledge/catalog.json';cat=m.catalog_read(catalog);P=R/'pilot';records=[P/'case-134.json',P/'case-172.json',P/'motion-windows.json'];checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
check('three_actual_records_pass_link_checker',all(m.check_record(cat,p) for p in records))
check('exact_ID_not_prefix',len(m.query(cat,catalog,concept_id='LAYOUT-SPLIT')['matches'])==1)
q=lambda **kw:m.query(cat,catalog,P/'usage-index.json',**kw)
check('work_ensemble_use_and_evidence_found',any(h['unit']['id']=='RC-COMP-007@v1' and h['evidence'] for h in q(query_text='업무 이미지 묶음')['uses']))
check('building_and_label_are_separate',any(h['unit']['id']=='RC-COMP-008@v1' for h in q(query_text='건물/기단')['uses']) and any(h['unit']['id']=='RC-COMP-005@v1' for h in q(query_text='지원 명찰')['uses']))
check('shared_visual_profile_returns_two_uses',len(q(query_text='크림 공간의 입체 정보 무대')['uses'])==2)
check('motion_results_have_observed_motion_units',all(h['unit']['observation_status']=='observed_sampled' and h['unit']['kind'] in ['flow','detail'] for h in q(concept_id='FUNCTION-REVEAL',motion_only=True)['uses']))
check('static_arrow_not_motion',not q(query_text='요청·지원 방향 라벨',motion_only=True)['uses'])
check('review_relevance_does_not_create_pass',all(h['knowledge_links'][0]['relation']=='review_relevant' for h in q(concept_id='MR-08')['uses']))
check('actual_review_statuses_return',any(any(r['status']=='hold' for r in h['reviews']) for h in q(concept_id='STYLE-3D')['uses']))
motion=read(records[-1]);check('two_asynchronous_event_links_preserved',len(motion['event_links'])==2 and all(x['relation']=='continues_after' for x in motion['event_links']))
check('original_raw_collection_bytes_preserved',sha(P/'preserved/static/original/collection.md')==sha(W/'collection-skill-structure-20261019/records/original/collection.md'))
test=R/'validation-fixtures';test.mkdir(exist_ok=True)
def reject(name,mutate):
    d=copy.deepcopy(read(records[0]))
    for row in d['source_records']+d['evidence']:row['path']=str((P/row['path']).resolve())
    mutate(d);p=test/(name+'.json');m.save(p,d)
    try:m.check_record(cat,p);ok=False
    except (ValueError,KeyError,TypeError) as e:ok=True;reason=str(e)
    check(name,ok,reason if ok else 'unexpected acceptance')
reject('dangling_use_definition_rejected',lambda d:d['uses'][0].update(definition_id='ABSENT'))
reject('unknown_concept_rejected',lambda d:d['knowledge_links'][0].update(concept_id='NOT-A-CONCEPT'))
reject('principle_as_observed_classification_rejected',lambda d:d['knowledge_links'][0].update(concept_id='MP-01'))
reject('observed_claim_without_evidence_rejected',lambda d:d['claims'][0].update(evidence_ids=[]))
reject('evaluated_link_without_review_rejected',lambda d:d['knowledge_links'][0].update(relation='evaluated_against'))
reject('automatic_company_approval_rejected',lambda d:d.update(company_approved=True))
reject('reversed_time_rejected',lambda d:d['uses'][0].update(time={'start':172,'end':134}))
reject('stale_evidence_hash_rejected',lambda d:d['evidence'][0].update(sha256='0'*64))
reject('unobserved_classified_as_observed_rejected',lambda d:next(x for x in d['units'] if x['id']==d['knowledge_links'][0]['unit_id']).update(observation_status='unobserved'))
def pending(d):d['reviews'][0].update(status='hold',next_probe=None)
reject('pending_review_without_probe_rejected',pending)
ci=copy.deepcopy(cat);ci['source_pins'][0]['sha256']='0'*64;bad=test/'stale-catalog.json';m.save(bad,ci)
try:m.catalog_read(bad);ok=False
except ValueError:ok=True
check('stale_catalog_rejected',ok)
idx=read(P/'usage-index.json')
idx['catalog_pin']['path']=str(catalog.resolve())
for row in idx['records']:row['path']=str((P/row['path']).resolve())
idx['records'][0]['sha256']='0'*64;m.save(test/'stale-index.json',idx)
try:m.query(cat,catalog,test/'stale-index.json',query_text='업무');ok=False
except ValueError as e:ok='stale pinned file' in str(e);reason=str(e)
check('stale_usage_index_rejected',ok,reason if ok else 'unexpected acceptance/rejection reason')

# 기본판/기존 후보는 수정하지 않고 신규 후보와 호환성만 검사한다.
for label,folder,pinsfile in [('backup12',R/'backup/draft12/company-video-grammar-analyzer',R/'eval-old-skill-pin.json')]:
    check(label+'_preserved',all(sha(Path(x['path']))==x['sha256'] for x in read(pinsfile)))
py='D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/.환경/Scripts/python.exe'
rv=subprocess.run([py,'-B','-X','utf8','C:/Users/User/.codex/skills/anthropic-skill-creator/scripts/quick_validate.py',str(S)],capture_output=True,text=True,encoding='utf-8')
check('standard_creator_validate',rv.returncode==0,rv.stdout+rv.stderr)
broken=[];count=0
for f in [S/'SKILL.md',*list((S/'references').glob('*.md'))]:
    for target in re.findall(r'\]\(([^\n]+?)\)',f.read_text(encoding='utf-8-sig')):
        target=target.strip('<>').split('#')[0]
        if not target or '://' in target:continue
        count+=1
        if not (f.parent/target).exists():broken.append(str(f)+': '+target)
check('candidate_reference_links_exist',not broken,{'count':count,'broken':broken})
sys.path.insert(0,str(S/'scripts'));import check_record
fixture=read(W/'collection-skill-update-20261019/validation/draft10-compatibility-fixture.json')
check('old_observation_requires_historical_mode',bool(check_record.check(fixture)) and not check_record.check(fixture,allow_historical=True))
fixture['skill_version']='0.1.0-draft.13';check('draft13_observation04_compatibility',not check_record.check(fixture))
fixture['source']['sha256']='bad';check('old_path_still_rejects_bad_source_hash',bool(check_record.check(fixture)))
out={'scope':'구조·참조·조회 경계; 내용 정확도/효과/스킬 일반 성능 아님','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks}
m.save(R/'validation-summary.json',out)
print(json.dumps({'passed':out['passed'],'total':out['total'],'failures':[x for x in checks if not x['passed']]},ensure_ascii=False))
raise SystemExit(0 if out['passed']==out['total'] else 1)
