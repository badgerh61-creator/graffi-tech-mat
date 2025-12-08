@echo off
REM =========================================================================
REM run-everything-dev.bat
REM Starts development environment: installs deps if needed and runs dev servers.
REM =========================================================================

setlocal

set SCRIPTS_DIR=%~dp0
set LOG_DIR=%SCRIPTS_DIR%\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo DEV ORCHESTRATOR START: %DATE% %TIME% > "%LOG_DIR%\dev_orchestrator.log"

echo Checking deps...
call "%SCRIPTS_DIR%\verify-node-python.bat" >> "%LOG_DIR%\dev_orchestrator.log" 2>&1

echo Starting backend in dev mode...
if exist "%SCRIPTS_DIR%\start-backend-dev.bat" (
  start "Backend-Dev" cmd /k "%SCRIPTS_DIR%\start-backend-dev.bat"
) else (
  echo No start-backend-dev.bat found — try starting python app manually. >> "%LOG_DIR%\dev_orchestrator.log"
)

echo Starting frontend in dev mode...
if exist "%SCRIPTS_DIR%\start-frontend-dev.bat" (
  start "Frontend-Dev" cmd /k "%SCRIPTS_DIR%\start-frontend-dev.bat"
) else (
  if exist package.json (
    start "Frontend-Dev" cmd /k "npm run dev"
  ) else (
    echo No frontend dev command found. >> "%LOG_DIR%\dev_orchestrator.log"
  )
)

echo Starting local watchers & watchers started. See separate windows for output.
exit /b 0
