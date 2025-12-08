@echo off
rem ====================================================================
rem verify-node-python.bat
rem Checks Node, npm, Python and pip versions and reports status.
rem ====================================================================

echo ==== Verifying Node and Python environment ====

rem Node
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Node NOT found on PATH.
) else (
  for /f "tokens=*" %%A in ('node -v') do set NODE_VER=%%A
  echo Node version: %NODE_VER%
)

rem npm
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo npm NOT found on PATH.
) else (
  for /f "tokens=*" %%A in ('npm -v') do set NPM_VER=%%A
  echo npm version: %NPM_VER%
)

rem Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Python NOT found on PATH.
) else (
  for /f "tokens=*" %%A in ('python --version 2^>^&1') do set PY_VER=%%A
  echo %PY_VER%
)

rem pip
where pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo pip NOT found on PATH.
) else (
  for /f "tokens=*" %%A in ('pip -V') do set PIP_VER=%%A
  echo %PIP_VER%
)

echo ==== Verification complete ====
