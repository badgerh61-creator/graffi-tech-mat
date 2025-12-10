@echo off
REM deploy-env-validate.bat - validate runtime environment

echo Checking Kubernetes context...
kubectl config current-context || exit /b 1

echo Checking access...
kubectl auth can-i create deployments || exit /b 1

echo Checking registry access...
docker info >nul 2>&1 || exit /b 1

echo Environment validated. Safe to deploy.
