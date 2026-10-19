# 실행 기록

- 실행일: 2026-10-19
- 요청: 제공된 사내 영상 세 표본의 전체 디자인·정보 관계·구성요소·시간 차이를 다음 조회용으로 수집. 새 화면/영상 없이 Markdown 기록.
- 읽은 스킬: 지정 `backup/draft10/company-video-grammar-analyzer/SKILL.md` (0.1.0-draft.10).
- 읽은 참조: `evidence-and-records.md`, `collection-record.md`, `design-and-patterns.md`, `motion-review.md`, `pattern-composition.md`, `source-coverage.md`, `design-density.md`.
- 원본 입력: 지정 `eval-inputs/new-section/input.md`와 그 폴더 PNG 3개만 사용. evals/·기존 분석·다른 실행·제작자 문서는 읽지 않았다.
- 실제 수행: PowerShell로 텍스트 읽기, 번들 Python/Pillow로 세 PNG의 규격/RGB·SHA-256 대조와 원본 좌표 ROI 17개 생성, `view_image`로 전체 3개와 ROI 17개 확인. ROI 좌표·저장 이력은 `collection.md` §6. 전체·일부 큰 ROI는 표시 도구에서 축소되었고, 금액·단위·부정어는 더 작은 ROI로 재확인했다.
- 주요 내용 검토: 11.5억과 5.4+5.9=11.3억을 동일 집계 분해로 확정하지 않음. EG-BIM/이지빔 Drawer의 동일성, “이들 S/W”의 범위를 미확정으로 보존. E204 하단 중첩·중앙 우측 가림을 전환/이동의 구현 확정과 구별. 교통 수요 분석 도안형 로고의 초기 TVA 약식 전사는 기각하고 확대 ROI/영문 풀이로 다시 확인해 전사 후보로 남김.
- 실제 파일 확인: UTF-8 저장 후 다시 읽어 핵심 부정문·721Copy·79회·합산 메모·ROI 항목을 확인. 입력 PNG 3개 해시는 명세와 일치. 별도 JSON 검사기나 독립 내용 검수는 실행하지 않았다.
- 도구 상태: 차단 없음. PowerShell이 InitializeDefaultDrives 경고를 출력했으나 읽기·생성 명령은 exit 0으로 완료했다. 일부 Python 콘솔의 한글 표시가 깨졌으나 저장 파일은 UTF-8로 재독해 확인했다.
- 한계: MP4 직접 접근·해시 계산·추출 로그 원문 재검증·새 시각 추출·연속 재생·오디오 청취/전사 없음. 세 장의 12초 간격을 연속 관찰로 환산하지 않음. 도구/입력 범위를 넘어선 전체 영상 검수·모션 곡선/지속시간·회사 승인·재사용 구현 검증을 주장하지 않음.
- 산출: `outputs/collection.md`, `outputs/execution.md`; 분석 파생 PNG는 같은 run의 `scratch/`에만 저장. PDF·새 디자인·영상·정본 등록·네트워크 사용·서브에이전트 실행·스킬 원본 수정 없음.
- 남은 대상: 표본 사이 두 구간과 창 밖의 영상, 음성/싱크, 산정 범위·지시어의 근거 문서, 미판독 UI, 모션의 내부/주변/퇴장. 추가 근거가 제공되고 별도 검수가 요청되면 이 순서로 보강할 수 있다.
