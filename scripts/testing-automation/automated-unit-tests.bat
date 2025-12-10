@echo off
title Running Unit Tests
color 0A
echo ==========================================
echo        RUNNING UNIT TESTS
echo ==========================================
echo.

REM Validate Node.js
node -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed.
    exit /b 1
)

echo Running backend unit tests...
cd backend
npm install --silent
npm run test || (
    echo [ERROR] Backend unit tests failed.
    exit /b 1
)
cd ..

echo Running frontend unit tests...
cd frontend
npm install --silent
npm run test || (
    echo [ERROR] Frontend unit tests failed.
    exit /b 1
)
cd ..

echo.
echo [SUCCESS] All unit tests passed!
exit /b 0
