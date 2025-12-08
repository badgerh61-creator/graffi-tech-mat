@echo off
REM test-security.bat

echo === Security Scans ===

where bandit >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Running Python security scan...
    bandit -r src\backend
) else (
    echo bandit not installed.
)

pushd src\frontend
where npm >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Checking Node vulnerabilities...
    npm audit --audit-level=high
) else (
    echo npm not installed.
)
popd

echo Security test complete.
