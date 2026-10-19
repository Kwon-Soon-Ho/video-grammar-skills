"""최종 레드팀 회귀 검사. D 자료를 읽고 메모리 복사만 검사한다.

출력 파일·영상·외부 통신을 사용하지 않는다. 검수 결정은 read 함수를
일시 대체하여 메모리에 주입하고 즉시 복원한다. 실제 사람 승인이 아니다.
"""
from pathlib import Path
import copy
import importlib.util
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('최종검토_자료검증', BASE / '07_실행도구/구형기록_보존검사.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
base = validator.read('04_기록규격/설명용_단계구성_예시.json')
tests = []


def actual_record():
    """원본 내용 검증이 아닌 관계 검사에 필요한 가상 구조 fixture."""
    r = copy.deepcopy(base)
    r['asset'].update(source_type='internal', path='fixture-only.mp4', sha256='0' * 64, duration_s=10)
    s = r['segments'][0]
    s.update(kind='continuous_scene', period={'start_s': 0, 'end_s': 1,
             'time_basis': 'presentation_timeline', 'uncertainty_s': 0.01})
    s['beats'] = []
    s['frames'] = [{'id': 'FIXTURE-FRAME-001', 'kind': 'extracted', 'path': 'fixture-only.png',
                    'source_pts': 0, 'time_base': {'num': 1, 'den': 24},
                    'source_frame_ordinal': 0, 'requested_s': 0, 'actual_s': 0,
                    'transform_ref': None}]
    r['scenario_segments'][0]['kind'] = 'original_scenario'
    e = r['evidence'][0]
    e.update(kind='frame', locator='fixture-only.png', target_id='FIXTURE-FRAME-001',
             sha256='0' * 64, period=copy.deepcopy(s['period']))
    r['claims'][0].update(support_mode='rendered_observation', measurement=None)
    return r


def case(name, edit, expected_valid=False, decision_edit=None):
    r = actual_record()
    edit(r)
    original_read = validator.read
    if decision_edit is not None:
        r['review'].update(state='approved', reviewer='fixture human reviewer',
                           reviewed_at='2026-10-14T00:00:00Z', object_version=r['version'],
                           approved_scope='structural fixture review',
                           approval_kind='structural_review', decision_ref='FIXTURE-DECISION-001',
                           evidence_versions={e['id']: e['version'] for e in r['evidence']})
        decision = {'id': 'FIXTURE-DECISION-001', 'state': 'approved',
                    'object_id': r['record_id'], 'object_version': r['version'],
                    'approval_kind': r['review']['approval_kind'],
                    'reviewer': r['review']['reviewer'], 'reviewed_at': r['review']['reviewed_at'],
                    'approved_scope': r['review']['approved_scope']}
        decision_edit(decision)

        def memory_read(rel):
            if rel == '05_출처와검토/검수결정.json':
                return {'version': '0.1.0', 'decisions': [decision]}
            return original_read(rel)
        validator.read = memory_read
    try:
        errors = validator.validate_record(r)
        tests.append({'name': name, 'expected_valid': expected_valid,
                      'actual_valid': not errors, 'passed': (not errors) == expected_valid,
                      'evidence': errors})
    except Exception as exc:
        tests.append({'name': name, 'expected_valid': expected_valid,
                      'actual_valid': None, 'passed': False,
                      'evidence': ['검증기 예외: ' + repr(exc)]})
    finally:
        validator.read = original_read


case('관측 구조 fixture 정상', lambda r: None, True)


def wrong_scenario(r):
    r['claims'][0]['support_mode'] = 'scenario_supported'
    r['evidence'][0].update(kind='design_profile', target_id=None)


def valid_scenario(r):
    r['claims'][0]['support_mode'] = 'scenario_supported'
    r['evidence'][0].update(kind='script', target_id=r['scenario_segments'][0]['id'])


case('시나리오 주장에 디자인 프로필만 근거로 사용 차단', wrong_scenario)
case('시나리오 주장에 실제 script 대상 연결 허용', valid_scenario, True)


def bad_scenario_target(r):
    valid_scenario(r)
    r['evidence'][0]['target_id'] = 'MISSING-SCENARIO'


case('script 근거의 없는 시나리오 대상 차단', bad_scenario_target)


def numerical(r):
    r['claims'][0].update(support_mode='numerical_estimate', measurement={
        'method': 'fixture bounding-box width measurement',
        'quantity': 'apparent_width', 'unit': 'px', 'value': 115,
        'uncertainty': 2, 'source_frame_refs': ['FIXTURE-FRAME-001'],
        'limitations': 'fixture only; does not recover AE Scale',
        'assumptions': ['same coordinate space']})


case('수치 추정 구조 fixture 정상', numerical, True)


def all_null_measurement(r):
    numerical(r)
    r['claims'][0]['measurement'].update(method=None, quantity=None, unit=None,
                                          value={'invented': True}, uncertainty=None,
                                          limitations=None, assumptions=[])


case('키만 존재하고 내용이 null/임의 객체인 수치 추정 차단', all_null_measurement)


def empty_unit(r):
    numerical(r)
    r['claims'][0]['measurement']['unit'] = '   '


case('수치 추정의 공백 단위 차단', empty_unit)


def non_numeric_value(r):
    numerical(r)
    r['claims'][0]['measurement']['value'] = '정확히 115였음'


case('수치 추정 값이 수치 아닌 문장일 때 차단', non_numeric_value)
case('승인 상태/시각이 일치하는 메모리 결정 정상', lambda r: None, True,
     decision_edit=lambda d: None)
case('rejected 결정을 approved 기록 근거로 쓰기 차단', lambda r: None,
     decision_edit=lambda d: d.update(state='rejected'))
case('stale 결정을 approved 기록 근거로 쓰기 차단', lambda r: None,
     decision_edit=lambda d: d.update(state='stale'))
case('검수 결정과 승인 기록 시각 불일치 차단', lambda r: None,
     decision_edit=lambda d: d.update(reviewed_at='2026-10-13T00:00:00Z'))
case('시각 없는 검수 결정을 approved 근거로 쓰기 차단', lambda r: None,
     decision_edit=lambda d: d.pop('reviewed_at'))

result = {'tests': tests, 'passed': sum(t['passed'] for t in tests), 'total': len(tests),
          'scope': '메모리 내 자료 관계 회귀검사. 실제 영상·측정·사람 승인 아님. D 파일 변경 없음.'}
print(json.dumps(result, ensure_ascii=False, indent=2))
if result['passed'] != result['total']:
    raise SystemExit(1)
