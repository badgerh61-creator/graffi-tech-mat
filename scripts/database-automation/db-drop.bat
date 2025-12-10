@echo off
setlocal

:: Usage: db-drop.bat [postgres|mongo]
set db=%1
if "%db%"=="" set db=postgres

if /I "%db%"=="postgres" (
    echo Dropping PostgreSQL database...
    if "%PGDATABASE%"=="" (
        echo Please set PGDATABASE and PGUSER environment variables.
        pause
        exit /b 1
    )
    psql -c "DROP DATABASE IF EXISTS %PGDATABASE%;" 2>nul
    if %errorlevel% neq 0 (
        echo Failed to drop database.
    ) else (
        echo Database %PGDATABASE% dropped.
    )
) else (
    echo MongoDB selected: dropping database via mongo shell...
    if "%MONGO_URI%"=="" (
        echo Please set MONGO_URI environment variable.
        pause
        exit /b 1
    )
    mongo %MONGO_URI% --eval "db.getSiblingDB('%MONGO_DB%').dropDatabase()"
)

endlocal
pause
