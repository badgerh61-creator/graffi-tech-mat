@echo off
set THEME_DIR=frontend\src\themes

if not exist "%THEME_DIR%" (
  echo Theme folder missing.
  exit /b 1
)

findstr "theme" "%THEME_DIR%\*.js" >nul
if %ERRORLEVEL% neq 0 (
  echo Theme presets not valid.
  exit /b 2
)

echo UI themes validated.
exit /b 0
