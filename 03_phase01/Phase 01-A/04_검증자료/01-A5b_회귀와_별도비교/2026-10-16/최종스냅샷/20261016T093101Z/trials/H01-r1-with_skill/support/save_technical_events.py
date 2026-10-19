import json
from pathlib import Path
p=Path('phase01a-a5b/trials/H01-r1-with_skill/support/technical-events.json')
p.write_text(json.dumps([{'event':'extra1 board-1.jpg missing','impact':'PNG extraction succeeded; viewed direct PNG/crops instead','reported_to_parent':True},{'event':'skill-evidence-catalog.json exclusive create FileExistsError on refresh','impact':'existing catalog preserved; subsequent checker used stale catalog and reported 17 unregistered new frames/crops','resolution':'generate skill-evidence-catalog-final.json at new path before finish','reported_to_parent':True}],ensure_ascii=False,indent=2),encoding='utf-8')
