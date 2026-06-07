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
  Write-Host "[1/3] generate_outputs.py ..."
  & $Python (Join-Path $Root "scripts\generate_outputs.py")
  Write-Host "[2/3] build_workbook.mjs ..."
  & $Node (Join-Path $Root "scripts\build_workbook.mjs")
  Write-Host "[3/4] build_latex.py ..."
  & $Python (Join-Path $Root "scripts\build_latex.py")
  Write-Host "[4/4] build_presentation.py ..."
  & $Python (Join-Path $Root "scripts\build_presentation.py")
  Write-Host ""
  Write-Host "Done. Open 06_dashboard\index.html to review."
  Write-Host "LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX)."
  Write-Host "PPTX pronto em 01_apresentacao\apresentacao_tramontina_22399036.pptx"
}
finally {
  Pop-Location
}
