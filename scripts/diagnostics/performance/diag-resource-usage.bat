@echo off
setlocal enabledelayedexpansion

:: diag-resource-usage.bat
:: Purpose: Capture resource usage over a short sample interval (CPU, mem, disk I/O, network)
:: Place: graffi-tech-scripts/diagnostics/performance/

set SCRIPT_DIR=%~dp0
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set ARTIFACT_DIR=%SCRIPT_DIR%..\artifacts\performance\%TIMESTAMP%
set LOG_FILE=%ARTIFACT_DIR%\performance.log
set TXT_REPORT=%ARTIFACT_DIR%\performance.txt
set JSON_REPORT=%ARTIFACT_DIR%\performance.json

if defined DIAG_OUTPUT_ROOT set ARTIFACT_DIR=%DIAG_OUTPUT_ROOT%\performance\%TIMESTAMP%

if not exist "%ARTIFACT_DIR%" mkdir "%ARTIFACT_DIR%"

echo [%DATE% %TIME%] Starting resource usage diagnostics > "%LOG_FILE%"

:: sample duration and interval (seconds)
set /a SAMPLE_SECONDS=30
set /a INTERVAL_SECONDS=5

:: Use PowerShell to sample perf counters
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$samples = @(); $end = (Get-Date).AddSeconds(%SAMPLE_SECONDS%); while ((Get-Date) -lt $end) { ^
     $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue; ^
     $mem = (Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue; ^
     $disk = (Get-Counter '\PhysicalDisk(_Total)\% Disk Time').CounterSamples.CookedValue; ^
     $netRecv = (Get-Counter '\Network Interface(*)\Bytes Received/sec' -ErrorAction SilentlyContinue).CounterSamples | Measure-Object -Property CookedValue -Sum; ^
     $netSent = (Get-Counter '\Network Interface(*)\Bytes Sent/sec' -ErrorAction SilentlyContinue).CounterSamples | Measure-Object -Property CookedValue -Sum; ^
     $samples += [pscustomobject]@{ Timestamp=(Get-Date).ToString('o'); CPU=[math]::Round($cpu,2); FreeMB=[math]::Round($mem,2); DiskPct=[math]::Round($disk,2); NetRx=[math]::Round($netRecv.Sum,2); NetTx=[math]::Round($netSent.Sum,2) }; ^
     Start-Sleep -Seconds %INTERVAL_SECONDS%; ^
  } ^
  $samples | ConvertTo-Json -Depth 3 | Out-File -FilePath (Join-Path '%ARTIFACT_DIR%' 'performance.json') -Encoding utf8; ^
  'Resource usage samples:' | Out-File -FilePath (Join-Path '%ARTIFACT_DIR%' 'performance.txt') -Encoding utf8; ^
  $samples | Format-Table -AutoSize | Out-String | Add-Content -Path (Join-Path '%ARTIFACT_DIR%' 'performance.txt'); ^
  Write-Host 'OK'"

if errorlevel 1 (
  echo [%DATE% %TIME%] ERROR: Performance collection failed. >> "%LOG_FILE%"
  exit /b 2
)

echo [%DATE% %TIME%] Completed. Reports in %ARTIFACT_DIR% >> "%LOG_FILE%"
echo Reports: "%TXT_REPORT%", "%JSON_REPORT%"
endlocal
exit /b 0
