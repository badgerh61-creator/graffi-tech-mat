@echo off
REM docker-publish.bat

SETLOCAL ENABLEDELAYEDEXPANSION

SET REGISTRY=registry.hub.docker.com/yourname
SET IMAGE_BACKEND=graffi-backend
SET IMAGE_FRONTEND=graffi-frontend
SET VERSION=1.0.0

docker tag %IMAGE_BACKEND%:latest %REGISTRY%/%IMAGE_BACKEND%:%VERSION%
docker tag %IMAGE_FRONTEND%:latest %REGISTRY%/%IMAGE_FRONTEND%:%VERSION%

echo Pushing images...
docker push %REGISTRY%/%IMAGE_BACKEND%:%VERSION%
docker push %REGISTRY%/%IMAGE_FRONTEND%:%VERSION%

echo Publish complete.
ENDLOCAL
