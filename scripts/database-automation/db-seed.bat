@echo off
REM db-seed.bat
REM Seeds initial data into the database. Designed to be idempotent.

SETLOCAL ENABLEDELAYEDEXPANSION

SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_USER=graffi_app
SET PG_DB=graffi_db
SET SEED_SQL=infra/db/seeds/seed.sql

echo === DB Seed ===

if not exist "%SEED_SQL%" (
    echo No seed file found at %SEED_SQL%. Creating a sample idempotent seed.
    mkdir infra\db\seeds >nul 2>&1
    (
    echo -- idempotent seed example
    echo DO \$\$
    echo BEGIN
    echo   IF NOT EXISTS (SELECT 1 FROM users WHERE email='admin@example.com') THEN
    echo     INSERT INTO users (email, name, role) VALUES ('admin@example.com','Admin','admin');
    echo   END IF;
    echo END;
    echo \$\$;
    ) > "%SEED_SQL%"
    echo Created example seed at %SEED_SQL% - edit to add your seeds.
)

where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo psql not found. Install PostgreSQL client tools.
    exit /b 1
)

echo Running seed SQL...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %PG_DB% -f "%SEED_SQL%"
IF %ERRORLEVEL% NEQ 0 (
    echo Seeding failed.
    exit /b 2
)

echo Seeding complete.
ENDLOCAL
