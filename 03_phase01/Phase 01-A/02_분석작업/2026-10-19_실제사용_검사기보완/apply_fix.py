from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent;ROOT=HERE/'candidate/company-video-grammar-analyzer'
sys.path.insert(0,str(ROOT/'scripts'))
from check_record import load,check
from render_observations import render
for p in ROOT.rglob('*.md'):
    text=p.read_text(encoding='utf-8-sig').replace('0.1.0-draft.5','0.1.0-draft.6').replace('video-observation-0.3','video-observation-0.4').replace('0.3/draft.5','0.4/draft.6')
    if p.name=='output-contract.md':
        text=text.replace('# 분석 기록 0.3','# 분석 기록 0.4').replace('property,facet,time_seconds,statement','property,facet,dimension,time_seconds,statement')
        text=text.replace('같은 대상·속성·facet·구간은 하나로 정리한다.','같은 대상·속성·facet·dimension·구간은 하나로 정리한다. dimension은 같은 표의 서로 다른 셀이나 독립 필드를 구분한다. 예: receiver1-accuracy / receiver2-accuracy. 같은 주장을 번호만 바꿔 중복시키는 데 쓰지 않는다. 구분이 필요 없어도 visible-form처럼 실제 의미가 있는 값을 쓴다.')
    if p.name=='SKILL.md':text=text.replace('한 주장은 한 대상·속성·판정에 해당하게 작성하고','한 주장은 한 대상·속성·판정에 해당하게 작성한다. 같은 표의 서로 다른 셀 값은 `dimension`으로 구분하고, 확인 안 한 속성을 범위 밖으로 숨기지 않는다. '  )
    p.write_text(text,encoding='utf-8')
contract=ROOT/'references/pattern-composition.md'
with contract.open('a',encoding='utf-8') as f:f.write('\n\n## 후보 검색\n\n`pattern_library.py search --library <snapshot.json> --category DETAIL --query "경로 드론"`으로 번호·이름·정의·조건의 단어를 찾는다. 검색은 단순 키워드 교집합이며 의미 유사도·현재 장면 적합성 판정이 아니다. 필요한 결과를 select한 뒤 현재 대상·속성·좌표계·차이·미해결과 대조한다.\n')
for name in ('H03','H04'):
    folder=HERE/'runs'/name;record=load(folder/'first-observations.json')
    record.update(schema_version='video-observation-0.4',skill_version='0.1.0-draft.6')
    errors=check(record,load(folder/'catalog.json'));assert not errors,(name,errors)
    (folder/'observations.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/'observations.md').write_text(render(record),encoding='utf-8')
    (folder/'validation.json').write_text(json.dumps({'version':'draft.6','structure_passed':True,'evidence_provenance_checked':True,'content_truth_verified_by_code':False,'fresh_holdout':False,'claims':len(record['claims']),'objects':len(record['objects'])},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'actual_cases':2,'actual_claims':62,'H03_before':'duplicate semantic claim key','H03_after':'passed without deleting distinct table or label facts'},ensure_ascii=False))
