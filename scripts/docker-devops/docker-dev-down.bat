@echo off
REM docker-dev-down.bat

docker-compose -f infra\docker-compose.yml down
echo Dev environment stopped.
