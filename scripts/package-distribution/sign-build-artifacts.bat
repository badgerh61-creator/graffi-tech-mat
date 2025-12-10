@echo off
REM sign-build-artifacts.bat
REM Signs binaries or ZIPs using signtool.exe (Windows SDK) or a configured signer

setlocal enabledelayedexpansion

set ARTIFACT=%1
if "%ARTIFACT%"=="" (
  echo Usage: sign-build-artifacts.bat path\to\artifact.zip
  exit /b 1
)

set LOGFILE=%~dp0logs\sign-%~n1-%date:~-10,2%%date:~-7,2%%date:~-4,4%.log
if not exist "%~dp0logs" mkdir "%~dp0logs"

echo [%date% %time%] Signing %ARTIFACT% >> "%LOGFILE%"

REM Attempt to find signtool
where signtool >nul 2>&1
if errorlevel 1 (
  echo signtool not found in PATH. Please install Windows SDK or provide signing tool. >> "%LOGFILE%"
  echo WARNING: signing skipped. >> "%LOGFILE%"
  exit /b 2
)

REM Configure below to your certificate / timestamp server
set CERT_PFX=C:\path\to\cert.pfx
set CERT_PASS=yourPfxPassword
set TIMESTAMP_URL=http://timestamp.digicert.com

if not exist "%CERT_PFX%" (
  echo Certificate file not found: %CERT_PFX% >> "%LOGFILE%"
  echo ERROR: certificate not found
  exit /b 3
)

echo Running signtool... >> "%LOGFILE%"
signtool sign /f "%CERT_PFX%" /p "%CERT_PASS%" /tr "%TIMESTAMP_URL%" /td SHA256 /fd SHA256 "%ARTIFACT%" >> "%LOGFILE%" 2>&1

if errorlevel 1 (
  echo signtool failed. Check log: %LOGFILE%
  exit /b 4
)

echo [%date% %time%] Signing complete for %ARTIFACT% >> "%LOGFILE%"
exit /b 0
