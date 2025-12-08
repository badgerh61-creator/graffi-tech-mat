@echo off
REM docker-clean-all.bat
REM Interactive clean: stops containers and prunes images, caches, volumes and networks.

SETLOCAL

echo WARNING: This will remove all stopped containers, unused images, networks, and volumes.
echo Type Y to proceed, anything else to cancel.
set /p CONFIRM="Proceed? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
  echo Aborted by user. No changes made.
  ENDLOCAL
  exit /b 0
)

echo Checking Docker...
where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found. Aborting.
  ENDLOCAL
  exit /b 1
)

echo Stopping all running containers first...
for /f "usebackq tokens=*" %%C in (`docker ps -q`) do (
  echo Stopping %%C ...
  docker stop %%C
)

echo Running aggressive system prune (images, caches, volumes)...
docker system prune -a --volumes -f

if ERRORLEVEL 1 (
  echo WARNING: docker system prune reported errors.
) else (
  echo Docker cleanup completed successfully.
)

ENDLOCAL
exit /b 0
