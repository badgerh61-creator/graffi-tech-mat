@echo off
REM build-release-package.bat
REM Creates a versioned release folder with frontend and backend artifacts

setlocal enabledelayedexpansion

:: === CONFIG ===
set ROOT_DIR=%~dp0
set DIST_DIR=%ROOT_DIR%dist
set RELEASES_DIR=%ROOT_DIR%releases
set VERSION=%1
if "%VERSION%"=="" set VERSION=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%
set VERSION=%VERSION: =0%
set RELEASE_DIR=%RELEASES_DIR%\release-%VERSION%
set LOGFILE=%ROOT_DIR%logs\release-%VERSION%.log

if not exist "%RELEASES_DIR%" mkdir "%RELEASES_DIR%"
if exist "%RELEASE_DIR%" rmdir /S /Q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"
if not exist "%ROOT_DIR%logs" mkdir "%ROOT_DIR%logs"

echo [%date% %time%] Creating release %VERSION% >> "%LOGFILE%"

:: Copy artifacts
if exist "%DIST_DIR%\frontend" (
  xcopy /E /I /Y "%DIST_DIR%\frontend" "%RELEASE_DIR%\frontend" >> "%LOGFILE%" 2>&1
) else (
  echo WARNING: frontend artifacts not found >> "%LOGFILE%"
)

if exist "%DIST_DIR%\backend" (
  xcopy /E /I /Y "%DIST_DIR%\backend" "%RELEASE_DIR%\backend" >> "%LOGFILE%" 2>&1
) else (
  echo WARNING: backend artifacts not found >> "%LOGFILE%"
)

:: Copy docs and assets if present
if exist "%ROOT_DIR%docs" xcopy /E /I /Y "%ROOT_DIR%docs" "%RELEASE_DIR%\docs" >> "%LOGFILE%" 2>&1
if exist "%ROOT_DIR%assets" xcopy /E /I /Y "%ROOT_DIR%assets" "%RELEASE_DIR%\assets" >> "%LOGFILE%" 2>&1

echo [%date% %time%] Release package created at %RELEASE_DIR% >> "%LOGFILE%"
echo Created release: %RELEASE_DIR%
exit /b 0
