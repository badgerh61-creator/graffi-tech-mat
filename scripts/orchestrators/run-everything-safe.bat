@echo off
REM =========================================================================
REM run-everything-safe.bat
REM Dry-run oriented orchestrator that lists planned steps, can run selected.
REM Usage: run-everything-safe.bat
REM =========================================================================

setlocal

set SCRIPTS_DIR=%~dp0

echo Planned steps:
echo 1) install-dependencies.bat
echo 2) build-docker.bat
echo 3) start-docker.bat
echo 4) db-seed.bat (optional)
echo 5) start-ai-engine.bat (optional)
echo.
set /p CHOICE=Type numbers to run (comma separated) or NONE to exit: 

if /I "%CHOICE%"=="NONE" (
  echo No actions selected. Exiting.
  exit /b 0
)

for %%A in (%CHOICE:,= %) do (
  if "%%A"=="1" call "%SCRIPTS_DIR%\install-dependencies.bat"
  if "%%A"=="2" call "%SCRIPTS_DIR%\build-docker.bat"
  if "%%A"=="3" call "%SCRIPTS_DIR%\start-docker.bat"
  if "%%A"=="4" if exist "%SCRIPTS_DIR%\db-seed.bat" call "%SCRIPTS_DIR%\db-seed.bat" else echo db-seed.bat not found.
  if "%%A"=="5" if exist "%SCRIPTS_DIR%\start-ai-engine.bat" call "%SCRIPTS_DIR%\start-ai-engine.bat" else echo start-ai-engine.bat not found.
)

echo Selected actions complete.
exit /b 0
