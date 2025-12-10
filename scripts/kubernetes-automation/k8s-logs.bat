@echo off
REM k8s-logs.bat - stream logs for a pod label or container
SETLOCAL

if "%~1"=="" (
  echo Usage: k8s-logs.bat <namespace> <label-selector> [container]
  echo Example: k8s-logs.bat staging app=graffi web
  exit /b 2
)

set NS=%1
set LABEL=%2
set CONTAINER=%3

for /f "tokens=1" %%p in ('kubectl get pods -n %NS% -l %LABEL% -o jsonpath^"{.items[0].metadata.name}^"') do set POD=%%p

if "%POD%"=="" (
  echo No pod found for selector %LABEL% in %NS%
  exit /b 1
)

if "%CONTAINER%"=="" (
  kubectl logs -n %NS% -f %POD%
) else (
  kubectl logs -n %NS% -f %POD% -c %CONTAINER%
)
ENDLOCAL
