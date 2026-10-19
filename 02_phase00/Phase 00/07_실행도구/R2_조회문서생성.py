from pathlib import Path
import json,hashlib,shutil
BASE=Path(__file__).resolve().parents[1]
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def save(p,s):
    dest=(BASE/p).resolve();assert dest.is_relative_to(BASE.resolve());raw=(s.rstrip()+'\n').encode('utf-8')
    if dest.exists() and dest.read_bytes()==raw:return
    if dest.exists():
        h=hashlib.sha256(dest.read_bytes()).hexdigest()[:10];q=BASE/'backup/R2_조회문서재생성'/dest.relative_to(BASE);q=q.with_name(q.stem+'_'+h+q.suffix);q.parent.mkdir(parents=True,exist_ok=True)
        if not q.exists():shutil.copy2(dest,q)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
def main():
    t=read('01_공통용어/공통용어사전.json');d=read('01_공통용어/용어판정기준.json');r=read('01_공통용어/분류운영규칙.json')
    lines=['# 용어별 적용 예와 반례','','현재75개용어의프로젝트적용초안이다. 모든예는설명용상황이며실제영상사례가아니다. 기존사전ID/정의는유지한다. 구현만모를때에는충분한관측태그를지우지않고구현주장을별도로미확인으로남긴다.','']
    for axis in t['axes']:
        lines+=['## '+axis['name_ko'],'','| 용어 | 적용 예 | 반례 | 판단을 보류할 때 |','|---|---|---|---|']
        for g in d['guides']:
            if g['axis']==axis['id']:lines.append('| '+' | '.join(g[k].replace('|','\\|') for k in ['name_ko','positive_example','negative_example','abstain_when'])+' |')
        lines.append('')
    lines+=['## 최소 근거의 뜻','','| 조건 | 필요한 근거 | 적용 한계 |','|---|---|---|']
    for key,v in r['evidence_rules'].items():lines.append('| `'+key+'` | '+' · '.join(v['requires'])+' | '+v['limit']+' |')
    lines+=['','[운영규칙](분류운영규칙.json) · [판정기준 정본](용어판정기준.json) · [출처](../05_출처와검토/R2_현황과출처.md)']
    save('01_공통용어/03_용어별적용예와반례.md','\n'.join(lines))
    pairs=read('01_공통용어/혼동쌍사례.json')
    p=BASE/'01_공통용어/04_복합화면과미분류처리.md';s=p.read_text(encoding='utf-8')
    start=s.index('| 구분 |');end=s.index('## 판단 상태')
    table=['| 구분 | 적용 기준 | 잘못된 처리 |','|---|---|---|']
    for pair in pairs['pairs']:table.append('| '+pair['title']+' | '+pair['contrast']+' | '+pair['avoid']+' |')
    save('01_공통용어/04_복합화면과미분류처리.md',s[:start]+'\n'.join(table)+'\n\n'+s[end:])
    d=read('01_공통용어/설명용분류사례.json');lines=['# 범위를 나눠 기록하는 설명용 사례','','이사례는설명문에조건이주어진합성상황이다. 실제관측·수치·회사승인·자동분류성능으로해석하지않는다. R4실제영상기록과다른연습계약이다.','']
    for c in d['cases']:
        lines+=['## '+c['title'],'',c['interpretation'],'','| 단위 / 범위 | 축 / 주장 | 태그 / 상태 | 이유 |','|---|---|---|---|']
        for a in c['annotations']:lines.append('| '+a['unit_id']+' / '+a['target_scope']+' | '+a['axis']+' / '+a['claim_scope']+' | '+(', '.join(a['term_ids']) or '없음')+' / '+a['status']+' | '+a['reason']+' |')
        lines.append('')
    lines+=['[사례 정본](설명용분류사례.json) · [분류 운영규칙](분류운영규칙.json)']
    save('01_공통용어/05_범위별분류사례.md','\n'.join(lines));print('R2 현재JSON에서 용어/사례 조회MD 재생성 완료')
if __name__=='__main__':main()
