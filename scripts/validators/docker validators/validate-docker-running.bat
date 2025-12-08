@echo off
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Docker daemon not running.
  exit /b 1
)

echo Docker daemon OK.
exit /b 0
