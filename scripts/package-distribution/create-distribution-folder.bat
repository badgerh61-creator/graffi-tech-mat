@echo off
REM create-distribution-folder.bat
REM Prepares and normalizes distribution folder structure

setlocal enabledelayedexpansion

set ROOT_DIR=%~dp0
set DIST_DIR=%ROOT_DIR%dist
set TMP_DIR=%ROOT_DIR%dist_tmp
set LOGFILE=%ROOT_DIR%logs\create-dist-%date:~-10,2%%date:~-7,2%%date:~-4,4%.log

if not exist "%ROOT_DIR%logs" mkdir "%ROOT_DIR%logs"
echo [%date% %time%] Preparing distribution folders... >> "%LOGFILE%"

REM Create temp then move to final to avoid partial states
if exist "%TMP_DIR%" rmdir /S /Q "%TMP_DIR%"
mkdir "%TMP_DIR%"

mkdir "%TMP_DIR%\frontend"
mkdir "%TMP_DIR%\backend"
mkdir "%TMP_DIR%\assets"

REM Copy from build outputs (adjust names if needed)
if exist "%ROOT_DIR%\dist\frontend" xcopy /E /I /Y "%ROOT_DIR%\dist\frontend" "%TMP_DIR%\frontend" >> "%LOGFILE%" 2>&1
if exist "%ROOT_DIR%\dist\backend" xcopy /E /I /Y "%ROOT_DIR%\dist\backend" "%TMP_DIR%\backend" >> "%LOGFILE%" 2>&1
if exist "%ROOT_DIR%\assets" xcopy /E /I /Y "%ROOT_DIR%\assets" "%TMP_DIR%\assets" >> "%LOGFILE%" 2>&1

REM Replace final dist atomically
if exist "%DIST_DIR%" rmdir /S /Q "%DIST_DIR%"
rename "%TMP_DIR%" dist

echo [%date% %time%] Distribution prepared at %DIST_DIR% >> "%LOGFILE%"
exit /b 0
