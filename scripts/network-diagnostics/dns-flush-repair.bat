@echo off
REM dns-flush-repair.bat
REM Flush DNS resolver cache and optionally renew DHCP/adapter

echo === DNS FLUSH & REPAIR ===
echo Flushing DNS resolver cache...
ipconfig /flushdns

echo Releasing DHCP lease...
ipconfig /release

echo Renewing DHCP lease...
ipconfig /renew

echo Resetting Winsock catalog...
netsh winsock reset

echo Resetting IP stack (requires admin and restart)...
netsh int ip reset

echo DNS flush & repair complete. A restart may be required for some changes to take effect.
pause
