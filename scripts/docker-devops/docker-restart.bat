@echo off
REM docker-restart.bat
REM Restarts all containers (stops running ones then starts them by id).

SETLOCAL EnableDelayedExpansion

echo Checking for Docker...
where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found. Aborting.
  exit /b 1
)

echo Getting list of all container IDs...
set "HAS_CONTAINERS="
for /f "usebackq tokens=*" %%C in (`docker ps -aq`) do (
  set "HAS_CONTAINERS=1"
  echo Restarting container %%C ...
  docker restart %%C
)

if not defined HAS_CONTAINERS (
  echo No containers found to restart.
)

ENDLOCAL
exit /b 0
