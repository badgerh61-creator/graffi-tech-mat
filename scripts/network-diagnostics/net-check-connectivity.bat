@echo off
REM net-check-connectivity.bat

echo Checking internet connectivity...

ping 8.8.8.8 -n 1 >nul
if %ERRORLEVEL%==0 (
    echo Internet OK (via Google DNS)
) else (
    echo No internet connection detected.
)

ping cloudflare.com -n 1 >nul
if %ERRORLEVEL%==0 (
    echo DNS resolution OK
) else (
    echo DNS seems down or slow.
)

echo Connectivity test complete.
