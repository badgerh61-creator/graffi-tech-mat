@echo off
REM port-scan-local.bat
REM Scan local ports (LISTENING) and optionally probe a range on localhost

echo === PORT SCAN - LISTENING PORTS ===
netstat -ano | findstr /i "LISTENING" | sort
echo.

REM Probe TCP ports on localhost in a small range for quick check (change range as needed)
set /p STARTPORT=Enter start port for probe (e.g. 1): 
set /p ENDPORT=Enter end port for probe (e.g. 1024): 

echo Scanning localhost ports %STARTPORT% to %ENDPORT% (may take some time)...
for /L %%p in (%STARTPORT%,1,%ENDPORT%) do (
  powershell -Command "if ((Test-NetConnection -ComputerName 'localhost' -Port %%p -WarningAction SilentlyContinue).TcpTestSucceeded) { Write-Output 'OPEN: %%p' }"
)
echo Port scan complete.
pause
