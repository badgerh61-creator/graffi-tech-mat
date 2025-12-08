@echo off
setlocal

:: Exports schema (Postgres shown). Usage: db-export-schema.bat output.sql
set out=%1
if "%out%"=="" set out=./db_schema.sql

if "%PGDATABASE%"=="" (
    echo Set PGDATABASE and PGUSER environment variables.
    pause
    exit /b 1
)

echo Exporting schema to %out% ...
pg_dump --schema-only --no-owner --no-privileges -f "%out%" %PGDATABASE%
if %errorlevel% neq 0 (
    echo pg_dump failed. Ensure pg_dump is available and env vars are set.
    pause
    exit /b 1
)

echo Schema exported to %out%.
endlocal
pause
