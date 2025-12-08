@echo off
REM scaffold-infra.bat
REM Creates docker-compose and basic infra files

SETLOCAL ENABLEDELAYEDEXPANSION

SET INFRA_DIR=infra
SET DC_FILE=%INFRA_DIR%\docker-compose.yml
SET K8S_DIR=%INFRA_DIR%\k8s

echo.
echo === Scaffolding infra in %INFRA_DIR% ===
echo.

if not exist "%INFRA_DIR%" mkdir "%INFRA_DIR%"
if not exist "%K8S_DIR%" mkdir "%K8S_DIR%"

if not exist "%DC_FILE%" (
    (
    echo version: "3.8"
    echo services:
    echo   backend:
    echo     build: ../src/backend
    echo     ports:
    echo       - "5000:5000"
    echo     environment:
    echo       - FLASK_ENV=development
    echo   frontend:
    echo     build: ../src/frontend
    echo     ports:
    echo       - "3000:3000"
    ) > "%DC_FILE%"
    echo Created docker-compose.yml
) else (
    echo docker-compose.yml exists
)

:: Kubernetes placeholders
if not exist "%K8S_DIR%\deployment.yaml" (
    (
    echo apiVersion: apps/v1
    echo kind: Deployment
    echo metadata:
    echo   name: backend
    echo spec:
    echo   replicas: 1
    echo   selector:
    echo     matchLabels:
    echo       app: backend
    echo   template:
    echo     metadata:
    echo       labels:
    echo         app: backend
    echo     spec:
    echo       containers:
    echo       - name: backend
    echo         image: your-registry/backend:latest
    echo         ports:
    echo         - containerPort: 5000
    ) > "%K8S_DIR%\deployment.yaml"
    echo Created k8s/deployment.yaml
) else (
    echo k8s/deployment.yaml exists
)

echo Infra scaffolding complete.
ENDLOCAL
