"""Explicit local knowledge/usage links. Validates references, not visual truth or R4 compliance."""
from pathlib import Path
import argparse,json,hashlib,math

def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(p):
    def unique(pairs):
        out={}
        for k,v in pairs:
            need(k not in out,'duplicate JSON key: '+k);out[k]=v
        return out
    def bad(s):raise ValueError('non-finite number: '+s)
    return json.loads(Path(p).read_text(encoding='utf-8-sig'),object_pairs_hook=unique,parse_constant=bad)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def local(base,p):return Path(p) if Path(p).is_absolute() else base/p
def verify_pin(row,base):
    p=local(base,row['path']);need(p.is_file(),'missing pinned file: '+str(p))
    need(sha(p)==row['sha256'],'stale pinned file: '+str(p));return p
def text(x):return isinstance(x,str) and bool(x.strip())
def rows(d,key):
    value=d.get(key);need(isinstance(value,list),'list required: '+key);out={}
    for row in value:
        need(isinstance(row,dict) and text(row.get('id')),'id required: '+key)
        need(row['id'] not in out,'duplicate '+key+' id: '+row['id']);out[row['id']]=row
    return out
def refs(value,known,name,nonempty=False):
    need(isinstance(value,list) and all(isinstance(x,str) for x in value),'ID list required: '+name)
    need(len(value)==len(set(value)),'duplicate refs: '+name)
    need(all(x in known for x in value),'dangling refs: '+name)
    need(not nonempty or bool(value),'empty refs: '+name)
def timecheck(t,duration):
    need(isinstance(t,dict),'time object required')
    a,b=t.get('start'),t.get('end')
    need(all(type(x) in (int,float) and math.isfinite(x) for x in [a,b]),'finite time required')
    need(0<=a<=b<=duration,'time outside source or reversed')

SOURCES=[('01_공통용어/공통용어사전.json','terms','term'),
 ('02_원칙과레이아웃/모션과정보전달원칙.json','principles','motion_principle'),
 ('02_원칙과레이아웃/화면설계원칙.json','principles','screen_principle'),
 ('02_원칙과레이아웃/레이아웃지식.json','layouts','layout_knowledge'),
 ('13_품질검수/품질항목_정본.json','cards','quality_question')]
CONTEXTS=[('current','14_스킬재구성/R8_현재사용안내.md'),
 ('motion_deep','02_원칙과레이아웃/모션원칙_심화카드.json'),
 ('motion_extensions','02_원칙과레이아웃/추가모션체계_연결후보.json'),
 ('layout_deep','02_원칙과레이아웃/레이아웃_심화지식.json'),
 ('layout_extensions','02_원칙과레이아웃/레이아웃_확장후보.json'),
 ('editorial','05_출처와검토/스킬심층검토/07_편집디자인과화면설계_추가검토.md'),
 ('source_reviews','05_출처와검토/스킬심층검토/스킬심층검토정본.json'),
 ('brand_roles','03_한맥디자인/07_회사CI와_화면역할_연결규칙.md'),
 ('assets','10_공용자산/자산목록.json'),
 ('r4_schema','04_기록규격/통합최소기록_스키마_v0.2.json'),
 ('review_policy','13_품질검수/03_판정운영기준.md')]
def make_catalog(base):
    base=Path(base).resolve();concepts=[];pins=[];contexts=[]
    for rel,key,kind in SOURCES:
        p=base/rel;d=load(p);pin={'path':str(p),'sha256':sha(p),'version':d.get('version',d.get('schema_version'))};pins.append(pin)
        for row in d[key]:concepts.append({**row,'kind':kind,'source_path':str(p),'source_sha256':pin['sha256']})
    for key,rel in CONTEXTS:
        p=base/rel;need(p.is_file(),'missing context: '+str(p));pin={'path':str(p),'sha256':sha(p)};pins.append(pin);contexts.append({'id':key,**pin})
    need(len({x['id'] for x in concepts})==len(concepts),'duplicate concept IDs')
    return {'schema_version':'video-knowledge-catalog-0.1','phase00':str(base),'concepts':concepts,'source_pins':pins,'contexts':contexts,'scope':'pinned local catalog; not source-content/rights/company approval'}
def catalog_read(p):
    p=Path(p).resolve();d=load(p);need(d.get('schema_version')=='video-knowledge-catalog-0.1','wrong catalog format')
    for pin in d['source_pins']:verify_pin(pin,p.parent)
    rows(d,'concepts');return d

def check_record(catalog,record_path):
    p=Path(record_path).resolve();d=load(p);base=p.parent
    need(d.get('schema_version')=='video-knowledge-links-0.1','wrong sidecar format')
    need(text(d.get('record_id')) and text(d.get('version')),'record id/version required')
    need(d.get('company_approved') is False and d.get('canonical_registered') is False,'sidecar must remain analysis draft')
    need(isinstance(d.get('limitations'),list) and bool(d['limitations']),'limitations required')
    source=d['source'];need(isinstance(source.get('sha256'),str) and len(source['sha256'])==64 and all(x in '0123456789abcdef' for x in source['sha256']),'source hash required')
    duration=source['duration_seconds'];need(type(duration) in (int,float) and math.isfinite(duration) and duration>0,'source duration required')
    groups={k:rows(d,k) for k in ['source_records','evidence','claims','units','facets','knowledge_links','uses','events','reviews','unknowns']}
    src,ev,cl,un,fa,kn,us,en,rv,uk=[groups[k] for k in ['source_records','evidence','claims','units','facets','knowledge_links','uses','events','reviews','unknowns']]
    need(src and ev and un,'source records/evidence/units required')
    for r in list(src.values())+list(ev.values()):verify_pin(r,base)
    for r in ev.values():timecheck(r['time'],duration)
    for r in cl.values():
        need(text(r.get('text')) and r.get('basis_kind') in ['observed','calculated','inferred'],'invalid claim')
        refs(r['source_record_ids'],src,'claim/source',True);refs(r['evidence_ids'],ev,'claim/evidence',r['basis_kind']!='inferred')
    for r in un.values():
        need(r.get('kind') in ['case','layout','component','visual_profile','flow','detail'],'invalid unit kind')
        need(r.get('observation_status') in ['observed_static','observed_sampled','unobserved'],'invalid unit observation status')
        need(all(text(r.get(k)) for k in ['title','definition_version','summary']),'unit definition missing')
    for r in fa.values():
        need(r['unit_id'] in un and r.get('domain') in ['information','screen','visual','motion'],'invalid facet target/domain')
        need(all(text(r.get(k)) for k in ['name','description']),'facet text missing')
        need(r.get('basis_kind') in ['observed','calculated','inferred'],'invalid facet basis');refs(r['claim_ids'],cl,'facet/claims',True)
    concepts={x['id']:x for x in catalog['concepts']}
    for r in kn.values():
        need(r['unit_id'] in un and r['concept_id'] in concepts,'unknown knowledge target')
        need(r.get('relation') in ['classified_as','review_relevant','evaluated_against'],'invalid knowledge relation')
        need(r.get('basis_kind')=='inferred' and text(r.get('rationale')),'classification/review relation needs inference rationale')
        refs(r['claim_ids'],cl,'knowledge/claims',True)
        if r['relation']=='classified_as':
            need(concepts[r['concept_id']]['kind']=='term','classification must point to taxonomy term')
            need(concepts[r['concept_id']].get('status')!='deprecated','deprecated term cannot classify new use')
            need(un[r['unit_id']]['observation_status']!='unobserved','unobserved unit cannot become observed classification')
        if r['relation']=='evaluated_against':need(any(x['unit_id']==r['unit_id'] and x['criterion_id']==r['concept_id'] for x in rv.values()),'evaluated link without review')
    for r in us.values():
        need(r['definition_id'] in un and r['case_unit_id'] in un and un[r['case_unit_id']]['kind']=='case','use target invalid')
        timecheck(r['time'],duration);refs(r['evidence_ids'],ev,'use/evidence',True);refs(r['claim_ids'],cl,'use/claims',True)
        for k in ['differences','unverified','conditions']:need(isinstance(r.get(k),list),'use list missing: '+k)
        for c in r['conditions']:need(text(c.get('text')) and c.get('validation') in ['untested','observed_case_only','tested_elsewhere'],'invalid condition')
    for r in en.values():
        need(r['unit_id'] in un and r.get('status') in ['observed_sampled','unobserved'],'event target/status invalid');timecheck(r['time'],duration)
        refs(r['claim_ids'],cl,'event/claims',r['status']!='unobserved')
        if r['status']=='observed_sampled':need(un[r['unit_id']]['observation_status']=='observed_sampled','event lacks observed motion unit')
        for k in ['start_bounds','end_bounds']:
            if r.get(k) is not None:
                a,b=r[k];timecheck({'start':a,'end':b},duration)
    for r in rv.values():
        need(r['unit_id'] in un and r['criterion_id'] in concepts,'review target invalid')
        need(r.get('status') in ['pass','fix','hold','not_applicable','not_reviewed'],'invalid review status')
        need(all(text(r.get(k)) for k in ['reason','reviewer','scope']),'review lacks reason/actor/scope')
        refs(r['evidence_ids'],ev,'review/evidence',r['status'] in ['pass','fix']);refs(r['claim_ids'],cl,'review/claims',r['status'] in ['pass','fix'])
        if r['status'] in ['hold','not_reviewed']:need(text(r.get('next_probe')),'pending review needs next probe')
    for r in uk.values():need(r['unit_id'] in un and all(text(r.get(k)) for k in ['question','impact','next_probe']),'unknown lacks target/question/impact/probe')
    for field,known,relations in [('composition_links',set(un)|set(us),['contains','anchors_to','precedes','overlaps','accompanies']),('event_links',set(en),['precedes','overlaps','continues_after','accompanies'])]:
        need(isinstance(d.get(field),list),'missing links: '+field)
        for r in d[field]:
            need(r['from'] in known and r['to'] in known and r['from']!=r['to'],'invalid '+field+' endpoints')
            need(r.get('relation') in relations and r.get('basis_kind') in ['observed','inferred'],'invalid relation/basis')
            refs(r['claim_ids'],cl,field+'/claims',True)
            if field=='event_links':need(en[r['from']]['status']!='unobserved' and en[r['to']]['status']!='unobserved','unobserved event cannot claim temporal relation')
    return d

def make_index(catalog,catalog_path,record_paths):
    records=[];ids=set()
    for p in record_paths:
        p=Path(p).resolve();d=check_record(catalog,p);need(d['record_id'] not in ids,'duplicate record id');ids.add(d['record_id'])
        records.append({'path':str(p),'sha256':sha(p),'record':d})
    return {'schema_version':'video-knowledge-use-index-0.1','catalog_pin':{'path':str(Path(catalog_path).resolve()),'sha256':sha(catalog_path)},'records':records,'scope':'linked draft records; not canonical registration or semantic search'}
def query(catalog,catalog_path,index_path=None,concept_id=None,query_text=None,motion_only=False,include_unobserved=False):
    concepts=catalog['concepts']
    if concept_id:
        matches=[x for x in concepts if x['id']==concept_id];need(matches,'unknown exact concept ID')
    else:
        q=query_text.casefold();matches=[x for x in concepts if any(q in str(x.get(k,'')).casefold() for k in ['id','name_ko','name_en','title','aliases'])]
    matched={x['id'] for x in matches};hits=[]
    if index_path:
        ip=Path(index_path).resolve();index=load(ip);need(index.get('schema_version')=='video-knowledge-use-index-0.1','wrong index format')
        cp=verify_pin(index['catalog_pin'],ip.parent);need(cp.resolve()==Path(catalog_path).resolve(),'index/catalog mismatch')
        for row in index['records']:
            p=verify_pin(row,ip.parent);d=check_record(catalog,p)
            need(d==row['record'],'index snapshot differs from pinned record')
            units={x['id']:x for x in d['units']}
            for use in d['uses']:
                u=units[use['definition_id']];links=[x for x in d['knowledge_links'] if x['unit_id']==u['id'] and x['concept_id'] in matched]
                searchable=[u['id'],u['title'],u['summary']]+[x['description'] for x in d['facets'] if x['unit_id']==u['id']]
                direct=bool(query_text and any(query_text.casefold() in str(s).casefold() for s in searchable))
                if not links and not direct:continue
                if u['observation_status']=='unobserved' and not include_unobserved:continue
                if motion_only and (u['kind'] not in ['flow','detail'] or u['observation_status']!='observed_sampled'):continue
                reviews=[x for x in d['reviews'] if x['unit_id']==u['id'] or x['unit_id']==use['case_unit_id']]
                hits.append({'record_id':d['record_id'],'record_path':str(p),'unit':u,'use':use,'knowledge_links':links,'reviews':reviews,'evidence':[x for x in d['evidence'] if x['id'] in use['evidence_ids']],'limitations':d['limitations']})
    return {'matches':matches,'uses':hits,'method':'exact ID or explicit substring; classification inference/review relevance are not effect approval','company_approved':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    c=s.add_parser('catalog');c.add_argument('--phase00',required=True);c.add_argument('--out',required=True)
    q=s.add_parser('query');q.add_argument('--catalog',required=True);q.add_argument('--index');g=q.add_mutually_exclusive_group(required=True);g.add_argument('--id');g.add_argument('--query');q.add_argument('--motion-only',action='store_true');q.add_argument('--include-unobserved',action='store_true')
    c=s.add_parser('check');c.add_argument('--catalog',required=True);c.add_argument('--record',required=True)
    c=s.add_parser('index');c.add_argument('--catalog',required=True);c.add_argument('--records',nargs='+',required=True);c.add_argument('--out',required=True)
    a=p.parse_args()
    try:
        if a.command=='catalog':d=make_catalog(a.phase00);save(a.out,d);out={'concepts':len(d['concepts']),'contexts':len(d['contexts']),'out':a.out}
        else:
            cat=catalog_read(a.catalog)
            if a.command=='check':d=check_record(cat,a.record);out={'valid':True,'record_id':d['record_id'],'scope':'reference/hash/range checks; not visual truth or R4 conformance'}
            elif a.command=='index':d=make_index(cat,a.catalog,a.records);save(a.out,d);out={'records':len(d['records']),'out':a.out}
            else:out=query(cat,a.catalog,a.index,a.id,a.query,a.motion_only,a.include_unobserved)
        print(json.dumps(out,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError,IndexError) as e:p.exit(2,type(e).__name__+': '+str(e)+'\n')
if __name__=='__main__':main()
