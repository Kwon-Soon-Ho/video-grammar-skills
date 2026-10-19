from pathlib import Path
import json,sys,hashlib,shutil,re,importlib.metadata
from prepare import OUT,ROOT,sha,write
PUB=OUT/'게시안';P='Phase 01-A';AN=f'{P}/02_분석작업/01-A2_작은예비';VE=f'{P}/04_검증자료/01-A2_작은예비';BK=f'{P}/backup/2026-10-16_01-A2_작은예비'
def copy(src,rel):
    dest=PUB/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
def main():
    # Preserve the initially generated prose before spacing/clarity edits.
    before=OUT/'backup/보고문_정리전';before.mkdir(parents=True,exist_ok=True)
    for rel in [f'{AN}/00_분석초안_읽기.md',f'{VE}/자체검수와_레드팀_보완.md',f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md']:
        src=PUB/rel;shutil.copy2(src,before/src.name)
    report=PUB/P/'05_결과보고/07_01-A2_작은예비분석_보고.md'
    report.write_text('''# 01-A2 결과 — 작은 실제 영상 예비 분석

2026-10-16 · 실행·자체검수·자체 레드팀·보완 재시험 완료. **사람 확인은 장헌 두 화면의 숫자 판독에 한정되며, 나머지는 미검수입니다.**

승인된 로컬 추출 방식으로 자료005 장헌과 자료013 EG-BIM 홈페이지를 순서대로 처리했습니다. 장헌 0~24초와 EG-BIM 0~15.5초에서 66개 이미지(59개 고유 시점)를 추출했습니다. 그중 장헌 14.5~18.5초와 EG-BIM 3~7초는 0.25초 간격으로 요청해 자세히 비교했습니다. 전체 영상이나 41개 자료의 성능 평가가 아닙니다.

## 확인한 내용

**장헌에서는 숫자 모션의 중간값과 이후 안정된 값을 구분했습니다.** 16초 화면의 매출 31억·48%는 중간값이고, 18초 화면에는 매출 39억·61%가 보입니다. 18초의 수주 55억·92%, 영업이익 5억·71%도 읽었습니다. 사용자는 두 화면의 제시 숫자 판독이 맞다고 답했습니다. 이 회신은 실제 회사 실적의 진위나 영상 전체의 승인으로 확대하지 않았습니다.

18초 값은 v4 문서 JH01 표와 일치합니다. v4는 완성 영상과 초기 기획서를 비교해 작성한 재구성 원고이므로 독립 정답이 아닙니다. 24초 화면은 JH02 표의 일부와 대응하지만, 문서의 프리캐스트 56%는 이 표본에 아직 보이지 않아 미확인으로 남겼습니다. 영상 전체에서 누락됐다고 판정하지 않았습니다.

**시나리오 없는 EG-BIM도 정상 경로로 처리했습니다.** 화면의 제목·설명문, 큰 E의 외관 변화, UI·도면·모델 이미지가 겹쳐 등장하는 순서를 관측 초안으로 기록했습니다. 새 대본을 만들거나 다른 홍보영상의 스토리보드를 사용하지 않았습니다. 작은 UI 글자와 실제 제품 성능, 정확한 모션 경로는 보류했습니다.

## 기술 검수와 실패

| 항목 | 확인한 결과와 한계 |
|---|---|
| 원본 식별 | 장헌은 90초·3840×1080, EG-BIM은 movie 헤더 기준 16.213333…초·3840×2160입니다. 선택 파일의 해시와 등록 경로를 고정했고 처리 전후 해시가 같습니다. |
| 시간 | 두 파일 모두 B-frame이 있습니다. MP4의 stts·ctts와 단일 rate-1 편집 목록을 직접 읽어, 디코드한 범위의 모든 표시 PTS와 대조했습니다. 장헌 원점 CTS는 1024/15360초, EG-BIM은 1000/60000초입니다. FPS×초로 프레임 번호를 만들지 않았습니다. |
| EG-BIM 길이 차이 | movie 헤더는 16.213333…초, video edit는 16.183333…초이며 PyAV container는 16.183333초를 보고했습니다. 0.03초 차이를 보존했습니다. 마지막 구간 재생이나 음성 동기를 검증한 것은 아닙니다. |
| 경로·리소스 | 자체 포함형 MP4와 등록된 두 경로만 허용했습니다. 외부 참조 거부와 시간·메모리·읽기·프레임·픽셀·출력 제한을 확인했습니다. 모든 적대적 파일이나 네이티브 취약점에 대한 보안 인증은 아닙니다. |
| 방향·SAR | 두 tkhd는 명시적 항등행렬이며 회전 없이 저장된 raster를 비례 축소했습니다. SAR 보고값 0/1은 미확인으로 남겼습니다. 표시비율과 정밀 좌표를 확정하지 않았습니다. |
| 음성 | 장헌은 AAC 44.1kHz mono, EG-BIM은 AAC 48kHz stereo 트랙이 있습니다. 청취·오디오 디코드·전사·영상과의 동기 검증은 하지 않았습니다. 실제 무음인지도 미확인입니다. |
| 실패 보존 | SAR 처리에서 두 차례 각각 두 파일이 중지됐고, 이어 장헌 SEI 부가정보 열거에서 오류가 났습니다. 실패 코드·로그·중간물을 보존하고 보완했습니다. 기록 생성 시 bundled Python에 jsonschema가 없는 오류도 보존했으며, 기존 Phase 00 검증 전용 환경으로 검사를 실행했습니다. 새 설치는 없습니다. |
| 재시험 | 기술 게이트 17항목을 확인했습니다. 보완 후 같은 조건으로 재추출한 66장의 이미지 해시·시각·프레임 순번이 모두 같습니다. 추출 재현성 확인이며 한국어 인식률이나 독립 성능 평가 수치가 아닙니다. |
| R4 | 기존 R4-1 검사기로 두 시간 기록의 형식·연결을 확인했습니다. 경계 오차 미상 등 미해결 항목은 장헌 33건, EG-BIM 35건으로 보존했습니다. 이는 결함 개수나 점수가 아닙니다. R4 통합 근거·공간 레코드의 이관은 완료하지 않았습니다. |

## 검수 상태와 남은 범위

장헌 두 화면의 제시 숫자는 실제 사용자 회신으로 한정 확인했습니다. 그 밖의 문구·수치·동작 초안과 EG-BIM 설명문은 사람 미검수입니다. 장헌 24초 이후와 EG-BIM 마지막 약 0.68초는 관찰하지 않았고, 선택한 표본 사이의 짧은 변화도 놓칠 수 있습니다. 66개 이미지를 모두 개별 확대 검토한 것은 아닙니다. 연락시트 네 장으로 개요를 읽고 핵심 PNG 여섯 장을 별도로 대조했습니다.

별도 AI API 호출과 전사는 각각 0건이고, 새 분석 스킬은 만들지 않았습니다. 현재 Codex에서 추출 화면을 읽었으므로 완전 오프라인 AI 분석은 아닙니다. 실제 호스트 모델 식별자와 내부 이미지 리사이즈 정보는 제공되지 않았습니다. 작성자 자체 레드팀을 수행했으며 독립 검토자나 별도 모델을 사용했다고 보고하지 않습니다.

A3·01-B·Phase 02와 기존 관리 스킬의 기본 전환은 착수하지 않았습니다. Phase 00 정본·봉인 보고와 원본 영상·문서를 수정하지 않았으며 AE·Computer Use 연결을 변경하지 않았습니다.

## 기록 위치

- [관측 초안과 실제 화면](../02_분석작업/01-A2_작은예비/00_분석초안_읽기.md)
- [자체검수·레드팀·보완](../04_검증자료/01-A2_작은예비/자체검수와_레드팀_보완.md)
- [사람 회신과 한정 확인 범위](../04_검증자료/01-A2_작은예비/사람확인_숫자판독_회신.json)
- [재추출 비교](../04_검증자료/01-A2_작은예비/보완후_재추출_비교.json)

중요한 검수 기록은 루트 작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2 아래에 기술·내용·보완으로 구분해 보존했습니다. 새 PDF는 만들지 않았습니다. 다음 검토 대상은 남은 내용 검수와 후속 A3 범위이며, 이번 숫자 확인을 후속 단계의 실행 승인으로 사용하지 않습니다.
''',encoding='utf-8')
    review=PUB/VE/'자체검수와_레드팀_보완.md'
    with review.open('a',encoding='utf-8') as f:f.write('\n후속 기록 생성 실패도 보존했다. bundled Python에서 jsonschema import가 실패했고, 기존 Phase 00/.환경 검증 전용 Python으로 R4-1 검사를 수행했다. 새 의존성 설치와 Phase 00 도구 변경은 없다. 장헌33/EG35개의 unresolved는 경계 오차 등 미확인 선언이며 오류 점수로 합산하지 않는다.\n')
    # Media artifacts and immutable actual execution paths.
    archived=[]
    for aid in ['자료005','자료013']:
        for phase in ['initial','detail','initial_retest','detail_retest']:
            for src in (OUT/'cases'/aid/phase).iterdir():
                rel=f'{AN}/{aid}/{phase}/{src.name}' if '_retest' not in phase else f'{BK}/재시험/{aid}/{phase}/{src.name}'
                copy(src,rel);archived.append({'execution_path':str(src),'archive_path':str(ROOT/rel),'sha256':sha(src)})
    j=PUB/AN/'보존위치_색인.json';write(j,archived)
    for name in ['입력고정과_컨테이너사전점검.json','문서본문_읽기전용추출.json','기준참조와_정정표검증.json']:
        copy(OUT/name,f'{AN}/{name}')
    copy(OUT/'사전게이트_시험.json',f'{VE}/사전게이트_시험.json')
    for src in (OUT/'backup').rglob('*'):
        if src.is_file():copy(src,f'{BK}/중간본과_실패/{src.relative_to(OUT/"backup").as_posix()}')
    for src in OUT.glob('*.py'):copy(src,f'{BK}/실행코드/{src.name}')
    for src in OUT.glob('run_*.json'):copy(src,f'{BK}/실행로그/{src.name}')
    for src in (OUT/'gate_tests').iterdir():copy(src,f'{BK}/게이트시험_합성자료/{src.name}')
    write(PUB/BK/'실패_추가기록.json',{'bundled_python_build_results_failure':{'exception':'ModuleNotFoundError: No module named jsonschema','action':'used existing Phase00/.환경/Scripts/python.exe for schema checks; -B -X utf8','new_install':False},'source_intermediate_copies':'중간본과_실패','scope':'all originally failed extraction attempt logs preserved; not removed from denominator'})
    deps={'schema_python':sys.executable,'schema_python_version':sys.version,'package_versions':{n:importlib.metadata.version(n) for n in ['jsonschema','referencing','attrs','rpds-py']},'extract_python':r'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe','extract_av':'19.0.1 isolated A1 runtime','new_packages_installed':False}
    write(PUB/VE/'실행환경_구분.json',deps)
    ai={'model_id':'host_not_exposed','separate_API_calls':0,'transcriptions':0,'image_processing':'current Codex model through local view_image','individual_PNGs':[str(OUT/'cases'/p) for p in ['자료005/initial/f_00480_016.000.png','자료005/initial/f_00540_018.000.png','자료005/initial/f_00720_024.000.png','자료005/detail/f_00495_016.500.png','자료013/initial/f_00240_004.000.png','자료013/initial/f_00930_015.500.png']],'contact_sheets':{'JH_initial':{'source':[1600,2040],'tool_display':[1405,1792]},'EG_initial':{'source':[1920,2340],'tool_display':[1440,1755]},'JH_detail':{'source':[1600,2295],'tool_display':[1312,1881]},'EG_detail':{'source':[1920,2340],'tool_display':[1440,1755]}},'internal_model_resize':'unknown','document_input':'read-only Word body paragraph XML and PPT slide body XML; no render/layout approval','image_scope':'66 selected frames viewed through 4 contact sheets; only 6 individual PNGs separately reviewed'}
    ai['individual_image_pins']=[{'path':p,'sha256':sha(Path(p))} for p in ai['individual_PNGs']]
    write(PUB/VE/'현재Codex_입력범위.json',ai)
    old=json.loads((ROOT/P/'00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8-sig'))
    copy(ROOT/P/'00_진행안내/01-A_계획상태.json',f'{BK}/변경전_안내/01-A_계획상태.json')
    old.update(version='0.4',state='A2_bounded_execution_reported_partial_human_confirmation',actual_media_analysis_runs=2,implementation_started=True,stage_A2_started=True,analyzer_implementation_started=False,company_media_opened_this_stage=2,human_content_reviews_pending=8,stage_A2_status='실행·자체레드팀·보완 재시험 보고. 장헌 두 화면 숫자 한정 확인, 나머지 사람 미검수',current_thread_media_work_stopped=True,next_decision='남은 내용 검수와 후속 범위 별도 검토; A3 자동 착수 없음')
    old.update(stage_A2_report=f'05_결과보고/07_01-A2_작은예비분석_보고.md',stage_A2_current_notice='00_진행안내/15_01-A2_실행결과_현재안내.json',human_content_reviews_pending_unit='claim groups, includes partially unreviewed fields; not error count',implementation_scope='A2용 제한 로컬 추출 보조 도구만. 분석 스킬 A3 미생성',stage_A2_primary_extraction_jobs=4,stage_A2_retest_extraction_jobs=4,stage_A2_images=66,stage_A2_unique_times=59,ground_truth_items=2,ground_truth_items_unit='user-confirmed frame numeric sets only, not independent generalization samples',human_content_review_record='04_검증자료/01-A2_작은예비/사람확인_숫자판독_회신.json',full_runtime_validation_completed=False,media_analysis_api_calls=0)
    write(PUB/P/'00_진행안내/01-A_계획상태.json',old)
    # Important reviews grouped by category, preserving originals and no PDF generation.
    important='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
    for category,names in {'기술검수':['사전게이트_시험.json','R4-1_규격검사_결과.json','실행환경_구분.json','현재Codex_입력범위.json'],'내용검수':['사람확인_숫자판독_회신.json','사람검수_대기.json'],'보완과_재시험':['자체검수와_레드팀_보완.md','보완후_재추출_비교.json']}.items():
        for name in names:copy(PUB/VE/name,f'{important}/{category}/{name}')
    # Read-only recheck of all pins created before work.
    refs=json.loads((OUT/'기준참조와_정정표검증.json').read_text(encoding='utf-8'))
    original_checks=[]
    for r in refs['refs']:original_checks.append({'path':r['path'],'unchanged':sha(ROOT/r['path'])==r['sha256']})
    for m in json.loads((OUT/'문서본문_읽기전용추출.json').read_text(encoding='utf-8')):original_checks.append({'path':m['path'],'unchanged':sha(Path(m['path']))==m['sha256']})
    for m in json.loads((OUT/'입력고정과_컨테이너사전점검.json').read_text(encoding='utf-8')):original_checks.append({'path':m['path'],'unchanged':sha(Path(m['path']))==m['sha256']})
    if not all(x['unchanged'] for x in original_checks):raise ValueError('source_modified')
    write(PUB/VE/'원본과_기준핀_재확인.json',original_checks)
    manifest=[]
    for src in sorted(PUB.rglob('*')):
        if src.is_file():manifest.append({'relative_path':src.relative_to(PUB).as_posix(),'sha256':sha(src),'bytes':src.stat().st_size})
    write(OUT/'게시명세.json',manifest)
    print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'original_pins_unchanged':all(x['unchanged'] for x in original_checks),'target_root':str(ROOT)},ensure_ascii=False))
if __name__=='__main__':main()
