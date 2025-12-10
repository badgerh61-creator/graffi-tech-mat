@echo off
REM port-force-kill.bat
REM Find process using a port and kill it (admin required). Usage: port-force-kill.bat 3000

if "%~1"=="" (
  echo Usage: %~nx0 PORT
  echo Example: %~nx0 3000
  pause
  exit /b 1
)

set PORT=%1

echo Finding PID using port %PORT%...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% " ^| findstr LISTENING') do set PID=%%a

if not defined PID (
  echo No process found listening on port %PORT%.
  pause
  exit /b 0
)

echo PID %PID% is listening on port %PORT%.
echo Attempting graceful termination...
taskkill /PID %PID% /T
timeout /t 2 >nul

REM If still alive, force kill
tasklist /FI "PID eq %PID%" | findstr %PID% >nul
if %ERRORLEVEL%==0 (
  echo Process still running; forcing termination...
  taskkill /F /PID %PID% /T
) else (
  echo Process terminated gracefully.
)

pause
