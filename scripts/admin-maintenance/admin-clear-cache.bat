@echo off
REM ====================================================================
REM admin-clear-cache.bat
REM Clears common caches used by the project.
REM Usage: admin-clear-cache.bat [all|npm|pip|docker]
REM ====================================================================

setlocal
set MODE=%~1
if "%MODE%"=="" set MODE=all

set LOG_DIR=%~dp0..\..\logs\admin
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOGFILE=%LOG_DIR%\admin-clear-cache_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

echo [%date% %time%] Clearing caches (mode=%MODE%) >> "%LOGFILE%"

if /I "%MODE%"=="all" (
  call "%~dp0admin-clear-cache.bat" npm
  call "%~dp0admin-clear-cache.bat" pip
  call "%~dp0admin-clear-cache.bat" docker
  goto :EOF
)

if /I "%MODE%"=="npm" (
  where npm >nul 2>&1
  if %ERRORLEVEL%==0 (
    echo [%date% %time%] npm cache clean --force >> "%LOGFILE%"
    npm cache clean --force >> "%LOGFILE%" 2>&1 || echo npm cache clean failed >> "%LOGFILE%"
  ) else echo npm not found >> "%LOGFILE%"
  goto :EOF
)

if /I "%MODE%"=="pip" (
  where python >nul 2>&1
  if %ERRORLEVEL%==0 (
    echo [%date% %time%] pip cache purge >> "%LOGFILE%"
    python -m pip cache purge >> "%LOGFILE%" 2>&1 || echo pip cache purge failed >> "%LOGFILE%"
  ) else echo python not found >> "%LOGFILE%"
  goto :EOF
)

if /I "%MODE%"=="docker" (
  where docker >nul 2>&1
  if %ERRORLEVEL%==0 (
    echo [%date% %time%] docker system prune -af >> "%LOGFILE%"
    docker system prune -af >> "%LOGFILE%" 2>&1 || echo docker prune failed >> "%LOGFILE%"
  ) else echo docker not found >> "%LOGFILE%"
  goto :EOF
)

echo Unknown mode: %MODE% >> "%LOGFILE%"
endlocal
exit /b 0
