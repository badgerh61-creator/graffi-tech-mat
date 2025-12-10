@echo off
REM docker-logs-follow.bat
REM Follow logs for a container name/ID or for docker-compose services if none specified.

SETLOCAL

where docker >nul 2>&1
IF ERRORLEVEL 1 (
  echo ERROR: Docker CLI not found.
  ENDLOCAL
  exit /b 1
)

IF "%~1"=="" (
  REM No argument - try to use docker-compose if present
  where docker-compose >nul 2>&1
  if ERRORLEVEL 0 (
    echo No container provided. Following docker-compose logs (tail 200).
    docker-compose logs -f --tail=200
    ENDLOCAL
    exit /b 0
  ) else (
    echo No container name provided and docker-compose not available.
    echo Usage: %~nx0 container_name_or_id
    ENDLOCAL
    exit /b 2
  )
) ELSE (
  echo Following logs for: %~1
  docker logs -f --tail 200 %~1
  ENDLOCAL
  exit /b 0
)

ENDLOCAL
