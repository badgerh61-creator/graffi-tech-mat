@echo off
REM db-migrate.bat
REM Run DB migrations (Alembic / Flask-Migrate). Idempotent and safe to rerun.

SETLOCAL ENABLEDELAYEDEXPANSION

SET MIGRATIONS_DIR=src\backend\migrations
SET MIGRATE_CMD=alembic

echo === DB Migrate ===

if not exist "%MIGRATIONS_DIR%" (
    echo Migrations directory not found: %MIGRATIONS_DIR%
    exit /b 1
)

where %MIGRATE_CMD% >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %MIGRATE_CMD% not found. Ensure Alembic or your migration tool is installed.
    exit /b 2
)

pushd %MIGRATIONS_DIR%
%MIGRATE_CMD% upgrade head
IF %ERRORLEVEL% NEQ 0 (
    echo Migrations failed.
    popd
    exit /b 3
)
popd

echo Migrations applied successfully.
ENDLOCAL
