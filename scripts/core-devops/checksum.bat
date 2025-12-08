@echo off
REM checksum.bat - create SHA256 checksums for files in artifacts/
SETLOCAL

if not exist "%~dp0..\automation\artifacts" (
  echo No artifacts directory found at ../automation/artifacts
  exit /b 1
)

pushd "%~dp0..\automation\artifacts"
echo Generating checksums into checksums.txt
if exist checksums.txt del /f checksums.txt
for /r %%F in (*) do (
  certutil -hashfile "%%F" SHA256 | find /v "hash of file" | findstr /r /v "^$" > tmp.txt
  for /f "skip=1 tokens=*" %%L in (tmp.txt) do set HASH=%%L & goto :got
  :got
  echo !HASH!  %%~fF>>checksums.txt
)
del tmp.txt 2>nul
echo Done. checksums.txt created.
popd
ENDLOCAL
