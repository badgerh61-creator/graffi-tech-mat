@echo off
REM docker-dev-up.bat

where docker-compose >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo docker-compose not found.
    exit /b 1
)

echo Starting dev environment...
docker-compose -f infra\docker-compose.yml up -d

echo Dev environment ready.
