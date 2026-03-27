$runId = 23635453400
$done = $false
$attempt = 0
$maxAttempts = 10
$interval = 90

while (-not $done -and $attempt -lt $maxAttempts) {
    $attempt++
    $r = gh run view $runId --json status,conclusion,databaseId | ConvertFrom-Json
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "$ts [$attempt/$maxAttempts] status=$($r.status) conclusion=$($r.conclusion)"

    if ($r.status -eq "completed") {
        $done = $true
        Write-Host "=== RUN FINISHED: status=$($r.status) conclusion=$($r.conclusion) ==="
    } elseif ($attempt -lt $maxAttempts) {
        Write-Host "  -> sleeping $interval s ..."
        Start-Sleep -Seconds $interval
    } else {
        Write-Host "=== POLLING LIMIT REACHED: status=$($r.status) conclusion=$($r.conclusion) ==="
    }
}
