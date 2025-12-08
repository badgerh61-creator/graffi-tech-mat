@echo off
:: =====================================================================
:: verify-certs.bat
:: Validates cert expiration dates and outputs findings.
:: =====================================================================

echo === CERTIFICATE VALIDATION ===

powershell -Command ^
"Get-ChildItem Cert:\\LocalMachine\\My | Select-Object Subject, NotAfter, Thumbprint"

echo.
echo If any certificate is expired or near expiry, renew immediately.
exit /b 0
