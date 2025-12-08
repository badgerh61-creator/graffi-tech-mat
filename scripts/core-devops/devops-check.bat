@echo off
REM devops-check.bat - verify required tools are installed

SETLOCAL
echo Checking required CLI tools...

set MISSING=

where git >nul 2>&1 || set MISSING=%MISSING% git
where docker >nul 2>&1 || set MISSING=%MISSING% docker
where kubectl >nul 2>&1 || set MISSING=%MISSING% kubectl
where helm >nul 2>&1 || set MISSING=%MISSING% helm
where az >nul 2>&1 || set MISSING=%MISSING% az
where gpg >nul 2>&1 || set MISSING=%MISSING% gpg
where 7z >nul 2>&1 || set MISSING=%MISSING% 7z

if "%MISSING%"=="" (
  echo All required CLIs found.
  exit /b 0
) else (
  echo Missing tools:%MISSING%
  echo Please install the above and re-run this script.
  exit /b 2
)
ENDLOCAL
