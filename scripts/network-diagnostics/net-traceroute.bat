@echo off
REM net-traceroute.bat
REM Usage: net-traceroute.bat host

if "%~1"=="" (
    echo Usage: %~nx0 host
    exit /b 1
)

tracert %1
