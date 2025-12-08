@echo off
REM maintenance-orchestrator.bat — unified maintenance CLI

set CMD=%1
shift

if "%CMD%"=="" (
  echo Usage: maintain ^<task^>
  echo.
  echo Available tasks:
  echo    rotate
  echo    temp
  echo    cache
  echo    cleanup
  echo    artifacts
  echo    backup-logs
  echo    backup-config
  echo    monitor
  echo    health
  echo    disk
  exit /b
)

if "%CMD%"=="rotate" call rotate-logs.bat
if "%CMD%"=="temp" call cleanup-temp.bat
if "%CMD%"=="cache" call cleanup-cache.bat
if "%CMD%"=="cleanup" call cleanup-logs.bat
if "%CMD%"=="artifacts" call purge-old-artifacts.bat
if "%CMD%"=="backup-logs" call backup-logs.bat
if "%CMD%"=="backup-config" call backup-config.bat
if "%CMD%"=="monitor" call log-monitor.bat
if "%CMD%"=="health" call watch-health.bat
if "%CMD%"=="disk" call disk-cleanup.bat
