@echo off
REM Basic backend security validator

type src\middlewares\auth.js >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Missing auth middleware.
  exit /b 1
)

findstr "helmet" package.json >nul
if %ERRORLEVEL% neq 0 (
  echo Helmet not installed. Security risk.
)

findstr "cors" package.json >nul
if %ERRORLEVEL% neq 0 (
  echo CORS library missing.
)

echo Backend security validation complete.
exit /b 0
