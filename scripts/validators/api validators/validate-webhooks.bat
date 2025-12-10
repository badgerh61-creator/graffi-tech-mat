@echo off
set HOOK=http://localhost:3000/webhook/test

curl -X POST -d "{}" %HOOK% >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Webhook not responding.
  exit /b 1
)

echo Webhook endpoint OK.
exit /b 0
