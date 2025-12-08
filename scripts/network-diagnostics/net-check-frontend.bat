@echo off
REM net-check-frontend.bat

powershell -Command "Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing"
