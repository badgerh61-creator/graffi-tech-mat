@echo off
rem ====================================================================
rem install-dependencies.bat
rem Installs Node, Python deps, and common tooling for the Graffi project.
rem Run from repository root.
rem ====================================================================

setlocal enabledelayedexpansion

echo ==== Install dependencies: frontend + backend ====

rem --- Node (frontend) dependencies ---
if exist package.json (
  echo Installing frontend (npm) dependencies...
  if exist package-lock.json (
    npm ci || (
      echo npm ci failed, falling back to npm install...
      npm install || goto :ERR_NPM
    )
  ) else (
    npm install || goto :ERR_NPM
  )
) else (
  echo No package.json found in %cd% — skipping npm install.
)

rem --- Python (backend) dependencies ---
if exist requirements.txt (
  echo Installing Python packages from requirements.txt...
  if not exist venv (
    echo Creating virtual environment...
    python -m venv venv || goto :ERR_PY_VENV
  )
  call venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install -r requirements.txt || goto :ERR_PIP
  call venv\Scripts\deactivate.bat
) else (
  echo No requirements.txt found — skipping pip install.
)

rem --- Optional: install global tooling ---
echo Checking for Docker CLI...
where docker >nul 2>&1 || echo Docker CLI not found on PATH.

echo All dependency installs attempted.
goto :EOF

:ERR_NPM
echo ERROR: npm install failed.
exit /b 1

:ERR_PY_VENV
echo ERROR: Python venv creation failed. Ensure Python is installed.
exit /b 2

:ERR_PIP
echo ERROR: pip install failed.
exit /b 3
