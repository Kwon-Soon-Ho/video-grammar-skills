"""Render the observation JSON as Markdown without adding facts or approval."""
import argparse
from pathlib import Path
from check_record import load,check

def render(d):
    errors=check(d)
    if errors:raise ValueError('; '.join(errors))
    out=[f'# {d["case_id"]} 분석 기록','',f'판본: {d["skill_version"]} / {d["schema_version"]}',f'원본: {d["source"]["path"]}',f'구간: {d["window_seconds"]}초',f'방법: {d["method"]}',f'음성 검수: {d["audio_reviewed"]}','','구조 검사와 시각 내용 확인·회사 승인은 별개다.','']
    if d['reuse_map'] is not None:
        m=d['reuse_map'];patterns={p['id']:p for p in d['pattern_refs']}
        out+=['## 전체 사례와 재사용 번호','']
        for key,label in [('layout_occurrence_ids','전체 레이아웃'),('flow_occurrence_ids','전체 흐름'),('detail_occurrence_ids','독립 세부 동작')]:
            out.append('- '+label+': '+', '.join(patterns[x]['pattern_id'] for x in m[key]))
        for link in m['links']:out.append('- '+patterns[link['from_id']]['pattern_id']+' '+link['relation']+' '+patterns[link['to_id']]['pattern_id']+' / '+link['basis_kind'])
        out.append('')
    out+=['## 전체 디자인','']
    for s in d['layout']['states']:
        out += [f'### {s["id"]} / {s["time_seconds"]}',s['composition'],f'전체 요소: {", ".join(s["element_object_ids"])}',f'근거: {", ".join(s["evidence_ids"])}','']
        for key,v in s['design_spec'].items():out.append(f'- {key}: {v["description"]} ({v["basis_kind"]}; {v["precision"]}; 주장 {v["claim_ids"]})')
        out.append('')
    out+=['## 전체 흐름과 세부 모션','']
    claims={c['id']:c for c in d['claims']}
    for g in sorted(d['motion_groups'],key=lambda x:0 if x['level']=='flow' else 1):
        out += [f'### {g["level"]}: {g["name"]} / {g["time_seconds"]}']
        for cid in g['claim_ids']:out.append(f'- [{cid}] {claims[cid]["statement"]}')
        out.append(f'반복 패턴 참조: {g["pattern_occurrence_ids"]}')
        out.append('')
    out+=['## 대상 식별과 고유 주장','']
    for o in d['objects']:
        out += [f'### {o["id"]}: {o["name"]}',o['shape_description'],f'식별: {o["identity"]["status"]} / {o["identity"]["label"]}; 후보 {o["identity"]["candidates"]}','']
        for c in d['claims']:
            if c['object_id']==o['id']:out.append(f'- [{c["id"]}] {c["property"]}/{c["facet"]}: {c["statement"]} ({c["basis_kind"]}; 내용 {c["content_review"]}; 근거 {c["evidence_ids"]})')
        out.append('')
    out+=['## 검토 행과 미해결','']
    for r in d['observation_rows']:out.append(f'- {r["object_id"]}/{r["property"]} {r["time_seconds"]}: {r["review_state"]}, {r["change"]}; 주장 {r["claim_ids"]}; 미해결 {r["unknown_ids"]}')
    for u in d['unknowns']:out.append(f'- [{u["id"]}] {u["state"]}: {u["question"]} / {u["reason"]} / 다음 확인: {u["next_probe"]}')
    out+=['','## 재사용 패턴','']
    for p in d['pattern_refs']:out.append(f'- [{p["id"]}] {p["pattern_id"]}: {p["match_status"]}; 차이 {p["differences"]}; 미검증 {p["unverified_dimensions"]}; 현행 주장 {p["current_claim_ids"]}; 스냅샷 {p["library_path"]}')
    out+=['','## 내용 검수 범위',f'- 검수한 고유 주장: {len(d["review"]["content_reviewed_claim_ids"])}/{len(d["claims"])}',f'- 주장 분모 검토 완료: {d["review"]["claim_denominator_complete"]}',f'- 남은 범위: {d["review"]["remaining_scope"]}',f'- 한계: {d["limitations"]}','']
    if d['handoff'] is not None:
        h=d['handoff'];out+=['## 다음 판단으로 인계','']
        for k in ('purpose','information_relation'):out.append(f'- {k}: {h[k]}')
        out += [f'- 원본 사실: {h["observed_claim_ids"]}',f'- 보존할 특징: {h["preserve_claim_ids"]}',f'- 열린 쟁점: {h["open_unknown_ids"]}']
        for c in h['condition_candidates']:out.append(f'- 조건 후보: {c}')
        for c in h['implementation_options']:out.append(f'- 구현 제안: {c}')
    out+=['','## 근거 파일','']
    for e in d['evidence']:out.append(f'- [{e["id"]}] {e["actual_seconds"]}초 / {e["role"]}: {e["path"]}')
    return '\n'.join(out)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--out',required=True);a=p.parse_args()
    source=Path(a.input).resolve();out=Path(a.out).resolve()
    if source==out or out.suffix.lower()!='.md':p.error('output must be a separate Markdown file')
    try:
        content=render(load(source));out.parent.mkdir(parents=True,exist_ok=True);out.write_text(content,encoding='utf-8');print(str(out))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
