@echo off
REM test-load-backend.bat

echo === Backend Load Test (ab) ===

where ab >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ApacheBench (ab) not installed.
    exit /b 1
)

ab -n 500 -c 20 http://localhost:5000/health

echo Load test done.
