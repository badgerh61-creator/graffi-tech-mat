@echo off
REM docker-build-prod.bat
REM Build production Docker images with version tag.

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_IMAGE=graffi-backend
SET FRONTEND_IMAGE=graffi-frontend
SET VERSION=1.0.0
SET REGISTRY=myregistry.example.com/yourorg

echo === Building production Docker images (tag %VERSION%) ===

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker not found.
    exit /b 1
)

docker build --no-cache -t %BACKEND_IMAGE%:%VERSION% -f src\backend\Dockerfile src\backend
IF %ERRORLEVEL% NEQ 0 exit /b 2

docker build --no-cache -t %FRONTEND_IMAGE%:%VERSION% -f src\frontend\Dockerfile src\frontend
IF %ERRORLEVEL% NEQ 0 exit /b 3

echo Tagging for registry...
docker tag %BACKEND_IMAGE%:%VERSION% %REGISTRY%/%BACKEND_IMAGE%:%VERSION%
docker tag %FRONTEND_IMAGE%:%VERSION% %REGISTRY%/%FRONTEND_IMAGE%:%VERSION%

echo Production images built and tagged.
ENDLOCAL
