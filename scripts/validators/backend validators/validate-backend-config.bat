@echo off
set CONFIG=src\config\config.js

if not exist "%CONFIG%" (
  echo Missing backend config.js
  exit /b 1
)

findstr "module.exports" "%CONFIG%" >nul
if %ERRORLEVEL% neq 0 (
  echo Invalid config.js (missing export)
  exit /b 2
)

echo Backend config OK.
exit /b 0
