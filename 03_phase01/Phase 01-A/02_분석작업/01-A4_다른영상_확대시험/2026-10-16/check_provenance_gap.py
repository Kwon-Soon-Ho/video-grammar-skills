from pathlib import Path
import sys,json,copy
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'skill-draft2/scripts'))
from check_observations import check
from prepare import write
manifest={r['id']:r for r in json.loads((B/'manifest.json').read_text(encoding='utf-8'))}
dframe=json.loads((B/'cases/A4-D/V01/실행기록.json').read_text(encoding='utf-8'))['frames'][0]
gframe=json.loads((B/'cases/A4-G/V05/실행기록.json').read_text(encoding='utf-8'))['frames'][0]
d={'schema_version':'a3-observation-0.1','case_id':'provenance-test-fixture','source':{k:manifest['A4-D'][k] for k in ['path','sha256']},'window_seconds':[0,8],'method':'fixture only','document_mode':'none','audio_reviewed':False,'evidence':[{'id':'f0','path':dframe['path'],'actual_seconds':'0','role':'within'}],'objects':[{'id':'o','name':'fixture','parent':None,'events':[{'description':'fixture, not a content finding','properties':['position'],'time_seconds':[0,1],'evidence_ids':['f0'],'direction_order':'unknown','easing':{'property':'position','classification':'unknown','basis':'fixture'},'status':'observed','limitations':[]}]}],'coverage':{k:[] for k in ['overview','secondary_details','internal_content','unresolved']},'hypotheses':[],'limitations':['not a video analysis result'],'files_read':[]}
bad=copy.deepcopy(d);bad['evidence'][0]['path']=gframe['path']
wrongtime=copy.deepcopy(d);wrongtime['evidence'][0]['actual_seconds']='0.5'
write(B/'root-audit/provenance-fixtures.json',{'valid':d,'cross_source':bad,'wrong_time':wrongtime})
write(B/'root-audit/draft2-provenance-gap.json',{'valid_errors':check(d),'cross_source_errors':check(bad),'wrong_time_errors':check(wrongtime),'finding':'Draft2 structure checker accepts different source frame and relabelled time. Catalog verifies extraction separately but checker does not join them. This is a demonstrated record validation gap, not proof that a test analyst made that mistake.'})
print('draft2',check(d),check(bad),check(wrongtime))
