@echo off
REM net-check-port.bat
REM Usage: net-check-port.bat host port

if "%~2"=="" (
    echo Usage: %~nx0 host port
    exit /b 1
)

set HOST=%1
set PORT=%2

echo Checking TCP port %PORT% on %HOST% ...

powershell -Command "Test-NetConnection -ComputerName '%HOST%' -Port %PORT%" 

echo Done.
