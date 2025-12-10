@echo off
REM docker-deploy-local.bat
REM Deploy locally using docker-compose. Usage: docker-deploy-local.bat [compose-file] [--force-recreate]

SETLOCAL

where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found.
  ENDLOCAL
  exit /b 1
)

set "COMPOSE=%~1"
if "%COMPOSE%"=="" set "COMPOSE=docker-compose.yml"

set "EXTRA=%~2"

if exist "%COMPOSE%" (
  echo Deploying stack using %COMPOSE% ...
  docker-compose -f "%COMPOSE%" up -d %EXTRA%
  if ERRORLEVEL 1 (
    echo ERROR: docker-compose up reported an error.
    ENDLOCAL
    exit /b 2
  ) else (
    echo Deployment completed (services should be up).
  )
) else (
  echo ERROR: Compose file %COMPOSE% not found. Aborting.
  ENDLOCAL
  exit /b 3
)

ENDLOCAL
exit /b 0
