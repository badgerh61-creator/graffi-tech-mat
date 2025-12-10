@echo off
setlocal enabledelayedexpansion

:: diag-export-report.bat
:: Purpose: Collect existing diagnostic artifacts and export to a single archive (ZIP) or copy to a destination
:: Place: graffi-tech-scripts/diagnostics/reporting/

set SCRIPT_DIR=%~dp0
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set DIAG_ROOT=%SCRIPT_DIR%..\artifacts
set EXPORT_DIR=%SCRIPT_DIR%..\exports
set ZIP_FILE=%EXPORT_DIR%\diagnostics-%TIMESTAMP%.zip
set LOG_FILE=%EXPORT_DIR%\export-%TIMESTAMP%.log

:: Destination override (optional)
if defined EXPORT_DEST set EXPORT_DEST=%EXPORT_DEST%

if not exist "%EXPORT_DIR%" mkdir "%EXPORT_DIR%"

echo [%DATE% %TIME%] Starting export of diagnostics > "%LOG_FILE%"

:: Gather all artifact directories under DIAG_ROOT
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$root = Resolve-Path '%DIAG_ROOT%' -ErrorAction SilentlyContinue; ^
   if (-not $root) { Write-Host 'NO_ARTIFACTS'; exit 0 } ; ^
   $files = Get-ChildItem -Path $root -Recurse -File | Select-Object -ExpandProperty FullName; ^
   if ($files.Count -eq 0) { Write-Host 'NO_ARTIFACTS'; exit 0 } ; ^
   $zip = Join-Path (Resolve-Path '%EXPORT_DIR%').Path ('diagnostics-%TIMESTAMP%.zip'); ^
   if (Test-Path $zip) { Remove-Item $zip -Force } ; ^
   Compress-Archive -Path (Join-Path $root '*') -DestinationPath $zip -Force; ^
   Write-Host $zip"

for /f "usebackq delims=" %%Z in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-ChildItem -Path '%DIAG_ROOT%' -Recurse -File).Count"`) do set FILECOUNT=%%Z

if "%FILECOUNT%"=="0" (
  echo [%DATE% %TIME%] No diagnostic files to export. >> "%LOG_FILE%"
  echo No artifacts found under %DIAG_ROOT%
  endlocal
  exit /b 0
)

:: If export destination provided, copy there
if defined EXPORT_DEST (
  echo [%DATE% %TIME%] Copying %ZIP_FILE% to %EXPORT_DEST% >> "%LOG_FILE%"
  copy /Y "%ZIP_FILE%" "%EXPORT_DEST%" >> "%LOG_FILE%" 2>&1
  if errorlevel 1 (
    echo [%DATE% %TIME%] ERROR copying to destination >> "%LOG_FILE%"
    exit /b 2
  )
)

echo [%DATE% %TIME%] Export complete: %ZIP_FILE% >> "%LOG_FILE%"
echo Exported: %ZIP_FILE%
endlocal
exit /b 0
