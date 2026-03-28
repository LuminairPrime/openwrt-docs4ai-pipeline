[CmdletBinding()]
param(
    [string[]]$InputFiles,
    [string]$OutputDir,
    [string]$ArchiveRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Import-Module (Join-Path $scriptRoot 'archive-processing-common.psm1') -Force

if (-not $ArchiveRoot) {
    $ArchiveRoot = Join-Path $scriptRoot 'OpenWrt_Archives'
}

if (-not $OutputDir) {
    $OutputDir = Join-Path (Get-DefaultProcessedRoot -BaseDirectory $scriptRoot) 'parsed'
}

if (-not $InputFiles -or $InputFiles.Count -eq 0) {
    $InputFiles = Get-ChildItem -Path $ArchiveRoot -Recurse -Filter '*.txt' | ForEach-Object { $_.FullName }
}

$resolvedArchiveRoot = (Resolve-Path $ArchiveRoot).Path
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

$primaryMessages = [System.Collections.Generic.List[object]]::new()
$sidelinedMessages = [System.Collections.Generic.List[object]]::new()
$droppedMessages = [System.Collections.Generic.List[object]]::new()

$inputBytes = 0L
$parsedCount = 0
$keywordMatchedCount = 0

foreach ($inputFile in $InputFiles) {
    $resolvedInputFile = (Resolve-Path $inputFile).Path
    $rawText = Read-TextWithFallback -Path $resolvedInputFile
    $inputBytes += (Get-Item $resolvedInputFile).Length

    $messageBlocks = Split-MboxMessages -RawText $rawText
    foreach ($messageBlock in $messageBlocks) {
        $relativeSource = $resolvedInputFile.Substring($resolvedArchiveRoot.Length).TrimStart('\') -replace '\\', '/'
        $message = Convert-ArchiveMessage -SourceFile $relativeSource -MessageRecord $messageBlock
        $parsedCount += 1
        if ($message.has_keyword_match) {
            $keywordMatchedCount += 1
        }

        switch ($message.disposition) {
            'primary' { $primaryMessages.Add($message) }
            'sidelined' { $sidelinedMessages.Add($message) }
            default { $droppedMessages.Add($message) }
        }
    }
}

$primaryPath = Join-Path $OutputDir 'messages-primary.jsonl'
$sidelinedPath = Join-Path $OutputDir 'messages-sidelined.jsonl'
$droppedPath = Join-Path $OutputDir 'messages-dropped.jsonl'

Write-JsonLines -Path $primaryPath -Items $primaryMessages.ToArray()
Write-JsonLines -Path $sidelinedPath -Items $sidelinedMessages.ToArray()
Write-JsonLines -Path $droppedPath -Items $droppedMessages.ToArray()

$outputBytes = @($primaryPath, $sidelinedPath, $droppedPath) | Where-Object { Test-Path $_ } | ForEach-Object { (Get-Item $_).Length } | Measure-Object -Sum | Select-Object -ExpandProperty Sum

$stats = [ordered]@{
    stage = '1A-parse'
    archive_root = $resolvedArchiveRoot
    input_files = $InputFiles.Count
    input_bytes = $inputBytes
    messages_parsed = $parsedCount
    messages_kept = [ordered]@{
        primary = $primaryMessages.Count
        sidelined = $sidelinedMessages.Count
        dropped = $droppedMessages.Count
    }
    output_bytes = $outputBytes
    reduction_pct = if ($inputBytes -gt 0) { [math]::Round((1 - ($outputBytes / $inputBytes)) * 100, 1) } else { 0.0 }
    keyword_match_rate = if ($parsedCount -gt 0) { [math]::Round(($keywordMatchedCount / $parsedCount) * 100, 1) } else { 0.0 }
}

Write-StageStats -OutputDir $OutputDir -Stats $stats
Write-QASamples -OutputDir $OutputDir -Items $primaryMessages.ToArray() -Count 8
Write-StageReadme -OutputDir $OutputDir -Title 'OpenWrt Archive Parse Output' -Bullets @(
    'messages-primary.jsonl contains messages kept for downstream threading and scoring.',
    'messages-sidelined.jsonl contains low-priority but potentially interesting messages.',
    'messages-dropped.jsonl contains bot, notification, and obvious-noise messages.',
    'stats.json and samples.md are QA artifacts for parser validation.'
)

Write-Host "[parse] Input files: $($InputFiles.Count)" -ForegroundColor Cyan
Write-Host "[parse] Parsed messages: $parsedCount" -ForegroundColor Cyan
Write-Host "[parse] Primary: $($primaryMessages.Count) | Sidelined: $($sidelinedMessages.Count) | Dropped: $($droppedMessages.Count)" -ForegroundColor Cyan
Write-Host "[parse] Output directory: $OutputDir" -ForegroundColor Green