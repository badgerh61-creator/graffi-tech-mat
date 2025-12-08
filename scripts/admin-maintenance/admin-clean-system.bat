@echo off
REM ====================================================================
REM admin-clean-system.bat
REM Consolidated maintenance: clears caches, temp files, and optionally restarts services.
REM Run as Administrator for best results.
REM ====================================================================

setlocal enabledelayedexpansion

set LOG_DIR=%~dp0..\..\logs\admin
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOGFILE=%LOG_DIR%\admin-clean-system_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%.log
echo [%date% %time%] Starting admin-clean-system >> "%LOGFILE%"

rem 1) Clear npm cache (if present)
if exist "%~dp0..\node_modules" (
  echo [%date% %time%] Clearing npm cache... >> "%LOGFILE%"
  npm cache clean --force >> "%LOGFILE%" 2>&1 || echo npm cache clean failed >> "%LOGFILE%"
) else (
  echo [%date% %time%] No node_modules detected - skipping npm cache. >> "%LOGFILE%"
)

rem 2) Clear Python pip cache (if python present)
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  echo [%date% %time%] Clearing pip cache... >> "%LOGFILE%"
  python -m pip cache purge >> "%LOGFILE%" 2>&1 || echo pip cache purge failed >> "%LOGFILE%"
) else (
  echo [%date% %time%] Python not found - skipping pip cache. >> "%LOGFILE%"
)

rem 3) Delete temporary build folders (safe list)
for %%D in (dist build .next node_modules\\.vite) do (
  if exist "%~dp0..\%%D" (
    echo [%date% %time%] Removing %%D >> "%LOGFILE%"
    rd /s /q "%~dp0..\%%D" >> "%LOGFILE%" 2>&1 || echo Failed to remove %%D >> "%LOGFILE%"
  )
)

rem 4) Clear system temp (only app temp files under project tmp)
set TMPDIR=%~dp0..\tmp
if exist "%TMPDIR%" (
  echo [%date% %time%] Clearing project tmp folder >> "%LOGFILE%"
  rd /s /q "%TMPDIR%" >> "%LOGFILE%" 2>&1
  mkdir "%TMPDIR%" >> "%LOGFILE%" 2>&1
) else (
  echo [%date% %time%] No project tmp folder found - creating one >> "%LOGFILE%"
  mkdir "%TMPDIR%" >> "%LOGFILE%" 2>&1
)

rem 5) Optionally restart services if user provided "restart" param
if /I "%~1"=="restart" (
  echo [%date% %time%] Restart requested - invoking admin-restart-services.bat >> "%LOGFILE%"
  call "%~dp0admin-restart-services.bat" >> "%LOGFILE%" 2>&1
)

echo [%date% %time%] admin-clean-system completed. >> "%LOGFILE%"
endlocal
exit /b 0
