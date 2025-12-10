@echo off
rem ====================================================================
rem verify-docker.bat
rem Verifies Docker is installed and daemon is running.
rem ====================================================================

echo ==== Verifying Docker ====

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Docker CLI not found on PATH. Install Docker Desktop or Docker CLI.
  exit /b 1
)

docker version >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Docker CLI present but cannot reach daemon. Is Docker Desktop running?
  docker info 2>nul || (
    echo docker info failed — ensure Docker daemon is started.
    exit /b 2
  )
)

echo Docker CLI and daemon reachable.
docker --version
exit /b 0
