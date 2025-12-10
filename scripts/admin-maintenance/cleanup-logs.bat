@echo off
REM cleanup-logs.bat — deletes logs older than X days

set LOG_DIR=logs\archive
set DAYS=14

if not exist %LOG_DIR% (
    echo No log archive directory found.
    exit /b
)

echo Deleting logs older than %DAYS% days...
forfiles /p %LOG_DIR% /s /m *.zip /d -%DAYS% /c "cmd /c del @path"

echo Old log cleanup complete.
