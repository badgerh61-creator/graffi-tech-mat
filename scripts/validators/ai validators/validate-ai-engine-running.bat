@echo off
curl http://localhost:5050/health >nul 2>&1

if %ERRORLEVEL% neq 0 (
  echo AI Engine is not running.
  exit /b 1
)

echo AI Engine online.
exit /b 0
