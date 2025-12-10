@echo off
REM db-healthcheck.bat
REM Simple connectivity and replication health checks for Postgres.

SETLOCAL ENABLEDELAYEDEXPANSION

SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_USER=postgres

echo === DB Healthcheck ===

where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo psql not found.
    exit /b 1
)

echo Checking connection...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "SELECT now() as server_time, version();" -q
IF %ERRORLEVEL% NEQ 0 (
    echo Connection test failed.
    exit /b 2
)

echo Checking replication status (if configured)...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "SELECT pid, application_name, state, sync_priority, sync_state FROM pg_stat_replication;" -q
echo Healthcheck completed.
ENDLOCAL
