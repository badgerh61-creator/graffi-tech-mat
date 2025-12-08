@echo off
set SCHEMA=docs\openapi.json

if not exist "%SCHEMA%" (
  echo Missing OpenAPI schema.
  exit /b 1
)

findstr "\"openapi\"" "%SCHEMA%" >nul
if %ERRORLEVEL% neq 0 (
  echo Invalid OpenAPI schema.
  exit /b 2
)

echo OpenAPI schema OK.
exit /b 0
