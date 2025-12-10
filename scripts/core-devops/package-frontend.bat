@echo off
REM package-frontend.bat - build frontend (npm/yarn)
SETLOCAL

if not exist "%~dp0..\frontend" (
  echo Frontend folder not found at ../frontend
  exit /b 1
)

pushd "%~dp0..\frontend"
if exist package.json (
  echo Installing frontend deps...
  npm ci

  echo Building frontend...
  npm run build
  if %ERRORLEVEL% neq 0 (
    echo Frontend build failed.
    popd
    exit /b 1
  )
  REM copy build artifacts
  if exist build rmdir /s /q ..\automation\artifacts\frontend
  xcopy /E /I /Y build ..\automation\artifacts\frontend >nul
  echo Frontend packaged to ../automation/artifacts/frontend
) else (
  echo package.json not found. Skipping frontend build.
)
popd
ENDLOCAL
