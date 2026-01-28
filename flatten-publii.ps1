# Two-stage flatten (forza Stage2):
# Stage1: move children from .\pyes-files\ to root (se esiste)
# Cleanup: rimuove output "vecchio" in root (index.html + cartelle tipiche)
# Stage2: move children from .\pyes\ to root (sovrascrivendo)
# Final: verifica index.html in root

$ErrorActionPreference = "Stop"

$stage1Folder = "pyes-files"
$stage2Folder = "pyes"

# Cosa pulire in root PRIMA di Stage2 (aggiungi/togli se serve)
$rootCleanup = @(
  "index.html",
  "404.html",
  "sitemap.xml",
  "robots.txt",
  "feed.xml",
  "assets",
  "themes",
  "media",
  "authors",
  "tags",
  "home"
)

$repoRoot = Get-Location
Write-Host "Repo root: $repoRoot"

function Remove-IfExists([string]$path) {
    if (Test-Path $path) {
        try { Remove-Item -LiteralPath $path -Force -ErrorAction Stop }
        catch { Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction Stop }
    }
}

function Move-ChildrenToRoot([string]$folderPath, [string]$label) {
    if (!(Test-Path $folderPath)) {
        Write-Host "[$label] Folder not found: $folderPath (skip)"
        return $false
    }

    Write-Host "[$label] Moving contents of '$folderPath' -> root (overwrite)..."
    Get-ChildItem -LiteralPath $folderPath -Force | ForEach-Object {
        $destPath = Join-Path $repoRoot $_.Name
        Remove-IfExists -path $destPath
        Move-Item -LiteralPath $_.FullName -Destination $repoRoot -Force -ErrorAction Stop
    }

    Remove-Item -LiteralPath $folderPath -Recurse -Force -ErrorAction Stop
    Write-Host "[$label] Done. Removed folder."
    return $true
}

# -----------------------
# Stage 1 (optional)
# -----------------------
$stage1Path = Join-Path $repoRoot $stage1Folder
Move-ChildrenToRoot -folderPath $stage1Path -label "STAGE1" | Out-Null

# -----------------------
# Cleanup root BEFORE Stage 2
# -----------------------
Write-Host "[CLEANUP] Removing old root output before STAGE2..."
foreach ($item in $rootCleanup) {
    $p = Join-Path $repoRoot $item
    if (Test-Path $p) {
        Write-Host "  - remove $item"
        Remove-IfExists -path $p
    }
}
Write-Host "[CLEANUP] Done."

# -----------------------
# Stage 2 (forced)
# -----------------------
$stage2Path = Join-Path $repoRoot $stage2Folder
$ok2 = Move-ChildrenToRoot -folderPath $stage2Path -label "STAGE2"
if (-not $ok2) {
    Write-Host "ERRORE: Non trovo la cartella '$stage2Folder' dopo STAGE1+cleanup."
    Write-Host "Cartelle presenti in root:"
    Get-ChildItem -LiteralPath $repoRoot -Directory | Select-Object Name
    exit 1
}

# Final check
$rootIndex = Join-Path $repoRoot "index.html"
if (!(Test-Path $rootIndex)) {
    Write-Host "ERRORE: index.html non trovato in root dopo STAGE2."
    exit 1
}

Write-Host "OK: flatten completato. Root index.html presente (da STAGE2)."
exit 0
