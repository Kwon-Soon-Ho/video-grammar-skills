# 수행 기록

작업 범위는 이 run-1 및 inputs/Phase00 사본이다. 지정 video-knowledge-curator SKILL.md 및 두 상대 참조만 실행 지침으로 읽었다. 다른 스킬/시험/평가 자료, 실제 D 프로젝트 자료는 열지 않았다. D 경로는 task.txt가 지정한 Python 실행파일의 존재 확인 및 실행에만 사용했다. 06_맞춤스킬/08_검증결과의 과거 평가는 읽지 않았다. 외부 네트워크/API/AE/CU/설치는 수행하지 않았다.

## 수행 명령과 읽은 범위

아래 `$runRoot`는 이 transcript.md가 있는 run-1 절대경로, `$dbRoot`는 `$runRoot\inputs\Phase00`다. 모든 명령은 PowerShell에서 실행했다. Python의 전체 실행 소스는 `outputs/수정과검사.py`에 보존했다. 이 스크립트는 v0.1.1 입력을 전제로 원본 backup을 배타 생성하므로 수정 후 그대로 재실행하는 용도가 아니다.

1. `Get-Content -LiteralPath "$runRoot\task.txt"`
   - 실제 요청, DB 루트, 지정 스킬, 지정 Python, 출력 폴더 및 사본 검사 한계를 확인했다. 종료코드 0.
2. `Get-Content -LiteralPath "$dbRoot\실행스킬\video-knowledge-curator\SKILL.md"`
   - 초안 실제 저장, backup/버전/허용 diff/관련 검사 및 운영 정본 보존 지침을 확인했다. 종료코드 0.
3. `Get-Content`로 위 스킬의 `references/작업기준.md`, `references/출력지침.md`, DB `입력메모.json`을 읽고 `Get-ChildItem -LiteralPath $dbRoot -Name`으로 루트의 직접 자식 이름만 확인했다. 종료코드 0.
4. `Get-Content`로 `00_운영계약/01_보존과버전_계약.md`, `00_운영계약/정본과표시_연결목록.json`, `작업초안/레이아웃지식_초안.json`을 읽었다. 02_원칙과레이아웃 및 07_실행도구의 직접 자식 파일 이름을 확인했다. 종료코드 0. 연결목록과 초안을 함께 출력한 응답 일부가 도구 출력 한도에서 잘려, 이후 관련 정본/메타데이터를 좁혀 다시 확인했다. 잘린 부분을 전부 읽었다고 주장하지 않는다.
5. `Get-Content -Raw | ConvertFrom-Json` 및 `Where-Object`로 레이아웃 정본의 버전/단일 초점 항목, 심화지식의 최상위 필드명을 확인했다. `Get-Content -TotalCount 180`으로 자료검증.py, `Get-Content -TotalCount 140`으로 R3_레이아웃자료검사.py를 확인했다. `Select-String -Pattern '단일 초점' -Context 2,16`으로 07_레이아웃별_선택조건과반례.md의 관련 절을 확인했다. 종료코드 0.
6. `Get-Content -TotalCount 165`로 구형기록_보존검사.py의 실제 목록 검사 구현과 IO 경계를 확인했다. 심화지식의 버전/권한 및 대상 카드 전체, 출처목록의 SRC-PROJECT-TAXONOMY/SRC-IMPECCABLE 선언만 선택 출력했다. `Test-Path -LiteralPath <task.txt 지정 Python>`은 True였다. 종료코드 0.
7. `Get-Content`로 04_기록규격/레이아웃지식_스키마.json을 확인하고, 연결목록에서 관련 ID/경로 항목을 선택 조회했다. 이 명령 끝의 불필요한 추가 조회에 `01_공通용어/공통용어사전.json`이라는 오타가 있었다. `-ErrorAction SilentlyContinue`로 오류 문구는 숨겨졌으며 그 묶음의 종료코드는 실제 1이었다. 해당 파일은 읽지 못했다. 이후 Python 기존 검사에서 올바른 `01_공통용어/공통용어사전.json` 경로를 실제로 읽어 참조를 검사했다.
8. `New-Item -ItemType Directory -Path "$runRoot\outputs" -Force` 및 PowerShell 단일 인용 here-string/Set-Content로 `outputs/수정과검사.py`를 작성했다. 다음 명령을 실제 1회 실행했다.

```powershell
& 'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe' -B "$runRoot\outputs\수정과검사.py" > "$runRoot\outputs\실행_stdout.txt" 2> "$runRoot\outputs\실행_stderr.txt"
$runExit = $LASTEXITCODE
Set-Content -LiteralPath "$runRoot\outputs\실행_exitcode.txt" -Value $runExit -Encoding utf8
Get-Content -LiteralPath "$runRoot\outputs\실행_stdout.txt"
Get-Content -LiteralPath "$runRoot\outputs\실행_stderr.txt"
exit $runExit
```

- 실제 Python 종료코드: 0. stdout은 실행_stdout.txt에 보존했으며 stderr 파일은 비어 있다.
- 원본과 backup SHA256: `0225b8ff97c7ab9441cbe6d1fd7539da8d97ce90bf2e9003d63f4f4ae6175306`.
- 수정 후 SHA256: `b3ce2109c82c28e9267cb87908ef692d189ec0f32c766a2c33567087db90ee0c`.
- 실제 지정 초안을 덮어쓰기 전에 backup을 배타 생성하고 원본과 바이트가 같은지 확인했다.
- 실제 변경은 `/version`, `/layouts/0/limits`, `/layouts/0/version` 세 필드이며 파일·대상 버전은 0.1.1 → 0.1.2다. limits는 요청 문구 그대로다.
- 기존 자료검증.validate_catalogs()로 현재 지식 목록을 검사했다. 후보 및 저장 후 초안은 구형기록_보존검사.validate_catalogs()에 layout 입력만 메모리로 대입하여 같은 구조/중복ID/용어축/출처/related ID 검사를 수행했다. 정본 경로를 후보로 덮어쓰지 않았다.
- 레이아웃 JSON 스키마, 중복 JSON key/비유한 수치 금지 파싱, 허용 변경 객체 대조, 나머지 13개 항목 불변, 버전 사본/저장 바이트 일치, backup 보존, 부모 메모/연결목록 버전·SHA 대조를 실제 실행했다. 검사 오류 합계는 0이다.
- 보호 대상 17개 파일의 전후 SHA가 모두 같다. 대상 목록 및 실제 해시는 실제결과.json에 있다. 모든 DB 파일 전체를 검사했다는 뜻은 아니다.
9. 이 transcript를 저장하고 `Get-Content outputs/변경.diff`, 결과 JSON 선택 출력, 초안/판본 사본/backup/정본 Get-FileHash 및 stderr 길이/종료코드를 다시 확인했다. 실제 확인 결과는 마지막 실행 도구 출력에 남는다.

## 오류·한계·미수행

PowerShell 초기화는 각 exec 호출 앞에서 `Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.` 경고를 출력했다. 경로를 명시한 읽기/쓰기와 지정 Python 실행은 진행되었으며 위 오타 조회 외의 실행 명령은 종료코드 0을 반환했다. 이 경고를 Python 검사 실패로 바꾸거나 숨기지 않는다.

지정 Python으로 동작한 검사만 통과로 보고한다. R3 전체 검사 코드는 외부 스킬 원문/사본 밖 경로를 읽으므로 실행하지 않았다. R4 통합 영상 기록 검사를 지식 초안에 적용하지 않았다. R6 전체 원문/자산 검사 및 R7 연결검사는 실행하지 않았다. 사본에 없는 자산을 찾으러 루트 밖으로 이동하지 않았다. 출처목록은 로컬 선언으로 확인했으며 외부 원문 본문을 새로 읽거나 실제 효과·사람 신원·회사 승인·사용권한을 검증하지 않았다.

초안은 운영 연결목록에 미등록 상태다. 운영 정본·기본 전환·고정 해시 재생성·생성문서 갱신·회사 승인 변경은 수행하지 않았다. status=reference는 원본 항목 값 그대로 보존했으며, 초안의 운영 정본 승격을 뜻하지 않는다. 새 설명용 사례나 실제 관측은 만들지 않았다. 추가 사용자 판단이 필요한 질문은 없었다. 자기채점, 없는 token 수 또는 전체 소요시간을 만들지 않았다.

## 마지막 독립 바이트 확인

위 9번 실제 확인은 종료코드 0이었다. diff와 결과 JSON을 다시 읽었으며, 지정 초안/판본 사본 SHA는 모두 `b3ce2109c82c28e9267cb87908ef692d189ec0f32c766a2c33567087db90ee0c`, backup/운영 레이아웃 정본 SHA는 모두 `0225b8ff97c7ab9441cbe6d1fd7539da8d97ce90bf2e9003d63f4f4ae6175306`이었다. Python 실행 stderr 길이는 실제 0바이트, 보존된 실행 종료코드는 0이었다.

추가로 지정 Python `-B -c`에서 pathlib.read_bytes()로 원본 backup/수정된 초안을 읽고 줄바꿈 수 및 바이트 역치환을 실제 확인했다. 명령의 핵심 코드는 다음과 같다.

```python
a = (r/'outputs/backup/지식문구수정_01/레이아웃지식_초안_v0.1.1.json').read_bytes()
b = (r/'inputs/Phase00/작업초안/레이아웃지식_초안.json').read_bytes()
reversed_equal = b.replace('단일 초점이 반드시 중앙 배치를 뜻하는 것은 아님'.encode(), '반드시 중앙 배치 아님'.encode(), 1).replace(b'0.1.2', b'0.1.1') == a
```

실제 stdout은 `{"original_CRLF": 0, "after_CRLF": 0, "original_LF": 411, "after_LF": 411, "reversed_equal": true}`였다. 종료코드 0. 이 확인으로 세 요청 변경을 되돌린 바이트가 원본과 같고 줄바꿈도 유지됨을 재확인했다. 판정 내용을 추가한 이 transcript 저장 외에 초안은 더 수정하지 않았다.
