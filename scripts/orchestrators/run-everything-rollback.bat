@echo off
REM =========================================================================
REM run-everything-rollback.bat
REM Stops services, attempts to restore last DB backup and reset environment.
REM =========================================================================

setlocal enabledelayedexpansion
set SCRIPTS_DIR=%~dp0
set BACKUP_DIR=%SCRIPTS_DIR%\backups

echo ROLLBACK START: %DATE% %TIME%

echo Stopping docker & services...
if exist "%SCRIPTS_DIR%\docker-stop-all.bat" (
  call "%SCRIPTS_DIR%\docker-stop-all.bat"
) else (
  docker-compose down --remove-orphans
)

echo Attempting DB restore from latest backup...
if exist "%BACKUP_DIR%\latest.sql" (
  echo Restoring latest.sql...
  rem Adjust the restore command to your DB — example for Postgres with dockerized container named graffi_db
  docker exec -i graffi_db psql -U postgres -d graffi_db < "%BACKUP_DIR%\latest.sql" 2>nul || (
    echo Postgres restore failed — try manual restore.
  )
) else (
  echo No latest.sql found in %BACKUP_DIR% — skipping restore.
)

echo Restoring environment file if .env.bak exists...
if exist "%SCRIPTS_DIR%\.env.bak" (
  copy /Y "%SCRIPTS_DIR%\.env.bak" "%SCRIPTS_DIR%\.env"
  echo Restored .env from .env.bak
) else (
  echo No .env.bak found — skipping.
)

echo Pruning unused docker resources...
docker system prune -f

echo Rollback completed.
exit /b 0
