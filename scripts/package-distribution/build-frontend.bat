@echo off
REM build-frontend.bat
REM Runs frontend production build and outputs to build/ or dist/

SETLOCAL ENABLEDELAYEDEXPANSION

SET FRONTEND_DIR=src\frontend
SET OUT_DIR=%FRONTEND_DIR%\build

echo === Building frontend ===

if not exist "%FRONTEND_DIR%" (
    echo Frontend folder not found.
    exit /b 1
)

pushd %FRONTEND_DIR%

where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo npm not found.
    popd
    exit /b 2
)

echo Installing dependencies (npm ci if lockfile present)...
if exist package-lock.json (
    npm ci --silent
) else (
    npm install --silent
)

echo Running production build...
REM Expecting scripts.build in package.json
npm run build --silent
IF %ERRORLEVEL% NEQ 0 (
    echo Frontend build failed.
    popd
    exit /b 3
)

echo Frontend build complete. Output in %OUT_DIR%
popd
ENDLOCAL
