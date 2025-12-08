@echo off
REM docker-stop.bat
REM Stops & removes backend and frontend containers

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_CONTAINER=graffi-backend-c
SET FRONTEND_CONTAINER=graffi-frontend-c

echo === Stopping containers ===

for %%C in (%BACKEND_CONTAINER% %FRONTEND_CONTAINER%) do (
    docker stop %%C 2>nul
    docker rm %%C 2>nul
)

echo Containers stopped & removed.
ENDLOCAL
