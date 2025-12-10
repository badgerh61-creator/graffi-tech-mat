@echo off
REM build-frontend-prod.bat
REM Builds frontend for production and copies output to dist/frontend

setlocal enabledelayedexpansion

:: === CONFIG ===
set ROOT_DIR=%~dp0
set FRONTEND_DIR=%ROOT_DIR%frontend
set OUT_DIR=%ROOT_DIR%dist\frontend
set LOGFILE=%ROOT_DIR%logs\build-frontend-%date:~-10,2%%date:~-7,2%%date:~-4,4%.log

:: create folders
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%ROOT_DIR%logs" mkdir "%ROOT_DIR%logs"

echo [%date% %time%] Starting frontend production build... >> "%LOGFILE%"

pushd "%FRONTEND_DIR%" || (
  echo Failed to cd into %FRONTEND_DIR% >> "%LOGFILE%"
  echo ERROR: frontend directory not found: %FRONTEND_DIR%
  exit /b 2
)

:: Ensure node and npm exist
where node >nul 2>&1
if errorlevel 1 (
  echo Node.js not found. Install Node 16+ and retry. >> "%LOGFILE%"
  echo ERROR: node not found
  popd
  exit /b 3
)

echo Installing dependencies... >> "%LOGFILE%"
npm ci >> "%LOGFILE%" 2>&1
if errorlevel 1 (
  echo npm ci failed. Check logs. >> "%LOGFILE%"
  popd
  exit /b 4
)

echo Running production build... >> "%LOGFILE%"
npm run build --if-present >> "%LOGFILE%" 2>&1
if errorlevel 1 (
  echo Build failed. See log: "%LOGFILE%"
  popd
  exit /b 5
)

REM Copy build output — common putpaths (adjust per framework)
if exist ".next" (
  xcopy /E /I /Y ".next" "%OUT_DIR%\.next" >> "%LOGFILE%" 2>&1
)
if exist "dist" (
  xcopy /E /I /Y "dist" "%OUT_DIR%\dist" >> "%LOGFILE%" 2>&1
)
if exist "build" (
  xcopy /E /I /Y "build" "%OUT_DIR%\build" >> "%LOGFILE%" 2>&1
)

echo [%date% %time%] Frontend build completed successfully. >> "%LOGFILE%"
popd
exit /b 0
