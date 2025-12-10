@echo off
REM scaffold-backend.bat
REM Creates a Python backend skeleton with virtualenv, basic app and requirements

SETLOCAL ENABLEDELAYEDEXPANSION

SET BACKEND_DIR=src\backend
SET VENV_DIR=%BACKEND_DIR%\.venv
SET APP_FILE=%BACKEND_DIR%\app.py
SET REQ_FILE=%BACKEND_DIR%\requirements.txt

echo.
echo === Scaffolding backend in %BACKEND_DIR% ===
echo.

if not exist "%BACKEND_DIR%" mkdir "%BACKEND_DIR%"

:: Create venv if python exists
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    if not exist "%VENV_DIR%" (
        echo Creating python venv...
        python -m venv "%VENV_DIR%"
        echo Created venv at %VENV_DIR%
    ) else (
        echo Virtualenv already exists at %VENV_DIR%
    )
) else (
    echo Python not found in PATH; skipping venv creation.
)

:: requirements
if not exist "%REQ_FILE%" (
    echo flask> "%REQ_FILE%"
    echo gunicorn>> "%REQ_FILE%"
    echo Created %REQ_FILE%
) else (
    echo %REQ_FILE% exists
)

:: Minimal Flask app
if not exist "%APP_FILE%" (
    (
    echo from flask import Flask, jsonify
    echo app = Flask(__name__)
    echo
    echo @app.route("/health")
    echo def health():
    echo     return jsonify({"status":"ok"})
    echo
    echo if __name__ == "__main__":
    echo     app.run(host="0.0.0.0", port=5000, debug=True)
    ) > "%APP_FILE%"
    echo Created %APP_FILE%
) else (
    echo %APP_FILE% exists
)

:: Create .env.example
if not exist "%BACKEND_DIR%\.env.example" (
    (
    echo FLASK_ENV=development
    echo FLASK_APP=app.py
    echo SECRET_KEY=change-me
    ) > "%BACKEND_DIR%\.env.example"
    echo Created .env.example
) else (
    echo .env.example exists
)

echo Backend scaffolding complete.
ENDLOCAL
