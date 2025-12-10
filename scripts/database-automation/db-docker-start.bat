@echo off
REM db-docker-start.bat
REM Starts a Docker Postgres container for local development (idempotent).

SETLOCAL ENABLEDELAYEDEXPANSION

SET CONTAINER_NAME=graffi-postgres
SET POSTGRES_VERSION=15
SET POSTGRES_PASSWORD=postgres
SET POSTGRES_DB=graffi_db
SET PG_PORT=5432
SET VOLUME_NAME=graffi_pgdata

echo === Start Docker Postgres for dev ===

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker not found. Install Docker Desktop.
    exit /b 1
)

:: Create volume if not exists
docker volume inspect %VOLUME_NAME% >nul 2>&1
if %ERRORLEVEL% neq 0 (
    docker volume create %VOLUME_NAME% >nul
    echo Created volume %VOLUME_NAME%
) else (
    echo Volume %VOLUME_NAME% exists
)

:: Start container if not running
docker ps -a --format "{{.Names}}" | findstr /I "%CONTAINER_NAME%" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Container %CONTAINER_NAME% already exists. Starting if stopped...
    docker start %CONTAINER_NAME% >nul 2>&1
) else (
    echo Creating and starting container %CONTAINER_NAME%...
    docker run -d --name %CONTAINER_NAME% -e POSTGRES_PASSWORD=%POSTGRES_PASSWORD% -e POSTGRES_DB=%POSTGRES_DB% -p %PG_PORT%:5432 -v %VOLUME_NAME%:/var/lib/postgresql/data postgres:%POSTGRES_VERSION%
)

echo Waiting for Postgres to be ready (checking up to 30s)...
SET /A COUNTER=0
:checkloop
timeout /t 2 >nul
docker exec %CONTAINER_NAME% pg_isready -U postgres >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Postgres is ready.
) else (
    SET /A COUNTER+=2
    if %COUNTER% GEQ 30 (
        echo Timeout waiting for Postgres to be ready.
        exit /b 2
    )
    goto checkloop
)

echo Docker Postgres ready.
ENDLOCAL
