@echo off
REM test-backend.bat

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_DIR=src\backend

echo === Backend Tests ===

if not exist "%BACKEND_DIR%" (
    echo Backend folder not found.
    exit /b 1
)

where pytest >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pytest not installed. Install with: pip install pytest
    exit /b 2
)

pushd %BACKEND_DIR%
pytest -q
popd

echo Backend tests complete.
ENDLOCAL
