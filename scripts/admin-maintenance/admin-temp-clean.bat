@echo off
REM ====================================================================
REM admin-temp-clean.bat
REM Removes temporary and orphan files inside project tmp & cache directories.
REM Usage: admin-temp-clean.bat [--dry-run]
REM ====================================================================

setlocal enabledelayedexpansion
set DRY=%~1
set TMP_ROOT=%~dp0..\..\tmp
set CACHE_ROOT=%~dp0..\..\cache
set LOG_DIR=%~dp0..\..\logs\admin
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOGFILE=%LOG_DIR%\admin-temp-clean_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

echo [%date% %time%] Starting temp-clean (dry=%DRY%) >> "%LOGFILE%"

for %%D in ("%TMP_ROOT%" "%CACHE_ROOT%") do (
  if exist "%%~D" (
    echo [%date% %time%] Cleaning %%~D >> "%LOGFILE%"
    if /I "%DRY%"=="--dry-run" (
      for /f "delims=" %%F in ('dir /B /S "%%~D" 2^>nul') do echo DRY: would remove %%F >> "%LOGFILE%"
    ) else (
      rd /s /q "%%~D" >> "%LOGFILE%" 2>&1
      mkdir "%%~D" >> "%LOGFILE%" 2>&1
    )
  ) else (
    echo [%date% %time%] Directory not found: %%~D >> "%LOGFILE%"
  )
)

echo [%date% %time%] Temp-clean finished. >> "%LOGFILE%"
endlocal
exit /b 0
