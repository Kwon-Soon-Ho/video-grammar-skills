# 분석 초안 출력

`observations.json`은 다음 필드를 가진다. 내용은 한국어로 작성해도 된다. 이 형식은 A3 분석 중간 형식이며 R4 통합 DB 형식이 아니다.

```json
{
  "schema_version": "a3-observation-0.1",
  "case_id": "입력 ID",
  "source": {"path": "원본 절대 경로", "sha256": "실제 해시"},
  "window_seconds": [0, 2],
  "method": "선택 프레임/원본 ROI 등 실제 사용 방법",
  "document_mode": "none",
  "audio_reviewed": false,
  "evidence": [{"id":"f1", "path":"PNG 절대 경로", "actual_seconds":"0", "role":"within"}],
  "objects": [{
    "id":"o1", "name":"관측 대상", "parent":null,
    "events":[{
      "description":"어떤 변화/유지인지",
      "properties":["position"],
      "time_seconds":[0,1],
      "evidence_ids":["f1","f2"],
      "direction_order":"관측한 방향/순서",
      "easing":{"property":"position","classification":"unknown","basis":"이유/표본"},
      "status":"observed",
      "limitations":[]
    }]
  }],
  "coverage":{"overview":"검사 범위", "secondary_details":"검사 결과", "internal_content":"검사 결과", "unresolved":[]},
  "hypotheses":[],
  "limitations":[],
  "files_read":[]
}
```

예시 f2는 실제 두 번째 프레임으로 채운다. evidence는 모두 실제 열람한 프레임이며 id/path/actual을 정확히 연결한다. 보강 프레임도 그 추출 로그를 files_read에 기록한다. status는 observed/uncertain/not_applicable 중 선택하고, 추측 구현은 hypotheses에만 둔다. easing 분류는 accelerate/decelerate/in_out/linear/unknown/not_applicable이며 실제 관측 속성과 연결한다. 이징 수치 측정이 있으면 각 입력값·단위·방법·오차/미상·한계를 추가한다.

`observations.md`에는 핵심 동작/순서, 근거 시점, 미해결만 간결히 정리한다. JSON에 발견을 남겼는데 보고서에는 화면 구성만 설명하는 일이 없도록 주요 동작을 함께 표시한다. 사용자 확인이 필요하면 이유와 해당 화면을 특정한다.

복수 원본/화면 비율 변형판은 원본마다 별도 관측 파일을 만든다. evidence 경로는 검증 카탈로그의 원본 추출 프레임 또는 검증된 크롭을 가리킨다. 보조 크롭만 별도로 봤다면 method/files_read에 원본 프레임·크롭 좌표를 연결해도 된다. 직접 근거로 쓴 크롭은 `evidence_catalog.py --logs ... --crops <crops.json> --out ...`으로 검증한다. crops.json은 `[{"path":"크롭 경로","parent_path":"원본 추출 프레임 경로","crop_xyxy_native_pixels":[0,0,100,100]}]` 형식이다. 현재 크롭 검증은 Pillow가 있는 환경의 RGB 무배율 크롭만 지원하며 부모 이미지의 해당 픽셀과 정확히 대조한다. 다른 변환은 검증된 원본 프레임을 직접 근거로 두고 변환 이력을 별도로 기록한다.

카탈로그 검사는 해당 파일의 원본 해시·표시시각·현재 PNG 해시를 대조한다. 비교 보고서는 양쪽 관측 파일과 각각의 장면 앵커 시각을 참조한다. 같은 시각이나 비슷한 화면만으로 근거 파일을 교환하지 않는다.
