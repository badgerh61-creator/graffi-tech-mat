@echo off
REM log-monitor.bat — stream backend.log in real time

echo Monitoring logs...
powershell -command "Get-Content -Path 'logs/backend.log' -Wait"
