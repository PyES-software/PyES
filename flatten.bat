@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0flatten-publii.ps1"
if errorlevel 1 (
  echo.
  echo Flatten FALLITO. Leggi l'errore sopra.
  pause
  exit /b 1
)

echo.
echo Flatten completato con successo.
pause
endlocal
