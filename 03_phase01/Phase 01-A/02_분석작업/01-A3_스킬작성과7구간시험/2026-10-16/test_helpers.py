from pathlib import Path
import importlib.util,json,copy,contextlib,sys
B=Path(__file__).resolve().parent;S=B/'company-video-grammar-analyzer/scripts'
version='v1'
if len(sys.argv)>1:
    S=B/'company-video-grammar-analyzer-workspace/skill-candidate-v2/scripts';version='v2'
def load(name):
    s=importlib.util.spec_from_file_location(name,S/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
cat=load('evidence_catalog');obs=load('check_observations')
log=B/'runs/setup/cases/자료013/T07/실행기록.json';data=json.loads(log.read_text(encoding='utf-8'));res=[]
def result(name,passed,detail):res.append(dict(name=name,passed=passed,detail=detail))
result('real_extraction_catalog',len(cat.catalog([log])['frames'])==23,'T07 actual files and normalized PTS')
temp_dir=B/'helper-test-fixtures';temp_dir.mkdir(exist_ok=True)
with contextlib.nullcontext(temp_dir) as tmp:
    p=Path(tmp)/'bad.json'
    for name,mutation in [('bad_hash',lambda d:d['frames'][0].update(sha256='0'*64)),('bad_pts',lambda d:d['frames'][0].update(reported_pts='1')),('duplicate_actual_time',lambda d:d['frames'].insert(1,copy.deepcopy(d['frames'][0]))),('changed_source',lambda d:d.update(input_sha256_after='0'*64))]:
        d=copy.deepcopy(data);mutation(d);p.write_text(json.dumps(d),encoding='utf-8')
        try:cat.catalog([p]);passed=False
        except ValueError:passed=True
        result(name,passed,'reject malformed/provenance conflict')
    fs=data['frames'];sample={'schema_version':'a3-observation-0.1','case_id':'synthetic-contract-test','source':{'path':'synthetic','sha256':data['input_sha256']},'window_seconds':[8.2,10.4],'method':'synthetic linkage only','document_mode':'none','audio_reviewed':False,'evidence':[{'id':str(i),'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'within'} for i,f in enumerate(fs[:3])],'objects':[{'id':'o','name':'synthetic','parent':None,'events':[{'description':'synthetic','properties':['position'],'time_seconds':[8.2,8.5],'evidence_ids':['0','1','2'],'direction_order':'synthetic','easing':{'property':'position','classification':'decelerate','basis':'synthetic test only'},'status':'observed','limitations':[]}]}],'coverage':{'overview':'synthetic','secondary_details':'synthetic','internal_content':'synthetic','unresolved':[]},'hypotheses':[],'limitations':['not a visual claim'],'files_read':[]}
    result('valid_linkage',not obs.check(sample),'synthetic observation structure, not actual content')
    for name,mutation in [('dangling',lambda d:d['objects'][0]['events'][0].update(evidence_ids=['missing'])),('curve_two_times',lambda d:d['objects'][0]['events'][0].update(evidence_ids=['0','1'])),('end_boundary',lambda d:d['evidence'][0].update(actual_seconds='10.4')),('event_outside',lambda d:d['objects'][0]['events'][0].update(time_seconds=[0,1])),('wrong_event_evidence_time',lambda d:d['objects'][0]['events'][0].update(time_seconds=[9,10])),('parent_cycle',lambda d:d['objects'][0].update(parent='o'))]:
        d=copy.deepcopy(sample);mutation(d);result(name,bool(obs.check(d)),'expected reject inconsistent linkage')
out=B/('helper-tests-'+version+'.json');out.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(res,ensure_ascii=False))
