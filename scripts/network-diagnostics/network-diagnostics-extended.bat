@echo off
REM network-diagnostics-extended.bat
REM Full system network diagnostics (DNS, routes, interfaces, connectivity, firewall status)

echo === NETWORK DIAGNOSTICS - START (%date% %time%) ===
echo.

echo -- IP configuration --
ipconfig /all
echo.

echo -- Active routes --
route print
echo.

echo -- Network interfaces (status) --
powershell -Command "Get-NetAdapter | Format-Table -AutoSize"
echo.

echo -- DNS resolver cache --
ipconfig /displaydns
echo.

echo -- Test connectivity to gateway and google DNS --
for /f "tokens=2 delims=:" %%G in ('powershell -Command "(Get-NetIPConfiguration).IPv4DefaultGateway.NextHop"') do set GW=%%G
if defined GW (
  echo Pinging gateway %GW%...
  ping -n 4 %GW%
) else (
  echo Gateway not found.
)
echo Pinging 8.8.8.8...
ping -n 4 8.8.8.8
echo.

echo -- Test common ports to localhost (80,443,9200,5601) --
powershell -Command "@(80,443,9200,5601) | ForEach-Object { Write-Output ('Port {0} -> {1}' -f $_, (Test-NetConnection -ComputerName 'localhost' -Port $_).TcpTestSucceeded) }"
echo.

echo -- DNS resolution checks --
nslookup github.com
nslookup google.com
echo.

echo -- Netstat (active connections) --
netstat -ano | findstr /i "tcp"
echo.

echo -- Firewall status (basic) --
powershell -Command "Get-NetFirewallProfile | Format-Table Name,Enabled,DefaultInboundAction,DefaultOutboundAction -AutoSize"
echo.

echo === NETWORK DIAGNOSTICS - END ===
pause
