# 실제 수행 기록

사용 스킬: inputs/Phase00/실행스킬/video-record-steward/SKILL.md 및 references/작업기준.md.
범위: own run의 합성 사본. 복구 대상 초안만 변경. 구형 자료는 읽기 검사만 수행.
시간/token 추정값은 기록하지 않음.

초기 PowerShell 파일 읽기에서 InitializeDefaultDrives 경고가 표시됐으나 명령 종료코드는 0이고 요청 파일 내용이 반환됨. 파일 목록 출력은 길어 일부 잘렸으며 필요한 파일은 개별 재조회함.

지정 대상/체크포인트의 실제 SHA256이 복구요청과 모두 일치함.
{
  "failed_current_expected": "f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9",
  "failed_current_actual": "f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9",
  "checkpoint_expected": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2",
  "checkpoint_actual": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2"
}

실행: ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\12_통합기록\\통합기록_작업초안.json"]
종료코드: 1
stdout/stderr: outputs/복구전_초안검사_stdout.txt, 복구전_초안검사_stderr.txt
{
  "valid": false,
  "errors": [
    "core: MAP-ONE: 변환 계산 좌표 불일치"
  ],
  "unresolved": [],
  "human_review_queue": [
    {
      "claim_id": "CL-ONE",
      "claim_version": "0.1.0",
      "priority": "normal",
      "reasons": [
        "주장 내용 사람 검수 필요"
      ],
      "status": "specimen_only",
      "routing": "실제 자료 확보 후 사용자 또는 지정 제작자/디자이너 검수. 이 검사기는 대신 승인하지 않음."
    },
    {
      "item_id": "SP-ROOT",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "SP-CROP",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "SP-RESIZE",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "TR-SP-CROP",
      "status": "specimen_only",
      "reason": "effective 변환 수치·적용 순서·근거 내용·회전/SAR 정책을 지정 담당자가 검수",
      "verified": false
    },
    {
      "item_id": "TR-SP-RESIZE",
      "status": "specimen_only",
      "reason": "effective 변환 수치·적용 순서·근거 내용·회전/SAR 정책을 지정 담당자가 검수",
      "verified": false
    },
    {
      "item_id": "G-ROOT",
      "status": "specimen_only",
      "reason": "대상·앵커·가림·ROI/모델 구분·오차 근거의 내용 검수. 계산 통과를 실측 확인으로 승격하지 않음",
      "verified": false
    },
    {
      "item_id": "G-RESULT",
      "status": "specimen_only",
      "reason": "대상·앵커·가림·ROI/모델 구분·오차 근거의 내용 검수. 계산 통과를 실측 확인으로 승격하지 않음",
      "verified": false
    }
  ],
  "coordinate_bindings": [],
  "integrated_review_states": [],
  "fact_verified": false,
  "human_identity_verified": false,
  "company_approved": false,
  "operational_release": false,
  "status": "invalid",
  "schema_version": "0.2.0",
  "scope": "기록 계약의 구조/연결 검사. 실제 영상·사람 검수·회사 승인·운영 반영 아님.",
  "source_json_sha256": "f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9"
}

현재 실패 파일을 backup/복구_20261015T073438Z_2882f959/실패한_통합기록_작업초안.json 에 배타 생성하여 보존했고 바이트/hash 일치를 재확인함. 기존 backup은 덮어쓰지 않음.

정상 체크포인트의 바이트를 임시 파일에 기록·확인한 뒤 지정 초안에 교체. JSON 재직렬화/필드 수정/버전 증가 없음. 복구 후 바이트와 SHA256 일치 확인.

실행: ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\12_통합기록\\통합기록_작업초안.json"]
종료코드: 0
stdout/stderr: outputs/복구후_초안검사_stdout.txt, 복구후_초안검사_stderr.txt
{
  "valid": true,
  "errors": [],
  "unresolved": [],
  "human_review_queue": [
    {
      "claim_id": "CL-ONE",
      "claim_version": "0.1.0",
      "priority": "normal",
      "reasons": [
        "주장 내용 사람 검수 필요"
      ],
      "status": "specimen_only",
      "routing": "실제 자료 확보 후 사용자 또는 지정 제작자/디자이너 검수. 이 검사기는 대신 승인하지 않음."
    },
    {
      "item_id": "SP-ROOT",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "SP-CROP",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "SP-RESIZE",
      "status": "specimen_only",
      "reason": "해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수",
      "verified": false
    },
    {
      "item_id": "TR-SP-CROP",
      "status": "specimen_only",
      "reason": "effective 변환 수치·적용 순서·근거 내용·회전/SAR 정책을 지정 담당자가 검수",
      "verified": false
    },
    {
      "item_id": "TR-SP-RESIZE",
      "status": "specimen_only",
      "reason": "effective 변환 수치·적용 순서·근거 내용·회전/SAR 정책을 지정 담당자가 검수",
      "verified": false
    },
    {
      "item_id": "G-ROOT",
      "status": "specimen_only",
      "reason": "대상·앵커·가림·ROI/모델 구분·오차 근거의 내용 검수. 계산 통과를 실측 확인으로 승격하지 않음",
      "verified": false
    },
    {
      "item_id": "G-RESULT",
      "status": "specimen_only",
      "reason": "대상·앵커·가림·ROI/모델 구분·오차 근거의 내용 검수. 계산 통과를 실측 확인으로 승격하지 않음",
      "verified": false
    },
    {
      "item_id": "design",
      "status": "specimen_only",
      "reason": "토큰 역할·적용 목적·프로젝트 예외 검수. 영상 필수 회사 규칙 승인과 구분",
      "verified": false
    },
    {
      "item_id": "TG-ASSET/video_type",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-ASSET",
      "status": "specimen_only",
      "reason": "설명 구간·화면 상태·동작의 의미 경계, 시나리오 연결, 프레임 표본의 충분성 검수",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/video_type",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/communication_purpose",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/information_relation",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/art_direction",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT",
      "status": "specimen_only",
      "reason": "설명 구간·화면 상태·동작의 의미 경계, 시나리오 연결, 프레임 표본의 충분성 검수",
      "verified": false
    },
    {
      "item_id": "TG-STATE/communication_purpose",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-STATE/information_relation",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-STATE/layout",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-STATE/art_direction",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-STATE",
      "status": "specimen_only",
      "reason": "설명 구간·화면 상태·동작의 의미 경계, 시나리오 연결, 프레임 표본의 충분성 검수",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/communication_purpose",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_function",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_property",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/timing",
      "status": "specimen_only",
      "reason": "분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님",
      "verified": false
    },
    {
      "item_id": "TG-BEAT",
      "status": "specimen_only",
      "reason": "설명 구간·화면 상태·동작의 의미 경계, 시나리오 연결, 프레임 표본의 충분성 검수",
      "verified": false
    },
    {
      "item_id": "run",
      "status": "specimen_only",
      "reason": "실행 주체·도구/모델·입출력·설정과 실제 작업 로그를 대조. 선언을 실행 증명으로 보지 않음",
      "verified": false
    }
  ],
  "coordinate_bindings": [],
  "integrated_review_states": [],
  "fact_verified": false,
  "human_identity_verified": false,
  "company_approved": false,
  "operational_release": false,
  "status": "draft_structure_pass",
  "schema_version": "0.2.0",
  "scope": "기록 계약의 구조/연결 검사. 실제 영상·사람 검수·회사 승인·운영 반영 아님.",
  "source_json_sha256": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2"
}

실행: ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\old_skill\\run-1\\inputs\\Phase00\\작업초안\\구형_추가자료.json"]
종료코드: 2
stdout/stderr: outputs/구형_추가자료_읽기검사_stdout.txt, 구형_추가자료_읽기검사_stderr.txt
{
  "valid": false,
  "status": "needs_migration",
  "schema_version": "0.1.0",
  "errors": [
    "구형 v0.1.0은 새 통합 기록으로 통과시키지 않음. 기록접수.py로 원문·누락 보존 후 명시 이관 필요."
  ],
  "unresolved": [],
  "legacy_shape_errors": [],
  "missing_or_review_items": [
    {
      "pointer": "/asset/version",
      "reason": "원본 영상 identity 미확인. JSON/파일명에서 추정 금지",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/asset/sha256",
      "reason": "원본 영상 identity 미확인. JSON/파일명에서 추정 금지",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/asset/duration_s",
      "reason": "재생 길이와 확인 근거 미확인",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/time_contract",
      "reason": "원점·PTS·구간/프레임·근거를 새 시간 계약에 명시 연결해야 함",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/targets",
      "reason": "원본/설명 구간/화면 상태/동작·대상의 범위와 버전 연결 필요",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/evidence",
      "reason": "자료 pin·선택 부분·주장 범위/근거 역할 연결 필요",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/segments/*/classification",
      "reason": "구형 태그는 출처와 범위를 검토할 후보. 상태/관측 사실 자동 생성 금지",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/run",
      "reason": "실제 수행 기록 미작성. 미실행과 구분해 보존",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/review",
      "reason": "구형 검수/승인 상태는 새 통합 context로 자동 이전하지 않음",
      "automatic_fill_allowed": false
    }
  ],
  "analysis_search_allowed": false,
  "company_rule_search_allowed": false,
  "fact_verified": false,
  "human_identity_verified": false,
  "company_approved": false,
  "operational_release": false,
  "source_json_sha256": "fc906a18a785b4e51ab5d5714483a6c0033d5726847556bd89cf613795509a47"
}

최종 보존 검증:
{
  "changed_existing_paths": [
    "12_통합기록/통합기록_작업초안.json"
  ],
  "added_paths": [
    "backup/복구_20261015T073438Z_2882f959/실패한_통합기록_작업초안.json"
  ],
  "existing_non_target_files_unchanged": true,
  "legacy_bytes_unchanged": true,
  "existing_backup_unchanged": true
}
최종 결과: outputs/검사결과.json. 모든 assert 통과. 구형 접수/이관 도구 main 및 receive는 호출하지 않음. 외부앱/미디어해석/웹/실제 DB 접근 없음.
