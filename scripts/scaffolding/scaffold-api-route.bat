@echo off
set route=%1

if "%route%"=="" (
    echo Usage: scaffold-api-route.bat routeName
    exit /b
)

mkdir backend\routes\%route%
echo module.exports = (app) => { app.get('/%route%', (req,res)=>res.send('%route% OK')); }; > backend\routes\%route%\index.js

echo API route "%route%" created.
pause
