@echo off
REM ============================================================
REM restore-database.bat
REM Restores the most recent database backup.
REM ============================================================

set BACKUP_DIR=backups
if not exist %BACKUP_DIR% (
    echo No backups directory found.
    exit /b 1
)

echo Finding latest backup...
for /f "delims=" %%F in ('dir /b /od "%BACKUP_DIR%"') do set LAST=%%F

echo Latest backup found: %LAST%
set FILE=%BACKUP_DIR%\\%LAST%

REM SQLite restore
if "%FILE:~-3%"==".db" (
    echo Restoring SQLite...
    copy /Y %FILE% database.sqlite
    echo SQLite restore complete.
    exit /b 0
)

REM PostgreSQL restore
if "%FILE:~-5%"==".dump" (
    echo Restoring PostgreSQL...
    pg_restore -U postgres -d postgres --clean --if-exists %FILE%
    echo PostgreSQL restore complete.
    exit /b 0
)

REM MySQL restore
if "%FILE:~-4%"==".sql" (
    echo Restoring MySQL...
    mysql -u root < %FILE%
    echo MySQL restore complete.
    exit /b 0
)

echo Unknown backup format: %FILE%
exit /b 1
