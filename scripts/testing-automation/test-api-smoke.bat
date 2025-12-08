@echo off
REM test-api-smoke.bat

echo === API Smoke Tests ===

echo Checking backend health...
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:5000/health' -UseBasicParsing"

echo Checking frontend...
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing"

echo Smoke tests finished.
