@echo off
REM =========================================================================
REM run-everything-parallel.bat
REM Starts multiple scripts in parallel command windows. Non-blocking.
REM =========================================================================

setlocal

set SCRIPTS_DIR=%~dp0

echo Starting services in parallel...

if exist "%SCRIPTS_DIR%\start-backend-dev.bat" (
  start "Backend" cmd /k "%SCRIPTS_DIR%\start-backend-dev.bat"
) else if exist "%SCRIPTS_DIR%\start-backend.bat" (
  start "Backend" cmd /k "%SCRIPTS_DIR%\start-backend.bat"
)

if exist "%SCRIPTS_DIR%\start-frontend-dev.bat" (
  start "Frontend" cmd /k "%SCRIPTS_DIR%\start-frontend-dev.bat"
) else if exist package.json (
  start "Frontend" cmd /k "npm run dev"
)

if exist "%SCRIPTS_DIR%\start-ai-engine.bat" (
  start "AI-Engine" cmd /k "%SCRIPTS_DIR%\start-ai-engine.bat"
)

if exist "%SCRIPTS_DIR%\watch-assets.bat" (
  start "Assets-Watcher" cmd /k "%SCRIPTS_DIR%\watch-assets.bat"
)

echo All start commands issued. Check the new windows for logs/output.
exit /b 0
