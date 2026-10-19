"""현재 통합 회귀 검사 별칭. 과거 v0.1 시험은 구형_v0.1_ 접두어 파일에 보존.
독립 레드팀 결과와 구분한다. 실제 영상/승인 검사 아님.
"""
from pathlib import Path
import json,importlib.util
BASE=Path(__file__).resolve().parents[1]
def load(path):
 s=importlib.util.spec_from_file_location('current_regression',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 tests=load(BASE/'07_실행도구/통합기록_규격시험.py');checker=load(BASE/'07_실행도구/통합기록_규격검사.py')
 result=tests.run(checker,json.loads((BASE/'04_기록규격/통합최소기록_스키마_v0.2.json').read_text(encoding='utf-8')))
 print(json.dumps({'count':result['count'],'passed':result['passed'],'all_passed':result['all_passed'],'source':'통합기록_규격시험.py','scope':'같은 통합 회귀의 진입점 별칭. 별도 독립 시험 개수로 합산하지 않음.'},ensure_ascii=False))
 return 0 if result['all_passed'] else 1
if __name__=='__main__':raise SystemExit(main())
