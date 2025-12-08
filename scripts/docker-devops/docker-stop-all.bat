@echo off
REM docker-stop-all.bat
REM Stops all running Docker containers.

SETLOCAL EnableDelayedExpansion

echo Checking for Docker...
where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found in PATH. Install Docker Desktop or Docker CLI and try again.
  exit /b 1
)

echo Retrieving running container IDs...
for /f "usebackq tokens=*" %%C in (`docker ps -q`) do (
  set "CID=%%C"
  if defined CID (
    echo Stopping container %%C ...
    docker stop %%C
  )
)

REM Check if any were running
for /f "usebackq tokens=*" %%C in (`docker ps -q`) do set RUNNING=1
if defined RUNNING (
  echo Some containers are still running.
) else (
  echo No running containers found (all stopped).
)

ENDLOCAL
exit /b 0
