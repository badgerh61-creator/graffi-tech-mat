@echo off
REM compress-artifacts.bat
REM Compresses a release folder into a timestamped zip file

setlocal enabledelayedexpansion

set ROOT_DIR=%~dp0
set RELEASE_DIR=%1
if "%RELEASE_DIR%"=="" set RELEASE_DIR=%ROOT_DIR%releases
set OUT_DIR=%ROOT_DIR%packages
set TIMESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set ZIPNAME=release-%TIMESTAMP%.zip
set ZIPPATH=%OUT_DIR%\%ZIPNAME%
set LOGFILE=%ROOT_DIR%logs\compress-%TIMESTAMP%.log

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%ROOT_DIR%logs" mkdir "%ROOT_DIR%logs"

echo [%date% %time%] Compressing %RELEASE_DIR% to %ZIPPATH% >> "%LOGFILE%"

powershell -NoProfile -Command ^
  "try { Remove-Item -Path '%ZIPPATH%' -ErrorAction SilentlyContinue } catch {} ; `
   Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIPPATH%' -Force ; exit $LASTEXITCODE" >> "%LOGFILE%" 2>&1

if errorlevel 1 (
  echo Compression failed. See %LOGFILE%
  exit /b 2
)

echo [%date% %time%] Compression successful: %ZIPPATH% >> "%LOGFILE%"
echo %ZIPPATH%
exit /b 0
