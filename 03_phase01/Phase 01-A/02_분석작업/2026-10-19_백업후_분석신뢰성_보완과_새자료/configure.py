from pathlib import Path
HERE=Path(__file__).resolve().parent;SKILL=HERE/'candidate/company-video-grammar-analyzer'
for p in SKILL.rglob('*.md'):
 t=p.read_text(encoding='utf-8-sig').replace('0.1.0-draft.6','0.1.0-draft.7');p.write_text(t,encoding='utf-8')
p=SKILL/'scripts/check_record.py';t=p.read_text(encoding='utf-8')
t=t.replace("'video-observation-0.4':'0.1.0-draft.6'","'video-observation-0.4':('0.1.0-draft.6','0.1.0-draft.7')")
t=t.replace("need(d['skill_version']==versions[d['schema_version']],'skill version mismatch')","supported=versions[d['schema_version']];supported=(supported,) if isinstance(supported,str) else supported\n    need(d['skill_version'] in supported,'skill version mismatch')")
t=t.replace("allow_historical or d.get('schema_version')=='video-observation-0.4'","allow_historical or (d.get('schema_version')=='video-observation-0.4' and d.get('skill_version')=='0.1.0-draft.7')")
p.write_text(t,encoding='utf-8')
p=SKILL/'references/motion-review.md';t=p.read_text(encoding='utf-8')
t=t.replace('## 가감속','## 반복·동반 효과와 사건 관계\n\n강조가 한 번 생긴 뒤 유지되는지, 강약·면적·색이 다시 변하는지 떨어진 여러 시점과 중간 표본을 대조한다. 외곽선·문구·표 셀을 한 강조라고 묶기 전 각각 확인한다. 반복 존재를 확인해도 표본 사이의 정확 주기·파형·동기화는 별도 미확정일 수 있다.\n\n문구 교체는 내용만 읽고 닫지 않는다. 중간에 남은 띠·경계·좁은 면의 형태와 폭, 새 문구의 판독 가능 시점을 살핀다. 서로 다른 대상의 사건은 같은 시각 표본에서 비교해 먼저/겹침/뒤를 구분한다. 얇은 띠가 보인다는 이유로 3D 회전이나 특정 마스크 구현을 확정하지 않는다.\n\n주 대상이 움직이면 주변 원형 빛·잔상·작은 광점도 독립 변화 후보로 살핀다. 화면 전체의 구도, 패널 외곽, 패널 내부 기준점에 대한 움직임을 분리하고, 방향을 확인했으면 정확 속도 미상이라는 이유로 방향까지 생략하지 않는다. 새로 발견한 요소는 대상·속성·근거·전체 레이아웃·세부 모션 기록에 함께 연결한다.\n\n## 가감속')
p.write_text(t,encoding='utf-8')
p=SKILL/'SKILL.md';t=p.read_text(encoding='utf-8').replace('## 전체 디자인과 반복 패턴','누락·오답 피드백을 받아 고칠 때는 [수정 검수](references/review-ledger.md)에 따라 이전 기록을 보존하고 지적 → 보완 주장 → 현재 근거를 연결한다. 이 검사는 이미 등록한 지적의 보완 추적이며 새 누락 발견이나 독립 품질 합격을 대신하지 않는다.\n\n## 전체 디자인과 반복 패턴')
p.write_text(t,encoding='utf-8')
