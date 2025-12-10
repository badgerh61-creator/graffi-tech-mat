@echo off
REM scaffold-frontend.bat
REM Creates a Node/React frontend skeleton + package.json + basic files

SETLOCAL ENABLEDELAYEDEXPANSION

SET FRONTEND_DIR=src\frontend
SET PACKAGE_FILE=%FRONTEND_DIR%\package.json
SET SRC_DIR=%FRONTEND_DIR%\src
SET PUBLIC_DIR=%FRONTEND_DIR%\public

echo.
echo === Scaffolding frontend in %FRONTEND_DIR% ===
echo.

if not exist "%FRONTEND_DIR%" mkdir "%FRONTEND_DIR%"
if not exist "%SRC_DIR%" mkdir "%SRC_DIR%"
if not exist "%PUBLIC_DIR%" mkdir "%PUBLIC_DIR%"

:: package.json
if not exist "%PACKAGE_FILE%" (
    (
    echo {
    echo   "name": "graffi-frontend",
    echo   "version": "0.1.0",
    echo   "private": true,
    echo   "scripts": {
    echo     "start": "react-scripts start",
    echo     "build": "react-scripts build",
    echo     "test": "react-scripts test --env=jsdom",
    echo     "lint": "echo No linter configured"
    echo   },
    echo   "dependencies": {},
    echo   "devDependencies": {}
    echo }
    ) > "%PACKAGE_FILE%"
    echo Created package.json (edit to add libs like react, vite etc.)
) else (
    echo package.json exists
)

:: simple index.html
if not exist "%PUBLIC_DIR%\index.html" (
    (
    echo <!doctype html>
    echo <html>
    echo <head>
    echo   <meta charset="utf-8" />
    echo   <meta name="viewport" content="width=device-width,initial-scale=1" />
    echo   <title>Graffi Frontend</title>
    echo </head>
    echo <body>
    echo   <div id="root"></div>
    echo </body>
    echo </html>
    ) > "%PUBLIC_DIR%\index.html"
    echo Created public/index.html
) else (
    echo public/index.html exists
)

:: simple App.js
if not exist "%SRC_DIR%\index.js" (
    (
    echo import React from "react";
    echo import { createRoot } from "react-dom/client";
    echo import App from "./App";
    echo const root = createRoot(document.getElementById("root"));
    echo root.render(<App />);
    ) > "%SRC_DIR%\index.js"

    (
    echo import React from "react";
    echo export default function App() {
    echo   return (
    echo     <div style={{fontFamily: "sans-serif", padding: 20}}>
    echo       <h1>Graffi Frontend</h1>
    echo       <p>Place frontend components here.</p>
    echo     </div>
    echo   );
    echo }
    ) > "%SRC_DIR%\App.js"
    echo Created src/index.js and src/App.js
) else (
    echo frontend src files exist
)

echo Frontend scaffolding complete. Run 'npm install' inside %FRONTEND_DIR% to add dependencies.
ENDLOCAL
