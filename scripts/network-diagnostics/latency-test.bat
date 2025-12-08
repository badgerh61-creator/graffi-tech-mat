@echo off
REM latency-test.bat
REM Simple latency tests (ping + PowerShell Test-NetConnection to measure TCP)

set HOSTS=8.8.8.8 github.com stackoverflow.com
echo === LATENCY TEST ===

for %%H in (%HOSTS%) do (
  echo.
  echo PING %%H (ICMP)...
  ping -n 5 %%H
  echo TCP connect test for %%H:443...
  powershell -Command "Test-NetConnection -ComputerName '%%H' -Port 443 | Select-Object ComputerName,RemoteAddress,TcpTestSucceeded,Latency | Format-List"
)

echo.
echo Latency tests complete.
pause
