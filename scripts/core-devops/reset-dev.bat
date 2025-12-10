@echo off
REM reset-dev.bat - stops containers, removes volumes, re-seeds local DB
SETLOCAL ENABLEDELAYEDEXPANSION

echo Resetting local development environment...

where docker-compose >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo docker-compose not found. Trying docker compose...
)

echo Stopping containers...
docker compose down --volumes --remove-orphans

echo Pruning unused resources (images/containers/networks) - confirm Y/N
docker system prune -a

if exist "./infra/seeds" (
  echo Restoring DB seed (if applicable)...
  REM Implement your DB seed command here, example for Postgres:
  REM docker exec -i graffi-postgres psql -U postgres -d graffi < infra/seeds/seed.sql
) else (
  echo No seeds folder found at ./infra/seeds - skipping DB seed.
)

echo Reset complete.
ENDLOCAL
