@echo off
REM deploy-canary.bat - canary rollout

set NS=%1
if "%NS%"=="" set NS=production

echo Deploying CANARY version...

kubectl apply -n %NS% -f k8s/canary/

echo Routing 10 percent traffic...
kubectl apply -n %NS% -f k8s/canary-10.yaml

timeout /t 20

echo Routing 50 percent traffic...
kubectl apply -n %NS% -f k8s/canary-50.yaml

timeout /t 20

echo Routing 100 percent traffic (full rollout)...
kubectl apply -n %NS% -f k8s/canary-100.yaml

echo Canary deployment complete.
