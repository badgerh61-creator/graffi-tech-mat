@echo off
where docker >nul
if %ERRORLEVEL% neq 0 (
  echo Docker CLI NOT installed.
  exit /b 1
)

docker --version
exit /b 0
