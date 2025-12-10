@echo off
set name=%1

if "%name%"=="" (
    echo Usage: scaffold-service.bat serviceName
    exit /b
)

mkdir backend\services\%name%
echo module.exports = { execute: () => { console.log('%name% service executed'); } }; > backend\services\%name%\index.js

echo Service "%name%" created.
pause
