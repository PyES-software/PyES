# Two-stage flatten SAFE:
# Stage1: move children from .\pyes-files\ to root (if it exists)
# Stage2: move children from .\pyes\ to root (overwrite any existing)
# Cleanup: remove only known "parallel root" folder(s) that should not remain (home)
# Does NOT delete assets/authors/tags etc. except when overwritten by Stage2 (intended).

$ErrorActionPreference = "Stop"

$stage1Folder = "pyes-files"
$stage2Folder = "pyes"

# Only folders that are NOT part of the real site and should never remain in root:
$cleanupFolders = @("home")

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
        # overwrite destination by removing it first (file or folder)
        Remove-IfExists -path $destPath
        Move-Item -LiteralPath $_.FullName -Destination $repoRoot -Force -ErrorAction Stop
    }

    Remove-Item -LiteralPath $folderPath -Recurse -Force -ErrorAction Stop
    Write-Host "[$label] Done. Removed folder."
    return $true
}

# --- Stage 1 (optional) ---
$stage1Path = Join-Path $repoRoot $stage1Folder
Move-ChildrenToRoot -folderPath $stage1Path -label "STAGE1" | Out-Null

# --- Stage 2 (required) ---
$stage2Path = Join-Path $repoRoot $stage2Folder
$ok2 = Move-ChildrenToRoot -folderPath $stage2Path -label "STAGE2"
if (-not $ok2) {
    Write-Host "ERRORE: Non trovo la cartella '$stage2Folder' in root (dopo STAGE1)."
    Write-Host "Cartelle presenti in root:"
    Get-ChildItem -LiteralPath $repoRoot -Directory | Select-Object Name
    exit 1
}

# --- Cleanup minimal ---
foreach ($f in $cleanupFolders) {
    $p = Join-Path $repoRoot $f
    if (Test-Path $p) {
        Write-Host "[CLEANUP] Removing '$f'..."
        Remove-IfExists -path $p
    }
}

# --- Final check ---
$rootIndex = Join-Path $repoRoot "index.html"
if (!(Test-Path $rootIndex)) {
    Write-Host "ERRORE: index.html non trovato in root dopo STAGE2."
    exit 1
}

Write-Host "OK: flatten SAFE completato. Root index.html presente."
exit 0
