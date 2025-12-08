@echo off

cd frontend
npm run build --dry-run >nul 2>&1

if %ERRORLEVEL% neq 0 (
  echo Frontend not build-ready.
  exit /b 1
)

echo Frontend build ready.
exit /b 0
