@echo off
REM ====================================================================
REM verify-ingestion-health.bat
REM Validates ingestion queues, processing folders, and checks for failures.
REM Reports counts and exits non-zero if critical issues found.
REM ====================================================================

setlocal enabledelayedexpansion
set PROCESS_ROOT=%cd%\processing
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\verify-ingest_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [%date% %time%] Starting ingestion health check >> "%LOGFILE%"

set /a ERRORS=0

for %%D in (images videos styles 3d presets moodboards prompts) do (
  set FOLDER=%PROCESS_ROOT%\%%D
  if not exist "!FOLDER!" (
    echo [%date% %time%] WARNING: processing folder missing: !FOLDER! >> "%LOGFILE%"
    set /a ERRORS+=1
  ) else (
    for /f %%N in ('dir /B /A:-D "!FOLDER!" 2^>nul ^| find /C /V ""') do set COUNT=%%N
    echo [%date% %time%] Queue: %%D => !COUNT! items >> "%LOGFILE%"
  )
)

rem Check for recent failures (files ending .failed)
for /r "%PROCESS_ROOT%" %%F in (*.failed) do (
  echo [%date% %time%] FAILED ITEM: %%~fF >> "%LOGFILE%"
  set /a ERRORS+=1
)

if %ERRORS% gtr 0 (
  echo [%date% %time%] Health check completed with %ERRORS% warnings/errors >> "%LOGFILE%"
  exit /b 3
) else (
  echo [%date% %time%] Health OK >> "%LOGFILE%"
  exit /b 0
)
