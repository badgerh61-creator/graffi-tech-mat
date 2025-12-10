@echo off
REM create-ci-template.bat
REM Adds a simple GitHub Actions workflow file for CI

SETLOCAL ENABLEDELAYEDEXPANSION

SET WF_DIR=.github\workflows
IF NOT EXIST "%WF_DIR%" mkdir "%WF_DIR%"

SET WF_FILE=%WF_DIR%\ci.yml

if not exist "%WF_FILE%" (
    (
    echo name: CI
    echo on:
    echo   push:
    echo     branches: [ main, master ]
    echo   pull_request:
    echo     branches: [ main, master ]
    echo jobs:
    echo   build:
    echo     runs-on: windows-latest
    echo     steps:
    echo     - uses: actions/checkout@v4
    echo     - name: Set up Node.js
    echo       uses: actions/setup-node@v4
    echo       with:
    echo         node-version: '18'
    echo     - name: npm install frontend deps
    echo       run: |
    echo         pushd src/frontend
    echo         npm ci || npm install
    echo         popd
    echo     - name: Run backend tests (python)
    echo       run: |
    echo         pushd src/backend
    echo         echo "Add test runner here"
    echo         popd
    ) > "%WF_FILE%"
    echo Created GitHub Actions CI template at %WF_FILE%
) else (
    echo CI workflow already exists
)

ENDLOCAL
