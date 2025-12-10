@echo off
REM firewall-rules-export.bat
REM Export current Windows firewall rules to a file (PowerShell required)

set OUTFILE=%~dp0firewall-rules-%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%.wfw
echo Exporting firewall rules to %OUTFILE%...
powershell -Command "Export-WindowsFirewallRules -FilePath '%OUTFILE%'" 2>nul

REM Fallback using netsh if above cmd is not available
if exist "%OUTFILE%" (
  echo Export completed using Export-WindowsFirewallRules.
) else (
  echo Primary PowerShell export unavailable — using netsh advfirewall export.
  netsh advfirewall export "%OUTFILE%"
)

echo Export finished: %OUTFILE%
pause
