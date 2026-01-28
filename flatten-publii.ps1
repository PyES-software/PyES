# Flatten output di Publii: sposta tutto da .\ pyes-files\ alla root del repo
# Esegui dalla ROOT del repo (branch gh-pages)

$siteFolderName = "pyes-files"  # <-- metti qui il nome ESATTO della cartella che Publii crea
$repoRoot = Get-Location
$siteFolder = Join-Path $repoRoot $siteFolderName

if (!(Test-Path $siteFolder)) {
  Write-Host "Cartella '$siteFolderName' non trovata in: $repoRoot"
  Write-Host "Controlla il nome o esegui lo script dalla root del repo."
  exit 1
}

# Sposta contenuti in root
Get-ChildItem -Path $siteFolder -Force | ForEach-Object {
  Move-Item -Path $_.FullName -Destination $repoRoot -Force
}

# Rimuove la sottocartella ormai vuota
Remove-Item -Path $siteFolder -Recurse -Force

Write-Host "OK: contenuti spostati in root e '$siteFolderName' rimossa."