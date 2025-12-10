@echo off
title Running E2E Tests
color 0C
echo ==========================================
echo          RUNNING E2E TESTS
echo ==========================================
echo.

REM Validate global test runner (Cypress or Playwright)
npx cypress -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Cypress not installed. Installing...
    npm install cypress --location=global
)

echo Launching E2E tests...
cd tests/e2e
npx cypress run || (
    echo [ERROR] E2E tests failed.
    exit /b 1
)

cd ../..

echo.
echo [SUCCESS] All E2E tests passed.
exit /b 0
