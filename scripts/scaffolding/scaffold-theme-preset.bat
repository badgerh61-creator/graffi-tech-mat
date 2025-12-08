@echo off
set theme=%1

if "%theme%"=="" (
    echo Usage: scaffold-theme-preset.bat themeName
    exit /b
)

mkdir frontend\src\themes\%theme%
echo export default { primary:'#000', secondary:'#fff' }; > frontend\src\themes\%theme%\index.js

echo Theme preset "%theme%" created.
pause
