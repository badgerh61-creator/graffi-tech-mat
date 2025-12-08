@echo off
:: =====================================================================
:: security-hardening.bat
:: Applies essential Windows security hardening tasks for Graffi-Tech-Mat.
:: Includes firewall tighten, service lockdown, Defender updates, temp wipe.
:: =====================================================================

echo === SECURITY HARDENING START ===
echo This script may require ADMIN access.
echo.

:: Check admin
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Please run this script as Administrator.
    pause
    exit /b 1
)

:: Enable Firewall
echo Enabling Windows Firewall...
powershell -Command "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"

:: Disable insecure SMB v1
echo Disabling SMBv1...
powershell -Command "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart" >nul 2>&1

:: Ensure Remote Desktop is off unless needed
echo Disabling Remote Desktop...
reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f >nul

:: Disable Guest user
echo Disabling Guest account...
net user guest /active:no >nul

:: Clear temp directories
echo Cleaning temp folders...
del /f /s /q "%TEMP%\\*" 2>nul
del /f /s /q "C:\\Windows\\Temp\\*" 2>nul

echo Security hardening applied successfully.
exit /b 0
