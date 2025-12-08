@echo off
rem ====================================================================
rem env-switch-mode.bat
rem Switch between .env.dev, .env.staging, .env.prod by copying to .env
rem Usage: env-switch-mode.bat dev   OR   env-switch-mode.bat prod
rem ====================================================================

if "%~1"=="" (
  echo Usage: %~nx0 ^<dev|staging|prod^>
  exit /b 1
)

set MODE=%~1
set SOURCE=.env.%MODE%
set DEST=.env

if not exist %SOURCE% (
  echo Source file %SOURCE% does not exist.
  exit /b 2
)

copy /Y %SOURCE% %DEST% >nul
if %ERRORLEVEL% neq 0 (
  echo Failed to copy %SOURCE% to %DEST%
  exit /b 3
)

echo Switched environment to %MODE% (^%SOURCE% -> %DEST%^)
exit /b 0
