@echo off
set API=http://localhost:3000

curl %API%/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo API down or not responding.
  exit /b 1
)

echo API endpoints valid.
exit /b 0
