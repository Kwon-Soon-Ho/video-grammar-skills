from pathlib import Path
import json, hashlib, importlib.util

ROOT=Path(__file__).resolve().parents[2]/'R8_시험/video-record-steward-workspace'
DEST=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):
        out=[]
        for k in sorted(a.keys()|b.keys()):
            if k not in a or k not in b:out.append({'path':p+'/'+k,'before':a.get(k),'after':b.get(k)})
            else:out.extend(diff(a[k],b[k],p+'/'+k))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':p,'before':a,'after':b}]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

case=ROOT/'iteration-1/eval-01-통합기록과_디자인연결_수정'
for variant in ['new_skill','old_skill']:
    run=case/variant/'run-1';base=run/'inputs/Phase00';before=read(run/'fixture_before.json')['files']
    snapshot={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    report={'variant':variant,'independent_observation':True,'changed_files':[k for k,v in before.items() if snapshot.get(k)!=v],
            'missing_files':[k for k in before if k not in snapshot],'added_files':[k for k in snapshot if k not in before],'inventory_count':len(before)}
    bp=run/('outputs/backup' if variant=='new_skill' else 'backup/requested-draft-fix')
    paths=['12_통합기록/통합기록_작업초안.json','작업초안/디자인적용_초안.json']
    records=[]
    for rel in paths:
        p=base/rel;b=bp/rel;original=read(b);final=read(p)
        records.append(final)
        report[rel]={'fixture_sha256':before[rel],'backup_sha256':sha(b),'backup_matches_fixture':sha(b)==before[rel],
                     'final_sha256':sha(p),'before_version':original.get('version'),'after_version':final.get('version'),
                     'json_diff':diff(original,final),'actual_final_data':final}
    r4,r5=records;link=r5['linked_r4_record'];report['link_check']={'path':link['path'],'id_matches':link['record_id']==r4['record_id'],
        'version_matches':link['version']==r4['version'],'sha_matches':link['sha256']==sha(base/paths[0]),'path_points_to_final':(base/link['path']).resolve()==(base/paths[0]).resolve()}
    tools=base/'07_실행도구'
    r4checker=module(tools/'자료검증.py','independent_r4_'+variant)
    r5checker=module(tools/'R5_디자인적용검사.py','independent_r5_'+variant)
    report['independent_r4_check']=r4checker.inspect_file(base/paths[0])
    report['independent_r5_check']=r5checker.inspect(r5,base=base)
    report['inspection_did_not_change_inputs']=snapshot=={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    dest=DEST/('steward_case1_'+variant+'_observation.json');dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in paths and not k.startswith('independent_r')},ensure_ascii=False))
    for rel in paths:print(rel,json.dumps({k:v for k,v in report[rel].items() if k!='actual_final_data'},ensure_ascii=False))
    print('checks',report['independent_r4_check']['valid'],report['independent_r5_check']['valid'])
