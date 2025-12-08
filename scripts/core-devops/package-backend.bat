@echo off
REM package-backend.bat - build backend and create artifact (dotnet as example)
SETLOCAL

if not exist "%~dp0..\backend" (
  echo Backend folder not found at ../backend
  exit /b 1
)

pushd "%~dp0..\backend"
echo Restoring and building backend...
dotnet restore
dotnet publish -c Release -o ../automation/artifacts/backend

if %ERRORLEVEL% neq 0 (
  echo Build failed.
  popd
  exit /b 1
)

echo Backend package created at ../automation/artifacts/backend
popd
ENDLOCAL
