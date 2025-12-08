@echo off
REM db-cleanup.bat
REM Cleanup dev DB container, volume and temp backups (prompted).

SETLOCAL ENABLEDELAYEDEXPANSION

SET CONTAINER_NAME=graffi-postgres
SET VOLUME_NAME=graffi_pgdata
SET BACKUP_DIR=backups\db

echo WARNING: This will remove local DB container, volume and backups. Press Ctrl-C to cancel.
pause

where docker >nul 2>&1
if %ERRORLEVEL%==0 (
    docker stop %CONTAINER_NAME% 2>nul
    docker rm %CONTAINER_NAME% 2>nul
    docker volume rm %VOLUME_NAME% 2>nul
    echo Docker container/volume removed (if existed).
) else (
    echo Docker not found or not available; skipping container/volume cleanup.
)

if exist "%BACKUP_DIR%" (
    echo Removing backup files in %BACKUP_DIR% ...
    rmdir /s /q "%BACKUP_DIR%"
    echo Backups removed.
) else (
    echo No backups directory found.
)

echo Cleanup complete.
ENDLOCAL
