@echo off
REM build-clean.bat
REM Remove build artifacts for a clean build

echo Cleaning backend dist, frontend build, node caches, python caches...

rmdir /s /q src\backend\dist 2>nul
rmdir /s /q src\frontend\build 2>nul
rmdir /s /q src\frontend\node_modules 2>nul
rmdir /s /q src\backend\.pytest_cache 2>nul
del /s /q src\backend\**\*.pyc 2>nul

echo Clean complete.
