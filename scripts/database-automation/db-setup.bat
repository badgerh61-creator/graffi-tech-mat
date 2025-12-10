@echo off
REM db-setup.bat
REM Creates a Postgres database, role, and runs initial migrations.
REM Edit the variables below for your environment.

SETLOCAL ENABLEDELAYEDEXPANSION

:: Config - change to your production/dev values
SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_SUPERUSER=postgres
SET PG_SUPERPASS=postgres
SET DB_NAME=graffi_db
SET DB_USER=graffi_app
SET DB_PASS=change-me
SET MIGRATIONS_DIR=src\backend\migrations

echo.
echo === Database Setup ===
echo Host: %PG_HOST% Port: %PG_PORT% DB: %DB_NAME% User: %DB_USER%
echo.

:: Check for psql
where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: psql not found in PATH. Please install PostgreSQL client tools.
    exit /b 1
)

:: Create user/role if not exists
echo Creating role if it doesn't exist...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '%DB_USER%') THEN CREATE ROLE %DB_USER% WITH LOGIN PASSWORD '%DB_PASS%'; ELSE ALTER ROLE %DB_USER% WITH PASSWORD '%DB_PASS%'; END IF; END \$\$;" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Could not create/alter role. Check credentials.
    exit /b 2
)

:: Create database if not exists and grant privileges
echo Creating database if it doesn't exist...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -c "SELECT 'CREATE DATABASE %DB_NAME%' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname='%DB_NAME%')\gexec" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;" 2>nul

echo Database and user ensured.

:: Run migrations if directory exists
if exist "%MIGRATIONS_DIR%" (
    echo Running migrations from %MIGRATIONS_DIR%...
    REM Assumes alembic or flask-migrate CLI is available; adjust as needed
    where alembic >nul 2>&1
    if %ERRORLEVEL%==0 (
        pushd %MIGRATIONS_DIR%
        alembic upgrade head
        popd
    ) else (
        echo alembic not found, skipping automatic migrations. Run migrations manually.
    )
) else (
    echo No migrations directory (%MIGRATIONS_DIR%) found — skipping migrations.
)

echo DB setup complete.
ENDLOCAL
