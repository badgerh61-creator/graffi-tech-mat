@echo off
REM deploy-inject-secrets.bat - inject secrets into k8s namespace

set NS=%1
if "%NS%"=="" set NS=production

echo Creating secrets in %NS%...

kubectl create secret generic graffi-secrets ^
  --from-literal=JWT_KEY=changeme ^
  --from-literal=DB_PASS=changeme ^
  -n %NS% ^
  --dry-run=client -o yaml | kubectl apply -f -

echo Secrets injected.
