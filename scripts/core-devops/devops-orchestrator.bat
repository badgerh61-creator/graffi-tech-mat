@echo off
REM devops-orchestrator.bat - a simple CLI to run devops tasks
SETLOCAL

set CMD=%1
shift

if "%CMD%"=="" (
  echo Usage: devops-orchestrator.bat ^<task^> [args...]
  echo Available: check reset cleanup package-backend package-frontend build release deploy destroy port-forward logs sign bump
  exit /b 1
)

if /I "%CMD%"=="check" call "%~dp0devops-check.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="reset" call "%~dp0reset-dev.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="cleanup" call "%~dp0cleanup-dev.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="package-backend" call "%~dp0package-backend.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="package-frontend" call "%~dp0package-frontend.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="build" call "%~dp0pipeline-build.bat" & exit /b %ERRORLEVEL%
if /I "%CMD%"=="release" shift & call "%~dp0pipeline-release.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="deploy" shift & call "%~dp0k8s-deploy.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="destroy" shift & call "%~dp0k8s-destroy.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="port-forward" shift & call "%~dp0k8s-port-forward.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="logs" shift & call "%~dp0k8s-logs.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="sign" shift & call "%~dp0sign-artifact-stub.bat" %* & exit /b %ERRORLEVEL%
if /I "%CMD%"=="bump" shift & call "%~dp0version-bump.bat" %* & exit /b %ERRORLEVEL%

echo Unknown task %CMD%
ENDLOCAL
