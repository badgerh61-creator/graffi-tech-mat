@echo off
REM net-dns-lookup.bat
REM Usage: net-dns-lookup.bat domain

if "%~1"=="" (
    echo Usage: %~nx0 domain
    exit /b 1
)

nslookup %1
