@echo off
REM ============================================================
REM backup-database.bat
REM Creates a timestamped database backup.
REM Supports PostgreSQL, MySQL, SQLite.
REM ============================================================

set BACKUP_DIR=backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%
set DATE=%DATE: =0%

echo === Database Backup Started ===
echo Timestamp: %DATE%
echo.

REM Detect SQLite first
if exist database.sqlite (
    echo Detected SQLite database...
    copy /Y database.sqlite %BACKUP_DIR%\\sqlite_backup_%DATE%.db
    echo SQLite backup completed.
    exit /b 0
)

REM Postgres?
where pg_dump >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Detected PostgreSQL...
    pg_dump -U postgres -F c --file=%BACKUP_DIR%\\pg_backup_%DATE%.dump
    echo PostgreSQL backup completed.
    exit /b 0
)

REM MySQL?
where mysqldump >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Detected MySQL/MariaDB...
    mysqldump -u root --all-databases > %BACKUP_DIR%\\mysql_backup_%DATE%.sql
    echo MySQL backup completed.
    exit /b 0
)

echo ERROR: No supported database engine detected.
exit /b 1
