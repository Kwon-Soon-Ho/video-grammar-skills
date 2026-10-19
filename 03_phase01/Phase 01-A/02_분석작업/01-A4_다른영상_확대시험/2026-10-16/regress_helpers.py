from pathlib import Path
B=Path(__file__).resolve().parent
s=(B.parent/'phase01a-a3/test_helpers.py').read_text(encoding='utf-8')
a=s.index('B=Path(');b=s.index('def load(')
s=s[:a]+"B=Path(__file__).resolve().parent;S=B/'skill-draft3/scripts';version='A4-draft3'\n"+s[b:]
s=s.replace("log=B/'runs/setup/cases/자료013/T07/실행기록.json'","log=B.parent/'phase01a-a3/runs/setup/cases/자료013/T07/실행기록.json'")
exec(compile(s,__file__,'exec'))
