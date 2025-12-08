@echo off
REM deploy-blue-green.bat - blue-green deployment

set NS=%1
if "%NS%"=="" set NS=production

echo Deploying BLUE version...

kubectl apply -n %NS% -f k8s/blue/

echo Switching traffic to BLUE service...
kubectl apply -n %NS% -f k8s/service-blue.yaml

echo Blue-Green deployment complete.
