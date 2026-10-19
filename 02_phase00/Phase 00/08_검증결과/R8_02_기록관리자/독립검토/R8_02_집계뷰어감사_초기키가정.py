"""집계/정적 뷰어의 JSON·HTML 구조 대조. JS·브라우저·생성기·채점기 실행 없음."""
from pathlib import Path
import json,hashlib,base64,re
from html.parser import HTMLParser
OUT=Path(__file__).resolve().parent;CROOT=OUT.parents[1];W=OUT.parent/'R8_시험/video-record-steward-workspace'
hashes={}
def raw(p):
    b=p.read_bytes();hashes[p.relative_to(CROOT).as_posix()]=hashlib.sha256(b).hexdigest();return b
def obj(p):return json.loads(raw(p).decode('utf-8-sig'))
def embed(p):
    text=raw(p).decode('utf-8-sig');marker='const EMBEDDED_DATA = ';start=text.index(marker)+len(marker)
    data,n=json.JSONDecoder().raw_decode(text[start:]);return text,data,text[start:start+n]
class Inventory(HTMLParser):
    def __init__(self):super().__init__();self.external=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','link','iframe','img','source']:
            for k,v in attrs:
                if k in ['src','href'] and v and v.startswith(('http:','https:','//')):self.external.append([tag,k,v])
comparison=obj(W/'비교결과_정본.json');raw(W/'비교결과_요약.md')
benchmark=obj(W/'iteration-2/benchmark.json')
raw_text,raw_data,raw_literal=embed(W/'원문보존/공식뷰어_생성원본.html')
text,data,literal=embed(W/'기록관리자_출력검토.html')
inv=Inventory();inv.feed(text)
meta=obj(W/'뷰어_표시검증.json');obj(W/'공식뷰어_실행기록.json');raw(W/'원문보존/LICENSE.txt')
errors=[];checked_output_count=0;grades={}
runmap={r.relative_to(W/'iteration-2').as_posix().replace('/','-'):r for r in (W/'iteration-2').glob('eval-*/*/run-1')}
for r in data['runs']:
    run=runmap[r['id']];grade=obj(run/'grading.json');grades[(r['eval_id'],r['configuration'])]=grade
    if r.get('grading')!=grade:errors.append(r['id']+':embedded grading differs')
    for f in r['outputs']:
        p=run/'outputs'/f['name'];b=raw(p);checked_output_count+=1
        if f['type']=='text':
            expected=b.decode('utf-8').replace('\r\n','\n').replace('\r','\n')
            if f['content']!=expected:errors.append(r['id']+':text '+f['name'])
        elif f['type']=='binary':
            if base64.b64decode(f['data_uri'].split(';base64,',1)[1])!=b:errors.append(r['id']+':binary '+f['name'])
        else:errors.append(r['id']+':unsupported output type')
comparison_errors=[];totals={}
for c in comparison['comparisons']:
    for arm,row in c['configurations'].items():
        grade=grades[(c['case'],arm)];exp=grade['expectations'];s=grade['summary'];key=(c['case'],arm)
        if row['expectations']!=exp or any(row[k]!=s[k] for k in ['passed','failed','total','pass_rate']):comparison_errors.append(str(key)+':grade mismatch')
        gp=W/'iteration-2'/f'eval-{c["case"]:02d}-{c["eval_name"]}'/arm/'run-1/grading.json'
        if row['grading_sha256']!=hashes[gp.relative_to(CROOT).as_posix()]:comparison_errors.append(str(key)+':grading hash mismatch')
        if s['passed']!=sum(x['passed'] is True for x in exp) or s['failed']!=sum(x['passed'] is False for x in exp) or s['total']!=len(exp) or s['pass_rate']!=s['passed']/s['total']:comparison_errors.append(str(key)+':arithmetic')
        totals.setdefault(arm,{'passed':0,'total':0});totals[arm]['passed']+=s['passed'];totals[arm]['total']+=s['total']
for row in benchmark['runs']:
    grade=grades[(row['eval_id'],row['configuration'])]
    if any(row['result'][k]!=grade['summary'][k] for k in ['passed','failed','total','pass_rate']) or row['expectations']!=grade['expectations']:comparison_errors.append('benchmark grade mismatch')
    if any(row['result'][k] is not None for k in ['time_seconds','tokens','tool_calls','errors']):comparison_errors.append('benchmark unavailable telemetry not null')
report={'scope':__doc__,'embedded_data_equal_official_raw':data==raw_data,'embedded_final_runs':len(data['runs']),'embedded_output_files_checked':checked_output_count,'viewer_errors':errors,'external_resource_tags':inv.external,'script_boundary_literal_safe':'</script' not in literal.casefold(),'display_and_raw_hash_match_record':hashes[(W/'기록관리자_출력검토.html').relative_to(CROOT).as_posix()]==meta['display_sha256'] and hashes[(W/'원문보존/공식뷰어_생성원본.html').relative_to(CROOT).as_posix()]==meta['official_raw_sha256'],'previous_outputs_type':type(data.get('previous_outputs')).__name__,'previous_outputs_keys':list(data.get('previous_outputs',{})),'previous_outputs_sample_structure':{k:list(v[0]) if isinstance(v,list) and v else type(v).__name__ for k,v in data.get('previous_outputs',{}).items()},'comparison_errors':comparison_errors,'final_condition_totals':totals,'benchmark_run_summary':benchmark['run_summary'],'C_result_hashes':hashes}
(OUT/'R8_02_집계뷰어근거.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='C_result_hashes'},ensure_ascii=True))
