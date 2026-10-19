from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE/'candidate/company-video-grammar-analyzer'
skill=ROOT/'SKILL.md';text=skill.read_text(encoding='utf-8')
text=text.replace('첫 패턴은 상세 분석한 뒤 카테고리·번호로 등록하고, 반복은 고정 스냅샷과 현행 근거·차이를 연결한다.','전체 사례를 보존하고 레이아웃·전체 흐름·독립 세부 동작에 각각 번호를 부여한다. [패턴 조합](references/pattern-composition.md)에 따라 사례의 `reuse_map`에서 각 번호와 순서·중첩·배치 관계를 연결한다. 첫 정의는 해당 단위를 상세히 분석하고 반복은 고정 스냅샷과 현행 근거·차이를 연결한다. 독립 재사용 가치가 없는 작은 변화마다 번호를 늘리지 않는다.')
skill.write_text(text,encoding='utf-8')
design=ROOT/'references/design-and-patterns.md';text=design.read_text(encoding='utf-8')
text=text[:text.index('## 첫 기록과 반복 기록')]+'''## 첫 기록과 반복 기록

전체 디자인과 흐름·세부는 사례 관측에 보존한다. 전체 사례를 한 CARD 패턴에 몰아넣지 않고 [패턴 조합](pattern-composition.md)의 독립 정의와 사례 연결을 사용한다. 처음 발견한 각 단위는 대상·상태·속성·순서·시간 근거·조건·미해결을 상세 기록한다. 번호를 나누는 기준은 독립 재사용 가능성이다. 문구·색·간격이 조금 다르다는 이유만으로 새 단위로 쪼개지 않는다.

카테고리: LAYOUT(전체 디자인), FLOW(전체 모션), TEXT(텍스트 등장·교체·퇴장), CARD(카드/UI 동작), TRANSITION(장면 전환), DETAIL(독립 세부 효과). 첫 번호는 해당 라이브러리의 다음 빈 번호로 배정한다. 기존 번호를 다른 뜻으로 바꾸지 않는다.

반복 기록 pattern_refs:[{id,pattern_id,pattern_sha256,library_path,library_sha256,object_ids,current_claim_ids,match_status,differences,unverified_dimensions}]. match_status=confirmed/candidate/mismatch. confirmed는 현재 자료에서 해당 범위를 대조했고 미검증 차원이 없을 때만 사용한다. 문구·크기·요소 수·화면비·시간·순서·가감속·내부 동작·겹침을 비교하고 차이와 미검증 부분을 남긴다. confirmed는 회사 승인이나 사용 효과 검증이 아니다.

`library_path`는 고정 스냅샷을 가리킨다. 스냅샷과 원본 관측이 달라지면 다시 확인한다. 과거 통합 CARD 항목은 이력으로 보존하고 새 분리 정의의 derived_from으로 연결한다. 과거 라이브러리를 자동 갱신하거나 과거 분석의 형식을 덮어쓰지 않는다.
'''
design.write_text(text,encoding='utf-8')
contract=ROOT/'references/output-contract.md';text=contract.read_text(encoding='utf-8').replace('pattern_refs, review,','pattern_refs, reuse_map, review,')
text+='\n`reuse_map`은 아직 조합 전이면 null, 패턴을 인용했으면 [패턴 조합 계약](pattern-composition.md)의 객체다. 과거 video-observation-0.2는 원본 보존 및 패턴 출처 조회에서만 읽는다. 현재 기록 검사는 0.3/draft.5를 사용한다.\n'
contract.write_text(text,encoding='utf-8')
renderer=ROOT/'scripts/render_observations.py';text=renderer.read_text(encoding='utf-8')
text=text.replace("    out+=['## 전체 디자인','']", """    if d['reuse_map'] is not None:
        m=d['reuse_map'];patterns={p['id']:p for p in d['pattern_refs']}
        out+=['## 전체 사례와 재사용 번호','']
        for key,label in [('layout_occurrence_ids','전체 레이아웃'),('flow_occurrence_ids','전체 흐름'),('detail_occurrence_ids','독립 세부 동작')]:
            out.append('- '+label+': '+', '.join(patterns[x]['pattern_id'] for x in m[key]))
        for link in m['links']:out.append('- '+patterns[link['from_id']]['pattern_id']+' '+link['relation']+' '+patterns[link['to_id']]['pattern_id']+' / '+link['basis_kind'])
        out.append('')
    out+=['## 전체 디자인','']""")
text=text.replace('f\'근거: {", ".join(s["evidence_ids"])}\'', 'f\'근거: {", ".join(s["evidence_ids"])}\'')
renderer.write_text(text,encoding='utf-8')
print('candidate instructions and rendering updated')
