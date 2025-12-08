@echo off
REM =========================================================================
REM run-everything-prod.bat
REM Production-oriented orchestrator: backup DB -> build -> artifacts -> deploy
REM =========================================================================

setlocal enabledelayedexpansion
set SCRIPTS_DIR=%~dp0
set LOG_DIR=%SCRIPTS_DIR%\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo PROD ORCHESTRATOR RUN - %DATE% %TIME% >> "%LOG_DIR%\prod_orchestrator.log"

echo WARNING: This script may modify production systems.
set /p CONFIRM=Type PROD to proceed: 
if /I NOT "%CONFIRM%"=="PROD" (
  echo Confirmation failed — aborting.
  exit /b 1
)

echo Step 1: Backup database...
if exist "%SCRIPTS_DIR%\backup-database.bat" (
  call "%SCRIPTS_DIR%\backup-database.bat" >> "%LOG_DIR%\prod_orchestrator.log" 2>&1
) else (
  echo No backup-database.bat found — ensure manual backup. >> "%LOG_DIR%\prod_orchestrator.log"
)

echo Step 2: Build backend and frontend...
call "%SCRIPTS_DIR%\build-backend-prod.bat" >> "%LOG_DIR%\prod_orchestrator.log" 2>&1
if errorlevel 1 (
  echo build-backend-prod failed. Aborting. >> "%LOG_DIR%\prod_orchestrator.log"
  exit /b 2
)
call "%SCRIPTS_DIR%\build-frontend-prod.bat" >> "%LOG_DIR%\prod_orchestrator.log" 2>&1
if errorlevel 1 (
  echo build-frontend-prod failed. Aborting. >> "%LOG_DIR%\prod_orchestrator.log"
  exit /b 3
)

echo Step 3: Create release package...
call "%SCRIPTS_DIR%\build-release-package.bat" >> "%LOG_DIR%\prod_orchestrator.log" 2>&1

echo Step 4: Deploy (custom deploy script or cloud CLI)
if exist "%SCRIPTS_DIR%\deploy-cloud.bat" (
  call "%SCRIPTS_DIR%\deploy-cloud.bat" >> "%LOG_DIR%\prod_orchestrator.log" 2>&1
) else (
  echo No deploy-cloud.bat provided — please deploy artifacts manually. >> "%LOG_DIR%\prod_orchestrator.log"
)

echo Production orchestrator finished. Check "%LOG_DIR%\prod_orchestrator.log"
exit /b 0
