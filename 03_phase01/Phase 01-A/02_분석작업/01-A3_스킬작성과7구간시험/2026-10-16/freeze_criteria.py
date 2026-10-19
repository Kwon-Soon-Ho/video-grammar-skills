from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent;W=B/'company-video-grammar-analyzer-workspace'
R=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
p=R/'Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/채점전용/실패사례와_내용대조기준.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['version']='a3-1';d['a3_frozen_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['prior_criteria_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
d['required_known_failure_cases'].append({'case_id':'T07','failure_family':'UI内部選択の変化','reference_level':'AI_source_observation_not_human_gold','reference_receipt':None,'must_check':['外枠がほぼ固定の間にも内部の選択が変わることを識別','表の選択行が上から下へ順番に変わる','対応するサムネイル枠が左から右へ1→2→3→4と変わる','状態間の重なり/薄れを連続的な位置移動やスクロールと断定しない','選択状態の切替と位置の速度曲線を区別し、AEの補間値を捏造しない'],'reference_evidence':['8.2/8.6/9.5/10.4 native frames','8.3 and9.2 double row mixtures; setup/ui-detail.jpg'],'grading':'root visual source comparison, not human confirmation'})
# Korean assertions for user-facing viewer.
d['required_known_failure_cases'][-1].update(failure_family='UI 내부 선택 변화',must_check=['외곽이 거의 고정인 동안 내부 선택 상태 변화를 식별','표 선택행의 위→아래 순차 변경','썸네일 선택 테두리의 왼쪽→오른쪽 1→2→3→4 변경','상태 중첩/연해짐을 연속 위치 이동이나 스크롤로 단정하지 않음','선택 교체와 위치 가감속을 구분하고 AE 보간값을 만들지 않음'])
(W/'criteria-frozen.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for c in d['required_known_failure_cases']:
    p=W/'iteration-1'/('eval-'+c['case_id'])/'eval_metadata.json';m=json.loads(p.read_text(encoding='utf-8'));m['eval_name']=c['case_id']+' '+c['failure_family'];m['assertions']=c['must_check'];m['reference_level']=c['reference_level'];p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('criteria frozen before analysis outputs')
