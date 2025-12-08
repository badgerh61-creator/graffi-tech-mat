@echo off
REM deploy-zero-downtime.bat - rolling update strategy

set NS=%1
if "%NS%"=="" set NS=production

echo Performing rolling update...

kubectl rollout restart deployment/graffi-backend -n %NS%
kubectl rollout restart deployment/graffi-frontend -n %NS%

echo Waiting for rollout...
kubectl rollout status deployment/graffi-backend -n %NS%
kubectl rollout status deployment/graffi-frontend -n %NS%

echo Zero-downtime deployment completed.
