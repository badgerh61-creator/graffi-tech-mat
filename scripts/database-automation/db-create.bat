@echo off
setlocal

:: Usage: db-create.bat [postgres|mongo]
set db=%1
if "%db%"=="" set db=postgres

if /I "%db%"=="postgres" (
    echo Creating PostgreSQL database...
    if "%PGDATABASE%"=="" (
        echo Please set PGDATABASE and PGUSER environment variables or pass connection via PG* env vars.
        pause
        exit /b 1
    )
    psql -c "CREATE DATABASE %PGDATABASE%;" 2>nul
    if %errorlevel% neq 0 (
        echo Could not create database or it already exists.
    ) else (
        echo Database %PGDATABASE% created.
    )
) else (
    echo MongoDB selected: creating database is automatic on first write.
)

endlocal
pause
