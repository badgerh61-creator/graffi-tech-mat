@echo off
echo ==============================================
echo     BUILDING DOCKER IMAGES (CLEAN BUILD)
echo ==============================================

echo Stopping active containers...
docker-compose down

echo Removing old images...
docker rmi graffi-tech-mat-frontend graffi-tech-mat-backend -f

echo Pruning cache...
docker image prune -f

echo Rebuilding containers...
docker-compose up --build --force-recreate

pause
