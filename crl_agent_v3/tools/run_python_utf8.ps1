[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$ScriptPath,

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArguments
)

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
$env:PYTHONUTF8 = "1"

if (-not (Test-Path -LiteralPath $ScriptPath -PathType Leaf)) {
    Write-Error "Python script path does not exist or is not a file: $ScriptPath"
    exit 2
}

$machineRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$productRoot = (Resolve-Path -LiteralPath (Join-Path $machineRoot "..")).Path
$pythonPath = Join-Path $productRoot "env\crl_agent_v3\python.exe"
if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    Write-Error "Official CRL Python interpreter does not exist: $pythonPath"
    exit 3
}

& $pythonPath -X utf8 $ScriptPath @ScriptArguments
exit $LASTEXITCODE
