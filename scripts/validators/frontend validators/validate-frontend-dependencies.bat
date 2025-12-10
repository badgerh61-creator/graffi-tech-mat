@echo off
cd frontend

npm ls >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Frontend dependencies missing or corrupted.
  exit /b 1
)

echo Frontend deps OK.
exit /b 0
