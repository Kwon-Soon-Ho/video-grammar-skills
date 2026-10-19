"""R3-1 JSON 조회본만 재생성한다. 원칙 정본·승인·분류·스킬은 변경하지 않는다."""
from pathlib import Path
import json,hashlib,shutil
BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,text):
    p=(BASE/rel).resolve()
    if not p.is_relative_to(BASE.resolve()):raise ValueError('Phase 00 밖 출력')
    raw=(text.rstrip()+'\n').encode('utf-8')
    if p.exists() and p.read_bytes()==raw:return
    if p.exists():
        q=BASE/'backup/R3_모션조회재생성'/rel;q=q.with_name(q.stem+'_'+sha(p)[:10]+q.suffix);q.parent.mkdir(parents=True,exist_ok=True)
        if not q.exists():shutil.copy2(p,q)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def render_cards(data,log,card_sha):
    by={s['id']:s for s in log['sources']}
    out=['# 모션 원칙별 적용 예와 반례','','모든 예는 프로젝트가 작성한 설명용 사례다. 실제 회사 영상·원문 예제·성능 검증 결과가 아니다. 기존43개 ID를 유지했고 사용자 A 선택으로 IP-10만 공식 Summary에 근거한 조건부 참고로 개정했다. 이 파일은 심화카드에서 생성했다.','',f"심화카드 v{data['version']} / SHA256 `{card_sha}`."]
    for c in data['cards']:
        s=by[c['source_refs'][0]]
        out+=['',f"## {c['id']} · {c['name_ko']}",'',f"출처: [{s['title']}]({s['url']}) · {c['source_read_depth']} · `{c['source_locator']}`",'',f"원문 요약: {c['source_summary_ko'] or '공식 강의의 항목명만 확인. 상세 정의는 강의 본문 미검토.'}",f"우리 적용 해석: {c['project_interpretation']}",'',f"- 적용 예: {c['positive_example']}",f"- 반례: {c['counterexample']}",f"- 기권·확인 조건: {c['abstain_when']}",f"- 관측 근거: {c['observables']}",f"- 검토 질문: {c['review_question']}",f"- 관련 원칙: {', '.join(c['related_ids']) or '현재 연결 없음'}",f"- 기본 추천: {'제외 — 활성화 검토 대기' if not c['recommendation_enabled'] else '조건부 참고 가능. 회사 필수 규칙 아님'}"]
    return '\n'.join(out)+'\n'
def main():
    rel='02_원칙과레이아웃/모션원칙_심화카드.json';data=read(rel);log=read('05_출처와검토/R3_모션_조사기록.json')
    write('02_원칙과레이아웃/03_모션원칙_적용예와반례.md',render_cards(data,log,sha(BASE/rel)))
if __name__=='__main__':main()
