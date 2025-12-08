@echo off
REM docker-build.bat
REM Builds backend & frontend Docker images.

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_IMAGE=graffi-backend
SET FRONTEND_IMAGE=graffi-frontend
SET VERSION=latest

echo === Building Docker images ===

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Docker not found.
    exit /b 1
)

echo Building backend image...
docker build -t %BACKEND_IMAGE%:%VERSION% -f src\backend\Dockerfile src\backend
IF %ERRORLEVEL% NEQ 0 (
    echo Backend build FAILED.
    exit /b 2
)

echo Building frontend image...
docker build -t %FRONTEND_IMAGE%:%VERSION% -f src\frontend\Dockerfile src\frontend
IF %ERRORLEVEL% NEQ 0 (
    echo Frontend build FAILED.
    exit /b 3
)

echo Docker images built successfully.
ENDLOCAL
