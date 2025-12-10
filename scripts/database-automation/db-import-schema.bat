@echo off
setlocal

:: Imports schema SQL file. Usage: db-import-schema.bat input.sql
set in=%1
if "%in%"=="" (
    echo Usage: db-import-schema.bat file.sql
    pause
    exit /b 1
)

if "%PGDATABASE%"=="" (
    echo Set PGDATABASE and PGUSER environment variables.
    pause
    exit /b 1
)

echo Importing schema from %in% into %PGDATABASE% ...
psql -d %PGDATABASE% -f "%in%"
if %errorlevel% neq 0 (
    echo Import failed.
    pause
    exit /b 1
)

echo Schema import complete.
endlocal
pause
