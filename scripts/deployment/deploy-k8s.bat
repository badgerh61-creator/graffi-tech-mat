@echo off
REM deploy-k8s.bat - deploy Kubernetes manifests

set NS=%1
if "%NS%"=="" set NS=production

echo Ensuring namespace exists...
kubectl get ns %NS% >nul 2>&1 || kubectl create ns %NS%

echo Applying manifests...
kubectl apply -n %NS% -f k8s/

echo Kubernetes deployment completed.
