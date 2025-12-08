@echo off
REM verify-checksums.bat
REM Creates SHA256 checksums for files in a folder and optionally verifies against provided .sha256 file

setlocal enabledelayedexpansion

set TARGET=%1
if "%TARGET%"=="" set TARGET=%~dp0packages
set OUTFILE=%~dp0packages\checksums-%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.sha256
set LOGFILE=%~dp0logs\checksums-%date:~-10,2%%date:~-7,2%%date:~-4,4%.log

if not exist "%TARGET%" (
  echo Target folder does not exist: %TARGET% >> "%LOGFILE%"
  echo ERROR: target folder not found: %TARGET%
  exit /b 2
)

if not exist "%~dp0logs" mkdir "%~dp0logs"
if not exist "%~dp0packages" mkdir "%~dp0packages"

echo [%date% %time%] Generating checksums for %TARGET% >> "%LOGFILE%"

REM Enumerate files and create SHA256 sums
> "%OUTFILE%" (
  for /R "%TARGET%" %%F in (*) do (
    certutil -hashfile "%%~fF" SHA256 | find /V "CertUtil" | find /V "SHA256" > temp.hash
    for /f "usebackq delims=" %%H in (temp.hash) do (
      set "h=%%H"
      setlocal enabledelayedexpansion
      echo !h! *%%~nxF
      endlocal
    )
  )
)
if exist temp.hash del temp.hash

echo Checksums written to %OUTFILE% >> "%LOGFILE%"
echo Done: %OUTFILE%
exit /b 0
