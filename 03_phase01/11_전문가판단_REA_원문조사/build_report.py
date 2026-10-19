from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, re, html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent.parent
OUT = WORK / 'output/pdf/20261019_video_skill_research.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

REPOS = {
 'P': ('DietrichGebert/ponytail','09c434ab73ca43761c5d8b0c5d341926c2fba710',ROOT/'snapshots/ponytail-09c434ab73ca43761c5d8b0c5d341926c2fba710'),
 'R': ('morluto/rea','95c8f57aa2eafab4c8d7d43482b33ceefaf96b16',ROOT/'snapshots/rea-95c8f57aa2eafab4c8d7d43482b33ceefaf96b16'),
 'I': ('pbakaus/impeccable','2f46b7a8b059af00d20dd13b64dbe165e7c6a742',ROOT/'selected-sources/pbakaus__impeccable-2f46b7a8b059af00d20dd13b64dbe165e7c6a742'),
 'T': ('trailofbits/skills','5c99c03fb8a9ea568432ecbcba5d86e9f4ac2bf0',ROOT/'selected-sources/trailofbits__skills-5c99c03fb8a9ea568432ecbcba5d86e9f4ac2bf0'),
 'S': ('obra/superpowers','bb92a77741419a4ab5f06e711a283343f1ada0c3',ROOT/'snapshots/superpowers-bb92a77741419a4ab5f06e711a283343f1ada0c3'),
 'M': ('mattpocock/skills','49dd158d1076134a641b33efb035946536778336',ROOT/'snapshots/skills-49dd158d1076134a641b33efb035946536778336'),
 'G': ('garrytan/gstack','8640ab4ff43accda6676105868935903232d8c93',ROOT/'snapshots/gstack-8640ab4ff43accda6676105868935903232d8c93'),
 'A': ('anthropics/skills','dbd4588f9e1033efb41dad4bef2f7947c8993d44',ROOT/'snapshots/skills-dbd4588f9e1033efb41dad4bef2f7947c8993d44'),
 'E': ('affaan-m/ECC','76aaa77df6adc5b889e689007bf99b9a4f74af34',ROOT/'snapshots/ECC-76aaa77df6adc5b889e689007bf99b9a4f74af34'),
 'V': ('vercel-labs/agent-skills','063bee94c3f4df8453406c830b0a7df0f2860278',ROOT/'snapshots/agent-skills-063bee94c3f4df8453406c830b0a7df0f2860278'),
}
SOURCES = [
 ('P1','P','skills/ponytail/SKILL.md','Before you write','판단 사다리와 생략 금지 조건','full'),
 ('P2','P','hooks/ponytail-map.js','const SAFE_PATH','색인의 범위·한글 경로·길이 제한','full'),
 ('P3','P','hooks/ponytail-activate.js','timeout: 3000','활성화와 색인 실패 처리','full'),
 ('P4','P','skills/ponytail-review/SKILL.md','Every finding needs','구체 사례를 요구하는 리뷰','full'),
 ('P5','P','skills/ponytail-debt/SKILL.md','ceiling','생략의 한계와 재검토 조건','full'),
 ('P6','P','benchmarks/results/2026-10-07-agentic.md','Only the 18','제작자 실험의 품질 분모와 한계','selected'),
 ('P7','P','benchmarks/agentic/README.md','contaminated','기준선 오염·평가기 자체 검사','selected'),
 ('R1','R','src/domain/evidence.ts','const evidenceBaseSchema','증거·분석기·관측 유형·의미 해시','full'),
 ('R2','R','src/domain/residualUnknown.ts','const residualUnknownObjectSchema','미해결 질문과 판본','full'),
 ('R3','R','src/application/investigation/EvidenceLedger.ts','expected_revision','상태 변경 충돌과 종료/입증의 분리','selected'),
 ('R4','R','src/domain/evidenceBundle.ts','const evidenceQualifies','증거 유형과 환경의 자격 검사','selected'),
 ('R5','R','src/application/investigation/EvidenceLedger.residualUnknown.test.ts','rejects inference for observed','추론만으로 관측 요구를 닫지 않는 테스트','selected'),
 ('R6','R','src/domain/reconstructionCoverage.ts','const boundarySchema','요구 목록·판정 경계·검증 계약','selected'),
 ('R7','R','src/domain/reconstructionCoverage.test.ts','keeps an incomplete inventory','등록 검사 통과와 완전성의 구분','selected'),
 ('R8','R','src/domain/reconstructionCoverageEvidence.ts','hasComparableEvidence','해당 판정이 인용한 증거의 자격','full'),
 ('R9','R','src/domain/reconstructionCoverageVerifierResults.ts','latestVerifierObservationsByVerifier','최신 판정 묶음과 충돌','full'),
 ('R10','R','src/domain/reconstructionVerificationSchemas.ts','const reconstructionClaimSchema','기존 재현 검사 유형의 범위','selected'),
 ('R11','R','src/application/binary/AnalysisSnapshotCache.ts','isSnapshotCacheable','재사용 조건과 상태성 작업 제외','selected'),
 ('R12','R','src/browser/PngVisualDiff.ts','Pixel comparison does not','정지 픽셀 비교의 한계','selected'),
 ('R13','R','src/browser/PlaywrightScenarioArtifacts.ts','animations: "disabled"','브라우저 캡처의 모션 제한','full'),
 ('R14','R','scripts/generate-skill-metadata.mjs','pinnedSpecifier','배포 지침과 실제 도구 판본 동기화','full'),
 ('R15','R','docs/reconstruction-obligation-ledgers.md','A required','의무·구현 담당·사례·검증 연결','full'),
 ('T1','T','plugins/audit-context-building/skills/audit-context-building/SKILL.md','follow the calls','이해 단계와 평가 단계 분리','full'),
 ('T2','T','plugins/audit-context-building/workflows/audit-context.js','const RECORD_SCHEMA','구조화 반환·예산·실패 필터링','selected'),
 ('T3','T','plugins/audit-context-building/evals/continuity-across-calls/graders/unbounded-length-path.md','Pass only','핵심 실패를 분별하는 평가 조건','full'),
 ('S1','S','skills/writing-skills/SKILL.md','Match the Form to the Failure','실패 종류에 맞는 지침 형태','selected'),
 ('S2','S','skills/verification-before-completion/SKILL.md','The Gate Function','완료 주장과 검증 근거 연결','selected'),
 ('I1','I','skill/SKILL.src.md','## Modes','장면 목적별 판단과 기존 맥락','selected'),
 ('I2','I','skill/reference/critique.md','### Hard Invariants','판단·검출의 격리와 한계 공개','selected'),
 ('I3','I','skill/reference/animate.md','## Set the motion thesis','모션 목적의 사전 명세','full'),
 ('I4','I','crates/context/src/critique_storage.rs','fn fingerprint_target','검수 대상의 실제 파일 지문','selected'),
 ('I5','I','crates/detect/tests/regex_only_note.rs','zero_finding_source_scan','미실행 검사와 무결점의 구분','selected'),
 ('G1','G','plan-design-review/SKILL.md','## The 0-10 Rating Method','설계 결함·대안·재평가','selected'),
 ('G2','G','plan-design-review/sections/review-sections.md','### Pass 2','상태 표와 검수 차원','selected'),
 ('A1','A','skills/skill-creator/agents/grader.md','### Step 4','사전 기준 밖 주장과 평가기 검토','selected'),
 ('A2','A','skills/skill-creator/scripts/aggregate_benchmark.py','metrics.get("output_chars"','누락값과 지표 대체 경로','selected'),
 ('M1','M','skills/engineering/domain-modeling/SKILL.md','### Offer ADRs sparingly','용어와 중요한 결정의 기록','full'),
 ('E1','E','skills/continuous-learning-v2/SKILL.md','## The Instinct Model','작은 규칙 후보·프로젝트 범위','selected'),
 ('E2','E','skills/continuous-learning-v2/scripts/instinct-cli.py','PROMOTE_CONFIDENCE_THRESHOLD','점수·프로젝트 수 기반 승격 경로','selected'),
 ('V1','V','skills/react-best-practices/rules/async-defer-await.md','impactDescription','조건·영향·예/반례를 묶은 규칙','full'),
 ('V2','V','packages/react-best-practices-build/src/validate.ts','!hasBad && !hasGood','문서 요구와 검사 조건의 차이','selected'),
]

audit=[]
for sid,key,rel,needle,why,scope in SOURCES:
    repo,commit,base=REPOS[key]
    p=base/rel
    raw=p.read_bytes()
    lines=raw.decode('utf-8-sig').splitlines()
    anchors=[i+1 for i,line in enumerate(lines) if needle in line]
    assert anchors, (sid,needle)
    audit.append(dict(id=sid,repository=repo,commit=commit,path=rel,local_path=str(p),sha256=sha256(raw).hexdigest(),line_count=len(lines),anchor_lines=anchors,review_scope=scope,finding=why,url=f'https://github.com/{repo}/blob/{commit}/{rel}#L{anchors[0]}'))
(ROOT/'source-audit.json').write_text(json.dumps({'method':'Static source inspection only. No third-party code, test suite, model benchmark or video analysis was executed. Selected means selected sections, not whole-file or whole-repository audit.','records':audit},ensure_ascii=False,indent=2),encoding='utf-8')
index_rows=''.join(f'<tr><td>{x["id"]}</td><td>{html.escape(x["repository"])}</td><td><a href="{html.escape(x["url"],quote=True)}">{html.escape(x["path"])}</a><br>고정 커밋 {x["commit"][:12]} · {x["anchor_lines"][0]}행</td><td>{html.escape(x["finding"])}</td><td>{x["review_scope"]}</td></tr>' for x in audit)
index_html='<!doctype html><html lang="ko"><meta charset="utf-8"><title>원본 코드 조사 근거</title><style>body{font:15px/1.6 system-ui,sans-serif;max-width:1300px;margin:40px auto;padding:0 24px;color:#18273a}h1{font-size:27px}table{border-collapse:collapse;width:100%}th,td{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid #d8e1eb}th{background:#18273a;color:white}a{color:#245aba;overflow-wrap:anywhere}tr:nth-child(even){background:#f1f5f9}</style><h1>GitHub 원본 코드 조사 근거</h1><p>2026-10-19 · 저장소 10개 · 근거 파일 41개. 링크는 조사한 고정 커밋을 가리킵니다. full은 파일 전체, selected는 해당 구간 열람이며 저장소 전수감사를 뜻하지 않습니다. 외부 코드와 테스트는 실행하지 않았습니다.</p><table><thead><tr><th>ID</th><th>저장소</th><th>원본 파일</th><th>확인한 구조</th><th>열람 범위</th></tr></thead><tbody>'+index_rows+'</tbody></table></html>'
(ROOT/'source-index.html').write_text(index_html,encoding='utf-8')

chapters=[]
def chapter(title, blocks): chapters.append({'title':title,'blocks':blocks})
def p(text): return {'kind':'p','text':text}
def h(text): return {'kind':'h','text':text}
def tab(headers,rows,widths=None): return {'kind':'table','headers':headers,'rows':rows,'widths':widths}

chapter('판단 절차와 근거 관리부터 가져온다',[
 p('첨부 텍스트와 공유 대화 3개를 모두 읽고, GitHub 원본 10개 저장소의 고정 커밋에서 관련 지침·실행 코드·테스트를 조사했다. 우선 적용할 것은 REA의 요구 항목과 근거 연결, Superpowers의 실패별 출력 설계, Trail of Bits의 가정 추적이다. Ponytail의 최적화 판단은 이 정확성 기반 위에 놓는다.'),
 p('현재 company-video-grammar-analyzer는 draft.3이며 A5b 중대 오류로 종료·보존 상태다. 이번 조사는 변경 제안이다. 스킬 수정, A5b 재개, A6·01-B·02 착수, 설치·훅 활성화는 수행하지 않았다.'),
 tab(['시점','차용할 구조','기대하는 변화'],[
 ['분석 스킬 보완','대상×속성×구간의 필수 기록, 원자 주장, 미해결 장부','알고도 빠뜨린 기록과 미검토를 드러냄'],
 ['분석 검증','원본에서 발견할 목록과 출력 주장 목록을 별도로 대조','잘못 본 것과 잘못 쓴 것을 분리'],
 ['01-B','조건·반례·근거 수준·승인 범위가 있는 사례 색인','겉모양이 비슷하다는 이유의 재사용 감소'],
 ['02 및 제작 검증','장면 목적·표현 대안·구현 선택·실제 렌더·수정 과제','재현 가능성과 새 내용 적용성을 따로 입증']],[.18,.43,.39]),
 h('이번 조사로 바뀐 판단'),
 p('앞선 답변의 큰 방향은 유효하다. 다만 여러 스킬을 합치면 전문가 판단이 이식된다는 해석은 과하다. 실제 구현은 작업 순서, 판단 입력, 필수 기록, 검증 조건을 유도하거나 검사한다. 영상 인식 능력과 좋은 디자인 선택은 별도 실증이 필요하다.'),
 p('REA의 장부는 등록된 요구의 누락을 찾아낸다. 대상 자체가 요구 목록에서 빠지면 장부만으로 발견할 수 없다. A를 4로 읽은 오인식도 observed라는 표식이나 파일 해시만으로 교정되지 않는다. 이 한계가 이번 적용 설계의 출발점이다. [R1,R6,R7]'),
])

chapter('조사 범위와 고정한 원본',[
 p('2026-10-19 한국시간 기준 조사. Ponytail·REA와 추가 6개는 소스 ZIP을 보존했다. Impeccable은 관련 13파일, Trail of Bits는 audit-context-building 관련 37파일을 원본 커밋에서 선택 다운로드했다. 저장소 전체를 내려받은 경우에도 전체 코드를 전수 감사한 것은 아니다. 파일별 열람 범위·행·SHA-256은 source-audit.json에 있다.'),
 tab(['대상','고정 커밋 앞 12자리','관심도: 스타 / 포크'],[
 ['Ponytail','09c434ab73ca','167,043 / 9,068'],['REA','95c8f57aa2ea','322,053 / 81,614'],
 ['Impeccable','2f46b7a8b059','82,716 / 4,994'],['Trail of Bits','5c99c03fb8a9','7,634 / 660'],
 ['Superpowers','bb92a7774141','약 301.6k / 26.9k'],['Matt Pocock Skills','49dd158d1076','약 296.2k / 24.9k'],
 ['gstack','8640ab4ff43a','약 136.8k / 20.3k'],['Anthropic Skills','dbd4588f9e10','약 182.0k / 21.6k'],
 ['ECC','76aaa77df6ad','약 283.2k / 42.1k'],['Vercel Agent Skills','063bee94c3f4','약 32.6k / 2.8k']],[.34,.30,.36]),
 p('정확 수치 4개는 GitHub API, 약수치 6개는 저장소 공개 페이지 표시값이다. 수집 시각과 반올림이 달라 순위 비교에 쓰지 않는다. 스타·포크는 관심과 채택의 단서이며 개별 스킬 성능 점수가 아니다. API 비로그인 조회 한도 이후에는 git ls-remote로 커밋을 확인하고 고정 ZIP을 받았다.'),
 p('Ponytail 패키지는 5.3.2. REA 패키지는 현재 6.7.0이며 공유 답변의 6.5.0/18aa9af2 이후 37커밋·214변경 파일을 비교했다. 주요 증거·완료 판정 구조는 현행 원본에서 다시 확인했다. 영상 기능 제안 #3609는 조회 시 open, 댓글 0, 담당자 없음이었다.'),
 p('실행하지 않은 것: 내려받은 훅·실행기·전체 테스트·외부 분석 엔진·모델 벤치마크·AE 재구현. 테스트 소스의 존재와 실제 통과를 구분했다. 추가 대화의 나머지 후보(Agency Agents 등)는 이번 심층 원본 검토 10개에 포함하지 않았다.'),
])

chapter('Ponytail: 무엇을 줄이고 무엇을 보존하는가',[
 h('판단 사다리는 충분조건을 통과한 뒤 선택한다'),
 p('SKILL.md는 관련 코드와 호출부·테스트·설정을 먼저 읽고 변경 범위를 잡게 한다. 그 뒤 기존 구현, 플랫폼, 설치된 의존성, 작은 새 구현 순서에서 과제를 완전히 해결하는 첫 선택을 고른다. 핵심 조건은 완전한 해결이다. 영상에서는 관찰 사실·필수 문구·정보 관계·요청 범위를 보존한 뒤 중복 설명과 불필요한 정밀 측정을 줄이는 방식으로 바꿔야 한다. [P1]'),
 tab(['원본 코드에서 확인','우리에게 유용한 것','그대로 옮길 때의 문제'],[
 ['map: 경량 식별자 색인','사례 요약→필요한 근거 상세 조회','정규식은 의미·모션·적용 조건을 모름'],
 ['review: 구체적인 실패 상황 요구','원본 시점·대상·잘못된 결과가 있는 검수 의견','취향을 관측 오답으로 판정하면 안 됨'],
 ['debt: 한계와 재검토 조건 기록','정밀 측정 생략 이유와 다시 볼 조건','미검토를 확인 완료처럼 닫으면 안 됨'],
 ['activate: 규칙과 색인 전달','작은 공통 원칙과 필요한 참조의 분리','세션 전체 자동 적용은 현재 시험 조건을 오염시킴']],[.29,.36,.35]),
 h('색인기의 직접 이식은 부적합하다'),
 p('ponytail-map.js는 git ls-files 또는 제한 디렉터리 탐색 뒤 소스 확장자·정규식으로 함수/클래스 이름을 찾는다. 기본 예산은 약 2,000자이고 파일 상한은 4,000개다. SAFE_PATH의 문자 집합은 한글 하위 경로를 포함하지 않는다. MP4·근거 JSON도 이 소스 색인의 대상이 아니다. 영상용 색인은 기존 사례 ID와 기록 메타데이터로 별도 작성해야 한다. [P2]'),
 p('현행 활성화 훅의 색인 실행 제한은 3초다. 실패하면 색인 없이 규칙을 전달한다. 첨부의 약 1초 설명은 현행 코드와 다르다. 이 실패 허용 방식은 선택적 색인에는 적합하지만 필수 원본·근거 검증 실패까지 통과시키는 규칙으로 확대하면 안 된다. [P3]'),
 h('효과 수치는 가져오지 않는다'),
 p('제작자 39과제·3조건·5반복 실험의 숨은 실행 검사는 18과제에만 있다. 나머지 21과제는 별도 AI 완성도 판단을 사용한다. 테스트가 있는 실행에서 주입 결함 검출률은 기본보다 항상 높지 않다. 코드량·시간 절감 결과를 영상 관측 정확도나 디자이너 공수 절감으로 환산할 수 없다. 과거 기준선이 훅에 오염됐다는 수정 이력은 우리 조건 격리에도 참고할 만하다. [P6,P7]'),
])

chapter('REA: 증거와 미해결 상태를 실행 규칙으로 만든다',[
 h('증거의 내용과 출처를 함께 묶는다'),
 p('Evidence는 대상 해시, provider, analysis_profile, 작업·설정, raw/normalized 결과, 관측 유형, authority, 환경, 한계, 근거 위치를 묶는다. ID는 의미 내용으로 계산하고 표시 경로·이름은 의미 해시에서 뺀다. 같은 내용의 저장 위치가 바뀌어도 의미 정체성을 유지하는 발상은 C:/D: 근거 연결 문제에 유용하다. 다만 현행 주소·파일 오프셋 위치 형식에는 영상의 실제 표시시각·ROI·부모 변환을 추가해야 한다. [R1]'),
 h('미해결 질문은 이유와 다음 확인을 보존한다'),
 p('ResidualUnknown은 질문·scope·현재 상태·지지/반대 근거·필요한 증거 유형·환경·다음 조사·판본을 갖는다. updateUnknown은 expected_revision이 현재 판본과 다르면 거부한다. 종료 상태에는 verified 외에 withdrawn/out-of-scope가 있어, 처리 종료와 사실 입증을 분리한다. [R2,R3]'),
 p('evidenceBundle.ts는 해소 근거가 지지 목록에 있는지와 유형·authority·환경 요구를 확인한다. 실제 테스트는 관측을 요구한 질문을 inferred 근거만으로 닫으려는 갱신을 거부하고 관측 근거를 추가한 갱신을 허용한다. 우리도 알려진 사실은 보존하고 정확한 AE 구현만 미상으로 남기는 식으로 쟁점을 작게 나눠야 한다. [R4,R5]'),
 h('형식 검사가 진실성을 판정하지는 않는다'),
 p('Evidence 생성의 기본 confidence는 observed다. 따라서 해당 필드가 채워졌다는 이유로 시각적 사실이 확인됐다고 할 수 없다. 타입과 해시는 레코드의 일관성을 확인하며, A를 4로 읽었는지는 판독 근거 대조가 필요하다. 영상용 설계는 관측/계산/추론의 종류, 내용 검수 여부, 사람 확인·회사 승인 범위를 각각 분리해야 한다. [R1,R8]'),
 h('재사용은 원본과 설정이 맞을 때만'),
 p('AnalysisSnapshotCache는 대상·분석 profile이 바뀌면 캐시를 비우고, 현재 UI 상태나 변경을 일으키는 작업은 재사용 대상에서 제외한다. 영상에서는 원본/추출 설정/실제시각 매핑/관측 판본/검수 판본별 재사용 가능 범위를 정하면 된다. 이것이 이미 본 프레임을 다시 디코딩하는 비용과 새 내용 검수 비용을 구분하는 기반이다. [R11]'),
])

chapter('REA: 등록 검사 통과와 전체 누락 해소를 구분한다',[
 p('reconstructionCoverage는 boundary에 required_surface_ids와 required_claim_ids를 명시하고 구현 담당·검증 차원·계약 해시·결과·잔여 미해결을 대조한다. 일부 검사만 통과해도 미충족 사유가 남으면 ready가 되지 않는다. 의무 장부는 원본 근거→필요한 사례→구현 담당→검증 결과를 연결한다. [R6,R15]'),
 h('테스트가 실제로 보여주는 경계'),
 p('reconstructionCoverage.test.ts의 누락 사례는 boundary에 cli.help와 cli.version을 요구하고 실제 inventory에는 하나만 둔다. 등록된 검사가 모두 통과해도 surface-missing으로 partial을 기대한다. 하지만 boundary 자체에 cli.version을 쓰지 않았다면 이 비교만으로는 발견되지 않는다. 영상의 카드 5개 중 1개가 최초 대상 목록부터 빠진 경우도 마찬가지다. [R7]'),
 tab(['우리에 필요한 별도 검사','무엇과 대조하는가','장부만으로 해결 가능한가'],[
 ['대상 발견 검수','원본 전체/내부/주변·정착 역추적','아니오: 시각 관찰 필요'],
 ['관찰→기록 누락','발견 목록 × 변화 속성 × 구간 ↔ 주장','상당 부분 구조화 가능'],
 ['내용 오답','원자 주장 ↔ 해당 원본 ROI·시간 표본','아니오: 의미 판독 필요'],
 ['근거 연결 오류','해시·실제 시각·ROI·부모 변환','코드 검사 가능'],
 ['표본 밖 전체 성공 주장','선언 범위 ↔ 실제 검수 범위','완료 규칙으로 차단 가능']],[.26,.47,.27]),
 p('검증 결과는 단순히 가장 좋은 이전 결과를 고르지 않는다. 최신 시각의 결과 묶음을 고르고, 같은 최신 시점에 충돌하는 판정이 있으면 불확실성을 유지한다. 우리에게 필요한 것은 과거 합격과 최신 실패를 모두 보존하면서 적용 대상 판본을 명시하는 것이다. [R9]'),
 h('영상 엔진으로는 바로 쓸 수 없다'),
 p('verify_reconstruction의 타입은 behavioral/structural-function/structural-artifact 중심이다. 임의 MP4의 대상·모션·AE 편집성을 판정하는 타입이나 실행기가 아니다. 조사한 src/bridge/scripts/package 범위에서 영상 분해·AE 생성 구현은 확인하지 못했다. PNG 비교는 OCR·의미 레이아웃을 하지 않으며 브라우저 시나리오 캡처는 animations를 disabled로 지정한다. 정지 UI 검사를 모션 검사로 전용하면 중요한 변화를 제거할 수 있다. [R10,R12,R13]'),
])

chapter('Trail of Bits와 Superpowers: 누락이 나는 과정을 바꾼다',[
 h('Trail of Bits: 하위 근거까지 연결해서 읽는다'),
 p('audit-context-building은 이해 단계에서 취약점 판정·수정 제안을 하지 않도록 분리한다. 중요한 원리는 함수 이름이나 상위 계약을 믿지 말고 실제 호출 경로와 분기까지 읽어 전제가 어디에서 성립하는지 기록하는 것이다. 영상으로 옮기면 외곽 패널 정착을 내부 UI 정지로 확장하지 않고, 대상·내부·주변의 변화가 어느 근거에서 확인됐는지 각각 연결한다. [T1]'),
 p('실제 audit-context.js는 Orient→Analyze→Synthesize를 실행하고 JSON schema의 필수 invariants/assumptions/calls/openQuestions를 받는다. 긴 분석은 파일에 저장하고 compact record를 통합한다. 단순한 시니어 페르소나보다 실행 구조가 구체적이다. 코드의 기본 분석 상한과 중요도 선택은 정밀 관찰 자원 배분에 참고할 수 있다. 필수 항목은 예산 때문에 조용히 제거하지 않아야 한다. [T2]'),
 p('주의할 구현: 선택한 작업의 결과에 filter(Boolean)을 적용하고, 최종 notAnalyzed는 상한 아래로 잘린 후보만 나열한다. 선택됐지만 결과가 없는 작업은 별도 실패 행으로 보존하는 영상용 설계가 필요하다. 이는 정적 읽기에서 확인한 이식 시 주의점이며 원본 전체 워크플로의 실행 실패를 재현한 결과는 아니다. [T2]'),
 p('continuity 평가기는 두 단계 아래의 특정 분기에서 한계 검사가 빠진 사실을 연결했을 때만 통과시킨다. 함수명을 나열하거나 다른 참인 내용을 많이 쓰는 답변은 통과하지 못한다. A5에서도 위치 감속 설명이 크기 감속을 대신하지 못하도록 속성별 성공 조건을 분리하는 데 직접 참고할 수 있다. [T3]'),
 h('Superpowers: 실패 유형에 맞게 지침의 형태를 고른다'),
 tab(['실패','원본의 설계 권고','우리 적용'],[
 ['규칙을 알지만 압박에서 생략','금지·위반 신호·압박 시험','관측 과정 로그가 있어야 이 유형 판정'],
 ['출력에 필요한 내용이 빠짐','필수 슬롯/정해진 출력 계약','속성마다 기록 또는 미검토 사유'],
 ['조건에 따라 달라져야 함','관측 가능한 조건으로 분기','가림·표본 부족·비적용을 구분'],
 ['출력 모양이 목적에 안 맞음','긍정적인 출력 구성 규정','원자 주장 목록→간결한 요약']],[.27,.37,.36]),
 p('writing-skills는 기계적으로 검사할 수 있는 제약을 자동화하고, 실제 실패와 대조해 표현을 시험하라고 한다. 그러나 지각 오인식을 단순한 규칙 위반으로 취급해서는 안 된다. verification-before-completion의 명령 출력 확인만으로도 영상 사실은 입증되지 않는다. 적절한 내용 검수 결과를 완료 근거로 연결해야 한다. [S1,S2]'),
])

chapter('Impeccable와 gstack: 디자이너 판단의 입력을 명시한다',[
 h('Impeccable: 제품 장르보다 이 화면의 목적을 먼저'),
 p('핵심 스킬은 Persuade/Operate/Read/Experience를 제품 전체가 아니라 해당 surface의 성공 조건으로 선택한다. 영상에는 장면마다 이해시킬 관계, 주의를 옮길 대상, 남겨야 할 맥락을 정하는 방식으로 옮길 수 있다. 분석 단계에서는 실제 전달 효과나 원제작 의도로 단정하지 않고 해석 후보로 남긴다. 새 기획 단계에서는 브리프와 연결된 선택 기준이 된다. [I1]'),
 p('animate.md는 focal moment, continuity, feedback, budget을 먼저 쓰게 한다. 이는 모션 이름을 고르기 전에 역할을 정하는 좋은 예다. 반면 웹 상호작용용 밀리초 표, CSS/WAAPI 선택, 기본 감속과 퇴장 규칙은 사내 렌더 영상의 관측 정답이나 필수 표현 규칙으로 복사하지 않는다. [I3]'),
 h('검수의 독립성과 실제 대상 판본'),
 p('critique는 디자인 판단 A와 검출/브라우저 근거 B의 결과를 서로 보여주지 않고 합성하도록 명시한다. 이것은 편향을 줄이기 위한 절차이며 두 검수자가 모두 틀리지 않는다는 보장은 아니다. Rust critique_storage는 호출자가 준 지문 대신 실제 로컬 파일 바이트의 SHA-256을 기록하고 이후 파일 변화 여부를 비교한다. 검수와 수정 대상의 판본을 결합하는 구현을 참고할 수 있다. [I2,I4]'),
 p('regex_only_note 테스트는 소스 텍스트 검사에서 0건이 나와도 HTML/DOM을 필요로 하는 규칙이 실행되지 않았음을 알리도록 한다. 영상에서도 JSON 검사 통과·OCR 미실행·모션 미검토를 각각 보고해야 한다. 검출기 미실행을 무결점으로 닫지 않는 방식이 유용하다. [I5]'),
 h('gstack: 추상적 취향을 구체적인 결함·대안으로'),
 p('plan-design-review는 차원별 점수, 점수가 낮은 구체 이유, 개선안, 반영 후 재평가를 요구한다. 별도 review-sections에는 정보 위계·상태 범위·여정 등의 표가 있다. 영상용 질문으로 바꾸면 첫 시선/다음 시선, 등장 전·변화 중·유지·퇴장, 긴 문구·요소 수·화면비 변경 때의 실패 조건을 명세할 수 있다. [G1,G2]'),
 p('그러나 0-10점은 전문가 판단을 설명하는 보조 장치다. 원본 인식 정확도, 회사 승인, 이해도 실험 점수와 같은 숫자로 합치지 않는다. 원본의 반복적인 개별 승인·웹 금지 스타일·10점까지 반복하는 운영 흐름은 우리에게 그대로 적용하지 않는다. 현재 1,000줄이 넘는 진입 문서에는 호스트·질문·도구 운영 규칙도 많이 섞여 있으므로 필요한 판단 단위만 선별한다.'),
])

chapter('나머지 네 후보: 기존 기반과 겹치는 부분을 선별한다',[
 tab(['후보','실제 파일에서 가져올 부분','적용 범위와 제한'],[
 ['Anthropic Skill Creator','사전 기대값 외 주장 검증, 평가 기준 자체 비평','A3부터 쓰던 기반을 보강. 도입 자체를 새 해결책으로 세지 않음'],
 ['Matt Domain Modeling','충돌하는 용어를 구체 사례로 정리, 중요한 결정의 이유','Phase 00 ID·용어사전에 연결. 별도 사전을 새 정본으로 만들지 않음'],
 ['ECC Continuous Learning','한 트리거·한 행동의 작은 후보, 프로젝트 범위와 근거','사람 피드백에서 규칙 후보만 추출. 자동 회사규칙 승격은 보류'],
 ['Vercel 규칙 체계','영향도·적용 조건·이유·예/반례','R7 검수 항목을 간결한 규칙 카드로 정리. React 규칙 자체는 전용하지 않음']],[.26,.36,.38]),
 h('Anthropic 집계기를 그대로 쓰면 지표 계약이 깨진다'),
 p('aggregate_benchmark.py는 grading이 없는 실행을 건너뛰고, 누락 시간값의 기본을 0으로 두며, tokens가 없으면 output_chars를 tokens 필드에 넣는 경로가 있다. A5의 미계측=null 원칙과 다르다. 우리 집계는 계획/착수/완료/중단을 모두 명시하고 actual_tokens와 output_chars를 별도 필드로 유지해야 한다. 주장 전수 검수 여부도 pass_rate와 분리한다. [A1,A2]'),
 h('ECC의 신뢰도는 회사 규칙의 입증 정도가 아니다'),
 p('instinct-cli.py에는 프로젝트 2개 이상, 평균 confidence 0.8 이상을 후보 조건으로 쓰는 promote 경로가 있다. 이는 도구의 휴리스틱이며 통계적으로 보정된 정확도나 회사 승인이라는 근거가 아니다. 같은 AI 오판이 반복될 수 있으므로 확인된 사용자 정정과 AI 제안을 분리하고 반례 시험·승인 범위를 거쳐야 한다. 자동 훅으로 모든 작업을 학습시키는 방식을 지금 연결하지 않는다. [E1,E2]'),
 h('문서상 필수 조건과 검사 구현도 비교해야 한다'),
 p('Vercel validate.ts는 좋은/나쁜 코드 예시 여부를 계산하지만, 오류 조건 !hasBad && !hasGood은 둘 다 없을 때만 참이다. 한 종류 예시만 있어도 이 분기는 오류를 내지 않는다. 예/반례 형식을 참고하더라도 우리 검증기는 실제 요구를 검사하는지 확인해야 한다. 스키마가 있다는 사실과 모든 의미 제약을 검사한다는 사실은 다르다. [V1,V2]'),
 p('Matt의 ADR 기준은 되돌리기 어렵고, 맥락 없이 의외이며, 실제 대안 간 선택이 있었을 때다. 모든 프레임에 결정 문서를 만들 필요는 없다. 영상 관측 사실과 새 제작에서 선택한 구현 방법은 별도 기록하되, 중요한 공통 선택의 이유만 오래 유지한다. [M1]'),
])

chapter('현재 A5b 실패에 무엇이 직접 도움이 되는가',[
 tab(['확인된 실패/한계','새로 넣을 실행 구조','남는 검증 과제'],[
 ['큰 A를 숫자 4로 확정','대상 ID와 형태 관측을 먼저 저장. 정체 주장에 구별 특징과 원본 ROI 연결','대상 재판독이 실제 오인식을 줄이는지 확인'],
 ['위치 감속 기록, 크기 감속 누락','같은 사건을 position/size별 행으로 분리. 각각 변화·근거·가감속·검토 상태','서로 다른 속성 곡선을 구분하는 회귀'],
 ['관측 가능한 변화까지 기권','미확정 원인과 다음 확인 수단, 확보한 표본 범위를 기록','판독 가능 여부를 출력과 독립적으로 채점'],
 ['사선 3개를 2개로 읽음. 첫 검수도 놓침','개수 주장을 분리하고 원본 크기 ROI에서 재대조','검수자와 검수 조건의 결함 검출 시험'],
 ['전체 precision 분모 미확정','중복 없는 주장 목록을 출력과 함께 고정. 추가 주장도 검수 대상','주장을 적게 써 누락을 숨기지 않는 별도 포괄성 검사'],
 ['봤지만 누락/처음 못 봄 구별 불가','최초 대상 목록·열람 근거·기록 시점·후속 발견 이력을 보존','당시 기록 없으면 원인 미상 유지']],[.29,.43,.28]),
 h('이미 있는 지침과 신규 구조를 구분한다'),
 p('draft.3에는 주변/내부 관찰, 역추적, 속성별 가감속, 주장·근거 역대조가 이미 있다. 신규 가치는 이 지침들을 필수 산출 단위와 검사 가능한 연결로 바꾸는 데 있다. 같은 지침을 더 강조하는 문장만 추가하면 실행 개선이 입증되지 않는다.'),
 p('현재 출력은 properties 배열과 하나의 easing 객체를 사건 안에 둘 수 있고 coverage가 자유 서술이다. 모든 변화 속성이 각각 닫혔는지 검사하기 어렵다. 기존 JSON은 보존하고 새 schema_version에서 속성별 관찰 행과 주장 ID를 제안한다. 정밀 수치는 쟁점을 해결할 때만 요구한다.'),
 p('본 표는 과거 실패 원인을 확정한 재채점이 아니다. 동일한 문제를 다음 판본에서 어떻게 검사할지에 대한 설계 제안이다. A5b 점수와 기존 사용자 확인 범위는 바뀌지 않는다.'),
])

chapter('제안 출력: 사실·상태·승인을 한 칸에 섞지 않는다',[
 p('한 status 필드에 관측 여부·확신·검수 완료·승인 상태를 모두 넣지 않는다. 아래는 설계 제안이며 실제 출력이나 현재 스킬이 지원하는 스키마가 아니다. 함께 저장한 proposed-record-example.json도 합성 예시다.'),
 tab(['축','예시 내용','이 축이 입증하지 않는 것'],[
 ['대상 식별','object_id, shape_description, identity 후보·확인 근거','객체 ID를 붙였다는 사실이 정체의 정답은 아님'],
 ['관찰 범위','구간·주변/내부 ROI·열람 표본·변화 속성','표본 사이 전체프레임을 봤다는 뜻은 아님'],
 ['근거 종류','observed / derived / inferred + 원자료 연결','사람 검수·회사 승인과 다름'],
 ['작업 상태','not_reviewed / reviewed / blocked + 사유','reviewed가 내용 정답이라는 뜻은 아님'],
 ['내용 판정','unverified / supported / contradicted / unresolved','검수 안 한 나머지 주장까지 합격시키지 않음'],
 ['승인 범위','승인 주체·주장 ID·자료·판본·적용 범위','AI 반복 발견을 사람 승인으로 바꾸지 않음']],[.23,.40,.37]),
 h('최소한 필요한 연결'),
 p('원본/실제시각/ROI → 관찰 행 → 원자 주장 → 내용 검수 결과를 연결한다. 별도로 발견된 대상·변화의 목록을 주장 목록과 대조해 기록 누락을 찾는다. 이후 재현을 할 때만 주장 → 제작 요구 → 구현 선택 → 실제 렌더/프로젝트 검수 연결을 확장한다.'),
 p('한 개의 관찰 행에는 대상 하나와 속성 하나를 두되, 같은 표본을 여러 행에서 참조할 수 있다. 확인 가능한 방향과 순서는 보존하고 가감속만 미확정으로 둘 수 있다. 변화 없음과 해당 없음은 확인 범위를 갖게 한다. 발견 못함은 후속 검수가 새로 찾았을 때 당시 목록과 비교해 기록한다.'),
 h('완료 검사는 두 종류'),
 p('구조 검사는 누락 필드·해시/시간/ROI 불일치·고아 주장·미검토 행을 찾는다. 내용 검수는 원본을 보고 대상 식별·개수·변화·순서·가감속을 판단한다. 두 결과를 따로 저장한다. source hash 일치나 파일 열람 기록만으로 사람이 그 내용을 정확히 이해했다는 결론을 만들지 않는다.'),
])

chapter('분해에서 재현·재사용으로 넘어가는 경계',[
 p('REA 공유 답변의 재현 루프는 후속 제작 검증에 유용하다. 그러나 지금의 A5 분석 종료 조건을 AE 재구현까지 자동 확대하지 않는다. 분석 정확도, 원본의 외형 재현, 편집 가능성, 다른 내용에 대한 재사용, 전달 적합성을 각각 평가한다.'),
 tab(['단계','남기는 자산','다음 단계로 넘기는 한계'],[
 ['관측','대상·문구·관계·시간 변화·원본 근거','원제작 의도와 정확한 AE 설정은 미상 가능'],
 ['제작 명세','관측 조건과 필요한 편집 요구','동일 화면을 만드는 복수 구현 허용'],
 ['구현 선택','텍스트/도형/그룹/효과 등 우리가 택한 방식','원래 제작자가 같은 방식을 썼다는 증거가 아님'],
 ['원본 재현 검증','특정 구간·대상·속성의 외형과 시간 조건','시작/끝만 맞아 중간도 맞는다고 하지 않음'],
 ['수정·전용 시험','문구 길이·요소 수·강조 대상·화면비 변경','확인한 입력 범위 밖으로 일반화하지 않음'],
 ['문법 후보·승인','적용 목적·조건·반례·근거·판본·승인 범위','재현 성공만으로 좋은 표현·회사 공통 규칙이 되지 않음']],[.23,.39,.38]),
 p('AE 제작기를 추가 개발할 때는 확정된 작은 명세로 제작·상태 읽기·렌더를 먼저 검사하는 제안이 타당하다. 이는 제작 계층의 검증 순서다. 이미 진행한 분석 개발을 되돌리거나 AEP가 없는 기존 MP4 분석을 반려하는 이유로 쓰지 않는다.'),
 p('Motion Vectorization 연구는 객체 외관과 시간별 변환을 분리하는 중간 표현이 참고점이다. 공개 README는 긴/복잡한 영상의 시간 비용과 Program Transformation 공개 범위의 제한을 남긴다. MoVer는 구조화된 SVG/GSAP 애니메이션의 공간·시간 조건을 검사하는 참고 사례다. 둘 다 임의 사내 MP4에서 편집 가능한 AE 레이어를 자동 복원하는 준비된 대체 엔진으로 채택하지 않는다.'),
 p('특히 검증 조건을 분석기와 제작기가 같은 오판에서 만들면, A를 4로 읽은 뒤 4를 잘 재현해도 통과할 수 있다. 관측 내용 검수는 원본에 독립적으로 연결하고, 재현 합격이 원본 해석의 진실성을 대신하지 않게 한다.'),
])

chapter('전문가의 판단을 실제 선택 규칙으로 표현한다',[
 h('사례를 많이 읽히는 것보다 선택 근거를 좁힌다'),
 p('장면의 메시지·정보 관계·시청 조건·필수 문구·제작 제약을 먼저 고정한다. 경량 색인으로 후보를 찾고 해당 사례의 원본 근거·적용 조건·반례만 상세 조회한다. 장르명이나 외형 태그만으로 선택하지 않는다. 검색 결과가 없거나 조건에 맞지 않으면 그 사실을 남긴다.'),
 tab(['판단 질문','필수 기록','통과의 근거'],[
 ['왜 이 표현인가','전달할 관계, 선택한 안, 제외한 대안과 이유','브리프·정보 관계와 구체적으로 연결'],
 ['무엇을 줄일 수 있나','보호할 사실/가독성/관계, 선택적 장식·정밀 측정','필수 조건 충족을 먼저 확인'],
 ['언제 쓰면 안 되나','긴 문구·요소 수·동시성·화면비 등의 반례','조건 변경 시험 또는 명시한 미검증'],
 ['무엇이 이미 검증됐나','사례/스킬/도구/출력/검수 판본과 정확한 범위','같은 이름의 옛 결과를 혼용하지 않음'],
 ['무엇이 아직 가설인가','원제작 의도·가능한 구현·전달 효과','새 관찰과 사람 확인을 분리']],[.25,.42,.33]),
 h('Ponytail식 선택 사다리를 영상용으로 바꾸면'),
 p('① 필수 내용과 이해 조건을 확인한다. ② 조건에 맞는 검증된 회사 사례가 있는지 본다. ③ 작은 변형으로 성립하는지 시험한다. ④ 기존 제작 기능으로 구현한다. ⑤ 필요한 새 표현만 탐색한다. 각 단계에서 조건을 못 맞추면 다음 선택으로 넘어간다. 기존 사례가 있다는 이유로 부적합한 형식을 강제하지 않는다.'),
 p('후보 개수나 화면 요소 수의 최소화 자체를 목표로 삼지 않는다. 과밀한 설명을 분할하는 추가 장면이나 관계를 보여주는 움직임이 이해에 필요할 수 있다. 품질 조건 안에서 제작·수정·검수의 전체 공수를 줄이는 것이 최적화 대상이다.'),
 h('지식·관측·판단의 저장 책임'),
 p('Phase 00은 용어와 원칙의 기반으로 유지한다. 01-A는 근거 있는 관측을 만든다. 01-B는 사례의 사용 조건·반례와 문법 후보를 정리한다. 02는 새 브리프의 대안과 선택을 검증한다. 이 책임을 분리하면 외부 전문가의 취향이 기존 영상의 사실이나 회사 승인으로 섞이는 일을 줄일 수 있다.'),
])

chapter('보완을 검증하는 작은 순서',[
 tab(['순서','구체 산출물','판정할 것'],[
 ['1. 새판본 설계','실패 원인 가설, 새 출력 계약, 기존 형식과의 연결','지침 추가와 실행 구조 변경의 차이'],
 ['2. 구조 검사 보완','대상×속성 행·주장·근거·검수 연결 검사','일부러 빠뜨린 행/틀린 근거가 검출되는가'],
 ['3. 개발 회귀','A/4·크기감속·선 순서·사선 개수 + 변경 영향 구간','기존 문제 개선과 다른 항목의 퇴행'],
 ['4. 검수기 시험','거짓 명칭·속성 누락·개수 오류·잘못된 통과 예','검수자/평가기 자체가 실패를 분별하는가'],
 ['5. 새 비교 계약','새 자료 노출 범위·기준·판본·모델/도구·자원 고정','현재 초안보다 정확성과 검수 부담이 나아지는가'],
 ['6. 후속 제작 검증','작은 명세→편집 결과→렌더→내용 변경 시험','원본 재현과 재사용을 각각 입증']],[.23,.45,.32]),
 p('개발 회귀는 이미 노출된 자료다. TOVA뿐 아니라 기준답안 준비 때 본 K-GEO도 완전 미노출로 재명명하지 않는다. 새 배치는 A5b의 중단 16회와 별도로 기록한다. 기존 중대 오류와 최초 채점은 덮어쓰지 않는다.'),
 h('한꺼번에 여러 스킬을 추가하면 원인을 알기 어렵다'),
 p('가능한 비교는 기존 draft.3, 출력 계약 개선, 필요할 때 대상 식별 재검수 추가처럼 변경 단위를 분리하는 것이다. 실제 조건 수·반복·자원은 별도 평가 계약에서 정한다. 여기서 제안한 실험은 실행하지 않았다. 관측 가능한 효과가 없는 항목까지 전부 도입하지 않는다.'),
 p('핵심 지표는 첫 결과의 대상 오답/핵심·세부 누락/회피 가능한 기권, 전체 중복 제거 주장 수와 검수 완료 비율, 반복 일치, 추가 열람·수정·내용 검수의 실제 시간이다. exact_tokens가 없으면 null로 두고 출력 문자 수와 섞지 않는다. 같은 품질의 비교쌍이 확인될 때만 공수 비율을 계산한다.'),
 p('사람의 기존 확인은 정확히 같은 자료·주장 범위만 참조한다. 새 사람 gold나 회사 공통 규칙 승인이 추가된 것으로 처리하지 않는다. 전체 영상·음성·정확한 AE 키프레임 복원은 현재 수정의 필수 범위로 추가하지 않는다.'),
])

chapter('앞선 답변에서 유지·정정·보류할 내용',[
 tab(['구분','판단'],[
 ['유지','페르소나보다 판단 순서·출력 계약·근거·검증 구조를 선별한다는 방향'],
 ['유지','관찰·추론·구현 선택·승인을 분리하고 재현과 재사용을 따로 검증한다는 방향'],
 ['정정','현행 Ponytail 색인 대기 한도는 3초. 한글 하위 경로와 영상 기록에는 직접 전용하기 어려움'],
 ['갱신','REA는 6.7.0 고정 소스로 재확인. 영상 기능 이슈는 여전히 제안 상태'],
 ['축소 해석','REA의 완전성 검사는 선언된 요구 집합 기준. 미발견 대상 자동 검출을 뜻하지 않음'],
 ['보류','첨부의 JetBrains 80과제 수치는 이번 확인에서 원문 출처를 확정하지 못해 채택 근거에서 제외'],
 ['보류','설치된 스킬의 실제 영상 성능 우위·공수 절감·전달력 향상은 이번 정적 조사로 입증하지 않음']],[.18,.82]),
 h('소스 취급과 이식 단위'),
 p('권장 이식 단위는 판단 질문, 필수 기록 칸, 전환 조건, 비교 가능한 검증 계약이다. 원본 프로젝트 전체 포크, 모든 자동 훅, 자동 학습·전역 승격, 웹 전용 금지 스타일·시간 수치는 현재 도입 대상에서 제외한다. 코드 복제가 필요해질 경우 파일별 출처와 이용 조건을 별도로 확인한다.'),
 p('원본에 표시된 이용 조건도 같지 않다. Ponytail·REA 등은 MIT 표시, Impeccable은 Apache-2.0, Trail of Bits 저장소는 CC-BY-SA-4.0이다. Anthropic 저장소처럼 구성별 조건을 확인해야 하는 경우도 있어 저장소 전체를 한 조건으로 간주하지 않는다. 이번 보고서는 원본 코드를 우리 스킬에 복사한 결과가 아니다.'),
 h('보존한 조사 산출물'),
 p('research/ponytail-rea-20261019 아래에 원본 ZIP·선택 소스·커밋/파일 목록·REA 변경 비교·영상 제안 이슈·source-audit.json·제안 기록 예시·보호 파일 해시 대조를 둔다. 기존 A5b 작업 공간과 D: 정본은 수정하지 않는다.'),
 p('가장 먼저 보완할 구조는 대상×속성의 관찰 행과 원자 주장·근거·검수 연결이다. 이후 필요한 디자이너 판단을 목적·조건·반례가 있는 선택 규칙으로 검증한다. 외부 스킬의 이름이나 인기보다 우리 실패를 줄였다는 증거가 채택 기준이다.'),
])

# Appendix uses exact commit links, with source statements kept separate from proposals.
for start in range(0,len(audit),14):
    blocks=[p('아래 링크는 조사 중 고정한 커밋의 파일과 확인한 행을 가리킨다. full은 파일 전체, selected는 관련 구간 열람이다. source-audit.json에 전체 경로·해시·행 목록이 있다. 테스트 파일 링크는 실행 통과의 증명이 아니다.')]
    for item in audit[start:start+14]:
        blocks.append({'kind':'source','id':item['id'],'text':item['finding']+' · '+item['review_scope']+' · '+str(item['anchor_lines'][0])+'행','path':item['path'],'url':item['url']})
    chapter('원본 코드 근거 '+str(start//14+1),blocks)

content={'title':'전문가 판단과 리버스 엔지니어링: 영상 스킬 파이프라인 적용 조사','date':'2026-10-19 Asia/Seoul','chapters':chapters,'sources':audit,'input_conversations':['https://chatgpt.com/s/t_6ad5613e3be08191b9bfc34d674a6c0b','https://chatgpt.com/s/t_6ad5630ab3c8819191f32fe85f75da44','https://chatgpt.com/s/t_6ad5632a9ce08191984fbf4d9c44aab5'],'supporting_research':['https://github.com/sxzhang25/MotionVectorization-ProgramTransformation','https://github.com/jama1017/MoVer','https://arxiv.org/html/2502.13372v2']}
(ROOT/'report-content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8')

example={'notice':'설계 검토용 합성 예시. 실제 영상 관측이나 현행 스키마의 유효한 파일이 아님.','schema_version':'proposal-only-0.1','source_id':'source-example','objects':[{'object_id':'o1','shape_description':None,'identity':{'label':None,'candidates':[],'supporting_claim_ids':[],'status':'unreviewed'}}],'observation_rows':[{'id':'or1','object_id':'o1','property':'size','time_window':None,'review_state':'not_reviewed','change':None,'direction_order':None,'easing':{'classification':None,'basis_evidence_ids':[],'limitation':None},'evidence_ids':[],'claim_ids':[],'unresolved_id':'u1'}],'claims':[],'unknowns':[{'id':'u1','question':'대상 크기의 변화와 가감속은 무엇인가?','state':'open','required_evidence':'같은 대상의 진행 중 실제 시각 표본과 원본 ROI','next_probe':None,'resolution':None}],'review':{'structure':'not_run','source_content':'not_reviewed','claim_denominator_complete':False,'company_approval':None}}
(ROOT/'proposed-record-example.json').write_text(json.dumps(example,ensure_ascii=False,indent=2),encoding='utf-8')

pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunB','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunB',italic='Malgun',boldItalic='MalgunB')
INK=colors.HexColor('#18273A'); MUTED=colors.HexColor('#52657A'); BLUE=colors.HexColor('#245ABA'); LINE=colors.HexColor('#D8E1EB')
styles={
 'title':ParagraphStyle('title',fontName='MalgunB',fontSize=19,leading=27,textColor=INK,spaceAfter=18,wordWrap='CJK'),
 'p':ParagraphStyle('p',fontName='Malgun',fontSize=10,leading=16,textColor=INK,spaceAfter=11,wordWrap='CJK'),
 'h':ParagraphStyle('h',fontName='MalgunB',fontSize=12,leading=18,textColor=BLUE,spaceBefore=7,spaceAfter=7,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='Malgun',fontSize=8.5,leading=13,textColor=INK,wordWrap='CJK'),
 'th':ParagraphStyle('th',fontName='MalgunB',fontSize=8.5,leading=13,textColor=colors.white,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='Malgun',fontSize=8,leading=12,textColor=MUTED,spaceAfter=5,wordWrap='CJK'),
}
def escape(s): return html.escape(s).replace('\n','<br/>')
def para(text,style='p'): return Paragraph(escape(text),styles[style])
def make_table(block):
    n=len(block['headers']); usable=499
    widths=[usable*x for x in (block.get('widths') or [1/n]*n)]
    rows=[[para(x,'th') for x in block['headers']]]+[[para(str(x),'cell') for x in row] for row in block['rows']]
    table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F4F9'),colors.white]),('LINEBELOW',(0,1),(-1,-1),.4,LINE)]))
    return table

def page_chrome(c,doc):
    w,h=doc.pagesize
    c.setFillColor(BLUE);c.rect(0,h-9,w,9,fill=1,stroke=0)
    c.setFont('Malgun',8);c.setFillColor(MUTED)
    c.drawString(48,h-32,'SOURCE REVIEW / VIDEO SKILL PIPELINE')
    c.drawRightString(w-48,h-32,'2026.10.19')
    c.setStrokeColor(LINE);c.line(48,41,w-48,41)
    c.drawString(48,27,'정적 원본 조사 · 변경 제안 · 기존 동결판 보존')
    c.drawRightString(w-48,27,str(doc.page))

story=[]
for idx,ch in enumerate(chapters):
    if idx: story.append(PageBreak())
    if idx==0:
        story.append(para('전문가 판단 · 리버스 엔지니어링','h'))
        story.append(para('사내 영상 기획·제작 스킬 파이프라인 적용 조사','small'))
    story.append(para(f'{idx+1:02d}  {ch["title"]}','title'))
    for b in ch['blocks']:
        if b['kind'] in ('p','h'): story.append(para(b['text'],b['kind']))
        elif b['kind']=='table': story.extend([make_table(b),Spacer(1,12)])
        elif b['kind']=='source':
            text=f'<b>[{b["id"]}]</b> {escape(b["text"])}<br/><link href="{html.escape(b["url"],quote=True)}" color="#245ABA">{escape(b["path"])}</link>'
            story.append(Paragraph(text,styles['small']));story.append(Spacer(1,5))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=58,bottomMargin=57,title=content['title'],author='Source research for company-video-grammar-analyzer')
doc.build(story,onFirstPage=page_chrome,onLaterPages=page_chrome)

before=json.loads((ROOT/'protected-before-report.json').read_text(encoding='utf-8-sig'))
after=[]
for row in before:
    digest=sha256(Path(row['path']).read_bytes()).hexdigest()
    after.append(dict(path=row['path'],sha256=digest,unchanged=digest.lower()==row['sha256'].lower()))
assert all(row['unchanged'] for row in after)
(ROOT/'preservation-after-report.json').write_text(json.dumps({'checked_utc':datetime.now(timezone.utc).isoformat(),'all_unchanged':True,'scope':'Only the 10 listed A5b files were rehashed in this research turn; not a re-audit of all 302 historical records.','files':after},ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'repo_count':len(REPOS),'source_review_records':len(audit),'third_party_code_executed':False,'tests_executed':False,'video_evaluations_executed':False,'pdf':str(OUT),'pdf_sha256':sha256(OUT.read_bytes()).hexdigest(),'repositories':[{ 'key':k,'repo':v[0],'commit':v[1],'local_root':str(v[2]),'archive_scope':'selected files' if 'selected-sources' in str(v[2]) else 'source zip','files_present':sum(1 for p in v[2].rglob('*') if p.is_file())} for k,v in REPOS.items()],'archives':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in ROOT.glob('*.zip')]}
(ROOT/'research-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# Every regeneration must also reach the user-designated project PDF archive.
import sys
sys.path.insert(0,str(ROOT.parent.parent/'tools'))
from archive_pdf import archive_pdf
archived=archive_pdf(OUT,'01_제출보고서/공통 조사/2026-10-19_전문가판단과_역설계',name='2026-10-19_전문가판단과_역설계_영상스킬_적용조사_v1.pdf',classification='외부 스킬 원본 조사 / 적용 설계 제안')
print(json.dumps({'pdf':str(OUT),'archived_pdf':archived['destination'],'archive_verified':archived['verified'],'chapters':len(chapters),'source_records':len(audit),'protected_unchanged':True},ensure_ascii=False))
