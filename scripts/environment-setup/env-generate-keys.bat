@echo off
rem ====================================================================
rem env-generate-keys.bat
rem Generates secure random keys and appends to .env.local (or .env).
rem Uses PowerShell for cryptographically secure random bytes -> base64.
rem ====================================================================

setlocal

set ENV_FILE=.env.local
if not exist %ENV_FILE% (
  echo Creating %ENV_FILE%
  copy NUL %ENV_FILE% >nul
)

rem Function: create key using PowerShell
for /f "usebackq tokens=*" %%K in (`powershell -NoProfile -Command "[Convert]::ToBase64String((New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes(32))"`) do set RAND_KEY=%%K

rem Trim any trailing '=' to keep it compact (optional)
set RAND_KEY=%RAND_KEY:~0,43%

echo GENERIC_APP_KEY=%RAND_KEY%>>%ENV_FILE%
echo WROTE: GENERIC_APP_KEY to %ENV_FILE%

rem Create a JWT secret
for /f "usebackq tokens=*" %%J in (`powershell -NoProfile -Command "[Convert]::ToBase64String((New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes(48))"`) do set JWT_KEY=%%J
set JWT_KEY=%JWT_KEY:~0,64%
echo JWT_SECRET=%JWT_KEY%>>%ENV_FILE%
echo WROTE: JWT_SECRET to %ENV_FILE%

echo ==== Key generation complete. Keep %ENV_FILE% secret. ====
endlocal
