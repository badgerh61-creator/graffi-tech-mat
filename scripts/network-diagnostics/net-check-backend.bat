@echo off
REM net-check-backend.bat

powershell -Command "Invoke-WebRequest -Uri 'http://localhost:5000/health' -UseBasicParsing"
