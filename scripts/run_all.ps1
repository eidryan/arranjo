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
  Write-Host "[1/5] generate_outputs.py ..."
  & $Python (Join-Path $Root "scripts\generate_outputs.py")
  Write-Host "[2/5] build_workbook.mjs ..."
  & $Node (Join-Path $Root "scripts\build_workbook.mjs")
  Write-Host "[3/5] build_latex.py ..."
  & $Python (Join-Path $Root "scripts\build_latex.py")
  Write-Host "[4/5] build_presentation.py ..."
  & $Python (Join-Path $Root "scripts\build_presentation.py")
  Write-Host "[5/5] polish_presentation.py ..."
  & $Python (Join-Path $Root "scripts\polish_presentation.py")
  Write-Host ""
  Write-Host "Done. Open 06_dashboard\index.html to review."
  Write-Host "LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX)."
  Write-Host "PPTX final em 01_apresentacao\apresentacao_final.pptx"
}
finally {
  Pop-Location
}
