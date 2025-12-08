@echo off
set component=%1

if "%component%"=="" (
    echo Usage: scaffold-component.bat ComponentName
    exit /b
)

mkdir frontend\src\components\%component%
echo import React from "react"; > frontend\src\components\%component%\%component%.jsx
echo export default function %component%(){return (<div>%component% Component</div>);} >> frontend\src\components\%component%\%component%.jsx

echo Component "%component%" created.
pause
