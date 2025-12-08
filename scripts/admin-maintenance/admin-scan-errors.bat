@echo off
REM ====================================================================
REM admin-scan-errors.bat
REM Scans logs for ERROR/WARNING patterns and summarizes findings.
REM Usage: admin-scan-errors.bat [logs_folder]
REM ====================================================================

setlocal enabledelayedexpansion
set LOG_SOURCE=%~1
if "%LOG_SOURCE%"=="" set LOG_SOURCE=%~dp0..\..\logs

set REPORT_DIR=%~dp0..\..\logs\admin
if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"
set REPORT=%REPORT_DIR%\admin-scan-errors_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.txt

echo Scan report generated at %REPORT% > "%REPORT%"
echo Scan start: %DATE% %TIME% >> "%REPORT%"
echo. >> "%REPORT%"

for /R "%LOG_SOURCE%" %%F in (*.log) do (
  findstr /I /N /C:"ERROR" /C:"WARN" "%%~fF" >> "%REPORT%" || rem no matches
)

echo. >> "%REPORT%"
echo Scan complete at %DATE% %TIME% >> "%REPORT%"

type "%REPORT%"
endlocal
exit /b 0
