@echo off
REM k8s-deploy.bat - deploy charts/manifests to Kubernetes cluster
SETLOCAL

if "%~1"=="" (
  echo Usage: k8s-deploy.bat <namespace> [chart|manifest]
  echo Example: k8s-deploy.bat staging chart
  exit /b 2
)

set NS=%1
set MODE=%2

echo Ensuring namespace %NS% exists...
kubectl get ns %NS% >nul 2>&1 || kubectl create ns %NS%

if /I "%MODE%"=="chart" (
  echo Deploying helm chart to %NS%...
  helm upgrade --install graffi .\charts\graffi -n %NS% --set image.tag=latest
) else (
  echo Applying kubernetes manifests to %NS%...
  kubectl apply -n %NS% -f k8s/
)

echo Deploy operation complete.
ENDLOCAL
