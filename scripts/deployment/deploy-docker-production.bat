@echo off
REM deploy-docker-production.bat - prod build + push

set TAG=%1

if "%TAG%"=="" (
  echo Usage: deploy-docker-production.bat ^<version-tag^>
  exit /b 1
)

echo Building production images with tag %TAG%...

docker build -t graffi/backend:%TAG% backend/
docker build -t graffi/frontend:%TAG% frontend/

echo Pushing to registry...
docker push graffi/backend:%TAG%
docker push graffi/frontend:%TAG%

echo Production Docker deployment complete.
