@echo off
REM Check if backend deps are installed

if not exist package.json (
  echo No backend package.json found.
  exit /b 2
)

npm ls >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Backend dependencies are missing or corrupted.
  exit /b 1
)

echo Backend dependencies OK.
exit /b 0
