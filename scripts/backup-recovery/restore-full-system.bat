@echo off
REM ============================================================
REM restore-full-system.bat
REM Performs a full system restore from backup directories.
REM ============================================================

echo === FULL SYSTEM RESTORE STARTED ===

REM 1. Restore database
if exist restore-database.bat (
    call restore-database.bat
) else (
    echo Missing restore-database.bat
)

REM 2. Restore config files
if exist backups\\configs (
    echo Restoring configs...
    for %%F in (backups\\configs\\*) do (
        set FILE=%%F
        copy /Y "%%F" . >nul
        echo Restored config: %%~nxF
    )
)

REM 3. Restore assets
if exist backups\\assets (
    echo Restoring assets...
    for /f "delims=" %%Z in ('dir /b /od backups\\assets') do set LAST_ASSET=%%Z
    powershell -NoProfile -Command "Expand-Archive -Path 'backups/assets/%LAST_ASSET%' -DestinationPath '.' -Force"
)

echo === FULL SYSTEM RESTORE COMPLETE ===
exit /b 0
