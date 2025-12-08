@echo off
REM backup-logs.bat — daily log backup

set LOG_DIR=logs
set BUP_DIR=backups\logs
set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%

mkdir "%BUP_DIR%" >nul 2>&1

echo Backing up logs...
powershell -NoProfile -Command "Compress-Archive -Path '%LOG_DIR%' -DestinationPath '%BUP_DIR%/logs-backup-%DATE%.zip' -Force"

echo Log backup complete.
