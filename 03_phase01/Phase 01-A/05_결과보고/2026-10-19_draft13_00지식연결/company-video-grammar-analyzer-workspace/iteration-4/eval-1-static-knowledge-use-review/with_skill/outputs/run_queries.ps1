$python = 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$tool = 'C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer/scripts/knowledge_links.py'
$catalog = Join-Path $PSScriptRoot 'knowledge-catalog.json'
$index = Join-Path $PSScriptRoot 'knowledge-use-index.json'
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '업무 이미지'
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '건물/기단'
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '역할판'
& $python -B -X utf8 $tool query --catalog $catalog --index $index --id LAYOUT-SPACE-CALLOUT
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query 'RC-COMP-002@v1'
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '조사' --motion-only
& $python -B -X utf8 $tool query --catalog $catalog --index $index --query '조사' --include-unobserved
