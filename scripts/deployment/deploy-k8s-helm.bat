@echo off
REM deploy-k8s-helm.bat - deploy helm chart to namespace

set NS=%1
set TAG=%2

if "%NS%"=="" (
    echo Usage: deploy-k8s-helm.bat ^<namespace^> ^<tag^>
    exit /b 1
)

if "%TAG%"=="" set TAG=latest

echo Deploying version %TAG% to namespace %NS%

helm upgrade --install graffi ./charts/graffi ^
  --namespace %NS% ^
  --set image.tag=%TAG%

echo Helm deployment complete.
