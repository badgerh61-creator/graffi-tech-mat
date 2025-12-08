@echo off
REM deploy-docker.bat - builds and runs full stack via Docker

echo Building Docker images...
docker compose build

echo Starting stack...
docker compose up -d

echo Deployment running at http://localhost:8080
