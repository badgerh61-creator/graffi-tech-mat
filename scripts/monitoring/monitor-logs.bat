@echo off
REM ============================================================
REM monitor-logs.bat
REM Streams logs from backend, frontend, or Docker containers.
REM Usage: monitor-logs backend | frontend | docker
REM ============================================================

if "%~1"=="" (
    echo Usage: %~nx0 ^<backend|frontend|docker^>
    exit /b 1
)

set TARGET=%1

if /I "%TARGET%"=="backend" (
    echo === Monitoring backend logs ===
    type backend.log
    exit /b 0
)

if /I "%TARGET%"=="frontend" (
    echo === Monitoring frontend logs ===
    type frontend.log
    exit /b 0
)

if /I "%TARGET%"=="docker" (
    echo === Docker real-time logs ===
    docker compose logs -f
    exit /b 0
)

echo Invalid target: %TARGET%
exit /b 2
