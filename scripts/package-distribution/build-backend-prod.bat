@echo off
REM build-backend-prod.bat
REM Builds backend for production and copies output to dist/backend

setlocal enabledelayedexpansion

:: === CONFIG ===
set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend
set OUT_DIR=%ROOT_DIR%dist\backend
set LOGFILE=%ROOT_DIR%logs\build-backend-%date:~-10,2%%date:~-7,2%%date:~-4,4%.log

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%ROOT_DIR%logs" mkdir "%ROOT_DIR%logs"

echo [%date% %time%] Starting backend production build... >> "%LOGFILE%"

pushd "%BACKEND_DIR%" || (
  echo ERROR: backend directory not found: %BACKEND_DIR% >> "%LOGFILE%"
  echo Backend directory not found: %BACKEND_DIR%
  exit /b 2
)

:: Example for Node backend
if exist "package.json" (
  where node >nul 2>&1
  if errorlevel 1 (
    echo Node.js not found. Install Node and retry. >> "%LOGFILE%"
    popd
    exit /b 3
  )
  echo Installing backend deps... >> "%LOGFILE%"
  npm ci >> "%LOGFILE%" 2>&1
  if errorlevel 1 (
    echo npm ci failed >> "%LOGFILE%"
    popd
    exit /b 4
  )
  echo Building backend... >> "%LOGFILE%"
  npm run build --if-present >> "%LOGFILE%" 2>&1
  if errorlevel 1 (
    echo Backend build failed >> "%LOGFILE%"
    popd
    exit /b 5
  )
  REM copy relevant folders
  xcopy /E /I /Y "dist" "%OUT_DIR%\dist" >> "%LOGFILE%" 2>&1
)

:: Example for Python: create venv and copy required files (adjust as needed)
if exist "requirements.txt" (
  echo Packaging Python backend... >> "%LOGFILE%"
  if not exist "%OUT_DIR%\venv" (
    python -m venv "%OUT_DIR%\venv" >> "%LOGFILE%" 2>&1
  )
  REM copy source
  xcopy /E /I /Y "." "%OUT_DIR%\src" /EXCLUDE:README.md >> "%LOGFILE%" 2>&1
)

echo [%date% %time%] Backend build complete. >> "%LOGFILE%"
popd
exit /b 0
