@echo off
REM Validates key .env values exist

setlocal enabledelayedexpansion

set ENV_FILE=.env
if not exist "%ENV_FILE%" (
  echo .env file missing.
  exit /b 2
)

for %%V in (API_URL DB_HOST DB_USER DB_PASS JWT_SECRET APP_KEY) do (
  findstr /B /C:"%%V=" "%ENV_FILE%" >nul
  if !ERRORLEVEL! neq 0 (
    echo Missing variable: %%V
    set ERR=1
  )
)

if "%ERR%"=="1" exit /b 1

echo All environment variables valid.
exit /b 0
