"""Regression and adversarial coverage checks. Not a visual accuracy score."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import json,sys,subprocess,re
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,digest
from source_coverage import summarize,union_length
from review_ledger import validate
OUT=HERE/'validation';OUT.mkdir(exist_ok=True)
results=[]
def test(name,ok,detail=''):
    results.append({'name':name,'passed':bool(ok),'detail':detail});assert ok,(name,detail)
d=load(HERE/'source-coverage.json');cat=load(HERE/'evidence-catalog.json');summary=summarize(d,cat)
test('real_two_sources_29_provisional_groups',summary['planning_groups']==29)
test('recorded_union_is_16_seconds_not_source_duration',summary['recorded_union_seconds']=='16' and summary['outside_recorded_windows_seconds']=='76784/125')
test('overview_does_not_certify_fine_review',summary['fine_review_completion']=='not_assessed' and not summary['discovery_completeness_verified'])
test('overlap_is_counted_once',union_length([(Fraction(0),Fraction(10)),(Fraction(5),Fraction(12)),(Fraction(12),Fraction(13))])==13)
def reject(name,mutation,text):
    v=deepcopy(d);mutation(v);error=''
    try:summarize(v,cat)
    except (ValueError,KeyError,TypeError,OSError) as e:error=str(e)
    test(name,text in error,error)
reject('gap_in_work_partition',lambda x:x['groups'][0]['planning_seconds'].__setitem__(1,24),'partition')
reject('overlap_in_work_partition',lambda x:x['groups'][1]['planning_seconds'].__setitem__(0,24),'partition')
reject('unplanned_source_tail',lambda x:x['sources'][-1].update(duration_seconds=212),'tail')
reject('pretending_exact_cut_boundary',lambda x:x['groups'][0].update(boundary_kind='exact_cut'),'boundary')
reject('missing_overview_evidence',lambda x:x['groups'][0].update(overview_evidence=[]),'missing overview')
reject('wrong_overview_time',lambda x:x['groups'][0]['overview_evidence'][0].update(actual_seconds=1),'time/bytes')
reject('wrong_overview_source',lambda x:x['groups'][0]['overview_evidence'][0].update(path=d['groups'][-1]['overview_evidence'][0]['path'],actual_seconds=d['groups'][-1]['overview_evidence'][0]['actual_seconds']),'time/bytes')
reject('changed_record_pin',lambda x:x['records'][0].update(sha256='0'*64),'bytes changed')
reject('cross_source_observation',lambda x:x['records'][0].update(source_id='NEW-P'),'cross-source record')
reject('wrong_record_group_assignment',lambda x:x['records'][0].update(group_ids=[d['groups'][0]['id']]),'group links')
reject('duplicate_work_group_id',lambda x:x['groups'].append(deepcopy(x['groups'][0])),'duplicate id')
v=deepcopy(d);v['records'].append(dict(v['records'][0],id='duplicate-window-for-union-test'))
test('repeated_window_does_not_inflate_recorded_seconds',summarize(v,cat)['recorded_union_seconds']=='16')
for code in ['NEW-N','NEW-P']:
    obs=load(HERE/'records'/code/'observations.json');ledger=load(HERE/'records'/code/'review-ledger.json')
    bounded=True
    if code=='NEW-P':
        rows=[r for r in obs['observation_rows'] if r['object_id']=='regional-link' and r['property']=='position']
        bounded=len(rows)==3 and sum(r['review_state']=='not_reviewed' for r in rows)==2 and next(r for r in rows if r['review_state']=='reviewed')['time_seconds']==[43.8,45.3]
    test(code+'_current_record_and_pins',bounded and not check(obs,cat) and validate(ledger,cat)['structure_passed'])
    test(code+'_old_version_requires_explicit_historical_read',bool(check(load(ledger['before']['path']))))
test('map_old_zoom_claim_rejected',next(c for c in load(HERE/'records/NEW-P/observations.json')['claims'] if c['id']=='c002')['content_review']=='rejected')
test('prior_draft7_backup_unchanged',all(digest(WORK/'analysis-reliability-20261019/candidate/company-video-grammar-analyzer'/f['relative'])==f['sha256'] for f in load(HERE/'backup/manifest.json')['files']))
for name in ['core','composition']:
    source=(WORK/'analysis-reliability-20261019'/('regression-'+name+'.py')).read_text('utf-8').replace('0.1.0-draft.7','0.1.0-draft.8')
    suffix=1
    while (HERE/f'validation-{name}-run{suffix}').exists():suffix+=1
    source=source.replace("OUT=HERE/'validation-"+name+"'", "OUT=HERE/'validation-"+name+'-run'+str(suffix)+"'")
    path=HERE/('regression-'+name+'.py');path.write_text(source,encoding='utf-8');subprocess.run([sys.executable,str(path)],check=True)
links=[]
for p in (HERE/'candidate/company-video-grammar-analyzer').rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text('utf-8')):
        if '://' not in target:links.append({'source':str(p),'target':target,'exists':(p.parent/target.split('#')[0]).exists()})
test('all_relative_reference_links_exist',all(x['exists'] for x in links))
(OUT/'results.json').write_text(json.dumps({'tests':results,'count':len(results),'all_passed':all(x['passed'] for x in results),'relative_links':links,'additional_suites':['38 prior core','34 prior composition'],'adaptation':'Prior fixture version changed to draft.8 only in separate copies. Original fixtures and pinned records preserved. No visual accuracy score.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_checks':len(results),'passed':True},ensure_ascii=False))
