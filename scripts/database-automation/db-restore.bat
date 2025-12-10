@echo off
REM db-restore.bat
REM Restores a backup file into a database. Use with caution.

SETLOCAL ENABLEDELAYEDEXPANSION

SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_USER=postgres
SET TARGET_DB=graffi_db
SET BACKUP_FILE=

echo === DB Restore ===
echo Usage: %~nx0 path\to\backup.sql
if "%~1"=="" (
    echo ERROR: No backup file specified.
    exit /b 1
) else (
    SET BACKUP_FILE=%~1
)

if not exist "%BACKUP_FILE%" (
    echo ERROR: Backup file not found: %BACKUP_FILE%
    exit /b 2
)

where pg_restore >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pg_restore not found. Install PostgreSQL client tools.
    exit /b 3
)

echo Stopping connections to target DB %TARGET_DB%...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '%TARGET_DB%';" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '%TARGET_DB%';" 2>nul

echo Dropping and recreating target DB...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "DROP DATABASE IF EXISTS %TARGET_DB%;" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -c "CREATE DATABASE %TARGET_DB%;" 2>nul

echo Restoring from %BACKUP_FILE% ...
pg_restore -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %TARGET_DB% -v "%BACKUP_FILE%"
IF %ERRORLEVEL% NEQ 0 (
    echo Restore failed.
    exit /b 4
)

echo Restore complete.
ENDLOCAL
