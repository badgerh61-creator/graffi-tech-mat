@echo off
REM net-ping-services.bat

echo Pinging Backend (localhost:5000)
powershell -Command "Test-NetConnection -ComputerName 'localhost' -Port 5000"

echo Pinging Frontend (localhost:3000)
powershell -Command "Test-NetConnection -ComputerName 'localhost' -Port 3000"

echo Pinging Postgres (localhost:5432)
powershell -Command "Test-NetConnection -ComputerName 'localhost' -Port 5432"

echo Pinging Redis (localhost:6379)
powershell -Command "Test-NetConnection -ComputerName 'localhost' -Port 6379"

echo Service checks complete.
