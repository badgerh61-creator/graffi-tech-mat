@echo off
set model=%1

if "%model%"=="" (
    echo Usage: scaffold-database-model.bat ModelName
    exit /b
)

mkdir backend\models\%model%
echo module.exports = { name: "%model%", schema: {} }; > backend\models\%model%\index.js

echo DB model "%model%" created.
pause
