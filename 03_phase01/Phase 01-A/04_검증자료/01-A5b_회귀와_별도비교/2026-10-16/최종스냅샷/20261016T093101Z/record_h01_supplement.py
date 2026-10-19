from pathlib import Path
import json,datetime
B=Path(__file__).resolve().parent;D=B/'blind/H01-r1'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
g=read(D/'grading.json');numeric=read(D/'numeric-audit.json');assert numeric['matched']==numeric['total']==80
resolution={}
for label in ['sample-A','sample-B']:
 updates=[]
 for c in g['samples'][label]['claims']:
  if c['supported'] is None:
   iscoord=('native_' in c['claim'] or 'mapT ' in c['claim'])
   # Every coordinate in each output was independently recomputed; related curve claims are checked against those same moving intervals.
   if iscoord or c['id'] in (['A-033','A-042','A-059'] if label=='sample-A' else ['B-038','B-053','B-076','B-080','B-091']):
    updates.append({'claim_id':c['id'],'supported':True,'evidence':'numeric-audit.json:80/80 original RGB statistics match; logo delta decreases across multiple moving intervals; English/map increase then decrease. This supports qualitative motion only, not AE parameters.'})
   elif c['id'] in (['A-015','A-021','A-034','A-035','A-036','A-037','A-045','A-048','A-056','A-060','A-061','A-065'] if label=='sample-A' else ['B-012','B-013','B-016','B-017','B-019','B-029','B-042','B-043','B-044','B-045','B-054','B-057','B-059','B-072','B-073','B-077','B-093']):
    updates.append({'claim_id':c['id'],'supported':True,'evidence':'root visually reopened listed sample-A/B native/crop evidence; same-source reference frames and pixel positions. Cropped partial strings interpreted with the output qualifiers; no full AE implementation inference.'})
 if label=='sample-B':updates.append({'claim_id':'B-036','supported':False,'evidence':'4.2 and4.4 source native logo crops show THREE yellow diagonal strokes inside O; output says TWO. Initial blinded grade marked it true incorrectly. A right-side three strokes are correct.','severity':'noncritical visual-detail count error; TOVA identity/function/metric meaning unchanged'})
 resolution[label]={'claim_updates':updates,'scope_incomplete':True,'claim_universe_complete':False,'precision_remains_null':True,'reason':'Additional declared coordinates and timing claims reviewed, but complete deduplication/atomization of every derived number and qualifier remains unproven within bounded review. No100% precision claim.','critical_errors':[]}
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'root AI after initial blinded grade, independently reopening source/crop; post-grade condition mapping was read so supplement is unblinded','initial_grading_preserved':True,'samples':resolution,'numeric_statistics_verified':80,'numeric_mismatches':0,'new_confirmed_wrong_claims':1,'initial_grader_false_positives_corrected':1,'new_reference_atoms_or_threshold_changes':0,'new_video_decode':0,'new_crops':0,'appropriate_unknown_not_avoidable':['AE exact curve/handles/implementation','Value of actual3D axis','map geographic scale'],'remaining_incomplete':'complete precision denominator; neither condition gets a full quality pass from this pair'}
(D/'review-supplement.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print({k:len(v['claim_updates']) for k,v in resolution.items()})
