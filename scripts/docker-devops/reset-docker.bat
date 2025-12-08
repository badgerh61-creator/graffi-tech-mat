@echo off
echo ==============================================
echo      FULL RESET FOR DOCKER + FRONTEND
echo ==============================================

echo Stopping containers...
docker-compose down

echo Removing old images...
docker rmi graffi-tech-mat-frontend graffi-tech-mat-backend -f

echo Pruning all unused data...
docker system prune -a -f

echo Cleaning frontend node_modules...
cd frontend
rmdir /S /Q node_modules 2>nul
del package-lock.json 2>nul

echo Reinstalling frontend dependencies...
npm install

cd ..

echo Rebuilding docker from scratch...
docker-compose up --build --force-recreate

pause
