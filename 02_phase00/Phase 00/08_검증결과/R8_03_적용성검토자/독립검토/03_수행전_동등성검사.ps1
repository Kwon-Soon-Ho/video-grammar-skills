$ErrorActionPreference = 'Stop'
$taskWorkspace = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-guidance-reviewer-workspace'
$taskDb = 'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00'
$taskAuditRoot = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_03_독립검토'
function Get-TaskDigest([string]$LiteralPath) { return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant() }
function Get-TaskMap([string]$Root) {
    $taskMap = @{}
    Get-ChildItem -LiteralPath $Root -Recurse -File | ForEach-Object {
        $taskRel = $_.FullName.Substring($Root.Length+1).Replace('\','/')
        $taskMap[$taskRel] = Get-TaskDigest $_.FullName
    }
    return $taskMap
}
$taskFreeze = Get-Content -LiteralPath ($taskWorkspace+'\평가기준_고정기록.json') -Raw | ConvertFrom-Json
$taskScope = Get-Content -LiteralPath ($taskWorkspace+'\수행자료_포함과분리.json') -Raw | ConvertFrom-Json
$taskCriteria = Get-Content -LiteralPath ($taskWorkspace+'\평가항목.json') -Raw | ConvertFrom-Json
$taskSourceMismatches = @()
foreach ($taskSource in $taskScope.included_source_hashes.PSObject.Properties) {
    if ((Get-TaskDigest ($taskDb+'\'+$taskSource.Name)) -ne $taskSource.Value) { $taskSourceMismatches += $taskSource.Name }
}
$taskPairs = @()
foreach ($taskCase in (Get-ChildItem -LiteralPath ($taskWorkspace+'\iteration-1') -Directory | Sort-Object Name)) {
    $taskOld = $taskCase.FullName+'\old_skill\run-1'
    $taskNew = $taskCase.FullName+'\new_skill\run-1'
    $taskOldMap = Get-TaskMap ($taskOld+'\inputs\Phase00')
    $taskNewMap = Get-TaskMap ($taskNew+'\inputs\Phase00')
    $taskOldCommon = @($taskOldMap.Keys | Where-Object { $_ -notlike '실행스킬/*' } | Sort-Object)
    $taskNewCommon = @($taskNewMap.Keys | Where-Object { $_ -notlike '실행스킬/*' } | Sort-Object)
    $taskMismatch = @()
    $taskSourceCopyMismatches = @()
    foreach ($taskSource in $taskScope.included_source_hashes.PSObject.Properties) {
        if (!$taskOldMap.ContainsKey($taskSource.Name) -or $taskOldMap[$taskSource.Name] -ne $taskSource.Value) { $taskSourceCopyMismatches += $taskSource.Name }
    }
    foreach ($taskRel in (@($taskOldCommon+$taskNewCommon) | Sort-Object -Unique)) {
        if (!$taskOldMap.ContainsKey($taskRel) -or !$taskNewMap.ContainsKey($taskRel) -or $taskOldMap[$taskRel] -ne $taskNewMap[$taskRel]) { $taskMismatch += $taskRel }
    }
    $taskFixtureErrors = @()
    $taskPreparationErrors = @()
    foreach ($taskRun in @($taskOld,$taskNew)) {
        $taskCurrent = if ($taskRun -eq $taskOld) { $taskOldMap } else { $taskNewMap }
        $taskFixture = Get-Content -LiteralPath ($taskRun+'\fixture_before.json') -Raw | ConvertFrom-Json
        $taskRecorded = @($taskFixture.files.PSObject.Properties)
        if ($taskCurrent.Count -ne $taskRecorded.Count) { $taskFixtureErrors += $taskRun+':count' }
        foreach ($taskEntry in $taskRecorded) {
            if (!$taskCurrent.ContainsKey($taskEntry.Name) -or $taskCurrent[$taskEntry.Name] -ne $taskEntry.Value) { $taskFixtureErrors += $taskRun+':'+$taskEntry.Name }
        }
        $taskDispatch = Get-Content -LiteralPath ($taskRun+'\dispatch.json') -Raw | ConvertFrom-Json
        if ($taskDispatch.status -ne 'prepared_not_dispatched' -or $taskDispatch.actual_model_trial -ne $false) { $taskPreparationErrors += $taskRun+':dispatch' }
        if ((Get-ChildItem -LiteralPath ($taskRun+'\outputs') -File -ErrorAction SilentlyContinue).Count -gt 0) { $taskPreparationErrors += $taskRun+':outputs_not_empty' }
    }
    $taskOldText = (Get-Content -LiteralPath ($taskOld+'\task.txt') -Raw).Replace($taskOld,'<RUN>')
    $taskNewText = (Get-Content -LiteralPath ($taskNew+'\task.txt') -Raw).Replace($taskNew,'<RUN>')
    $taskCaseId = [int]($taskCase.Name.Substring(5,2))
    $taskMetadata = Get-Content -LiteralPath ($taskCase.FullName+'\eval_metadata.json') -Raw | ConvertFrom-Json
    $taskAssertionList = $taskCriteria.cases.PSObject.Properties[[string]$taskCaseId].Value.expectations
    $taskPairs += [ordered]@{
        case = $taskCase.Name
        common_old_count = $taskOldCommon.Count
        common_new_count = $taskNewCommon.Count
        common_mismatches = $taskMismatch
        copied_source_mismatches = $taskSourceCopyMismatches
        normalized_task_equal = ($taskOldText -ceq $taskNewText)
        old_skill_files = @($taskOldMap.Keys | Where-Object { $_ -like '실행스킬/*' } | Sort-Object)
        new_skill_files = @($taskNewMap.Keys | Where-Object { $_ -like '실행스킬/*' } | Sort-Object)
        fixture_mismatches = $taskFixtureErrors
        preparation_errors = $taskPreparationErrors
        assertions_count = @($taskAssertionList).Count
        metadata_assertions_equal = ((ConvertTo-Json -InputObject @($taskAssertionList) -Compress) -ceq (ConvertTo-Json -InputObject @($taskMetadata.assertions) -Compress))
    }
}
$taskTransformChecks = @()
foreach ($taskTransform in $taskScope.transforms) {
    $taskSourcePath = $taskDb+'\'+$taskTransform.source
    $taskSourceText = Get-Content -LiteralPath $taskSourcePath -Raw
    $taskFirstInput = ($taskWorkspace+'\iteration-1\eval-01-한국어_수치_무음과_부분판정\old_skill\run-1\inputs\Phase00\')+$taskTransform.source
    $taskExcerpt = Get-Content -LiteralPath $taskFirstInput -Raw
    $taskChunks = [regex]::Matches($taskSourceText,'(?ms)^## ([^\r\n]+)\r?\n(.*?)(?=^## |\z)')
    $taskExpectedChunks = foreach ($taskHeading in $taskTransform.included_headings) { @($taskChunks | Where-Object { $_.Groups[1].Value.Trim() -eq $taskHeading }) }
    $taskTransformChecks += [ordered]@{
        source = $taskTransform.source
        source_hash_matches = ((Get-TaskDigest $taskSourcePath) -eq $taskTransform.original_sha256)
        output_hash_matches = ((Get-TaskDigest $taskFirstInput) -eq $taskTransform.output_sha256)
        expected_heading_count = @($taskTransform.included_headings).Count
        actual_headings = @([regex]::Matches($taskExcerpt,'(?m)^## ([^\r\n]+)') | ForEach-Object { $_.Groups[1].Value.Trim() })
        selected_original_sections_present = (@($taskExpectedChunks | Where-Object { !$taskExcerpt.Contains($_.Value.Trim()) }).Count -eq 0)
        creator_section_present = $taskExcerpt.Contains('## Anthropic Skill Creator')
    }
}
$taskResult = [ordered]@{
    review_type = 'pre_dispatch_static_fairness_check_not_model_trial'
    criteria_hash = Get-TaskDigest ($taskWorkspace+'\평가항목.json')
    criteria_hash_matches_freeze = ((Get-TaskDigest ($taskWorkspace+'\평가항목.json')) -eq $taskFreeze.criteria_sha256)
    evals_file = 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-guidance-reviewer\evals\evals.json'
    evals_hash_matches_freeze = ((Get-TaskDigest 'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-guidance-reviewer\evals\evals.json') -eq $taskFreeze.evals_sha256)
    included_source_files_checked = @($taskScope.included_source_hashes.PSObject.Properties).Count
    included_source_mismatches = $taskSourceMismatches
    pairs = $taskPairs
    source_excerpt_checks = $taskTransformChecks
    actual_model_trials_executed_by_this_audit = 0
    limits = @('instruction-based isolation only','generic evaluation references remain in original knowledge/index text','knowledge-assisted development comparison, not unseen generalization or isolated skill effect')
}
$taskResult | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath ($taskAuditRoot+'\03_수행전_동등성검사.json') -Encoding utf8
$taskResult | ConvertTo-Json -Depth 12
