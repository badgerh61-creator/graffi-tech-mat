@echo off
echo ==============================================
echo   GRAFFI-TECH-MAT FRONTEND AUTO SETUP
echo ==============================================

cd frontend

echo Removing node_modules and package-lock (if present)...
rmdir /S /Q node_modules 2>nul
del package-lock.json 2>nul

echo Installing core packages (this may take a few minutes)...
npm install

echo Installing THREE.JS, R3F, ZUSTAND...
npm install three @react-three/fiber zustand

echo Frontend setup complete!
pause
