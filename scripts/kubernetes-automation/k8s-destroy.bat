@echo off
REM k8s-destroy.bat - remove a helm release or namespace
SETLOCAL

if "%~1"=="" (
  echo Usage: k8s-destroy.bat <namespace> [releaseName]
  exit /b 2
)

set NS=%1
set REL=%2

if not "%REL%"=="" (
  echo Uninstalling helm release %REL% in %NS%...
  helm uninstall %REL% -n %NS%
) else (
  echo Deleting namespace %NS% and all resources...
  kubectl delete ns %NS%
)

echo Destroy complete.
ENDLOCAL
