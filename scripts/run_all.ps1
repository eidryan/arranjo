$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Node = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$NodeModules = Join-Path $Root "node_modules"
$BundledNodeModules = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"

if (-not (Test-Path $NodeModules)) {
  New-Item -ItemType Junction -Path $NodeModules -Target $BundledNodeModules | Out-Null
}

Push-Location $Root
try {
  & $Python (Join-Path $Root "scripts\generate_outputs.py")
  & $Node (Join-Path $Root "scripts\build_workbook.mjs")
}
finally {
  Pop-Location
}
