@echo off
setlocal enabledelayedexpansion

:: diag-network-report.bat
:: Purpose: Network checks: IPs, interfaces, DNS, ping, traceroute, open ports (basic), route table
:: Place: graffi-tech-scripts/diagnostics/network/

set SCRIPT_DIR=%~dp0
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set ARTIFACT_DIR=%SCRIPT_DIR%..\artifacts\network\%TIMESTAMP%
set LOG_FILE=%ARTIFACT_DIR%\network.log
set TXT_REPORT=%ARTIFACT_DIR%\network-report.txt
set JSON_REPORT=%ARTIFACT_DIR%\network-report.json

if defined DIAG_OUTPUT_ROOT set ARTIFACT_DIR=%DIAG_OUTPUT_ROOT%\network\%TIMESTAMP%

if not exist "%ARTIFACT_DIR%" mkdir "%ARTIFACT_DIR%"

echo [%DATE% %TIME%] Starting network diagnostics > "%LOG_FILE%"

:: Targets for ping/traceroute - configurable via env
if not defined NET_TARGETS set NET_TARGETS=8.8.8.8 google.com

:: Use PowerShell to collect structured network info
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$out = @{}; ^
   $out.HostName = $env:COMPUTERNAME; ^
   $out.Timestamp = (Get-Date).ToString('o'); ^
   $out.Interfaces = Get-NetIPAddress -AddressFamily IPv4 | Select-Object InterfaceAlias,IPAddress,PrefixLength,AddressState; ^
   $out.DNS = (Get-DnsClientServerAddress -AddressFamily IPv4 | Select-Object InterfaceAlias,ServerAddresses); ^
   $out.Routes = Get-NetRoute -AddressFamily IPv4 | Select-Object ifIndex,DestinationPrefix,NextHop,RouteMetric; ^
   $targets = '%NET_TARGETS%'.Split(' '); ^
   $out.Pings = @(); foreach ($t in $targets) { $r = Test-Connection -ComputerName $t -Count 4 -ErrorAction SilentlyContinue; if ($r) { $out.Pings += @{ Target=$t; AvgMs=($r | Measure-Object ResponseTime -Average).Average } } else { $out.Pings += @{ Target=$t; Error='Unreachable' } } } ^
   $json = $out | ConvertTo-Json -Depth 5; $json | Out-File -FilePath (Join-Path '%ARTIFACT_DIR%' 'network-report.json') -Encoding utf8; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value '=== Network Report ==='; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value ('Timestamp: ' + (Get-Date).ToString()); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value ''; ^
   Get-NetIPAddress -AddressFamily IPv4 | Format-Table -AutoSize | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt'); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value ''; ^
   Get-DnsClientServerAddress -AddressFamily IPv4 | Format-Table -AutoSize | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt'); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value ''; ^
   foreach ($t in '%NET_TARGETS%'.Split(' ')) { Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') -Value ('--- Ping: ' + $t); Test-Connection -ComputerName $t -Count 4 -ErrorAction SilentlyContinue | Format-Table | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'network-report.txt') } ^
   Write-Host 'OK'"

if errorlevel 1 (
  echo [%DATE% %TIME%] ERROR: Network collection failed. >> "%LOG_FILE%"
  exit /b 2
)

:: Optional traceroute (windows tracert)
for %%T in (%NET_TARGETS%) do (
  echo [%DATE% %TIME%] Traceroute %%T >> "%LOG_FILE%"
  tracert -d %%T > "%ARTIFACT_DIR%\tracert-%%T.txt"
)

echo [%DATE% %TIME%] Completed. Reports in %ARTIFACT_DIR% >> "%LOG_FILE%"
echo Reports: "%TXT_REPORT%", "%JSON_REPORT%"
endlocal
exit /b 0
