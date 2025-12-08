@echo off
set page=%1

if "%page%"=="" (
    echo Usage: scaffold-react-page.bat PageName
    exit /b
)

mkdir frontend\src\pages\%page%
echo import React from "react"; > frontend\src\pages\%page%\index.jsx
echo export default function %page%(){return (<div>%page% Page</div>);} >> frontend\src\pages\%page%\index.jsx

echo React page "%page%" created.
pause
