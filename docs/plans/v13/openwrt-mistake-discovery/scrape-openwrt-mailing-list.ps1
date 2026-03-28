<#
.SYNOPSIS
Hardened OpenWrt Archive Scraper.
Fixes .NET absolute pathing and catches silent HTTP download failures.
#>

# 1. Force absolute path resolution to prevent .NET directory desync
$BaseDir = Join-Path (Get-Location).ProviderPath "OpenWrt_Archives"

$Lists = @{
    "bugs"  = "https://lists.openwrt.org/pipermail/openwrt-bugs/"
    "devel" = "https://lists.openwrt.org/pipermail/openwrt-devel/"
}

foreach ($List in $Lists.GetEnumerator()) {
    $OutFolder = Join-Path $BaseDir $List.Name
    $null = New-Item -ItemType Directory -Path $OutFolder -Force
    
    Write-Host "Fetching index for $($List.Name)..." -ForegroundColor Cyan
    try {
        $html = (Invoke-WebRequest -Uri $List.Value -UseBasicParsing -ErrorAction Stop).Content
    } catch {
        Write-Warning "Failed to access $($List.Value). Skipping list."
        continue
    }

    $regex = 'href="((202[3-9]|[2-9]\d{3})-[a-zA-Z]+\.(txt\.gz|zip))"'
    $matches = [regex]::Matches($html, $regex)

    foreach ($m in $matches) {
        $fileName = $m.Groups[1].Value
        $ext = $m.Groups[3].Value
        
        $downloadUrl = "$($List.Value)$fileName"
        $archivePath = Join-Path $OutFolder $fileName
        $extractPath = Join-Path $OutFolder ($fileName -replace '\.(txt\.gz|zip)$', '.txt')

        if (Test-Path -LiteralPath $extractPath) { 
            Write-Host "Skipping $fileName (already extracted)" -ForegroundColor DarkGray
            continue 
        }

        Write-Host "Downloading $fileName..."
        try {
            # 2. Strict error action: Abort if the file 404s or fails to route
            Invoke-WebRequest -Uri $downloadUrl -OutFile $archivePath -UseBasicParsing -ErrorAction Stop
        } catch {
            Write-Warning "Download failed for ${fileName}: $($_.Exception.Message)"
            continue # Skip to the next file
        }

        # 3. Final sanity check before handing off to .NET
        if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) {
            Write-Warning "File $archivePath missing from disk. Skipping extraction."
            continue
        }

        Write-Host "Extracting $fileName..."
        try {
            if ($ext -eq 'txt.gz') {
                $inFile = [System.IO.File]::OpenRead($archivePath)
                $outFile = [System.IO.File]::Create($extractPath)
                $gzip = New-Object System.IO.Compression.GZipStream($inFile, [System.IO.Compression.CompressionMode]::Decompress)
                
                try {
                    $gzip.CopyTo($outFile)
                } finally {
                    if ($null -ne $gzip) { $gzip.Dispose() }
                    if ($null -ne $outFile) { $outFile.Dispose() }
                    if ($null -ne $inFile) { $inFile.Dispose() }
                }
                Remove-Item -LiteralPath $archivePath -Force
            } 
            elseif ($ext -eq 'zip') {
                Expand-Archive -Path $archivePath -DestinationPath $OutFolder -Force
                Remove-Item -LiteralPath $archivePath -Force
            }
        } catch {
            Write-Warning "Failed to extract $fileName. Exception: $_"
        }
    }
}

Write-Host "Archive scraping complete." -ForegroundColor Green