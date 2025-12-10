@echo off
REM docker-rebuild-all.bat
REM Stops containers, removes images, rebuilds all

SETLOCAL ENABLEDELAYEDEXPANSION

call docker-stop.bat

echo Removing old images...
docker rmi graffi-backend:latest -f 2>nul
docker rmi graffi-frontend:latest -f 2>nul

call docker-build.bat
call docker-run.bat

ENDLOCAL
