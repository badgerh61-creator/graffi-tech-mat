@echo off
REM deploy-local.bat - runs backend + frontend locally

echo Starting backend...
start cmd /k "cd backend && dotnet run"

echo Starting frontend...
start cmd /k "cd frontend && npm start"

echo Local deployment running.
