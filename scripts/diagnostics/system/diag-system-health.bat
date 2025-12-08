@echo off
setlocal enabledelayedexpansion

:: diag-system-health.bat
:: Purpose: Gather OS and system health info (CPU, memory, disk, uptime, installed updates)
:: Place: graffi-tech-scripts/diagnostics/system/

:: --------- Configuration ----------
set SCRIPT_DIR=%~dp0
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set ARTIFACT_DIR=%SCRIPT_DIR%..\artifacts\system\%TIMESTAMP%
set LOG_FILE=%ARTIFACT_DIR%\system-health.log
set TXT_REPORT=%ARTIFACT_DIR%\system-health.txt
set JSON_REPORT=%ARTIFACT_DIR%\system-health.json

:: Optional env overrides
if defined DIAG_OUTPUT_ROOT set ARTIFACT_DIR=%DIAG_OUTPUT_ROOT%\system\%TIMESTAMP%

:: create folders
if not exist "%ARTIFACT_DIR%" mkdir "%ARTIFACT_DIR%"

:: Logging helper
echo [%DATE% %TIME%] Starting system health diagnostics > "%LOG_FILE%"

:: Run PowerShell to collect structured data and save JSON + human readable
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$out = @{}; ^
   $out.HostName = $env:COMPUTERNAME; ^
   $out.Timestamp = (Get-Date).ToString('o'); ^
   $out.OS = Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture,LastBootUpTime; ^
   $out.CPU = Get-CimInstance -ClassName Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed; ^
   $out.Memory = @{ TotalMB = [math]::Round((Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory/1MB,2); FreeMB = [math]::Round((Get-CimInstance -ClassName Win32_OperatingSystem).FreePhysicalMemory/1024,2) }; ^
   $out.Drives = Get-CimInstance -ClassName Win32_LogicalDisk -Filter 'DriveType=3' | Select-Object DeviceID,@{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,2)}},@{n='SizeGB';e={[math]::Round($_.Size/1GB,2)}}; ^
   $out.Uptime = ((Get-Date) - (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime).ToString(); ^
   $out.ServicesFailing = Get-Service | Where-Object {$_.Status -ne 'Running'} | Select-Object Name,Status; ^
   $out.ProcessesTop = Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 10 -Property Id,ProcessName,CPU,WorkingSet; ^
   $json = $out | ConvertTo-Json -Depth 5; ^
   $json | Out-File -FilePath (Join-Path '%ARTIFACT_DIR%' 'system-health.json') -Encoding utf8; ^
   "" | Out-File -FilePath (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Encoding utf8; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value '=== System Health Report ==='; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value ('Timestamp: ' + (Get-Date).ToString()); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value ''; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value '--- OS ---'; ^
   Get-CimInstance -ClassName Win32_OperatingSystem | Format-List | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt'); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value ''; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value '--- CPU ---'; ^
   Get-CimInstance -ClassName Win32_Processor | Format-List | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt'); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value ''; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value '--- Drives ---'; ^
   Get-CimInstance -ClassName Win32_LogicalDisk -Filter 'DriveType=3' | Format-Table DeviceID, @{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,2)}}, @{n='SizeGB';e={[math]::Round($_.Size/1GB,2)}} -AutoSize | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt'); ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value ''; ^
   Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt') -Value '--- Top Processes (by CPU) ---'; ^
   Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 10 Id,ProcessName,CPU,WorkingSet | Format-Table | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'system-health.txt'); ^
   Write-Host 'OK'"
if errorlevel 1 (
  echo [%DATE% %TIME%] ERROR: PowerShell collection failed. >> "%LOG_FILE%"
  exit /b 2
)

echo [%DATE% %TIME%] Completed. Reports written to %ARTIFACT_DIR% >> "%LOG_FILE%"
echo Reports: "%TXT_REPORT%", "%JSON_REPORT%"
endlocal
exit /b 0
