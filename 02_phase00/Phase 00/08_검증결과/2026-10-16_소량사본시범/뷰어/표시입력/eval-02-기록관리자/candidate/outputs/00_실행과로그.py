"""Run the bounded inspection/update/re-read as separate processes and log exact I/O."""
from pathlib import Path
import json
import os
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SCRIPT = OUT / '01_기록관리_실행.py'
records = []
prefix = sys.argv[1] + '_' if len(sys.argv) == 2 else ''
assert len(sys.argv) <= 2 and all(c.isalnum() or c == '_' for c in prefix)
for number, mode in enumerate(['inspect', 'update', 'verify'], 1):
    args = [sys.executable, '-B', '-X', 'utf8', str(SCRIPT), mode]
    result = subprocess.run(args, cwd=str(OUT), capture_output=True, env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}, check=False)
    stem = prefix + f'{number:02}_{mode}'
    for suffix, content in [('stdout.txt', result.stdout), ('stderr.txt', result.stderr)]:
        path = OUT / f'{stem}.{suffix}'
        assert not path.exists(), 'log collision'
        path.write_bytes(content)
    record = {'argv': args, 'cwd': str(OUT), 'exit_code': result.returncode, 'stdout_file': stem + '.stdout.txt', 'stderr_file': stem + '.stderr.txt', 'time_seconds': None, 'tokens': None}
    (OUT / f'{stem}.command.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    records.append(record)
    print(json.dumps(record, ensure_ascii=False))
    print(result.stdout.decode('utf-8', errors='replace'))
    if result.stderr:
        print(result.stderr.decode('utf-8', errors='replace'), file=sys.stderr)
    if result.returncode:
        break
(OUT / (prefix + '실행명령_종료목록.json')).write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
raise SystemExit(records[-1]['exit_code'])
