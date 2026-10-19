"""정본 JSON에서 조회용 MD·팔레트만 생성. 원칙/회사 승인/분류 의미는 수정하지 않는다."""
from pathlib import Path
import json,hashlib,shutil,datetime,importlib.util
from urllib.parse import quote
BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,value):
    p=(BASE/rel).resolve()
    if not p.is_relative_to(BASE.resolve()):raise ValueError('Phase00 밖 출력')
    raw=((json.dumps(value,ensure_ascii=False,indent=2)+'\n') if not isinstance(value,str) else value.rstrip()+'\n').encode('utf-8')
    if p.exists() and p.read_bytes()==raw:return
    if p.exists():
        q=BASE/'backup/조회문서재생성'/p.relative_to(BASE);q=q.with_name(q.stem+'_'+sha(p)[:10]+q.suffix);q.parent.mkdir(parents=True,exist_ok=True)
        if not q.exists():shutil.copy2(p,q)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def text(v):
    if isinstance(v,list):v=' · '.join(map(str,v))
    return str(v or '미기록').replace('|','\\|').replace('\n','<br>')
def source_note(paths):return '\n\n정본: '+', '.join('`'+p+'` SHA256 `'+sha(BASE/p)+'`' for p in paths)+'. 조회문서만 고쳐도 정본은 변경되지 않는다.\n\n'
def main():
    rel='01_공통용어/공통용어사전.json';d=read(rel)
    lines=['# 공통 용어 조회',source_note([rel]),'정의·상태는 현재 정본을 그대로 표시한다. 분류 단위·적용 예 보완은 R2에서 진행한다.\n','| ID / 명칭 | 축 / 상태 | 정의 | 포함 조건 | 제외·한계 | 별칭 / 출처 |','|---|---|---|---|---|---|']
    for x in d['terms']:lines.append('| '+' | '.join(text(v) for v in [x['id']+' / '+x['name_ko'],x['axis']+' / '+x['status'],x['definition'],x['include_when'],x['exclude_or_limit'],text(x['aliases'])+' / '+text(x['source_refs'])])+' |')
    write('01_공통용어/용어목록.md','\n'.join(lines))
    rels=['02_원칙과레이아웃/'+f for f in ['모션과정보전달원칙.json','화면설계원칙.json','레이아웃지식.json']]
    lines=['# 원칙과 레이아웃 조회',source_note(rels),'현재 초안의 조회본이다. 조사 깊이·적용 예·반례의 확장은 R3에서 별도 검수한다.\n']
    for rel in rels:
        d=read(rel);lines+=['## '+Path(rel).stem,'','| ID / 명칭 | 정의 | 적용 조건 | 한계 / 상태 | 출처 |','|---|---|---|---|---|']
        for x in d.get('principles',d.get('layouts',[])):lines.append('| '+' | '.join(text(v) for v in [x['id']+' / '+x['name_ko'],x['definition'],x.get('consider_when',x.get('fit_conditions')),text(x.get('avoid_or_adjust_when',x.get('limits')))+' / '+x['status'],x['source_refs']])+' |')
        lines.append('')
    write('02_원칙과레이아웃/지식목록.md','\n'.join(lines))
    spec=importlib.util.spec_from_file_location('r1',BASE/'07_실행도구/R1_자산검사.py');r1=importlib.util.module_from_spec(spec);spec.loader.exec_module(r1)
    c=read('10_공용자산/회사목록.json');a=read('10_공용자산/자산목록.json');k=read('10_공용자산/CI색상목록.json');inspection=r1.inspect(c,a,k)
    if not inspection['valid']:raise ValueError(inspection['errors'])
    company_names={x['company_id']:x['name_ko'] for x in c['companies']}
    originals=sum(x['role']=='original' for x in a['records']);edits=sum(x['file']['path'].startswith('10_공용자산/02_작업자료/') for x in a['records'])
    index=['# 8개 회사 CI·심볼 찾아보기','', f'사용자 확인 범위: 8개 모두 별도 회사. 보존원본{originals}개, 편집용AI{edits}개. 초기분리SVG/PNG 각20개, 추가모음PNG41개는보존원본에포함.','', '삼안 명시색·㈜장헌 형태규정이 포함된 제공문서를 확보했다. 공식 최신판/지정색 승인은 미확인. 관측색과 문서명시 draft값을 구분하며, 제공 PNG와 AI 내보내기 색을 서로 덮어쓰지 않았다.','', '| 회사 | 편집용 AI | 보유 심볼 | 부족한 자료 |','|---|---|---|---|']
    for company in c['companies']:
        cid=company['company_id'];name=company_names[cid];folder='주식회사장헌' if cid=='jangheon' else name
        records=[x for x in a['records'] if cid in x['company_ids']];edits=[x for x in records if x['file']['path'].startswith('10_공용자산/02_작업자료/')];has_symbol=any('심볼' in x['file']['path'] for x in records)
        index.append(f'| [{name}]({folder}/00_CI와심볼_안내.md) | {len(edits)}개 | '+('있음' if has_symbol else '미제공')+' | '+('벡터 AI·별도 심볼·공식 가이드' if cid=='sanha' else '공식 가이드·최신판 확인')+' |')
        lines=['# '+name+' — CI·심볼 자산 안내','',f'회사ID `{cid}`. 회사명단은 사용자 확인, 공식 최신CI·지정색·배포범위는 미확인.','', '## 바로 사용할 파일 찾기','', '| 파일 / 용도 | 역할 | 원본 연결 |','|---|---|---|']
        for asset in records:
            p=asset['file']['path'];relative='../../../'+p.replace('10_공용자산/','')
            # This MD lives at 10_공용자산/04_조회용자료/회사명, two levels to 10_공용자산.
            relative='../../'+p.removeprefix('10_공용자산/')
            relation=' · '.join(x['target']['asset_id']+'@'+x['target']['record_version'] for x in asset['relationships']) or '제공 원본'
            lines.append('| ['+Path(p).name+']('+quote(relative,safe='/._-')+') | '+asset['role']+' | '+relation+' |')
        original=next(x for x in records if x['role']=='original' and x['file']['path'].endswith(folder+'_CI_제공원본.png'))
        lines+=['','## CI 조회','',f"![{name} 제공 CI](../../{original['file']['path'].removeprefix('10_공용자산/')})",'','투명 PNG는 밝은 배경에서 확인한다. 원본/변환본 색공간이 같다는 가정으로 서로 덮어쓰지 않는다.','', '## 화면에서 참고할 관측색','', '아래는 제공 PNG의 alpha255 픽셀 관측값이다. ICC가 없어 sRGB 표시를 가정했다. 회사 지정색·브랜드 역할 승인값으로 쓰지 않는다.','', '| 관측값 | 픽셀 근거 |','|---|---|']
        palette=r1.palette(cid,c,k,include_observed=True,assets=a)
        for x in palette['colors']:lines.append('| `'+x['screen_value']['hex']+'` | '+x['evidence_locator']+' |')
        vectors=[x for x in k['colors'] if x['company_id']==cid and x['source_level']=='vector_literal']
        lines+=['','## AI 원문 색 채널','', 'CMYK/RGB 원문 채널을 보존했다. 프로필·공식 가이드가 없으므로 화면 HEX 자동 변환은 보류한다. 클리핑/그라디언트 내부값은 대표색 역할과 다르다.','', '| 원문 값 | 원문 위치 |','|---|---|']
        for x in vectors:lines.append('| '+x['raw_value']['notation']+' `'+json.dumps(x['raw_value']['value'])+'` | '+x['evidence_locator']+' |')
        declared=[x for x in k['colors'] if x['company_id']==cid and x['source_level']=='official_declared']
        if declared:
            lines+=['','## 제공 문서의 명시색 — draft','', '원문에 적힌 값을 보존했다. 최신판·공식 권위·색공간 확인 전이므로 공식 기본 팔레트에 반환하지 않는다.','', '| 원문 명칭 | 원문 표기 | 상태 |','|---|---|---|']
            for x in declared:lines.append('| '+x['label_in_source']+' | '+x['raw_value']['notation']+' `'+str(x['raw_value']['value'])+'` | '+x['verification']['state']+' |')
        if cid=='jangheon':lines+=['','## 제공 문서의 형태 규정 — draft','', '추가모음 AI page1/2에 글자의 형태·굵기·비례를 임의 변경하지 말고 매뉴얼 데이터의 확대·축소·복사를 사용하라는 설명이 있다. 원문 출처와 함께 기록했으며 회사 필수규칙 승인으로 승격하지 않았다.']
        lines+=['','## 남은 확인','', '- 제공문서/CI의 공식 권위·최신판 확인과 지정색의 색공간/프로필.','- 밝은/어두운 배경형, 최소 크기·보호 공간, 단색형은 가이드 확인 후 추가.','- 영문 법인명의 공식 표기와 폰트·이미지·도표 자산은 미확보.']
        if cid=='sanha':lines.append('- 제공자료는 CI PNG 1개. AI/SVG 원본과 별도 심볼이 없어 벡터 재구성·심볼 분리는 보류. 임의 트레이싱으로 원본을 만들지 않았다.')
        if cid=='halla':lines.append('- 제공 심볼은 HALLA 워드마크 전체다. 파란 삼각형만 분리해 공식 심볼로 만들지 않았다.')
        if cid=='jangheon':lines.append('- 장헌산업과 별도 회사로 보존. 3D 심볼의 그라디언트·그림자도 그대로 복제했다.')
        if cid=='saman':lines.append('- 추가모음의 CI_영문시그니처_kr_2025.png는 국문가로형과 SHA256이 같다. 두제공명·해시를 보존하되 영문형으로 자동판정하지 않는다.')
        lines+=['', '[전체 목록](../00_회사별자산목록.md)',source_note(['10_공용자산/회사목록.json','10_공용자산/자산목록.json','10_공용자산/CI색상목록.json'])]
        write('10_공용자산/04_조회용자료/'+folder+'/00_CI와심볼_안내.md','\n'.join(lines))
        write('10_공용자산/04_조회용자료/'+folder+'/화면색_관측팔레트.json',{'company_id':cid,'status':'observed_not_official','canonical_sha256':sha(BASE/'10_공용자산/CI색상목록.json'),'palette':palette})
    write('10_공용자산/04_조회용자료/00_회사별자산목록.md','\n'.join(index))
    write('08_검증결과/R1_실자료_등록검사.json',inspection)
    print(json.dumps({'generated':'용어·지식 조회 / 8회사 MD와 관측 팔레트','inspection':inspection},ensure_ascii=False))
if __name__=='__main__':main()
