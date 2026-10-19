import json
from pathlib import Path
r=Path.cwd()/'phase01a-a4'
(r/'requests/A4-S-V06S_retest_extra.json').write_text(json.dumps([245.9,'7379/30']),'utf-8')
(r/'requests/A4-W-V06W_retest_extra.json').write_text(json.dumps(['7180/30','7181/30']),'utf-8')
