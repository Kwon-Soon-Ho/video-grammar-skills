from pathlib import Path
import importlib.util
ROOT=Path('D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
OUT=Path('C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\analysis-reliability-20261019\\fresh')
spec=importlib.util.spec_from_file_location('gate_reference',Path('C:\\Users\\User\\Documents\\ChatGPT\\업무@사내 영상 생성기\\phase01a-a5a\\candidate\\tool\\prepare.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sha=module.sha;write=module.write;preflight=module.preflight
