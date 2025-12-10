@echo off
REM backup-config.bat — backups configuration files

set SRC=config
set DST=backups\config
set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%

mkdir "%DST%" >nul 2>&1

echo Backing up config folder...
powershell -NoProfile -Command "Compress-Archive -Path '%SRC%' -DestinationPath '%DST%/config-%DATE%.zip' -Force"

echo Config backup finished.
