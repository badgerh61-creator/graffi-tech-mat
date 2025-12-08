@echo off
REM k8s-port-forward.bat - port-forward a service or pod
SETLOCAL

if "%~1"=="" (
  echo Usage: k8s-port-forward.bat <namespace> <svc-or-pod> <localPort>:<remotePort>
  echo Example: k8s-port-forward.bat staging svc/graffi 8080:80
  exit /b 2
)

set NS=%1
set TARGET=%2
set PORTMAP=%3

kubectl port-forward -n %NS% %TARGET% %PORTMAP%
ENDLOCAL
