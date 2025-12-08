@echo off
REM docker-logs.bat

if "%~1"=="" (
    echo Streaming logs for ALL containers...
    docker logs graffi-backend-c -f
    docker logs graffi-frontend-c -f
) else (
    echo Logs for container: %~1
    docker logs %~1 -f
)
