@echo off
REM sign-artifact-stub.bat - placeholder to sign artifacts
SETLOCAL

if "%~1"=="" (
  echo Usage: sign-artifact-stub.bat path\to\artifact
  exit /b 2
)

set ART=%~1

where gpg >nul 2>&1
if %ERRORLEVEL%==0 (
  echo Signing %ART% with gpg...
  gpg --output "%ART%.asc" --armor --detach-sign "%ART%"
  echo Signature written to %ART%.asc
  exit /b 0
)

where signtool >nul 2>&1
if %ERRORLEVEL%==0 (
  echo Signing %ART% with signtool (Windows certificate)...
  REM signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "%ART%"
  echo (Uncomment and configure signtool command)
  exit /b 0
)

echo No signing tool (gpg or signtool) found. Please install or configure one.
ENDLOCAL
