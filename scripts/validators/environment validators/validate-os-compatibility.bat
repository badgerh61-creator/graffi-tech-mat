@echo off
REM Validates Windows 10/11 compatibility

systeminfo | findstr /i "Windows 10 Windows 11" >nul
if %ERRORLEVEL% neq 0 (
  echo Unsupported OS detected.
  exit /b 1
)

echo OS is compatible.
exit /b 0
