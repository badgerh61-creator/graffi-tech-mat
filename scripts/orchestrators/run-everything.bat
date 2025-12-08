@echo off
REM =========================================================================
REM run-everything.bat
REM Interactive master orchestrator — runs core setup, build, start, and checks.
REM Usage: run-everything.bat [--dry-run]
REM =========================================================================

setlocal enabledelayedexpansion

set SCRIPTS_DIR=%~dp0
if "%SCRIPTS_DIR:~-1%"=="\" set SCRIPTS_DIR=%SCRIPTS_DIR:~0,-1%

set LOG_DIR=%SCRIPTS_DIR%\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOG_FILE=%LOG_DIR%\orchestrator_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.log
set DRYRUN=0

if "%~1"=="--dry-run" set DRYRUN=1

echo ================================================== | tee "%LOG_FILE%"
echo RUN EVERYTHING - %DATE% %TIME% | tee -a "%LOG_FILE%"
echo Dry-run: %DRYRUN% | tee -a "%LOG_FILE%"

:CONFIRM
echo.
echo This will run the full local pipeline:
echo 1) Install deps
echo 2) Build docker images
echo 3) Start docker stack
echo 4) Seed DB (if available)
echo 5) Start AI services
echo.
set /p USER_CONFIRM=Type YES to proceed (or NO to abort): 
if /I "%USER_CONFIRM%"=="YES" goto :PROCEED
if /I "%USER_CONFIRM%"=="NO" (
  echo Aborted by user. | tee -a "%LOG_FILE%"
  exit /b 0
)
echo Please type YES or NO.
goto CONFIRM

:PROCEED
if "%DRYRUN%"=="1" (
  echo [DRY-RUN] Would run: install-dependencies.bat, build-docker.bat, start-docker.bat, seed-db.bat, start-ai-engine.bat. | tee -a "%LOG_FILE%"
  echo Dry-run complete.
  exit /b 0
)

echo Step 1/5: Installing dependencies... | tee -a "%LOG_FILE%"
call "%SCRIPTS_DIR%\install-dependencies.bat" 2>&1 | tee -a "%LOG_FILE%"
if errorlevel 1 (
  echo install-dependencies failed. See log. | tee -a "%LOG_FILE%"
  goto :ROLLBACK_PROMPT
)

echo Step 2/5: Building docker images... | tee -a "%LOG_FILE%"
call "%SCRIPTS_DIR%\build-docker.bat" 2>&1 | tee -a "%LOG_FILE%"
if errorlevel 1 (
  echo build-docker failed. | tee -a "%LOG_FILE%"
  goto :ROLLBACK_PROMPT
)

echo Step 3/5: Starting docker stack... | tee -a "%LOG_FILE%"
call "%SCRIPTS_DIR%\start-docker.bat" 2>&1 | tee -a "%LOG_FILE%"
if errorlevel 1 (
  echo start-docker failed. | tee -a "%LOG_FILE%"
  goto :ROLLBACK_PROMPT
)

echo Step 4/5: Seeding database (if seed script exists)... | tee -a "%LOG_FILE%"
if exist "%SCRIPTS_DIR%\db-seed.bat" (
  call "%SCRIPTS_DIR%\db-seed.bat" 2>&1 | tee -a "%LOG_FILE%"
) else (
  echo No db-seed.bat found — skipping. | tee -a "%LOG_FILE%"
)

echo Step 5/5: Starting AI engine (if present)... | tee -a "%LOG_FILE%"
if exist "%SCRIPTS_DIR%\start-ai-engine.bat" (
  call "%SCRIPTS_DIR%\start-ai-engine.bat" 2>&1 | tee -a "%LOG_FILE%"
) else (
  echo No start-ai-engine.bat found — skipping. | tee -a "%LOG_FILE%"
)

echo All steps completed. | tee -a "%LOG_FILE%"
exit /b 0

:ROLLBACK_PROMPT
echo.
set /p RB=Do you want to attempt automatic rollback (stop & reset containers)? Type YES to rollback:
if /I "%RB%"=="YES" goto :ROLLBACK
echo Leaving system as-is. Manual intervention required. | tee -a "%LOG_FILE%"
exit /b 1

:ROLLBACK
echo Running rollback: stopping containers and restoring last known state... | tee -a "%LOG_FILE%"
if exist "%SCRIPTS_DIR%\reset-docker.bat" (
  call "%SCRIPTS_DIR%\reset-docker.bat" 2>&1 | tee -a "%LOG_FILE%"
) else (
  echo reset-docker.bat not found — attempting docker stop/prune... | tee -a "%LOG_FILE%"
  docker-compose down --rmi local --volumes --remove-orphans 2>&1 | tee -a "%LOG_FILE%"
)
echo Rollback complete. | tee -a "%LOG_FILE%"
exit /b 1
