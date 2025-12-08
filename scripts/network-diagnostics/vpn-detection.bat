@echo off
REM vpn-detection.bat
REM Detect common VPN adapter names and active default routes via PowerShell

echo === VPN DETECTION ===
echo Network adapters:
powershell -Command "Get-NetAdapter -Physical:$false | Select-Object Name,InterfaceDescription,Status | Format-Table -AutoSize"

echo.
echo Checking for typical VPN interface names and IP ranges...
powershell -Command ^
  "$adapters = Get-NetAdapter; ^
   $vpn = $adapters | Where-Object { $_.InterfaceDescription -match 'VPN|TAP|TUN|OpenVPN|WireGuard|Cisco|GlobalProtect|AnyConnect' -or $_.Name -match 'VPN|TAP|TUN|WireGuard' }; ^
   if ($vpn) { $vpn | Format-Table Name,InterfaceDescription,Status -AutoSize } else { Write-Output 'No obvious VPN adapter names detected.' }"

echo.
echo Checking default route and gateway (if routed via VPN it may differ)...
powershell -Command "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Select-Object -First 5 | Format-Table -AutoSize"

echo.
echo If you suspect VPN, check adapter IPs and DNS servers above for private/VPN ranges.
pause
