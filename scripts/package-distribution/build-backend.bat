@echo off
REM build-backend.bat
REM Builds a Python wheel and sdist for the backend.

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_DIR=src\backend
SET DIST_DIR=%BACKEND_DIR%\dist

echo === Building backend artifacts ===

if not exist "%BACKEND_DIR%" (
    echo Backend folder not found: %BACKEND_DIR%
    exit /b 1
)

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH.
    exit /b 2
)

pushd %BACKEND_DIR%

REM Ensure build tools
python -m pip install --upgrade pip setuptools wheel build >nul 2>&1

REM Clean previous dist
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"

REM Build wheel + sdist
python -m build
IF %ERRORLEVEL% NEQ 0 (
    echo Backend build failed.
    popd
    exit /b 3
)

echo Backend artifacts created in %DIST_DIR%
popd
ENDLOCAL
