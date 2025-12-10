@echo off
REM rollback-k8s.bat - rollback to previous revision

set NS=%1
if "%NS%"=="" set NS=production

echo Rolling back backend...
kubectl rollout undo deployment/graffi-backend -n %NS%

echo Rolling back frontend...
kubectl rollout undo deployment/graffi-frontend -n %NS%

echo Rollback complete.
