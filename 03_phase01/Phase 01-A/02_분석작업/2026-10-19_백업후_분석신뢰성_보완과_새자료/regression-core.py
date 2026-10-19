"""Synthetic adversarial checks of record/registry behavior, not video accuracy."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import sys,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import check as check_impl,load,digest,PROPERTIES
def check(d,catalog=None):return check_impl(d,catalog,allow_historical=True)
from pattern_library import add,validate_library
from render_observations import render as render_impl
def render(d):
    value=deepcopy(d);value.update(schema_version='video-observation-0.4',skill_version='0.1.0-draft.7',reuse_map=None)
    for claim in value['claims']:claim.setdefault('dimension',claim['id'])
    return render_impl(value)
OUT=HERE/'validation-core';OUT.mkdir(exist_ok=True)
catalog=load(WORK/'phase01a-a5b/trials/H02-r1-with_skill/support/evidence-catalog.json')
unique={}
for frame in catalog['frames']:unique.setdefault(str(frame['actual_playback_seconds']),frame)
frames=list(unique.values())[:3]
times=[float(Fraction(str(f['actual_playback_seconds']))) for f in frames];window=[min(times),max(times)+0.1]
ev=[{'id':f'f{i}','path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'within'} for i,f in enumerate(frames)]
eids=[e['id'] for e in ev]
claims=[]
for cid,prop,facet in [('c1','identity','identity'),('c2','size','value'),('c3','size','easing'),('c4','position','direction')]:
    c={'id':cid,'object_id':'o1','property':prop,'facet':facet,'time_seconds':window,'statement':f'합성 검사 문장 {cid}; 실제 영상 사실 아님','basis_kind':'observed','evidence_ids':eids,'content_review':'supported'}
    if facet=='easing':c['easing']={'classification':'decelerate','basis_evidence_ids':eids,'method':'합성 검사 조건','limitation':'실제 시각 판독 결과 아님'}
    claims.append(c)
d={'reuse_map':None,'schema_version':'video-observation-0.2','skill_version':'0.1.0-draft.4','case_id':'SYNTHETIC-CHECK-ONLY','source':{'path':'synthetic-not-a-source-video','sha256':frames[0]['source_sha256']},'window_seconds':window,'method':'합성 레코드로 구조 검사; 기존 PNG는 파일 연결 확인에만 사용','document_mode':'none','audio_reviewed':False,'files_read':[],'evidence':ev,'objects':[{'id':'o1','name':'합성 대상','parent':None,'shape_description':'합성 테스트용 묘사','required_properties':['identity','size','position'],'excluded_properties':{p:'합성 최소 사례에서 해당 없음' for p in PROPERTIES-{'identity','size','position'}},'identity':{'status':'reviewed','label':'합성 대상','candidates':[],'claim_ids':['c1']}}],'observation_rows':[],'claims':claims,'unknowns':[],'discovery':{'forward_evidence_ids':eids,'reverse_evidence_ids':eids,'unresolved_ids':[]},'layout':{'canvas':{'aspect_ratio':'16:9','coordinate_system':'native raster'},'states':[{'id':'s1','time_seconds':window,'evidence_ids':eids,'composition':'합성 레이아웃 검사','element_object_ids':['o1'],'claim_ids':['c1','c2'],'design_spec':{k:{'description':'합성 디자인 치수','basis_kind':'observed','precision':'qualitative','claim_ids':['c1']} for k in ('hierarchy','alignment','spacing','typography','color','background','shapes')},'unresolved_ids':[]}],'unresolved_ids':[]},'motion_groups':[{'id':'flow1','level':'flow','name':'합성 전체 흐름','time_seconds':window,'object_ids':['o1'],'claim_ids':['c2','c4'],'pattern_occurrence_ids':[]},{'id':'detail1','level':'detail','name':'합성 세부 모션','time_seconds':window,'object_ids':['o1'],'claim_ids':['c3'],'pattern_occurrence_ids':[]}],'pattern_refs':[],'review':{'content_reviewed_claim_ids':['c1','c2','c3','c4'],'claim_denominator_complete':True,'remaining_scope':['합성 검사이며 실제 관측·회사 승인 아님']},'handoff':{'purpose':{'text':'합성 목적 가설','basis_kind':'inferred','claim_ids':['c1']},'information_relation':None,'observed_claim_ids':['c1','c2'],'preserve_claim_ids':['c1'],'open_unknown_ids':[],'condition_candidates':[{'condition':'합성 조건','reason':'검사기 확인','claim_ids':['c1'],'counterexample':None,'validation_state':'untested'}],'implementation_options':[{'proposal':'합성 구현 제안','basis_kind':'inferred','claim_ids':['c2'],'verification_needed':'실제 렌더 확인'}]},'limitations':['합성 검사 입력; 실제 영상 재분석 결과나 패턴 지식으로 사용 금지']}
for prop,cids in [('identity',['c1']),('size',['c2','c3']),('position',['c4'])]:d['observation_rows'].append({'id':'r-'+prop,'object_id':'o1','property':prop,'time_seconds':window,'review_state':'reviewed','change':'unchanged' if prop=='identity' else 'changed','evidence_ids':eids,'claim_ids':cids,'unknown_ids':[],'reason':''})
results=[]
def record(name,passed,detail=''):
    results.append({'name':name,'passed':bool(passed),'detail':detail});assert passed,(name,detail)
record('valid_declared_record_and_provenance',not check(d,catalog),str(check(d,catalog)))
record('structure_only_does_not_require_catalog',not check(d))

def reject(name,change):
    value=deepcopy(d);change(value);errors=check(value,catalog);record(name,bool(errors),str(errors))
reject('missing_declared_size_row',lambda x:x['observation_rows'].pop(1))
reject('coverage_gap',lambda x:x['observation_rows'][1].update(time_seconds=[window[0]+0.01,window[1]]))
reject('dangling_claim',lambda x:x['observation_rows'][0]['claim_ids'].append('missing'))
reject('cross_property_claim',lambda x:x['claims'][2].update(property='position'))
reject('unreviewed_identity_as_confirmed',lambda x:x['claims'][0].update(content_review='not_reviewed'))
reject('inferred_identity_as_observed',lambda x:x['claims'][0].update(basis_kind='inferred'))
reject('unresolved_identity_with_label',lambda x:x['objects'][0]['identity'].update(status='unresolved'))
reject('false_review_completion',lambda x:x['claims'][1].update(content_review='not_reviewed'))
reject('duplicate_claim',lambda x:x['claims'].append({**x['claims'][1],'id':'c5'}))
reject('insufficient_curve_samples',lambda x:x['claims'][2]['easing'].update(basis_evidence_ids=eids[:2]))
reject('unlinked_easing_evidence',lambda x:x['claims'][2]['easing'].update(basis_evidence_ids=['missing']))
reject('unfinished_row_without_unknown',lambda x:x['observation_rows'][1].update(review_state='not_reviewed'))
reject('unscreened_property',lambda x:x['objects'][0]['excluded_properties'].pop('color'))
reject('missing_full_design_dimension',lambda x:x['layout']['states'][0]['design_spec'].pop('typography'))
reject('layout_missing_discovered_object',lambda x:x['layout']['states'][0].update(element_object_ids=[]))
reject('missing_motion_detail',lambda x:x['motion_groups'].pop())
reject('missing_motion_flow',lambda x:x['motion_groups'].pop(0))
reject('confirmed_implementation',lambda x:x['handoff']['implementation_options'][0].update(basis_kind='observed'))
reject('cross_source_evidence',lambda x:x['source'].update(sha256='0'*64))
reject('wrong_evidence_time',lambda x:x['evidence'][0].update(actual_seconds=str(times[0]+0.001)))
reject('parent_cycle',lambda x:x['objects'][0].update(parent='o1'))
reject('historical_schema_cannot_be_new_pass',lambda x:x.update(schema_version='a3-observation-0.1'))
for name,value in [('malformed_list',[]),('null',None),('missing_keys',{}),('malformed_interval',{**d,'window_seconds':[1]})]:record(name,bool(check(value,catalog)))
u={'id':'u1','object_id':'o1','question':'합성 크기 확인','state':'open','reason':'합성 미확정','required_basis_kind':'observed','next_probe':'원본 ROI 보강','resolution_claim_ids':[]}
partial=deepcopy(d);partial['unknowns']=[u];partial['observation_rows'][1].update(review_state='unresolved',unknown_ids=['u1'])
record('partial_facts_preserved_with_open_question',not check(partial,catalog),str(check(partial,catalog)))
partial['unknowns'][0].update(state='resolved',resolution_claim_ids=['c2']);partial['claims'][1]['basis_kind']='inferred'
record('inferred_evidence_cannot_resolve_observed_question',bool(check(partial,catalog)))

source=OUT/'synthetic-record.json';source.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'synthetic-observations.md').write_text(render(d),encoding='utf-8')
record('markdown_contains_flow_detail_layout_and_unknown_scope',all(s in render(d) for s in ('전체 디자인','flow:','detail:','검토 행과 미해결','c3','합성 검사')))
library=OUT/'synthetic-pattern-library.json'
if library.exists():raise RuntimeError('Validation output already contains a library; use a new validation directory')
pattern={'category':'TEXT','name':'합성 검사 전용 - 실제 패턴 아님','source':{'case_id':d['case_id'],'source_sha256':d['source']['sha256'],'observation_path':str(source),'observation_sha256':digest(source),'claim_ids':['c1','c2','c3']},'design_spec':{'layout':'합성 전체 레이아웃','typography':'합성 타이포','color':'합성 색','information_relation':'합성 관계'},'motion_spec':{'flow':'합성 흐름','detail':'합성 세부','timing':'합성 시간','properties':'합성 속성','unknowns':[]},'applicability':'검사기에서만 사용','counterexamples':['실제 영상에 사용 금지'],'status':'draft','supersedes':None}
pattern_path=OUT/'synthetic-pattern-input.json';pattern_path.write_text(json.dumps(pattern,ensure_ascii=False,indent=2),encoding='utf-8')
first=add(library,pattern_path);old_snapshot=Path(first['library_snapshot_path']);old_hash=digest(old_snapshot)
record('category_number_assigned',first['pattern_id']=='PAT-TEXT-0001')
pattern['name']='합성 다음 판본';pattern['supersedes']=first['pattern_id'];pattern_path.write_text(json.dumps(pattern,ensure_ascii=False,indent=2),encoding='utf-8')
second=add(library,pattern_path)
record('append_preserves_number_and_snapshot',second['pattern_id']=='PAT-TEXT-0002' and digest(old_snapshot)==old_hash and load(library)['patterns'][0]['sha256']==first['pattern_sha256'])
occurrence={'id':'occ1','pattern_id':first['pattern_id'],'pattern_sha256':first['pattern_sha256'],'library_path':str(old_snapshot),'library_sha256':old_hash,'object_ids':['o1'],'current_claim_ids':['c2','c3'],'match_status':'confirmed','differences':['합성 사례의 차이'],'unverified_dimensions':[]}
repeat=deepcopy(d);repeat['pattern_refs']=[occurrence];repeat['motion_groups'][1]['pattern_occurrence_ids']=['occ1']
record('repeat_reuses_pinned_first_pattern',not check(repeat,catalog),str(check(repeat,catalog)))
repeat['pattern_refs'][0]['unverified_dimensions']=['진행 중 속도 미검수'];record('unreviewed_repeat_not_confirmed',bool(check(repeat,catalog)))
repeat=deepcopy(d);repeat['pattern_refs']=[{**occurrence,'pattern_sha256':'0'*64}];record('changed_pattern_pin_rejected',bool(check(repeat,catalog)))
tampered=load(library);tampered['patterns'][0]['name']='변조';failed=False
try:validate_library(tampered)
except ValueError:failed=True
record('tampered_pattern_rejected',failed)
pattern['status']='approved';pattern_path.write_text(json.dumps(pattern,ensure_ascii=False),encoding='utf-8');before=digest(library);failed=False
try:add(library,pattern_path)
except ValueError:failed=True
record('registration_cannot_grant_approval',failed and digest(library)==before)
output={'utc':datetime.now(timezone.utc).isoformat(),'scope':'synthetic structure/provenance/registry/renderer adversarial checks; not vision accuracy or independent trial','tests':results,'passed':sum(r['passed'] for r in results),'total':len(results),'all_passed':all(r['passed'] for r in results),'real_video_accuracy_proven':False}
(OUT/'checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in output.items() if k!='tests'},ensure_ascii=False))



