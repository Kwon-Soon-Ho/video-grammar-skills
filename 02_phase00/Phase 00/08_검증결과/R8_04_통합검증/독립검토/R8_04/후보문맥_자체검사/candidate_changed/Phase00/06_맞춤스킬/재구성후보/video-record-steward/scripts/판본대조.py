"""R4/R5 초안의 전후 판본 또는 정확 복원 바이트 대조. 읽기 전용·표준 라이브러리."""
from pathlib import Path
import argparse,json,hashlib,re,math
def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict(raw):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d:raise ValueError('중복 JSON 키: '+k)
            d[k]=v
        return d
    def reject(x):raise ValueError('비유한 JSON 수: '+x)
    value=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=reject)
    def walk(v):
        if isinstance(v,str):v.encode('utf-8')
        elif isinstance(v,float) and not math.isfinite(v):raise ValueError('비유한 JSON 수')
        elif isinstance(v,dict):
            for k,x in v.items():walk(k);walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(value);return value
def inspect_bytes(before,after,mode='content_edit',checkpoint=None,checkpoint_sha=None):
    errors=[]
    result={'valid':False,'mode':mode,'before_sha256':sha(before),'after_sha256':sha(after),'bytes_changed':before!=after,'errors':errors,'scope':'R4/R5 초안 전후 식별/규격판본·소유기록 판본 또는 요청 checkpoint byte 대조만. 허용 필드·R4/R5 전체 구조·내용·권한 검사는 별도.','writes_performed':False,'content_verified':False,'company_approved':False,'operational_release':False}
    a=b=None
    try:
        if mode=='exact_restore':
            if checkpoint is None or not isinstance(checkpoint_sha,str) or not re.fullmatch('[0-9a-f]{64}',checkpoint_sha):errors.append('정확 복원에는 checkpoint bytes와 명시한 SHA256 필요')
            elif sha(checkpoint)!=checkpoint_sha:errors.append('checkpoint SHA 불일치')
            elif after!=checkpoint:errors.append('복원 후 bytes가 checkpoint와 다름')
            # Broken pre-recovery bytes may be truncated JSON. Do not require them to parse.
            b=None;a=strict(after)
        elif mode=='content_edit':
            b=strict(before);a=strict(after)
            if not isinstance(a,dict) or not isinstance(b,dict):raise ValueError('기록 객체 필요')
            keys=[k for k in ['record_id','application_id'] if k in a or k in b]
            if len(keys)!=1:errors.append('R4 record_id 또는 R5 application_id 한 종류 필요')
            elif not isinstance(b.get(keys[0]),str) or not b.get(keys[0]) or b.get(keys[0])!=a.get(keys[0]):errors.append('동일 논리 기록의 ID 보존 필요')
            if not all(isinstance(x.get('schema_version'),str) and x['schema_version'].strip() for x in [a,b]):errors.append('규격 schema_version 필요')
            elif b.get('schema_version')!=a.get('schema_version'):errors.append('내용 수정으로 schema_version을 변경하지 않음')
            if not all(isinstance(x.get('version'),str) and x['version'].strip() for x in [a,b]):errors.append('소유 기록의 비어 있지 않은 version 필요')
            elif before!=after and b['version']==a['version']:errors.append('참조 메타데이터를 포함한 bytes 변경은 소유 기록의 새 version 필요')
        else:errors.append('지원하지 않는 대조 mode')
        if not isinstance(a,dict):errors.append('복원/수정 결과는 기록 객체 필요')
        if isinstance(a,dict):result['after_record_version']=a.get('version')
        if isinstance(b,dict):result['before_record_version']=b.get('version')
    except (ValueError,UnicodeError,RecursionError) as e:errors.append(type(e).__name__+': '+str(e))
    result['valid']=not errors;return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--mode',choices=['content_edit','exact_restore'],default='content_edit');p.add_argument('--checkpoint',type=Path);p.add_argument('--checkpoint-sha');a=p.parse_args()
    try:r=inspect_bytes(a.before.read_bytes(),a.after.read_bytes(),a.mode,a.checkpoint.read_bytes() if a.checkpoint else None,a.checkpoint_sha)
    except OSError as e:r={'valid':False,'errors':[str(e)],'writes_performed':False,'content_verified':False,'company_approved':False,'operational_release':False}
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False));return 0 if r['valid'] else 1
if __name__=='__main__':raise SystemExit(main())
