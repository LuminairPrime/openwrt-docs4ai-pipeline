[CmdletBinding(PositionalBinding = $false)]
param(
	[string]$WorkingDir = (Get-Location).Path,
	[string]$ConfigDir,
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$DiracArgs
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$defaultDiracRoot = Join-Path $scriptRoot 'tmp\dirac-fix-builds-20260513-130010\infcode\tmp\dirac-pr-submit-20260515'
$diracRoot = if ($env:DIRAC_PR_ROOT) { $env:DIRAC_PR_ROOT } else { $defaultDiracRoot }
$cliEntry = Join-Path $diracRoot 'cli\dist\cli.mjs'

if (-not (Test-Path $WorkingDir -PathType Container)) {
	throw "Working directory does not exist: $WorkingDir"
}

if (-not (Test-Path $cliEntry)) {
	throw "Built Dirac CLI not found at $cliEntry"
}

if (-not $ConfigDir) {
	$ConfigDir = Join-Path $diracRoot '.dirac-config-pr'
}

if ((Test-Path $ConfigDir) -and -not (Test-Path $ConfigDir -PathType Container)) {
	throw "Config path exists but is not a directory: $ConfigDir"
}

if (-not (Test-Path $ConfigDir -PathType Container)) {
	New-Item -ItemType Directory -Path $ConfigDir -ErrorAction Stop | Out-Null
}

if (-not $DiracArgs -or $DiracArgs.Count -eq 0) {
	$DiracArgs = @('auth')
}

& npx --yes node@24 --version | Out-Null
if ($LASTEXITCODE -ne 0) {
	throw 'Node 24 is not available via npx.'
}

Push-Location $diracRoot
try {
	& npx --yes node@24 $cliEntry --cwd $WorkingDir --config $ConfigDir @DiracArgs
	if ($LASTEXITCODE -ne 0) {
		throw "Dirac CLI exited with code $LASTEXITCODE"
	}
}
finally {
	Pop-Location
}