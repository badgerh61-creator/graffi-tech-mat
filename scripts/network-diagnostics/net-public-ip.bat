@echo off
REM net-public-ip.bat

powershell -Command "(Invoke-WebRequest -Uri 'https://api.ipify.org').Content"
