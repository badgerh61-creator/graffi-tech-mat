@echo off
REM k8s-logs-multi.bat - print logs from all pods matching selector (non-streaming)
SETLOCAL

if "%~1"=="" (
  echo Usage: k8s-logs-multi.bat <namespace> <label-selector>
  exit /b 2
)

set NS=%1
set LABEL=%2

for /f "tokens=*" %%p in ('kubectl get pods -n %NS% -l %LABEL% -o jsonpath^"{.items[*].metadata.name}^"') do (
  for %%x in (%%p) do (
    echo ========== Logs for %%x ==========
    kubectl logs -n %NS% %%x
  )
)
ENDLOCAL
