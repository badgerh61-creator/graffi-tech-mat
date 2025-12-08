@echo off
REM firewall-rules-apply.bat
REM Apply (import) firewall rules from a previously exported file.
REM Usage: firewall-rules-apply.bat path\to\file.wfw

if "%~1"=="" (
  echo Usage: %~nx0 path\to\firewall-file.wfw
  pause
  exit /b 1
)

set FILE=%~1

if not exist "%FILE%" (
  echo File not found: %FILE%
  pause
  exit /b 1
)

echo Applying firewall rules from %FILE% ...
netsh advfirewall import "%FILE%"
if %ERRORLEVEL%==0 (
  echo Firewall rules imported successfully.
) else (
  echo Import failed. Try running as Administrator.
)

pause
