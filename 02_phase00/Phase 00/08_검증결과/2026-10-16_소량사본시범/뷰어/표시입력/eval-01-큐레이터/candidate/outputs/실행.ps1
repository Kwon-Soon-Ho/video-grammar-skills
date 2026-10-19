param([Parameter(Mandatory=$true)][string]$ScriptName, [Parameter(Mandatory=$true)][string]$LogName)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$PythonExe = 'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe'
$OutputDir = $PSScriptRoot
$ScriptPath = Join-Path -Path $OutputDir -ChildPath $ScriptName
$StdoutPath = Join-Path -Path $OutputDir -ChildPath ($LogName + '.stdout.txt')
$StderrPath = Join-Path -Path $OutputDir -ChildPath ($LogName + '.stderr.txt')
$CommandPath = Join-Path -Path $OutputDir -ChildPath ($LogName + '.실행.json')
$Utf8 = New-Object System.Text.UTF8Encoding($false)
& $PythonExe -B $ScriptPath 1> $StdoutPath 2> $StderrPath
$RunExit = $LASTEXITCODE
$Record = [ordered]@{
    executable = $PythonExe
    arguments = @('-B', $ScriptPath)
    cwd = (Get-Location).Path
    environment = @{PYTHONUTF8='1'; PYTHONIOENCODING='utf-8'; PYTHONDONTWRITEBYTECODE='1'}
    stdout = $StdoutPath
    stderr = $StderrPath
    exit_code = $RunExit
}
[System.IO.File]::WriteAllText($CommandPath, ($Record | ConvertTo-Json -Depth 8), $Utf8)
$LogRecord = 'COMMAND: ' + $PythonExe + ' -B ' + $ScriptPath + "`nEXIT: " + $RunExit + "`nSTDOUT: " + $StdoutPath + "`nSTDERR: " + $StderrPath + "`n"
[System.IO.File]::AppendAllText((Join-Path $OutputDir 'transcript.txt'), $LogRecord, $Utf8)
Get-Content -LiteralPath $StdoutPath -Raw
if ((Get-Item -LiteralPath $StderrPath).Length -gt 0) { Get-Content -LiteralPath $StderrPath -Raw }
exit $RunExit
