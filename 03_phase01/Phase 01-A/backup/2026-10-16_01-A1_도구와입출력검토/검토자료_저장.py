"""01-A1 문서/진단 결과 게시. 실제 회사 영상 접근·분석·스킬 개발 없음."""
from pathlib import Path
import ast, datetime, hashlib, importlib.metadata, importlib.util, json, os, re, shutil
from urllib.parse import quote, unquote

W = Path(__file__).resolve().parent
P = Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
D = P/'Phase 01-A'
LIVE = D/'06_도구와계약/01-A1_도구와입출력검토'
B = D/'backup/2026-10-16_01-A1_도구와입출력검토'
R = P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A1_도구와입출력검토'
ST = W/'게시안'
ST.mkdir(exist_ok=True)
targets = []
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def txt(p): return p.read_text(encoding='utf-8-sig')
def load(p): return json.loads(txt(p))
def stage(dest, data):
    rel = dest.relative_to(P).as_posix()
    out = ST/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    targets.append({'relative':rel,'before':sha(dest) if dest.exists() else None,'after':sha(out)})
def mdlink(dest, base, label):
    return '['+label+']('+quote(os.path.relpath(dest,base.parent).replace('\\','/'),safe='/:._-')+')'
def remap_links(content, src, dst):
    def fix(m):
        u=m.group(1)
        if re.match(r'https?://',u): return m.group(0)
        to=(src.parent/unquote(u)).resolve()
        return ']('+quote(os.path.relpath(to,dst.parent).replace('\\','/'),safe='/:._-')+')'
    return re.sub(r'\]\(([^)\n]+)\)',fix,content)

# 기존 참조는 읽기 전용. 입력은 JSON 목록이며 MP4 자체를 읽지 않는다.
prior = load(W.parent/'phase01a-plan/게시명세.json')
protected = [s for s in prior['sources'] if s['path'].startswith('Phase 00/')]
for s in protected: assert sha(P/s['path']) == s['sha256'],s['path']
for folder in ['02_분석작업','03_분석스킬','04_검증자료']:
    assert [f.name for f in (D/folder).rglob('*') if f.is_file()] == ['00_예약폴더_안내.md']
inputs=load(D/'00_진행안내/09_제공자료_묶음목록.json')
assert len(inputs['cards']) == 23
result=load(W/'합성진단_결과.json')
assert result['passed'] == result['total'] == 18
first=load(W/'backup/01_첫진단_실패보존/합성진단_결과.json')
assert first['passed'] == 16 and first['total'] == 17
assert result['company_media_opened'] == result['api_calls'] == 0
assert not result['analyzer_skill_created']
for p in W.glob('*.py'):
    ast.parse(txt(p),filename=str(p))

approval={
    'id':'사용자회신_20261016_01-A_계획A승인',
    'date':'2026-10-16','source':'현재 대화의 사용자 직접 회신',
    'question':'01-A 진행 계획을 확인해 주세요. 선택 후에도 먼저 01-A1의 도구·입출력 기준 검토만 진행합니다.',
    'verbatim':'A. 장헌 → 시나리오 없는 EG-BIM 홈페이지 → 복합 자료 → 별도 확인 시험 순서 (추천)',
    'approved':'진행 계획 A와 시험 순서. 이번 실행은 01-A1만.',
    'not_implied':['01-A2 실제 분석 착수','01-A3 새 스킬 제작','기존 세 스킬 기본 전환','무제한 외부 API·과금'],
    'actual_media_analysis_runs':0,'skill_created':False,
}
stage(LIVE/'사용자선택_기록.json',approval)
env={'python_version':os.sys.version,'python_executable':os.sys.executable,
     'path_commands':{k:shutil.which(k) for k in ['ffmpeg','ffprobe']},
     'packages':{},'scope':'현재 bundled runtime/PATH만. PC 전체 조사 아님'}
for n in ['Pillow','numpy','av','opencv-python','scenedetect','openai']:
    try: env['packages'][n]=importlib.metadata.version(n)
    except importlib.metadata.PackageNotFoundError: env['packages'][n]=None
stage(LIVE/'기본환경_확인결과.json',env)

sources=[
('pyav-release','https://pypi.org/project/av/19.0.1/','배포 판본·Python 조건·해시 조회. 공급망 전체 인증 아님'),
('pyav-metadata','https://pypi.org/pypi/av/19.0.1/json','확보 원본과 SHA-256. JSON 사본 보존'),
('pyav-tag','https://github.com/PyAV-Org/PyAV/tree/v19.0.1','고정 원문. 선택 파일은 sdist에서 발췌 보존'),
('pyav-time','https://pyav.basswood.io/docs/stable/api/time.html','19.0.0 stable 시간 설명. 19.0.1 코드/실행 대조 필요'),
('pyav-container','https://pyav.basswood.io/docs/stable/api/container.html','열기·탐색·도구 보고값의 범위'),
('pyav-video','https://pyav.basswood.io/docs/stable/api/video.html','영상 프레임·변환 참조'),
('ffprobe','https://ffmpeg.org/ffprobe.html','메타데이터/packet/frame 교차확인 후보; CLI 미실행'),
('ffmpeg-license','https://ffmpeg.org/legal.html','빌드·구성요소에 따라 달라지는 조건. 법률 판정 아님'),
('openai-images','https://developers.openai.com/api/docs/guides/images-vision','resize/detail·한국어/작은 글자/공간 판단 한계; 모델 미선택'),
('openai-speech','https://developers.openai.com/api/docs/guides/speech-to-text','25MB 파일 한도·모델별 timestamp 지원; 실제 전사 미실행'),
]
source_record={'date':'2026-10-16','web_sources':[{'id':i,'url':u,'scope':s,'reviewed':True} for i,u,s in sources],
    'obsolete_reference':{'url':'https://pyav.org/docs/stable/','observed_version':'9.0.x','use_as_19_authority':False},
    'pinned_archives':load(W/'도구자료_확보목록.json')['files'],
    'local_baselines':protected,
    'notes':['공식 웹·공개 원본만 사용. 회사 파일 내용/키를 검색·업로드하지 않음',
             '원본 확보 manifest의 executed:false는 다운로드 당시 이력. 이후 격리 import·합성 실행은 별도 기록'],
}
stage(LIVE/'출처목록.json',source_record)
for name in ['정적검토_파일목록.json','격리런타임_검토결과.json','합성진단_결과.json']:
    stage(LIVE/name,load(W/name))
for p in sorted(W.glob('0[0-5]_*.md')): stage(LIVE/p.name,txt(p))

planp=D/'00_진행안내/01-A_계획상태.json'
plan=load(planp)
assert plan['approved'] is False and plan['actual_media_analysis_runs']==0
plan.update({
 'version':'0.2','state':'A1_review_complete_A2_pending_user_route_choice',
 'approved':True,'approved_choice':'A','approval_record':(LIVE/'사용자선택_기록.json').relative_to(D).as_posix(),
 'approved_execution_scope':'01-A1 only; later stages reported and reviewed separately',
 'current_stage':'01-A1','stage_A1_status':'completed_review_and_bounded_synthetic_diagnostics',
 'stage_A1_report':(LIVE/'00_검토결과_쉽게보기.md').relative_to(D).as_posix(),
 'stage_A2_started':False,'stage_A2_authorized':False,'analyzer_implementation_started':False,
 'diagnostic_code_created':True,'diagnostic_case_results':{'first_passed':16,'first_total':17,'retest_passed':18,'retest_total':18},
 'implementation_started':False,'implementation_started_definition':'실제 회사 영상 분석 도구·스킬 구현. A1 고정 합성 진단 코드는 별도',
 'redteam_execution_performed':True,'redteam_execution_scope':'A1 원문/계약/고정 합성 자료에 대한 작성자 자체 반대 관점 검토',
 'independent_redteam_performed':False,'self_review_performed':True,
 'actual_media_analysis_runs':0,'media_analysis_api_calls':0,'skill_created':False,
 'default_skill_promotion':False,'phase00_modified':False,
 'public_package_network_downloads':True,'company_media_opened_this_stage':0,
 'runtime_install_scope':'격리 작업폴더 wheel 추출/import만. 전역 설치 없음',
 'human_content_reviews_pending':0,'next_decision':'A2 도구·외부 AI 처리 범위 4안',
 'full_runtime_validation_completed':False,
})
stage(planp,plan)
statusp=D/'00_진행안내/기획서검토_현황.json'
s=load(statusp); s.update({'phase01a_plan_approved':True,'approved_test_order':'장헌→무문서EG-BIM→복합→별도확인',
 'phase01a_current_stage':'01-A1 검토·합성진단 완료 / A2 선택 대기', 'analysis_started':False,'skill_development_started':False})
stage(statusp,s)

main=P/'00기획/07_Phase01-A_진행계획.md'
t=txt(main)
t=t.replace('2026-10-16 · 검토용 계획 v0.1 · **계획 확인 전: 실제 영상 분석·스킬 개발·모델/API 시험 미실행**',
'''2026-10-16 · 계획 v0.2 · **사용자 A안 선택 접수 / 01-A1 검토·합성 진단 완료 / 01-A2 선택 대기**

장헌 → 시나리오 없는 EG-BIM 홈페이지 → 복합 자료 → 별도 확인 시험 순서를 승인받았습니다. 이번 실행은 먼저 01-A1만 진행한다는 범위에 한정했습니다. 실제 회사 영상 분석·새 분석 스킬 개발·별도 AI API 시험은 아직 미실행입니다.
'''+mdlink(LIVE/'00_검토결과_쉽게보기.md',main,'01-A1 결과와 다음 처리 방식'))
t=t.replace('## 이번 계획에서 요청할 선택','## 계획 선택 이력 — A안 회신 접수, 아래 선택은 종료')
t=t.replace('계획 확인 전에는 어떤 시험도 시작하지 않습니다. A/B/C를 선택하면 먼저 **01-A1만** 착수해 구체적인 도구·기능 범위를 보고합니다.',
 'A안 회신을 받아 **01-A1만** 실행했습니다. 고정 합성 도형 진단은 수행했고, 실제 회사 영상 분석과 후속 스킬 개발은 아직 시작하지 않았습니다.')
stage(main,t)
testp=D/'00_진행안내/11_테스트영상_선정안.md'
t=txt(testp).replace('2026-10-16 · 계획 확인 전 · 실제 영상 파일 열람/규격 조사/프레임 추출 없음',
 '2026-10-16 · 사용자 A안 시험 순서 선택 접수 · 실제 회사 영상 파일 열람/규격 조사/프레임 추출 없음')
stage(testp,t)
readp=D/'00_진행안내/10_01-A_계획_읽는순서.md'
stage(readp,'''# 01-A — 현재 읽는 순서

2026-10-16 · 사용자 A안 접수. 01-A1 검토·합성 진단 완료, 01-A2 선택 대기.

1. '''+mdlink(LIVE/'00_검토결과_쉽게보기.md',readp,'01-A1 결과 쉽게 보기')+'''
2. '''+mdlink(LIVE/'05_다음단계_처리방식_검토안.md',readp,'첫 예비 시험의 도구·외부 AI 처리 방식 4안')+'''
3. '''+mdlink(main,readp,'전체 계획과 현재 상태')+'''
4. [시험 영상](11_테스트영상_선정안.md) · [검수·레드팀](12_단계별검수와_레드팀계획.md) · [기존 스킬](13_Phase00와_기존스킬_활용표.md)

장헌 → 시나리오 없는 EG-BIM → 복합 → 별도 확인 순서는 유지합니다. 실제 회사 영상 분석·전사·API 호출·새 스킬 개발은 아직 시작하지 않았습니다. 자료 묶음 확인을 반복하지 않습니다.
''')
rootp=D/'00_먼저읽기.md'
t=txt(rootp).replace('**입력자료 연결은 완료했고 01-A 진행 계획은 검토 대기입니다. 실제 영상 분석과 스킬 개발은 시작하지 않았습니다.**',
 '**입력자료 연결과 계획 A안 선택은 완료했습니다. 01-A1 도구·입출력 검토와 합성 진단까지 마쳤고 01-A2는 처리 방식 선택 대기입니다. 실제 회사 영상 분석과 새 스킬 개발은 시작하지 않았습니다.**')
t=t.replace('계획 확인 후 01-A1부터 단계별로 보고합니다.','01-A1 결과와 다음 단계 선택안을 먼저 확인합니다.')
t=t.replace('최종 납품 상태·첫 시험 대상은 별도이며 분석은 미시작입니다.','첫 시험은 장헌→무문서 EG-BIM 순서로 선택했습니다. 최종 납품 상태·실제 내용 검수는 별도이며 분석은 미시작입니다.')
t=t.replace('- Phase 01-A/05_결과보고: 자료 준비 결과만','- Phase 01-A/05_결과보고: 자료 준비·계획·01-A1 검토 결과\n- Phase 01-A/06_도구와계약: 01-A1 도구 원문 검토·입출력 계약·합성 진단')
t+='\n## 최신: 01-A1 결과\n\n'+mdlink(LIVE/'00_검토결과_쉽게보기.md',rootp,'검토 결과 쉽게 보기')+' · '+mdlink(LIVE/'05_다음단계_처리방식_검토안.md',rootp,'다음 처리 방식 4안')+'\n\n고정 합성 진단 18/18 통과는 회사 영상 성능 평가가 아닙니다. 원문·실행값 차이와 시간/회전 함정을 보완하고 미검증 기능을 분리했습니다. Phase 00 기준과 스킬 기본 경로는 변경하지 않았습니다.\n'
stage(rootp,t)
indexp=P/'00기획/00_최신기획_읽는순서.md'
t=txt(indexp).replace('이번 01-A 계획은 검토 대기이며 실제 분석·개발은 시작하지 않았습니다.',
 '01-A 계획 A안의 시험 순서를 접수했고 01-A1 도구·입출력 검토와 고정 합성 진단을 마쳤습니다. 01-A2 처리 방식은 선택 대기이며 실제 회사 영상 분석·새 분석 스킬 개발은 시작하지 않았습니다.')
t+='\n'+mdlink(LIVE/'00_검토결과_쉽게보기.md',indexp,'최신 01-A1 결과')+'\n'
stage(indexp,t)
reportp=D/'05_결과보고/06_01-A1_도구와입출력검토_보고.md'
stage(reportp,'# 01-A1 결과 보고\n\n2026-10-16\n\n'+mdlink(LIVE/'00_검토결과_쉽게보기.md',reportp,'요약·세부 검토·다음 선택안')+'''

계획 A안의 시험 순서를 반영하고 이번 실행을 A1만으로 제한했습니다. 실제 회사 MP4는 열지 않았습니다. PyAV 고정 원본·코드·의존성·라이선스·외부 통신 기능과 공식 API 입력 제약을 조사하고, 입력·시간·좌표·근거·실패·사람 검수 계약을 정리했습니다.

고정 도형 첫 진단 16/17에서 시간 단위 미설정 반환값에 대한 문서와 실제 코드의 차이를 발견했습니다. 실패를 보존하고 None/falsy 처리와 반례를 보완해 18/18 재시험을 통과했습니다. 같은 도구로 생성·디코딩한 한정 진단이며 회사 영상 성능 평가가 아닙니다.

작성자 자체 반대 관점 검토로 GENPTS·회전 정보 부재·좌표 변환·의존성 배포·무문서 SW·후속 승인 확대 문제를 검토했습니다. 실제 MP4·음성·비영 회전 메타데이터·SAR·bounded 범용 도구와 전체 native 라이선스는 미검증 또는 후속 과제로 남겼습니다. 독립 레드팀/사람 내용 승인으로 기록하지 않았습니다.

현재 실제 영상 분석 0건, 회사 자료 API 0건, 새 분석 스킬 0개입니다. 관리용 세 스킬 기본 전환 보류·Phase 00 정본 유지·02/03/04 예약 폴더 유지를 확인합니다.
''')
# 중요 기록은 현재 문서와 별개인 시점 사본. 링크는 정본 결과 위치로 다시 맞춘다.
for name in ['00_검토결과_쉽게보기.md','04_레드팀과_보완기록.md','05_다음단계_처리방식_검토안.md']:
    stage(R/name,remap_links(txt(W/name),LIVE/name,R/name))
for name in ['합성진단_결과.json','격리런타임_검토결과.json']:
    stage(R/name,load(W/name))
stage(R/'사용자선택_기록.json',approval)
stage(R/'출처와기준.json',source_record)

# 사전 검증: 기존 파일 충돌, 링크, JSON, 비의도 문자, 분석 폴더/보호 파일.
for x in targets:
    p=P/x['relative']; st=ST/x['relative']
    assert (sha(p)==x['before']) if x['before'] else not p.exists(),p
    content=txt(st)
    assert '\ufffd' not in content and not re.search(r'[\u3040-\u30ff]',content),p
    if p.suffix=='.json': json.loads(content)
    if p.suffix=='.md':
        for url in re.findall(r'\]\(([^)\n]+)\)',content):
            if re.match(r'https?://',url): continue
            dest=(p.parent/unquote(url)).resolve()
            try: staged=ST/dest.relative_to(P.resolve())
            except ValueError: staged=None
            assert dest.exists() or (staged and staged.exists()),(p,url)
manifest={'date':'2026-10-16','targets':targets,'protected_phase00':protected,
 'execution_scope':'A1-only','company_videos_opened':0,'media_api_calls':0,'new_skills':0}
(W/'게시명세.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if os.environ.get('A1_PUBLISH') != '1':
    print(json.dumps({'mode':'preflight','files':len(targets),'protected_phase00':len(protected),'diagnostic_passed':18},ensure_ascii=False))
    raise SystemExit(0)
assert not B.exists() and not R.exists() and not LIVE.exists()
B.mkdir(parents=True)
for x in targets:
    p=P/x['relative']; st=ST/x['relative']
    assert sha(p)==x['before'] if x['before'] else not p.exists(),p
    if x['before']:
        prev=B/'변경전'/x['relative']; prev.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,prev); assert sha(prev)==x['before']
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(st.read_bytes()); assert sha(p)==x['after']
for sub in ['검토원본','합성진단','backup']:
    shutil.copytree(W/sub,B/sub)
for p in W.iterdir():
    if p.is_file(): shutil.copy2(p,B/p.name)
for s in protected: assert sha(P/s['path'])==s['sha256']
for folder in ['02_분석작업','03_분석스킬','04_검증자료']:
    assert [f.name for f in (D/folder).rglob('*') if f.is_file()] == ['00_예약폴더_안내.md']
verification={'date':'2026-10-16','published_files':len(targets),
 'backed_up_previous_files':sum(x['before'] is not None for x in targets),
 'phase00_reference_files_unchanged':len(protected),'reserved_folders_unchanged':3,
 'diagnostic_first':{'passed':16,'total':17},'diagnostic_retest':{'passed':18,'total':18},
 'company_media_analysis_runs':0,'media_api_calls':0,'new_analysis_skills':0,
 'independent_redteam_performed':False,'author_self_redteam_performed':True,
 'A2_started':False,'A2_user_choice_pending':True,
 'source_archives_backup':str(B/'검토원본'),'global_install':False,
 'isolated_runtime':str(W/'후보런타임')}
for dest in [W/'저장검증_결과.json',B/'저장검증_결과.json',LIVE/'저장검증_결과.json',R/'저장검증_결과.json']:
    dest.write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(verification,ensure_ascii=False))
