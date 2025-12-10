@echo off
REM db-create-user.bat
REM Create a database role/user with limited privileges for your application.

SETLOCAL ENABLEDELAYEDEXPANSION

SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_SUPERUSER=postgres
SET PG_SUPERPASS=postgres
SET APP_USER=graffi_app
SET APP_PASS=change-me
SET APP_DB=graffi_db

echo === Create DB User ===

where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo psql not found.
    exit /b 1
)

echo Creating/altering user %APP_USER%...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '%APP_USER%') THEN CREATE ROLE %APP_USER% WITH LOGIN PASSWORD '%APP_PASS%'; ELSE ALTER ROLE %APP_USER% WITH PASSWORD '%APP_PASS%'; END IF; END \$\$;" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Failed to create/alter role.
    exit /b 2
)

echo Granting minimal privileges on DB %APP_DB%...
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -c "GRANT CONNECT ON DATABASE %APP_DB% TO %APP_USER%;" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -d %APP_DB% -c "GRANT USAGE ON SCHEMA public TO %APP_USER%;" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -d %APP_DB% -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO %APP_USER%;" 2>nul
psql -h %PG_HOST% -p %PG_PORT% -U %PG_SUPERUSER% -d %APP_DB% -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO %APP_USER%;" 2>nul

echo User %APP_USER% created/updated.
ENDLOCAL
