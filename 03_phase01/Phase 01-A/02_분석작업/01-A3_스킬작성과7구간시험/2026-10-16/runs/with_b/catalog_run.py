from pathlib import Path
import json,sys
root=Path.cwd();sys.path.insert(0,str(root/'phase01a-a3/company-video-grammar-analyzer/scripts'));from evidence_catalog import catalog
p=root/'phase01a-a3/runs/with_b'; files=[root/'phase01a-a2-retest/analysis_input/cases/자료005/T04/실행기록.json',root/'phase01a-a2-retest/analysis_input/cases/자료005/T05/실행기록.json',root/'phase01a-a2-retest/analysis_input/cases/자료013/T06/실행기록.json',root/'phase01a-a3/runs/setup/cases/자료013/T07/실행기록.json']+list((p/'cases').glob('*/*/실행기록.json'))
d=catalog(files);(p/'evidence_catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');print('catalog passed',len(d['frames']))
