from pathlib import Path
import hashlib,json,os,re,shutil
from urllib.parse import quote,unquote
W=Path(__file__).resolve().parent
P=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
D=P/'Phase 01-A';H=D/'00_진행안내/새채팅인계'
B=D/'backup/2026-10-16_새채팅인계'
R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_새채팅인계'
ST=W/'게시안';ST.mkdir(exist_ok=True);targets=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def read(p):return p.read_text(encoding='utf-8-sig')
def stage(p,data):
    rel=p.relative_to(P).as_posix();out=ST/rel;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    targets.append({'relative':rel,'before':sha(p) if p.exists() else None,'after':sha(out)})
def link(p,base,label):return '['+label+']('+quote(os.path.relpath(p,base.parent).replace('\\','/'),safe='/:._-')+')'
prior=load(W.parent/'phase01a-a1/게시명세.json')
protected=prior['protected_phase00']
for s in protected:assert sha(P/s['path'])==s['sha256'],s['path']
for name in ['02_분석작업','03_분석스킬','04_검증자료']:
    assert [p.name for p in (D/name).rglob('*') if p.is_file()]==['00_예약폴더_안내.md']
receipt={
 'id':'사용자회신_20261016_01-A2_처리방식A', 'date':'2026-10-16',
 'source':'현재 대화의 사용자 직접 회신',
 'question':'01-A2의 첫 예비 시험은 어떤 방식으로 진행할까요? 기존 시험 순서는 유지합니다.',
 'verbatim':'A. 로컬에서 시간·프레임을 추출하고 현재 Codex에서 작은 구간의 화면 검토부터 진행 — 음성 전사가 필요하면 API 처리 범위 별도 검토 (추천)',
 'scope':'장헌→무문서 EG-BIM의 제한된 실제 입력/화면 검토·검수·레드팀·보완·보고를 새 채팅에서 진행',
 'not_implied':['새 스킬 A3 제작','전체 영상 일괄 분석','별도 API 모델/비용/업로드 범위 확정','기존 스킬 기본 전환'],
 'current_thread_actions_after_answer':'A1 계약·현재 상태와 자료 목록 재조회만. 실제 회사 MP4 미열람',
 'actual_media_analysis_runs_at_handoff':0,'media_api_calls_at_handoff':0,
 'transfer_request_verbatim':'잠깐 Phase 01-A는 다른 채팅에서 옮겨서 하고 싶어. 새 채팅 생성하고 Phase 00 기록과 01-A이어서 해야할 작업 기록 후 채팅 너가 생성하고 이어서 작업해줄 수 있어?',
 'new_thread_creation_authorized':True,'continue_work_in_new_thread_authorized':True,
}
stage(D/'00_진행안내/14_01-A2_A안_선택기록.json',receipt)
stage(H/'00_새채팅_이어하기.md',read(W/'Phase01-A_새채팅_이어하기.md'))
additional=[
 'Phase 01-A/00_진행안내/09_제공자료_묶음목록.json',
 'Phase 01-A/00_진행안내/11_테스트영상_선정안.md',
 'Phase 01-A/00_진행안내/12_단계별검수와_레드팀계획.md',
 'Phase 01-A/00_진행안내/13_Phase00와_기존스킬_활용표.md',
]
live=D/'06_도구와계약/01-A1_도구와입출력검토'
additional += [p.relative_to(P).as_posix() for p in sorted(live.iterdir()) if p.is_file()]
refs={'date':'2026-10-16','purpose':'인계 시점 기준 파일/출처 바이트 확인. 내용 승인이나 runtime 전체 검증 아님',
 'phase00':protected,
 'phase01a':[{'path':r,'sha256':sha(P/r)} for r in additional],
 'working_runtime':str(W.parent/'phase01a-a1/후보런타임'),
 'runtime_global_install':False,'actual_company_mp4_opened':0,
 'notes':'새 채팅은 현재 상태/회신을 우선해 읽고, 과거 미시작/선택대기 보고를 현재 승인으로 오해하지 않는다.'}
stage(H/'01_인계시점_참조목록.json',refs)
planp=D/'00_진행안내/01-A_계획상태.json';plan=load(planp)
assert not plan['stage_A2_started'] and plan['actual_media_analysis_runs']==0
plan.update({'version':'0.3','state':'A2_route_A_authorized_transfer_to_new_thread',
 'current_stage':'01-A2','stage_A2_authorized':True,'stage_A2_started':False,
 'stage_A2_status':'새 채팅에서 실행 예정. 현재는 기준 문서 조회만 완료',
 'stage_A2_route':'A: 로컬 추출 + 현재 Codex 화면 검토. 필요 시 음성 API 범위 별도 검토',
 'stage_A2_approval_record':'00_진행안내/14_01-A2_A안_선택기록.json',
 'approved_execution_scope':'01-A1 결과 완료. 사용자 최신 회신으로 01-A2 경로 A 실행 승인. A3 이후는 후속 검토',
 'next_decision':None,'A2_route_choice_pending':False,
 'current_thread_media_work_stopped':True,
 'handoff_document':'00_진행안내/새채팅인계/00_새채팅_이어하기.md',
 'handoff_note':'계획·A1 결과의 기존 선택대기 문구는 작성 당시 이력. 새 채팅 생성 정보는 별도 기록',
})
stage(planp,plan)
s=D/'00_진행안내/기획서검토_현황.json';a=load(s)
a.update({'phase01a_current_stage':'01-A2 A안 승인 / 새 채팅에서 실제 작업 예정',
 'phase01a_A2_authorized':True,'analysis_started':False,'skill_development_started':False,
 'current_handoff':'새채팅인계/00_새채팅_이어하기.md'})
stage(s,a)
readp=D/'00_진행안내/10_01-A_계획_읽는순서.md'
stage(readp,'# 01-A 현재 읽는 순서\n\n2026-10-16 · 01-A1 완료. 01-A2 A안 선택 접수. 사용자 요청으로 새 채팅에서 이어서 실행합니다.\n\n1. '+link(H/'00_새채팅_이어하기.md',readp,'새 채팅 인계와 바로 할 일')+'\n2. '+link(D/'00_진행안내/14_01-A2_A안_선택기록.json',readp,'최신 사용자 선택')+'\n3. '+link(live/'00_검토결과_쉽게보기.md',readp,'01-A1 결과')+'\n4. '+link(P/'00기획/07_Phase01-A_진행계획.md',readp,'전체 진행 계획')+'\n\n장헌 → 시나리오 없는 EG-BIM → 복합 → 별도 확인 순서는 유지합니다. 같은 도구 선택이나 자료 묶음 확인을 반복하지 않습니다. 인계 시점 실제 회사 영상 분석·새 스킬 제작·별도 AI API 호출은 0건입니다.\n')
rootp=D/'00_먼저읽기.md';t=read(rootp)
t=t.replace('01-A2는 처리 방식 선택 대기입니다.','01-A2 A안은 승인됐고 사용자 요청으로 새 채팅에서 이어서 진행합니다.')
t=t.replace('01-A1 결과와 다음 단계 선택안을 먼저 확인합니다.','최신 새 채팅 인계와 01-A2 A안 회신을 먼저 확인합니다.')
t+='\n## 최신 새 채팅 인계\n\n'+link(H/'00_새채팅_이어하기.md',rootp,'Phase 00 기준과 01-A2 이어 할 일')+'\n\n로컬 추출 + 현재 Codex의 작은 구간 화면 검토를 승인받았습니다. 이전 A1 보고의 4안 비교/선택 대기는 이력입니다. 인계 시점 실제 회사 MP4는 열지 않았습니다.\n'
stage(rootp,t)
main=P/'00기획/07_Phase01-A_진행계획.md';t=read(main)
t=t.replace('계획 v0.2 · **사용자 A안 선택 접수 / 01-A1 검토·합성 진단 완료 / 01-A2 선택 대기**',
 '계획 v0.3 · **계획 A안·01-A2 처리 방식 A안 접수 / 01-A1 완료 / 새 채팅에서 01-A2 실행 예정**')
t=t.replace('이번 실행은 먼저 01-A1만 진행한다는 범위에 한정했습니다.',
 '01-A1 결과 제출 뒤 사용자가 01-A2의 로컬 추출 + 현재 Codex 화면 검토를 승인했습니다. 사용자 요청으로 새 채팅에서 실행을 이어갑니다.')
t+='\n최신 이어하기: '+link(H/'00_새채팅_이어하기.md',main,'새 채팅 인계와 실행 범위')+'\n'
stage(main,t)
index=P/'00기획/00_최신기획_읽는순서.md';t=read(index)
t=t.replace('01-A2 처리 방식은 선택 대기이며','01-A2 처리 방식 A안을 승인받았고 새 채팅으로 인계하며')
t+='\n'+link(H/'00_새채팅_이어하기.md',index,'최신 새 채팅 인계')+'\n'
stage(index,t)
report=D/'05_결과보고/07_새채팅_인계보고.md'
stage(report,'# Phase 01-A 새 채팅 인계 보고\n\n2026-10-16\n\n'+link(H/'00_새채팅_이어하기.md',report,'Phase 00 기록과 01-A2 바로 이어 할 일')+'\n\n사용자의 새 채팅 생성·이어서 실행 요청을 접수했습니다. 01-A2 A안 승인 기록과 현재 계획/진행 안내를 보완했습니다. 실제 회사 MP4는 열지 않았으며 전사·별도 API·새 스킬 제작은 미시작입니다. Phase 00 정본·회신·기본 스킬 경로는 변경하지 않았습니다.\n\n이 채팅은 인계 뒤 분석을 하지 않습니다. 새 채팅의 생성/진행 정보는 인계 폴더의 새채팅_생성기록.json으로 별도 남깁니다.\n')
stage(R/'00_새채팅_이어하기.md',read(W/'Phase01-A_새채팅_이어하기.md'))
stage(R/'01-A2_A안_선택기록.json',receipt)
for x in targets:
    p=P/x['relative'];st=ST/x['relative'];t=read(st)
    assert (sha(p)==x['before']) if x['before'] else not p.exists(),p
    assert '\ufffd' not in t and not re.search(r'[\u3040-\u30ff]',t),p
    if p.suffix=='.json':json.loads(t)
    if p.suffix=='.md':
        for u in re.findall(r'\]\(([^)\n]+)\)',t):
            if '://' in u:continue
            q=(p.parent/unquote(u)).resolve()
            assert q.exists() or (ST/q.relative_to(P.resolve())).exists(),(p,u)
m={'date':'2026-10-16','targets':targets,'phase00_protected':protected,'company_media_opened':0}
(W/'게시명세.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),'utf-8')
if os.environ.get('HANDOFF_PUBLISH')!='1':
    print(json.dumps({'mode':'preflight','files':len(targets),'phase00_references':len(protected)},ensure_ascii=False));raise SystemExit(0)
assert not B.exists() and not H.exists() and not R.exists()
B.mkdir(parents=True)
for x in targets:
    p=P/x['relative'];assert sha(p)==x['before'] if x['before'] else not p.exists(),p
    if x['before']:
        b=B/'변경전'/x['relative'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
        assert sha(b)==x['before']
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ST/x['relative']).read_bytes());assert sha(p)==x['after']
for s in protected:assert sha(P/s['path'])==s['sha256']
for f in W.iterdir():
    if f.is_file():shutil.copy2(f,B/f.name)
out={'files':len(targets),'previous_files_backed_up':sum(bool(x['before']) for x in targets),
 'phase00_reference_files_unchanged':len(protected),'A2_authorized':True,'A2_media_started':False,
 'analysis_skill_created':False,'company_media_opened':0,'external_media_API_calls':0,
 'handoff_document':str(H/'00_새채팅_이어하기.md')}
for dest in [W/'인계저장_결과.json',B/'인계저장_결과.json',R/'인계저장_결과.json']:
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
