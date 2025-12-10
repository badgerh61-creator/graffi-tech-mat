@echo off
REM Check backend routes folder structure

set ROUTES_DIR=src\routes

if not exist "%ROUTES_DIR%" (
  echo Missing routes directory.
  exit /b 1
)

dir "%ROUTES_DIR%" | findstr ".js" >nul
if %ERRORLEVEL% neq 0 (
  echo No route files found.
  exit /b 2
)

echo Routes validated.
exit /b 0
