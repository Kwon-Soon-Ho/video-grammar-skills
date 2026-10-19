from pathlib import Path
import json
import os
import subprocess
import sys

OUT = Path(__file__).resolve().parent
args = [sys.executable, '-B', '-X', 'utf8', str(OUT / '02_보고서작성.py')]
assert not (OUT / '04_finalize.command.json').exists()
result = subprocess.run(args, cwd=OUT, capture_output=True, env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}, check=False)
(OUT / '04_finalize.stdout.txt').write_bytes(result.stdout)
(OUT / '04_finalize.stderr.txt').write_bytes(result.stderr)
command = {'argv': args, 'cwd': str(OUT), 'exit_code': result.returncode, 'stdout_file': '04_finalize.stdout.txt', 'stderr_file': '04_finalize.stderr.txt', 'time_seconds': None, 'tokens': None}
(OUT / '04_finalize.command.json').write_text(json.dumps(command, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(command, ensure_ascii=False))
print(result.stdout.decode('utf-8', errors='replace'))
if result.stderr:
    print(result.stderr.decode('utf-8', errors='replace'), file=sys.stderr)
raise SystemExit(result.returncode)
