@echo off
REM ====================================================================
REM admin-log-rotate.bat
REM Rotates logs older than X days (default 7).
REM Usage: admin-log-rotate.bat [days]
REM ====================================================================

setlocal
set DAYS=%~1
if "%DAYS%"=="" set DAYS=7

set LOG_ROOT=%~dp0..\..\logs
set LOG_ARCHIVE=%LOG_ROOT%\archive
if not exist "%LOG_ARCHIVE%" mkdir "%LOG_ARCHIVE%"

echo Rotating logs older than %DAYS% days...

forfiles /p "%LOG_ROOT%" /s /m *.log /d -%DAYS% /c "cmd /c echo Moving @path && move @path \"%LOG_ARCHIVE%\" >nul 2>&1"

echo Log rotation complete.
endlocal
exit /b 0
