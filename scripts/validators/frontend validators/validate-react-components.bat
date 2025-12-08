@echo off
set DIR=frontend\src\components

if not exist "%DIR%" (
  echo Components directory missing.
  exit /b 1
)

dir "%DIR%" | findstr ".jsx" >nul
if %ERRORLEVEL% neq 0 (
  echo No components found.
  exit /b 2
)

echo React components present.
exit /b 0
