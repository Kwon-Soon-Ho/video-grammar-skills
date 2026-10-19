# 실제 수행 기록

지정 task.txt, 수행사본_범위.json 및 지정 스킬 본문/기록연결기준·수정과복구·보고지침을 읽었다. 자체 수행사본의 관련 도구 코드와 보존 계약만 조회했다. 초기 PowerShell 실행은 FileSystem InitializeDefaultDrives 경고를 냈으나 명령은 exit 0으로 내용을 반환했다. 파일 목록 출력과 대용량 현재 JSON 출력은 도구 출력에서 일부 잘렸다. 복구에 필요한 원문/해시는 아래 Python에서 전체 바이트로 재검사했다.

실행 런타임: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe -B -X utf8. 검사기의 BASE는 자체 inputs/Phase00로 계산됨을 소스에서 확인. 웹/API/미디어/AE/CU/외부 앱 및 실운영 DB를 사용하지 않았다. 기록접수.py는 검사기가 strict_json/diagnose를 불러오는 경우에만 읽기 함수가 실행되며 receive/접수 CLI는 실행하지 않았다.

## failed_current_structure

명령(JSON argv): ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\12_통합기록\\통합기록_작업초안.json"]

종료코드: 1

stdout:
```json
{
  "valid": false,
  "errors": [
    "core: MAP-ONE: \ubcc0\ud658 \uacc4\uc0b0 \uc88c\ud45c \ubd88\uc77c\uce58"
  ],
  "unresolved": [],
  "human_review_queue": [
    {
      "claim_id": "CL-ONE",
      "claim_version": "0.1.0",
      "priority": "normal",
      "reasons": [
        "\uc8fc\uc7a5 \ub0b4\uc6a9 \uc0ac\ub78c \uac80\uc218 \ud544\uc694"
      ],
      "status": "specimen_only",
      "routing": "\uc2e4\uc81c \uc790\ub8cc \ud655\ubcf4 \ud6c4 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \uc81c\uc791\uc790/\ub514\uc790\uc774\ub108 \uac80\uc218. \uc774 \uac80\uc0ac\uae30\ub294 \ub300\uc2e0 \uc2b9\uc778\ud558\uc9c0 \uc54a\uc74c."
    },
    {
      "item_id": "SP-ROOT",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-CROP",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-RESIZE",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-CROP",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-RESIZE",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "G-ROOT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
      "verified": false
    },
    {
      "item_id": "G-RESULT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
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
  "scope": "\uae30\ub85d \uacc4\uc57d\uc758 \uad6c\uc870/\uc5f0\uacb0 \uac80\uc0ac. \uc2e4\uc81c \uc601\uc0c1\u00b7\uc0ac\ub78c \uac80\uc218\u00b7\ud68c\uc0ac \uc2b9\uc778\u00b7\uc6b4\uc601 \ubc18\uc601 \uc544\ub2d8.",
  "source_json_sha256": "f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9"
}
```

stderr:
```text
```

## checkpoint_structure

명령(JSON argv): ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\backup\\이전작업\\통합기록_정상체크포인트.json"]

종료코드: 0

stdout:
```json
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
        "\uc8fc\uc7a5 \ub0b4\uc6a9 \uc0ac\ub78c \uac80\uc218 \ud544\uc694"
      ],
      "status": "specimen_only",
      "routing": "\uc2e4\uc81c \uc790\ub8cc \ud655\ubcf4 \ud6c4 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \uc81c\uc791\uc790/\ub514\uc790\uc774\ub108 \uac80\uc218. \uc774 \uac80\uc0ac\uae30\ub294 \ub300\uc2e0 \uc2b9\uc778\ud558\uc9c0 \uc54a\uc74c."
    },
    {
      "item_id": "SP-ROOT",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-CROP",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-RESIZE",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-CROP",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-RESIZE",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "G-ROOT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
      "verified": false
    },
    {
      "item_id": "G-RESULT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
      "verified": false
    },
    {
      "item_id": "design",
      "status": "specimen_only",
      "reason": "\ud1a0\ud070 \uc5ed\ud560\u00b7\uc801\uc6a9 \ubaa9\uc801\u00b7\ud504\ub85c\uc81d\ud2b8 \uc608\uc678 \uac80\uc218. \uc601\uc0c1 \ud544\uc218 \ud68c\uc0ac \uaddc\uce59 \uc2b9\uc778\uacfc \uad6c\ubd84",
      "verified": false
    },
    {
      "item_id": "TG-ASSET/video_type",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-ASSET",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/video_type",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/information_relation",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/art_direction",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-STATE/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/information_relation",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/layout",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/art_direction",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_function",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_property",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/timing",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "run",
      "status": "specimen_only",
      "reason": "\uc2e4\ud589 \uc8fc\uccb4\u00b7\ub3c4\uad6c/\ubaa8\ub378\u00b7\uc785\ucd9c\ub825\u00b7\uc124\uc815\uacfc \uc2e4\uc81c \uc791\uc5c5 \ub85c\uadf8\ub97c \ub300\uc870. \uc120\uc5b8\uc744 \uc2e4\ud589 \uc99d\uba85\uc73c\ub85c \ubcf4\uc9c0 \uc54a\uc74c",
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
  "scope": "\uae30\ub85d \uacc4\uc57d\uc758 \uad6c\uc870/\uc5f0\uacb0 \uac80\uc0ac. \uc2e4\uc81c \uc601\uc0c1\u00b7\uc0ac\ub78c \uac80\uc218\u00b7\ud68c\uc0ac \uc2b9\uc778\u00b7\uc6b4\uc601 \ubc18\uc601 \uc544\ub2d8.",
  "source_json_sha256": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2"
}
```

stderr:
```text
```

## legacy_readonly_check

명령(JSON argv): ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\작업초안\\구형_추가자료.json"]

종료코드: 2

stdout:
```json
{
  "valid": false,
  "status": "needs_migration",
  "schema_version": "0.1.0",
  "errors": [
    "\uad6c\ud615 v0.1.0\uc740 \uc0c8 \ud1b5\ud569 \uae30\ub85d\uc73c\ub85c \ud1b5\uacfc\uc2dc\ud0a4\uc9c0 \uc54a\uc74c. \uae30\ub85d\uc811\uc218.py\ub85c \uc6d0\ubb38\u00b7\ub204\ub77d \ubcf4\uc874 \ud6c4 \uba85\uc2dc \uc774\uad00 \ud544\uc694."
  ],
  "unresolved": [],
  "legacy_shape_errors": [],
  "missing_or_review_items": [
    {
      "pointer": "/asset/version",
      "reason": "\uc6d0\ubcf8 \uc601\uc0c1 identity \ubbf8\ud655\uc778. JSON/\ud30c\uc77c\uba85\uc5d0\uc11c \ucd94\uc815 \uae08\uc9c0",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/asset/sha256",
      "reason": "\uc6d0\ubcf8 \uc601\uc0c1 identity \ubbf8\ud655\uc778. JSON/\ud30c\uc77c\uba85\uc5d0\uc11c \ucd94\uc815 \uae08\uc9c0",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/asset/duration_s",
      "reason": "\uc7ac\uc0dd \uae38\uc774\uc640 \ud655\uc778 \uadfc\uac70 \ubbf8\ud655\uc778",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/time_contract",
      "reason": "\uc6d0\uc810\u00b7PTS\u00b7\uad6c\uac04/\ud504\ub808\uc784\u00b7\uadfc\uac70\ub97c \uc0c8 \uc2dc\uac04 \uacc4\uc57d\uc5d0 \uba85\uc2dc \uc5f0\uacb0\ud574\uc57c \ud568",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/targets",
      "reason": "\uc6d0\ubcf8/\uc124\uba85 \uad6c\uac04/\ud654\uba74 \uc0c1\ud0dc/\ub3d9\uc791\u00b7\ub300\uc0c1\uc758 \ubc94\uc704\uc640 \ubc84\uc804 \uc5f0\uacb0 \ud544\uc694",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/evidence",
      "reason": "\uc790\ub8cc pin\u00b7\uc120\ud0dd \ubd80\ubd84\u00b7\uc8fc\uc7a5 \ubc94\uc704/\uadfc\uac70 \uc5ed\ud560 \uc5f0\uacb0 \ud544\uc694",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/segments/*/classification",
      "reason": "\uad6c\ud615 \ud0dc\uadf8\ub294 \ucd9c\ucc98\uc640 \ubc94\uc704\ub97c \uac80\ud1a0\ud560 \ud6c4\ubcf4. \uc0c1\ud0dc/\uad00\uce21 \uc0ac\uc2e4 \uc790\ub3d9 \uc0dd\uc131 \uae08\uc9c0",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/run",
      "reason": "\uc2e4\uc81c \uc218\ud589 \uae30\ub85d \ubbf8\uc791\uc131. \ubbf8\uc2e4\ud589\uacfc \uad6c\ubd84\ud574 \ubcf4\uc874",
      "automatic_fill_allowed": false
    },
    {
      "pointer": "/review",
      "reason": "\uad6c\ud615 \uac80\uc218/\uc2b9\uc778 \uc0c1\ud0dc\ub294 \uc0c8 \ud1b5\ud569 context\ub85c \uc790\ub3d9 \uc774\uc804\ud558\uc9c0 \uc54a\uc74c",
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
```

stderr:
```text
```

복구 전 실패본을 C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-record-steward-workspace\iteration-2\eval-03-정확한_체크포인트_복구\new_skill\run-1\inputs\Phase00\backup\복구작업\통합기록_실패본.json에 배타 생성하고 전체 바이트와 SHA를 대조했다. 복구 요청의 SHA와 실패본/정상본이 모두 일치했고 ID도 동일했다. 정상본 version 0.1.0 그대로 복구하며 새 version을 부여하지 않는다.

## exact_restore_comparison

명령(JSON argv): ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\실행스킬\\video-record-steward\\scripts\\판본대조.py", "--before", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\backup\\복구작업\\통합기록_실패본.json", "--after", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\12_통합기록\\통합기록_작업초안.json", "--mode", "exact_restore", "--checkpoint", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\backup\\이전작업\\통합기록_정상체크포인트.json", "--checkpoint-sha", "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2"]

종료코드: 0

stdout:
```json
{
  "valid": true,
  "mode": "exact_restore",
  "before_sha256": "f94804859022f09c248c5c73ef9e014649fdbab06dcec16f83aa6afe94ec14b9",
  "after_sha256": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2",
  "bytes_changed": true,
  "errors": [],
  "scope": "R4/R5 초안 전후 식별/규격판본·소유기록 판본 또는 요청 checkpoint byte 대조만. 허용 필드·R4/R5 전체 구조·내용·권한 검사는 별도.",
  "writes_performed": false,
  "content_verified": false,
  "company_approved": false,
  "operational_release": false,
  "after_record_version": "0.1.0"
}
```

stderr:
```text
```

## restored_structure

명령(JSON argv): ["D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\07_실행도구\\자료검증.py", "--record", "C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase00-build\\R8_시험\\video-record-steward-workspace\\iteration-2\\eval-03-정확한_체크포인트_복구\\new_skill\\run-1\\inputs\\Phase00\\12_통합기록\\통합기록_작업초안.json"]

종료코드: 0

stdout:
```json
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
        "\uc8fc\uc7a5 \ub0b4\uc6a9 \uc0ac\ub78c \uac80\uc218 \ud544\uc694"
      ],
      "status": "specimen_only",
      "routing": "\uc2e4\uc81c \uc790\ub8cc \ud655\ubcf4 \ud6c4 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \uc81c\uc791\uc790/\ub514\uc790\uc774\ub108 \uac80\uc218. \uc774 \uac80\uc0ac\uae30\ub294 \ub300\uc2e0 \uc2b9\uc778\ud558\uc9c0 \uc54a\uc74c."
    },
    {
      "item_id": "SP-ROOT",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-CROP",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "SP-RESIZE",
      "status": "specimen_only",
      "reason": "\ud574\uc0c1\ub3c4\u00b7SAR\u00b7\ud68c\uc804\uba54\ud0c0/\uc801\uc6a9 \uc5ec\ubd80\uac00 \uc6d0\ubcf8 \uc774\ubbf8\uc9c0/\ub3c4\uad6c \uae30\ub85d\uacfc \ub9de\ub294\uc9c0 \uc0ac\uc6a9\uc790 \ub610\ub294 \uc9c0\uc815 \ub2f4\ub2f9\uc790 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-CROP",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TR-SP-RESIZE",
      "status": "specimen_only",
      "reason": "effective \ubcc0\ud658 \uc218\uce58\u00b7\uc801\uc6a9 \uc21c\uc11c\u00b7\uadfc\uac70 \ub0b4\uc6a9\u00b7\ud68c\uc804/SAR \uc815\ucc45\uc744 \uc9c0\uc815 \ub2f4\ub2f9\uc790\uac00 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "G-ROOT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
      "verified": false
    },
    {
      "item_id": "G-RESULT",
      "status": "specimen_only",
      "reason": "\ub300\uc0c1\u00b7\uc575\ucee4\u00b7\uac00\ub9bc\u00b7ROI/\ubaa8\ub378 \uad6c\ubd84\u00b7\uc624\ucc28 \uadfc\uac70\uc758 \ub0b4\uc6a9 \uac80\uc218. \uacc4\uc0b0 \ud1b5\uacfc\ub97c \uc2e4\uce21 \ud655\uc778\uc73c\ub85c \uc2b9\uaca9\ud558\uc9c0 \uc54a\uc74c",
      "verified": false
    },
    {
      "item_id": "design",
      "status": "specimen_only",
      "reason": "\ud1a0\ud070 \uc5ed\ud560\u00b7\uc801\uc6a9 \ubaa9\uc801\u00b7\ud504\ub85c\uc81d\ud2b8 \uc608\uc678 \uac80\uc218. \uc601\uc0c1 \ud544\uc218 \ud68c\uc0ac \uaddc\uce59 \uc2b9\uc778\uacfc \uad6c\ubd84",
      "verified": false
    },
    {
      "item_id": "TG-ASSET/video_type",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-ASSET",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/video_type",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/information_relation",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT/art_direction",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-SEGMENT",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-STATE/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/information_relation",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/layout",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE/art_direction",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-STATE",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/communication_purpose",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_function",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/motion_property",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT/timing",
      "status": "specimen_only",
      "reason": "\ubd84\ub958\uc758 \ub300\uc0c1\u00b7\uadfc\uac70 \ucda9\ubd84\uc131\u00b7\uc758\ubbf8 \uac80\uc218. classified\ub294 \ud574\ub2f9 \ucd9c\ucc98\uc5d0 \ub300\ud55c \ud0dc\uadf8\uc774\uba70 \uad00\uce21/\ud68c\uc0ac \uc2b9\uc778 \uc544\ub2d8",
      "verified": false
    },
    {
      "item_id": "TG-BEAT",
      "status": "specimen_only",
      "reason": "\uc124\uba85 \uad6c\uac04\u00b7\ud654\uba74 \uc0c1\ud0dc\u00b7\ub3d9\uc791\uc758 \uc758\ubbf8 \uacbd\uacc4, \uc2dc\ub098\ub9ac\uc624 \uc5f0\uacb0, \ud504\ub808\uc784 \ud45c\ubcf8\uc758 \ucda9\ubd84\uc131 \uac80\uc218",
      "verified": false
    },
    {
      "item_id": "run",
      "status": "specimen_only",
      "reason": "\uc2e4\ud589 \uc8fc\uccb4\u00b7\ub3c4\uad6c/\ubaa8\ub378\u00b7\uc785\ucd9c\ub825\u00b7\uc124\uc815\uacfc \uc2e4\uc81c \uc791\uc5c5 \ub85c\uadf8\ub97c \ub300\uc870. \uc120\uc5b8\uc744 \uc2e4\ud589 \uc99d\uba85\uc73c\ub85c \ubcf4\uc9c0 \uc54a\uc74c",
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
  "scope": "\uae30\ub85d \uacc4\uc57d\uc758 \uad6c\uc870/\uc5f0\uacb0 \uac80\uc0ac. \uc2e4\uc81c \uc601\uc0c1\u00b7\uc0ac\ub78c \uac80\uc218\u00b7\ud68c\uc0ac \uc2b9\uc778\u00b7\uc6b4\uc601 \ubc18\uc601 \uc544\ub2d8.",
  "source_json_sha256": "4f309bf8061d4973956f82fa36b74b587403995cdf93545c54411209139b4ec2"
}
```

stderr:
```text
```

복구 결과: exact_checkpoint_restored; 정상본과 전체 바이트 동일. 실제 변경 기존 파일: ["12_통합기록/통합기록_작업초안.json"]; 추가 backup: ["backup/복구작업/통합기록_실패본.json"]; 삭제: []; 임시 파일 잔존: False.

JSON diff:
```json
[
  {
    "pointer": "/spatial_contract/geometries/0/coordinates/x/num",
    "before": 301,
    "after": 300
  },
  {
    "pointer": "/version",
    "before": "0.1.1",
    "after": "0.1.0"
  }
]
```

기존 R5 직접 참조 읽기 대조:
```json
[]
```

검사 결과는 구조/참조 범위이며 미해결·사람 검수 대기는 result.json 및 원시 결과에 그대로 보존했다. 구형 파일 접수·이관·수정, manifest/pin 재생성 및 R5 링크 갱신은 하지 않았다. 복구 이후 추가 수정/롤백은 없었다. 미수집 실행 시간/token은 null. 복구 직전 재대조와 동일 폴더 os.replace는 전 파일시스템 transaction/완전 동시성 제어 보장이 아니다.
