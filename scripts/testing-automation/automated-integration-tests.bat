@echo off
title Running Integration Tests
color 0B

echo ==========================================
echo       RUNNING INTEGRATION TESTS
echo ==========================================
echo.

REM Ensure backend server is running
echo Checking if backend is running...
tasklist /FI "IMAGENAME eq node.exe" | find /I "node.exe" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Backend not running. Starting backend...
    start cmd /c "cd backend && npm run dev"
    timeout /t 5 >nul
)

echo Executing integration tests...
cd tests/integration
npm install --silent
npm run test || (
    echo [ERROR] Integration tests failed.
    exit /b 1
)

cd ../..

echo.
echo [SUCCESS] Integration tests completed.
exit /b 0
