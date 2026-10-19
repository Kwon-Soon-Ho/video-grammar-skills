"""Phase 00 read-only re-audit: catalog reads, then memory-only fixtures.

No video/file truth is asserted. Fixture paths and hashes are deliberately fake.
Run with Phase 00/.환경/Scripts/python.exe -B. This script writes no files.
"""
from pathlib import Path
import argparse
import copy
import importlib.util
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser()
parser.add_argument('--phase00-root', type=Path, default=Path(
    'D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00'))
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('phase00_reaudit_validator',
    args.phase00_root / '07_실행도구/자료검증.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

example = validator.read('04_기록규격/설명용_단계구성_예시.json')
fixture = copy.deepcopy(example)
fixture['asset'].update(source_type='internal', path='fixture-only.mp4',
    sha256='0' * 64, duration_s=10, metadata={})
segment = fixture['segments'][0]
segment.update(kind='continuous_scene', period={'start_s': 0, 'end_s': 1,
    'time_basis': 'presentation_timeline', 'uncertainty_s': 0.01})
segment['beats'] = []
segment['frames'] = [{'id': 'REAUDIT-FRAME', 'kind': 'extracted',
    'path': 'fixture-only.png', 'source_pts': 0,
    'time_base': {'num': 1, 'den': 24}, 'source_frame_ordinal': 0,
    'requested_s': 0, 'actual_s': 0, 'transform_ref': None}]
fixture['scenario_segments'][0]['kind'] = 'original_scenario'
fixture['evidence'][0].update(kind='frame', locator='fixture-only.png',
    target_id='REAUDIT-FRAME', sha256='0' * 64,
    period=copy.deepcopy(segment['period']))
fixture['claims'][0].update(support_mode='rendered_observation', measurement=None)

tests = []
def case(name, edit, expected_valid):
    record = copy.deepcopy(fixture)
    edit(record)
    errors = validator.validate_record(record)
    tests.append({'name': name, 'expected_valid': expected_valid,
        'actual_valid': not errors, 'gap_reproduced': (not errors) != expected_valid,
        'errors': errors})

case('normal memory fixture', lambda record: None, True)
case('frame actual_s=100 exceeds asset duration_s=10',
    lambda record: record['segments'][0]['frames'][0].update(actual_s=100), False)
case('frame actual_s=2 exceeds containing segment end_s=1',
    lambda record: record['segments'][0]['frames'][0].update(actual_s=2), False)
case('evidence period start_s=9 exceeds end_s=1',
    lambda record: record['evidence'][0].update(period={'start_s': 9, 'end_s': 1,
        'time_basis': 'presentation_timeline', 'uncertainty_s': 0}), False)
case('evidence period end_s=100 exceeds asset duration_s=10',
    lambda record: record['evidence'][0].update(period={'start_s': 0, 'end_s': 100,
        'time_basis': 'presentation_timeline', 'uncertainty_s': 0}), False)

print(json.dumps({'scope': 'Read-only catalogs and memory-only fictional structural fixtures; '
    'no video analysis, file-content verification, approval, or D writes.',
    'catalog_errors': validator.validate_catalogs(),
    'current_example_errors': validator.validate_record(example),
    'fixture': fixture, 'tests': tests}, ensure_ascii=False, indent=2))
