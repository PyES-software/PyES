# Two-stage flatten (forzato):
# Stage 1: move children from .\pyes-files\ to repo root (overwriting)
# Stage 2: move children from .\pyes\ to repo root (overwriting)
# If index.html already in root after Stage1, Stage2 is skipped.

$ErrorActionPreference = "Stop"

$stage1Folder = "pyes-files"
$stage2Folder = "pyes"     # <-- cartella del sito "vero"

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
        Write-Host "[$label] Folder not found: $folderPath"
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
# Stage 1
# -----------------------
$stage1Path = Join-Path $repoRoot $stage1Folder
Move-ChildrenToRoot -folderPath $stage1Path -label "STAGE1" | Out-Null

# If Stage1 already produced a root index.html, we are done
$rootIndex = Join-Path $repoRoot "index.html"
if (Test-Path $rootIndex) {
    Write-Host "[INFO] index.html already in root after STAGE1. Skipping STAGE2."
    exit 0
}

# -----------------------
# Stage 2 (forced)
# -----------------------
$stage2Path = Join-Path $repoRoot $stage2Folder
$ok2 = Move-ChildrenToRoot -folderPath $stage2Path -label "STAGE2"

# Final check
if (!(Test-Path (Join-Path $repoRoot "index.html"))) {
    Write-Host "ERRORE: index.html non trovato in root dopo STAGE2."
    Write-Host "Controlla cosa e' stato estratto da '$stage1Folder' (magari il sito e' in un'altra cartella, non '$stage2Folder')."
    exit 1
}

Write-Host "OK: flatten completato. Root index.html presente."
exit 0
