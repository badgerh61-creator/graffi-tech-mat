@echo off
:: =====================================================================
:: penetration-quicktest.bat
:: Performs a quick local security audit:
:: - Open ports scan
:: - Firewall rules check
:: - Unsecured services check
:: =====================================================================

echo === QUICK PENETRATION TEST ===

:: Check for open ports with netstat
echo -- OPEN PORTS --
netstat -ano | findstr LISTENING

echo.

:: Check firewall status
echo -- FIREWALL STATUS --
powershell -Command "Get-NetFirewallProfile"

echo.

:: Check insecure services
echo -- INSECURE SERVICES CHECK --
sc query RemoteRegistry | findstr RUNNING
sc query TermService   | findstr RUNNING
sc query WinRM         | findstr RUNNING

echo If any service above should NOT be running, disable manually.
exit /b 0
