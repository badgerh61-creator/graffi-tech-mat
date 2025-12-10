@echo off
REM ============================================================
REM backup-assets.bat
REM Compresses the assets folder into a timestamped archive.
REM ============================================================

set ASSET_DIR=assets
set BACKUP_DIR=backups\\assets

if not exist backups mkdir backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

if not exist %ASSET_DIR% (
    echo No assets folder found.
    exit /b 1
)

set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%
set ZIP=%BACKUP_DIR%\\assets_%DATE%.zip

echo Compressing assets -> %ZIP%
powershell -NoProfile -Command "Compress-Archive -Path '%ASSET_DIR%' -DestinationPath '%ZIP%' -Force"

echo Assets backup completed.
