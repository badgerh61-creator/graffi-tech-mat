@echo off
REM ============================================================
REM backup-configs.bat
REM Backs up all config files (.env, .yaml, .json).
REM ============================================================

set BACKUP_DIR=backups\\configs
if not exist backups mkdir backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%
set DATE=%DATE: =0%

echo === Backing up config files ===

for %%F in (
    .env
    .env.local
    config.json
    settings.json
    app.yaml
) do (
    if exist %%F (
        copy /Y %%F %BACKUP_DIR%\\%%~nF_%DATE%%%~xF >nul
        echo Backed up: %%F
    )
)

echo Configuration backup completed.
