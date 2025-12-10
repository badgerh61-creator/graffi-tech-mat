@echo off
REM db-backup.bat
REM Creates a timestamped pg_dump backup and keeps the last N backups (rotation).

SETLOCAL ENABLEDELAYEDEXPANSION

SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_USER=postgres
SET PG_DB=graffi_db
SET BACKUP_DIR=backups\db
SET KEEP=7

echo === DB Backup ===
echo Backups stored in %BACKUP_DIR% (keeping last %KEEP%)

mkdir "%BACKUP_DIR%" >nul 2>&1

where pg_dump >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pg_dump not found. Install PostgreSQL client tools.
    exit /b 1
)

FOR /F "tokens=1-4 delims=/ " %%a IN ('date /t') DO set TODAY=%%c-%%a-%%b
FOR /F "tokens=1-2 delims=: " %%a IN ('time /t') DO set TTIME=%%a%%b
SET TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%

SET FNAME=%BACKUP_DIR%\%PG_DB%_%TIMESTAMP%.sql

echo Creating backup: %FNAME%
pg_dump -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -F c -b -v -f "%FNAME%" %PG_DB%
IF %ERRORLEVEL% NEQ 0 (
    echo Backup failed.
    exit /b 2
)

echo Backup complete.

:: Rotation: delete older files beyond KEEP
echo Rotating backups, keeping last %KEEP%...
powershell -Command "Get-ChildItem -Path '%BACKUP_DIR%' -Filter '%PG_DB%_*.sql' | Sort-Object LastWriteTime -Descending | Select-Object -Skip %KEEP% | ForEach-Object { Remove-Item \$_ -Force }"

echo Backup rotation complete.
ENDLOCAL
