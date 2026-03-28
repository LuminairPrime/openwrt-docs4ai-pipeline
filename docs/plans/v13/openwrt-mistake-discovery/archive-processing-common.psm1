Set-StrictMode -Version Latest

$script:MboxBoundaryRegex = '(?m)^From\s+\S+(?:@\S+|\s+at\s+\S+)\s{2}\w{3}\s+\w{3}\s{1,2}\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}\s*$'

$script:KeywordPatterns = @(
    'error:', 'warning:', 'fail(?:ed|ure|ing)?', 'broken', 'regression', 'crash',
    'segfault', 'panic', 'oops', 'backtrace', 'bug', 'should\s+(?:use|be|have|call)',
    'instead\s+of', 'proper(?:ly)?', 'correct(?:ly)?', 'wrong', 'incorrect',
    'mistake', 'typo', 'you\s+need\s+to', 'you\s+must', 'do\s+not|don''t',
    'better\s+(?:to|way|approach)', 'right\s+way', 'memory\s+leak',
    'use[-.\s]after[-.\s]free', 'double\s+free', 'null[-.\s]pointer',
    'buffer[-.\s]overflow', 'heap', 'stack\s+overflow', 'uninitialized',
    'out[-.\s]of[-.\s]bounds', 'undefined\s+behavior', 'race[-.\s]condition',
    'deadlock', 'mutex', 'lock(?:ing)?', 'atomic', 'thread[-.\s]safe', 'synchroniz',
    'CFLAGS', 'LDFLAGS', 'Makefile', 'PKG_', 'compile', 'linker',
    'undefined\s+reference', 'implicit\s+declaration', '-Werror', '-Wno-',
    'out[-.\s]of[-.\s]tree', 'kmod', 'ubus', 'uci', 'procd', 'netifd',
    'hotplug', 'rpcd', 'luci', 'uhttpd', 'libubox', 'ustream', 'blobmsg',
    'init\.d', 'rc\.d', '\[PATCH\s+v[2-9]', 'Fixes:', 'inline', 'static',
    'volatile', 'const', 'malloc', 'calloc', 'realloc', 'free\(', 'strlen',
    'strcpy', 'strncpy', 'snprintf', 'sprintf', 'socket', 'bind\(', 'ioctl', 'netlink'
)

$script:CategoryPatterns = [ordered]@{
    'memory-management' = 'malloc|calloc|realloc|free\(|memory\s+leak|use[-.\s]after[-.\s]free|double\s+free|null[-.\s]pointer|buffer[-.\s]overflow|heap|segfault'
    'concurrency' = 'thread|mutex|lock(?:ing)?|race[-.\s]condition|deadlock|atomic|synchron'
    'build-system' = 'Makefile|PKG_|CONFIG_|compile|linker|CFLAGS|LDFLAGS|kmod|out[-.\s]of[-.\s]tree|-Werror|-Wno-'
    'c-language' = 'inline|static\s+.*void|implicit\s+declaration|undefined\s+behavior|cast|const|volatile|gcc|musl'
    'uci-config' = 'uci[_\s]|/etc/config|uci\.batch|uci-defaults|option|config\s+\w+'
    'procd-init' = 'procd|init\.d|rc\.d|respawn|service|procd_set_param|procd_close_instance'
    'networking' = 'netifd|firewall|nftables|iptables|bridge|vlan|interface|socket|netlink|bind\('
    'ubus-ipc' = 'ubus|blobmsg|libubox|ustream|uloop'
    'luci-frontend' = 'luci|uhttpd|rpcd|cbi|\.js|javascript|rpc'
    'kernel-driver' = 'kmod|dts|device[-.\s]tree|kernel|insmod|modprobe|module_init'
    'patch-maintenance' = 'bump|upstream|obsolete|remove.*patch|supersed|cherry[-.\s]pick|backport'
    'package-packaging' = 'ipk|opkg|feed|PKG_SOURCE|PKG_HASH|PKG_VERSION'
}

function Get-DefaultProcessedRoot {
    param(
        [string]$BaseDirectory
    )

    return Join-Path $BaseDirectory 'OpenWrt_Archives_Processed_Small'
}

function Read-TextWithFallback {
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    $utf8NoBom = [System.Text.UTF8Encoding]::new($false, $true)
    try {
        return [System.IO.File]::ReadAllText($Path, $utf8NoBom)
    }
    catch {
        $latin1 = [System.Text.Encoding]::GetEncoding('iso-8859-1')
        return [System.IO.File]::ReadAllText($Path, $latin1)
    }
}

function Split-MboxMessages {
    param(
        [Parameter(Mandatory)]
        [string]$RawText
    )

    $matches = [regex]::Matches($RawText, $script:MboxBoundaryRegex, 'Multiline')
    $messages = [System.Collections.Generic.List[object]]::new()

    if ($matches.Count -eq 0) {
        return $messages
    }

    for ($index = 0; $index -lt $matches.Count; $index++) {
        $start = $matches[$index].Index
        $end = if ($index + 1 -lt $matches.Count) { $matches[$index + 1].Index } else { $RawText.Length }
        $text = $RawText.Substring($start, $end - $start)
        $messages.Add([pscustomobject]@{
                from_line = $matches[$index].Value.TrimEnd()
                byte_offset = $start
                text = $text
            })
    }

    return $messages
}

function Split-MessageBlock {
    param(
        [Parameter(Mandatory)]
        [string]$MessageText
    )

    $withoutBoundary = $MessageText -replace '^[^\r\n]+(?:\r?\n)', ''
    $boundaryMatch = [regex]::Match($withoutBoundary, '(?:\r?\n){2}')

    if (-not $boundaryMatch.Success) {
        return [pscustomobject]@{
            headers = $withoutBoundary.TrimEnd()
            body = ''
        }
    }

    $headerBlock = $withoutBoundary.Substring(0, $boundaryMatch.Index)
    $bodyBlock = $withoutBoundary.Substring($boundaryMatch.Index + $boundaryMatch.Length)
    return [pscustomobject]@{
        headers = $headerBlock
        body = $bodyBlock
    }
}

function Convert-EncodedWord {
    param(
        [Parameter(Mandatory)]
        [string]$EncodedWord
    )

    $match = [regex]::Match($EncodedWord, '^=\?([^?]+)\?([BbQq])\?([^?]+)\?=$')
    if (-not $match.Success) {
        return $EncodedWord
    }

    $charset = $match.Groups[1].Value
    $encodingFlag = $match.Groups[2].Value.ToUpperInvariant()
    $payload = $match.Groups[3].Value

    try {
        $encoding = [System.Text.Encoding]::GetEncoding($charset)
    }
    catch {
        $encoding = [System.Text.Encoding]::UTF8
    }

    if ($encodingFlag -eq 'B') {
        try {
            $bytes = [Convert]::FromBase64String($payload)
            return $encoding.GetString($bytes)
        }
        catch {
            return $EncodedWord
        }
    }

    $quotedPrintable = $payload.Replace('_', ' ')
    $buffer = [System.Collections.Generic.List[byte]]::new()
    for ($index = 0; $index -lt $quotedPrintable.Length; $index++) {
        if ($quotedPrintable[$index] -eq '=' -and $index + 2 -lt $quotedPrintable.Length) {
            $hex = $quotedPrintable.Substring($index + 1, 2)
            if ($hex -match '^[0-9A-Fa-f]{2}$') {
                [void]$buffer.Add([byte]([Convert]::ToByte($hex, 16)))
                $index += 2
                continue
            }
        }
        $chars = $encoding.GetBytes([string]$quotedPrintable[$index])
        foreach ($byte in $chars) {
            [void]$buffer.Add([byte]$byte)
        }
    }

    return $encoding.GetString($buffer.ToArray())
}

function Decode-MimeHeader {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrEmpty($Value)) {
        return $Value
    }

    return [regex]::Replace($Value, '=\?[^?]+\?[BbQq]\?[^?]+\?=', {
            param($match)
            Convert-EncodedWord -EncodedWord $match.Value
        })
}

function Convert-HeaderBlockToMap {
    param(
        [Parameter(Mandatory)]
        [string]$HeaderBlock
    )

    $lines = $HeaderBlock -split '\r?\n'
    $unfolded = [System.Collections.Generic.List[string]]::new()
    foreach ($line in $lines) {
        if ($line -match '^[ \t]' -and $unfolded.Count -gt 0) {
            $unfolded[$unfolded.Count - 1] += (' ' + $line.Trim())
        }
        else {
            $unfolded.Add($line)
        }
    }

    $map = [ordered]@{}
    foreach ($line in $unfolded) {
        $separatorIndex = $line.IndexOf(':')
        if ($separatorIndex -lt 1) {
            continue
        }
        $name = $line.Substring(0, $separatorIndex).Trim().ToLowerInvariant()
        $value = Decode-MimeHeader -Value $line.Substring($separatorIndex + 1).Trim()
        if ($map.Contains($name)) {
            $map[$name] = @($map[$name]) + $value
        }
        else {
            $map[$name] = $value
        }
    }

    return $map
}

function Normalize-EmailAddress {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $Value
    }

    $normalized = $Value.Trim()
    $normalized = $normalized -replace '\s+at\s+', '@'
    $normalized = $normalized -replace '^<', ''
    $normalized = $normalized -replace '>$', ''
    return $normalized
}

function Parse-FromHeader {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return [pscustomobject]@{ name = ''; address = '' }
    }

    if ($Value -match '^(.*)<([^>]+)>$') {
        return [pscustomobject]@{
            name = $Matches[1].Trim(' "')
            address = Normalize-EmailAddress -Value $Matches[2].Trim()
        }
    }

    if ($Value -match '^([^()]+)\(([^)]+)\)$') {
        return [pscustomobject]@{
            name = $Matches[2].Trim()
            address = Normalize-EmailAddress -Value $Matches[1].Trim()
        }
    }

    return [pscustomobject]@{
        name = ''
        address = Normalize-EmailAddress -Value $Value
    }
}

function Parse-MessageIdList {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return @()
    }

    $matches = [regex]::Matches($Value, '<[^>]+>')
    if ($matches.Count -eq 0) {
        return ,@($Value.Trim())
    }

    return ,@($matches | ForEach-Object { $_.Value.Trim() })
}

function Parse-MailDate {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    $cleaned = $Value -replace '\s*\([^)]+\)\s*$', ''
    $formats = @(
        'ddd, d MMM yyyy HH:mm:ss zzz',
        'ddd, dd MMM yyyy HH:mm:ss zzz',
        'ddd, d MMM yyyy HH:mm:ss',
        'ddd, dd MMM yyyy HH:mm:ss',
        'd MMM yyyy HH:mm:ss zzz',
        'dd MMM yyyy HH:mm:ss zzz',
        'yyyy-MM-dd HH:mm:ss'
    )

    foreach ($format in $formats) {
        try {
            return [datetime]::ParseExact($cleaned.Trim(), $format, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::AllowWhiteSpaces)
        }
        catch {
        }
    }

    $result = $null
    if ([datetime]::TryParse($cleaned, [ref]$result)) {
        return $result
    }

    return $null
}

function Convert-QuotedPrintableBody {
    param(
        [string]$Value,
        [System.Text.Encoding]$Encoding = [System.Text.Encoding]::UTF8
    )

    if ([string]::IsNullOrEmpty($Value)) {
        return $Value
    }

    $merged = $Value -replace '=\r?\n', ''
    $buffer = [System.Collections.Generic.List[byte]]::new()
    for ($index = 0; $index -lt $merged.Length; $index++) {
        if ($merged[$index] -eq '=' -and $index + 2 -lt $merged.Length) {
            $hex = $merged.Substring($index + 1, 2)
            if ($hex -match '^[0-9A-Fa-f]{2}$') {
                [void]$buffer.Add([byte]([Convert]::ToByte($hex, 16)))
                $index += 2
                continue
            }
        }
        foreach ($byte in $Encoding.GetBytes([string]$merged[$index])) {
            [void]$buffer.Add([byte]$byte)
        }
    }

    return $Encoding.GetString($buffer.ToArray())
}

function Get-BodyContent {
    param(
        [Parameter(Mandatory)]
        [string]$Body,
        [hashtable]$Headers
    )

    $contentType = if ($Headers.Contains('content-type')) { [string]$Headers['content-type'] } else { 'text/plain; charset=utf-8' }
    $transferEncoding = if ($Headers.Contains('content-transfer-encoding')) { [string]$Headers['content-transfer-encoding'] } else { '' }
    $charset = 'utf-8'

    if ($contentType -match 'charset="?([^";]+)') {
        $charset = $Matches[1]
    }

    try {
        $textEncoding = [System.Text.Encoding]::GetEncoding($charset)
    }
    catch {
        $textEncoding = [System.Text.Encoding]::UTF8
    }

    $bodyText = $Body
    if ($contentType -match 'multipart/' -and $contentType -match 'boundary="?([^";]+)"?') {
        $boundary = $Matches[1]
        $parts = $Body -split [regex]::Escape("--$boundary")
        foreach ($part in $parts) {
            if ($part -match '(?im)^Content-Type:\s*text/plain') {
                $splitPart = Split-MessageBlock -MessageText $part
                $partHeaders = Convert-HeaderBlockToMap -HeaderBlock $splitPart.headers
                return Get-BodyContent -Body $splitPart.body -Headers $partHeaders
            }
        }
    }

    if ($transferEncoding -match 'quoted-printable') {
        $bodyText = Convert-QuotedPrintableBody -Value $bodyText -Encoding $textEncoding
    }

    return $bodyText
}

function Split-IntoSentences {
    param(
        [string]$Text
    )

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return @()
    }

    $normalized = ($Text -replace '\r', '') -replace '\n{2,}', ". `n"
    return @($normalized -split '(?<=[.!?])\s+(?=[A-Z0-9])' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
}

function Extract-QuotedContextPairs {
    param(
        [string[]]$Lines
    )

    $pairs = [System.Collections.Generic.List[object]]::new()
    $quoteBuffer = [System.Collections.Generic.List[string]]::new()
    $inQuote = $false
    $correctionRegex = [regex]::new('should|instead|wrong|incorrect|fix|proper|better|use\s+.+\s+not|issue|problem\s+here|this\s+(?:is|was)\s+(?:because|due\s+to)|you\s+need|must\s+be|don''t\s+do', 'IgnoreCase')

    for ($index = 0; $index -lt $Lines.Count; $index++) {
        if ($Lines[$index] -match '^\s*>') {
            $quoteBuffer.Add($Lines[$index])
            $inQuote = $true
            continue
        }

        if ($inQuote) {
            $endIndex = [math]::Min($index + 4, $Lines.Count - 1)
            $followingText = ($Lines[$index..$endIndex] -join ' ')
            if ($correctionRegex.IsMatch($followingText)) {
                $pairs.Add([pscustomobject]@{
                        quoted = ($quoteBuffer | ForEach-Object { $_ -replace '^\s*>\s?', '' }) -join "`n"
                        response = ($Lines[$index..$endIndex]) -join "`n"
                        line_index = $index
                    })
            }
            $quoteBuffer.Clear()
            $inQuote = $false
        }
    }

    return $pairs
}

function Summarize-DiffBody {
    param(
        [string[]]$Lines
    )

    $outputLines = [System.Collections.Generic.List[string]]::new()
    $mentionedFiles = [System.Collections.Generic.List[string]]::new()
    $inDiff = $false
    $hunkLineCount = 0
    $maxHunkLines = 5

    for ($index = 0; $index -lt $Lines.Count; $index++) {
        $line = $Lines[$index]

        if ($line -match '^diff --git a/(\S+)') {
            $inDiff = $true
            $hunkLineCount = 0
            $mentionedFiles.Add($Matches[1])
            $outputLines.Add("[diff: $($Matches[1])]")
            continue
        }

        if ($inDiff) {
            if ($line -match '^@@\s.*@@\s*(.*)') {
                $context = $Matches[1].Trim()
                if ($context) {
                    $outputLines.Add("[hunk: $context]")
                }
                $hunkLineCount = 0
                continue
            }

            if ($line -match '^[+-][^+-]' -and $hunkLineCount -lt $maxHunkLines) {
                $outputLines.Add($line)
                $hunkLineCount += 1
                continue
            }

            if ($line -match '^--\s*$') {
                $inDiff = $false
                break
            }

            continue
        }

        $outputLines.Add($line)
    }

    return [pscustomobject]@{
        body = ($outputLines -join "`n").Trim()
        files = @($mentionedFiles | Select-Object -Unique)
    }
}

function Remove-QuotedLines {
    param(
        [string[]]$Lines
    )

    return @($Lines | Where-Object { $_ -notmatch '^\s*>' })
}

function Remove-SignatureBlock {
    param(
        [string[]]$Lines
    )

    $signatureIndex = -1
    for ($index = 0; $index -lt $Lines.Count; $index++) {
        if ($Lines[$index] -match '^--\s*$') {
            $signatureIndex = $index
            break
        }
    }

    if ($signatureIndex -ge 0) {
        if ($signatureIndex -eq 0) {
            return @()
        }
        return @($Lines[0..($signatureIndex - 1)])
    }

    return $Lines
}

function Get-MessageTextViews {
    param(
        [string]$BodyText
    )

    $lines = @($BodyText -split '\r?\n')
    $withoutSignature = Remove-SignatureBlock -Lines $lines
    $quotedPairs = Extract-QuotedContextPairs -Lines $withoutSignature
    $diffSummary = Summarize-DiffBody -Lines $withoutSignature
    $forScoringLines = Remove-QuotedLines -Lines ($diffSummary.body -split '\r?\n')
    $bodyForScoring = ($forScoringLines -join "`n").Trim()

    return [pscustomobject]@{
        body_no_diff = $diffSummary.body
        body_for_scoring = $bodyForScoring
        quoted_context_pairs = @($quotedPairs)
        mentioned_files = $diffSummary.files
    }
}

function Get-MentionedCommits {
    param(
        [string]$Text
    )

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return @()
    }

    $matches = [regex]::Matches($Text, '(?i)\b[a-f0-9]{7,12}\b')
    return ,@($matches | ForEach-Object { $_.Value.ToLowerInvariant() } | Select-Object -Unique)
}

function Get-KeywordMatches {
    param(
        [string]$Text
    )

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return @()
    }

    $matches = [System.Collections.Generic.List[string]]::new()
    foreach ($pattern in $script:KeywordPatterns) {
        if ($Text -match $pattern) {
            [void]$matches.Add($pattern)
        }
    }
    return ,@($matches | Select-Object -Unique)
}

function Get-StructuralSignals {
    param(
        [string]$Text
    )

    return [pscustomobject]@{
        has_compiler_error = [bool]($Text -match '\w+\.[ch]:\d+:\d+:\s*(error|warning):')
        has_stack_trace = [bool]($Text -match '(Call Trace:|BUG:|Oops:|Unable to handle|RIP:|PC is at)')
        has_shell_error = [bool]($Text -match '(command not found|No such file|Permission denied|Segmentation fault)')
        has_build_error = [bool]($Text -match '(make\[\d+\]: \*\*\*|ERROR:|FATAL:.*not found|collect2: error)')
        has_code_block = [bool]($Text -match '(?m)(^[\t ]{4,}\S.*\n){3,}')
        has_reference_urls = [bool]($Text -match 'https?://(bugs\.|github\.com/|git\.|lore\.kernel\.org/|patchwork\.)')
        has_patch_revision = [bool]($Text -match '\[PATCH\s+v[2-9]')
    }
}

function Get-MessageDisposition {
    param(
        [string]$FromAddress,
        [string]$Subject,
        [string]$BodyForScoring,
        [string[]]$KeywordMatches,
        [string]$InReplyTo
    )

    $subjectText = if ($Subject) { $Subject } else { '' }
    $bodyText = if ($BodyForScoring) { $BodyForScoring } else { '' }

    if ($FromAddress -match 'noreply(?:@|\s+at\s+)github\.com' -or $FromAddress -match 'buildbot@|ci@|jenkins@') {
        return 'dropped'
    }

    if ($subjectText -match '\[VOTE\]' -or $subjectText -match '\b(?:CI|buildbot|patchwork)\b') {
        return 'sidelined'
    }

    $asciiLetters = [regex]::Matches($subjectText + ' ' + $bodyText, '[A-Za-z]').Count
    if ($asciiLetters -lt 20 -and -not $InReplyTo) {
        return 'dropped'
    }

    if ($KeywordMatches.Count -eq 0 -and -not $InReplyTo -and $bodyText.Length -lt 40) {
        return 'dropped'
    }

    return 'primary'
}

function Get-Categories {
    param(
        [string]$Text
    )

    $categories = [System.Collections.Generic.List[string]]::new()
    foreach ($entry in $script:CategoryPatterns.GetEnumerator()) {
        if ($Text -match $entry.Value) {
            [void]$categories.Add($entry.Key)
        }
    }

    if ($categories.Count -eq 0) {
        [void]$categories.Add('uncategorized')
    }

    return ,@($categories)
}

function Write-JsonLines {
    param(
        [Parameter(Mandatory)]
        [string]$Path,
        [Parameter(Mandatory)]
        [object[]]$Items
    )

    $directory = Split-Path -Parent $Path
    if ($directory) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    $lines = foreach ($item in $Items) {
        $item | ConvertTo-Json -Depth 8 -Compress
    }
    [System.IO.File]::WriteAllLines($Path, $lines, [System.Text.UTF8Encoding]::new($false))
}

function Write-StageStats {
    param(
        [Parameter(Mandatory)]
        [string]$OutputDir,
        [Parameter(Mandatory)]
        [hashtable]$Stats
    )

    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    $statsPath = Join-Path $OutputDir 'stats.json'
    $Stats | ConvertTo-Json -Depth 8 | Set-Content -Path $statsPath -Encoding utf8
}

function Write-QASamples {
    param(
        [Parameter(Mandatory)]
        [string]$OutputDir,
        [Parameter(Mandatory)]
        [object[]]$Items,
        [int]$Count = 10
    )

    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    $samplePath = Join-Path $OutputDir 'samples.md'
    $builder = [System.Text.StringBuilder]::new()
    [void]$builder.AppendLine('# QA Samples')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Randomly selected records for manual inspection.')
    [void]$builder.AppendLine('')

    if ($Items.Count -eq 0) {
        [void]$builder.AppendLine('_No items available._')
    }
    else {
        $selected = if ($Items.Count -le $Count) { $Items } else { $Items | Get-Random -Count $Count }
        $sampleIndex = 1
        foreach ($item in $selected) {
            [void]$builder.AppendLine("## Sample $sampleIndex")
            [void]$builder.AppendLine('')
            [void]$builder.AppendLine('```json')
            [void]$builder.AppendLine(($item | ConvertTo-Json -Depth 6))
            [void]$builder.AppendLine('```')
            [void]$builder.AppendLine('')
            $sampleIndex += 1
        }
    }

    $builder.ToString() | Set-Content -Path $samplePath -Encoding utf8
}

function Write-StageReadme {
    param(
        [Parameter(Mandatory)]
        [string]$OutputDir,
        [Parameter(Mandatory)]
        [string]$Title,
        [Parameter(Mandatory)]
        [string[]]$Bullets
    )

    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    $readmePath = Join-Path $OutputDir 'README.md'
    $builder = [System.Text.StringBuilder]::new()
    [void]$builder.AppendLine("# $Title")
    [void]$builder.AppendLine('')
    foreach ($bullet in $Bullets) {
        [void]$builder.AppendLine("- $bullet")
    }
    $builder.ToString() | Set-Content -Path $readmePath -Encoding utf8
}

function Convert-ArchiveMessage {
    param(
        [Parameter(Mandatory)]
        [string]$SourceFile,
        [Parameter(Mandatory)]
        [object]$MessageRecord
    )

    $split = Split-MessageBlock -MessageText $MessageRecord.text
    $headers = Convert-HeaderBlockToMap -HeaderBlock $split.headers
    $fromInfo = Parse-FromHeader -Value ([string]($headers['from']))
    $messageId = [string]($headers['message-id'])
    if ([string]::IsNullOrWhiteSpace($messageId)) {
        $messageId = "<$($SourceFile -replace '[\\/ ]', '_'):$($MessageRecord.byte_offset)>"
    }

    $references = @(Parse-MessageIdList -Value ([string]($headers['references'])))
    $inReplyToList = @(Parse-MessageIdList -Value ([string]($headers['in-reply-to'])))
    $inReplyTo = if ($inReplyToList.Count -gt 0) { $inReplyToList[0] } else { $null }
    $dateValue = Parse-MailDate -Value ([string]($headers['date']))
    $bodyText = Get-BodyContent -Body $split.body -Headers $headers
    $views = Get-MessageTextViews -BodyText $bodyText
    $keywordMatches = @(Get-KeywordMatches -Text (([string]($headers['subject'])) + "`n" + $views.body_for_scoring))
    $structuralSignals = Get-StructuralSignals -Text $views.body_for_scoring
    $mentionedCommits = @(Get-MentionedCommits -Text ($views.body_no_diff))
    $allText = (([string]($headers['subject'])) + "`n" + $views.body_no_diff)
    $categories = @(Get-Categories -Text $allText)
    $disposition = Get-MessageDisposition -FromAddress $fromInfo.address -Subject ([string]($headers['subject'])) -BodyForScoring $views.body_for_scoring -KeywordMatches $keywordMatches -InReplyTo $inReplyTo

    return [pscustomobject]@{
        source_file = $SourceFile
        byte_offset = $MessageRecord.byte_offset
        mbox_from_line = $MessageRecord.from_line
        message_id = $messageId
        in_reply_to = $inReplyTo
        references = $references
        from_addr = $fromInfo.address
        from_name = $fromInfo.name
        date_raw = [string]($headers['date'])
        date_iso = if ($dateValue) { $dateValue.ToString('o') } else { $null }
        subject = [string]($headers['subject'])
        body_for_scoring = $views.body_for_scoring
        body_no_diff = $views.body_no_diff
        quoted_context_pairs = $views.quoted_context_pairs
        mentioned_files = $views.mentioned_files
        mentioned_commits = $mentionedCommits
        keyword_matches = $keywordMatches
        structural_signals = $structuralSignals
        categories = $categories
        has_patch_subject = [bool](([string]($headers['subject'])) -match '\[PATCH')
        has_keyword_match = ($keywordMatches.Count -gt 0)
        disposition = $disposition
    }
}

Export-ModuleMember -Function *