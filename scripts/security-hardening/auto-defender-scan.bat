@echo off
:: =====================================================================
:: auto-defender-scan.bat
:: Forces a Windows Defender full system scan.
:: =====================================================================

echo === WINDOWS DEFENDER SCAN ===
echo Starting full Defender antivirus scan...

REM Update signatures
powershell -Command "Update-MpSignature"

REM Full scan
powershell -Command "Start-MpScan -ScanType FullScan"

echo Scan triggered. You can check progress in Windows Security.
exit /b 0
