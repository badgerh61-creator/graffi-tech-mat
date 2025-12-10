@echo off
REM version-bump.bat - bump semver in VERSION file or package.json (simple)
SETLOCAL

set TYPE=%1
if "%TYPE%"=="" set TYPE=patch

set VERSION_FILE=%~dp0\..\VERSION

if not exist "%VERSION_FILE%" (
  echo 0.1.0 > "%VERSION_FILE%"
)

for /f "usebackq tokens=1 delims=" %%v in ("%VERSION_FILE%") do set CURVER=%%v

for /f "tokens=1-3 delims=." %%a in ("%CURVER%") do (
  set MAJOR=%%a
  set MINOR=%%b
  set PATCH=%%c
)

if "%TYPE%"=="major" set /a MAJOR+=1 & set MINOR=0 & set PATCH=0
if "%TYPE%"=="minor" set /a MINOR+=1 & set PATCH=0
if "%TYPE%"=="patch" set /a PATCH+=1

set NEWVER=%MAJOR%.%MINOR%.%PATCH%
echo %NEWVER% > "%VERSION_FILE%"
echo Version bumped %CURVER% -> %NEWVER%
ENDLOCAL
