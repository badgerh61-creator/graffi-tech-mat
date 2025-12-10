@echo off
set name=%1

if "%name%"=="" (
    echo Usage: scaffold-feature-module.bat moduleName
    exit /b
)

mkdir src\modules\%name%
echo export const %name%Module = {} > src\modules\%name%\index.js

echo Feature module "%name%" created successfully.
pause
