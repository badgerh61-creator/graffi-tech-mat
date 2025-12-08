@echo off
REM cleanup-dev.bat - remove common build/temp artifacts

echo Cleaning build artifacts...
IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist
IF EXIST .parcel-cache rmdir /s /q .parcel-cache
IF EXIST node_modules rmdir /s /q node_modules

echo Cleaning .tmp and logs...
del /f /q *.tmp >nul 2>&1
del /f /q *.log >nul 2>&1

echo Cleanup finished.
