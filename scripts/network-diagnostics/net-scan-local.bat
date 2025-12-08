@echo off
REM net-scan-local.bat

echo Scanning local machine for common dev ports...

for %%p in (80 443 3000 5000 5432 6379 9200 9300) do (
    powershell -Command "if (Test-NetConnection -Port %%p -WarningAction SilentlyContinue).TcpTestSucceeded { Write-Host 'Port %%p: OPEN' } else { Write-Host 'Port %%p: closed' }"
)

echo Scan complete.
