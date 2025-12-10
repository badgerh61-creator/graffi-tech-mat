@echo off
docker compose version >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo docker compose not installed.
  exit /b 1
)

echo Docker compose OK.
exit /b 0
