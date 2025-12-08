@echo off
REM version-bump.bat <major|minor|patch> [path-to-package.json]
set TYPE=%1
if "%TYPE%"=="" set TYPE=patch

set PJSON=%2
if "%PJSON%"=="" set PJSON=%~dp0\..\package.json

REM If there is a VERSION file, bump that first
set VERSION_FILE=%~dp0\..\VERSION
if exist "%VERSION_FILE%" (
  for /f "usebackq tokens=1 delims=" %%v in ("%VERSION_FILE%") do set CURVER=%%v
) else (
  REM Try package.json (very simple extraction)
  if exist "%PJSON%" (
    for /f "tokens=2 delims=:" %%a in ('type "%PJSON%" ^| findstr /i "\"version\""') do set VERRAW=%%a
    set VERRAW=%VERRAW: =%
    set VERRAW=%VERRAW:"=%
    set VERRAW=%VERRAW:,=%
    set CURVER=%VERRAW%
  ) else (
    set CURVER=0.1.0
  )
)

for /f "tokens=1-3 delims=." %%a in ("%CURVER%") do (
  set MAJOR=%%a
  set MINOR=%%b
  set PATCH=%%c
)

if "%TYPE%"=="major" (set /a MAJOR+=1 & set MINOR=0 & set PATCH=0)
if "%TYPE%"=="minor" (set /a MINOR+=1 & set PATCH=0)
if "%TYPE%"=="patch" (set /a PATCH+=1)

set NEWVER=%MAJOR%.%MINOR%.%PATCH%

echo Bumped %CURVER% -> %NEWVER%

REM write back
echo %NEWVER% > "%VERSION_FILE%"
if exist "%PJSON%" (
  powershell -Command "(Get-Content '%PJSON%') -replace '\"version\"\s*:\s*\".*?\"','\"version\": \"%NEWVER%\"' | Set-Content '%PJSON%'"
)
exit /b 0
