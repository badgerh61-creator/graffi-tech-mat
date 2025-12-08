@echo off
REM docker-prune-forced.bat
REM Forcefully prunes unused images, containers, networks and volumes. NON-INTERACTIVE (CI safe).

SETLOCAL

where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found.
  ENDLOCAL
  exit /b 1
)

echo Executing non-interactive system prune (images, volumes, networks)...
docker system prune -a --volumes -f

if ERRORLEVEL 1 (
  echo WARNING: docker system prune returned an error.
  ENDLOCAL
  exit /b 2
) else (
  echo Prune complete.
)

ENDLOCAL
exit /b 0
