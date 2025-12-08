@echo off
REM rotate-logs.bat — rotates & compresses logs

set LOG_DIR=logs
set ARCHIVE_DIR=logs\archive
set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%

mkdir "%LOG_DIR%" >nul 2>&1
mkdir "%ARCHIVE_DIR%" >nul 2>&1

echo Rotating logs on %DATE%...

for %%L in (backend.log frontend.log system.log error.log api.log) do (
    if exist %LOG_DIR%\%%L (
        echo Compressing %%L...
        powershell -NoProfile -Command "Compress-Archive -Path '%LOG_DIR%/%%L' -DestinationPath '%ARCHIVE_DIR%/%%L-%DATE%.zip' -Force"
        echo Clearing file: %%L
        echo. > %LOG_DIR%\%%L
    )
)

echo Log rotation complete.

