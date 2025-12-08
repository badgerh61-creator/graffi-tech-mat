@echo off
REM docker-run.bat
REM Runs backend & frontend containers (auto-detect if already running)

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_IMAGE=graffi-backend
SET FRONTEND_IMAGE=graffi-frontend
SET BACKEND_CONTAINER=graffi-backend-c
SET FRONTEND_CONTAINER=graffi-frontend-c

echo === Starting containers ===

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker not installed.
    exit /b 1
)

:: Backend
docker ps --format "{{.Names}}" | findstr /I "%BACKEND_CONTAINER%" >nul
if %ERRORLEVEL%==0 (
    echo Backend already running: %BACKEND_CONTAINER%
) else (
    docker run -d --name %BACKEND_CONTAINER% -p 5000:5000 %BACKEND_IMAGE%
)

:: Frontend
docker ps --format "{{.Names}}" | findstr /I "%FRONTEND_CONTAINER%" >nul
if %ERRORLEVEL%==0 (
    echo Frontend already running: %FRONTEND_CONTAINER%
) else (
    docker run -d --name %FRONTEND_CONTAINER% -p 3000:3000 %FRONTEND_IMAGE%
)

echo Containers started.
ENDLOCAL
