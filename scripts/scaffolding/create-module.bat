@echo off
REM create-module.bat
REM Usage: create-module.bat ModuleName
REM Creates a new backend module with blueprint files

IF "%~1"=="" (
    echo Usage: %~nx0 ModuleName
    exit /b 1
)

SET MODULE=%~1
SET MOD_DIR=src\backend\modules\%MODULE%
SET INIT_FILE=%MOD_DIR%\__init__.py
SET ROUTES_FILE=%MOD_DIR%\routes.py
SET README=%MOD_DIR%\README.md

echo Creating module %MODULE% ...

if not exist "%MOD_DIR%" mkdir "%MOD_DIR%"

if not exist "%INIT_FILE%" (
    echo # module init > "%INIT_FILE%"
    echo Created %INIT_FILE%
) else (
    echo %INIT_FILE% exists
)

if not exist "%ROUTES_FILE%" (
    (
    echo from flask import Blueprint, jsonify
    echo
    echo bp = Blueprint("%MODULE%", __name__, url_prefix="/%MODULE%")
    echo
    echo @bp.route("/")
    echo def index():
    echo     return jsonify({"module":"%MODULE%", "status":"ok"})
    ) > "%ROUTES_FILE%"
    echo Created %ROUTES_FILE%
) else (
    echo %ROUTES_FILE% exists
)

if not exist "%README%" (
    (
    echo # %MODULE% module
    echo
    echo This folder contains the %MODULE% module for the backend.
    ) > "%README%"
    echo Created module README
) else (
    echo Module README exists
)

echo Module %MODULE% created. Remember to register the blueprint in your app.
