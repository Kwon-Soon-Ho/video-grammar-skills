# 실행 기록

- 실행: 지정 스킬을 사용한 세 표본 수집. 산출물은 같은 폴더의 `collection.md`, `execution.md` 두 Markdown 파일뿐이다.
- 시작 UTC 기록: **2026-10-19 04:58:37 UTC**. 실제 시계 도구의 최초 확인값이다. 스킬과 input.md 최초 읽기 직후에 시계를 확인했으며, 그보다 앞선 읽기 호출의 개별 시작 시각은 수집하지 않았다. 최초 작업 시작의 초 단위 시각을 소급 추정하지 않는다.
- 종료 UTC: **2026-10-19 05:03:38 UTC**. 수집 기록과 실행 본문 저장 뒤 시계 도구에서 확인한 값이다. 이 종료 시각 문장 반영은 그 확인 뒤에 수행했다.

## 실제 읽은 자료

스킬 기준 경로: `C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/collection-skill-update-20261019/candidate/company-video-grammar-analyzer/`.

- `SKILL.md`
- 연결된 `references/evidence-and-records.md`, `collection-record.md`, `design-and-patterns.md`, `motion-review.md`, `design-density.md`, `pattern-composition.md`, `source-coverage.md`
- 지정 입력 폴더 `C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/collection-skill-update-20261019/eval-inputs/new-section/`의 `input.md` 및 아래 세 PNG

실제 본 전체 원본 PNG: `f_05760_192.000.png`, `f_06120_204.000.png`, `f_06480_216.000.png`. view_image의 original 옵션으로 열었으나 표시 시스템에서 각각 6000×1688로 축소되었다. 이어 원본 래스터에서 아래 부분 화면을 메모리로 잘라 직접 보았다. 좌표는 7680×2160 원본 기준 `(left, top, right, bottom)`이며 저장 파일을 만들지 않았다.

| PNG 시각 | 실제 본 추가 ROI |
|---:|---|
| 192초 | (4700,700,7300,1700): 비용 정의·총액·도상. 이 표시만 2048×788로 축소됨. (1080,780,3080,1300): TOVA/KNGIL/GAIA 로고·본문, 원본 크기 표시 |
| 204초 | (4600,260,6150,1260): EG-BIM 제목·기능·설명; (4600,1300,6100,2000): Drawer·721Copy·5.4억원; (6070,1300,7370,2000): 공간정보·79회·5.9억원. 모두 원본 크기 표시 |
| 216초 | (4800,690,6800,1130): 제외 문장; (6580,690,7580,1050): 첫 줄 끝 ‘기준이 부족해’; (4670,1170,6670,1620): 향후 조건·보조 도식. 모두 원본 크기 표시 |

## 수행과 한계

세 PNG의 SHA-256을 실제 파일에서 계산해 input.md와 대조했고 모두 일치했다. 전체 구성, 문구, 정보 관계, 표본 사이 상태 차이, 재사용 검색용 로컬 후보와 적용 조건, 미관측/판독 제한을 collection.md에 작성하고 저장된 말미를 다시 읽었다. 원본 MP4 자체·추출 로그·음성·시나리오·편집 프로젝트는 보지 않았다. 자료의 원본 길이·시간 매핑·원본 SHA는 입력 인용이며 이번에 독립 검증한 것은 PNG 파일 해시다.

추가 ROI를 표시하기 위해 node_repl에서 sharp import를 한 차례 시도했으나 `Unsupported import specifier ../package.json` 오류로 실패했다. 그 경로로 이미지를 읽었다고 주장하지 않는다. 이후 PowerShell System.Drawing으로 메모리 크롭·PNG 인코딩 후 시각 표시했다. 셸에는 FileSystem 드라이브 초기화 경고가 있었으나 지정 파일 읽기·해시·크롭·저장은 성공 결과를 받았다.

네트워크, 새 영상 추출, 원본·스킬 수정, 다른 프로젝트 기록/분석/시험 정의/형제 실행 열람, PDF·새 디자인·영상·JSON 생성은 수행하지 않았다. 연속 재생·광류/픽셀 이동 측정·이징 추정·가독성 전수 검사·사용자 내용 검수·회사 규칙 승인·DB 정본 등록·재사용 적용 시험도 수행하지 않았다. 후속 확인 범위는 collection.md U1–U7에 남겼다.
