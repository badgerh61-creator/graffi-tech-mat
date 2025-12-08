@echo off
REM ====================================================================
REM admin-restart-services.bat
REM Restarts named Windows services or docker stack services.
REM Usage: admin-restart-services.bat [serviceName|--docker-compose]
REM Examples:
REM   admin-restart-services.bat graffi-backend
REM   admin-restart-services.bat --docker-compose
REM ====================================================================

setlocal
set ARG=%~1
set LOG_DIR=%~dp0..\..\logs\admin
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOGFILE=%LOG_DIR%\admin-restart-services_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

echo [%date% %time%] Restarting services (arg=%ARG%) >> "%LOGFILE%"

if "%ARG%"=="--docker-compose" (
  if exist "%~dp0..\docker-compose.yml" (
    echo [%date% %time%] Restarting docker-compose stack >> "%LOGFILE%"
    pushd "%~dp0\.."
    docker compose down >> "%LOGFILE%" 2>&1
    docker compose up -d >> "%LOGFILE%" 2>&1
    popd
  ) else (
    echo docker-compose.yml not found at project root >> "%LOGFILE%"
  )
  goto :EOF
)

if "%ARG%"=="" (
  echo Usage: %~nx0 [serviceName|--docker-compose]
  exit /b 1
)

rem Try to restart as Windows service
sc query "%ARG%" >nul 2>&1
if %ERRORLEVEL%==0 (
  echo [%date% %time%] Restarting Windows service %ARG% >> "%LOGFILE%"
  net stop "%ARG%" >> "%LOGFILE%" 2>&1
  net start "%ARG%" >> "%LOGFILE%" 2>&1
  goto :EOF
)

echo [%date% %time%] Service %ARG% not found as Windows service. Trying docker container restart by name. >> "%LOGFILE%"
docker ps -a --filter "name=%ARG%" --format "{{.Names}}" | findstr /R /C:"%ARG%" >nul
if %ERRORLEVEL%==0 (
  echo [%date% %time%] Restarting docker container %ARG% >> "%LOGFILE%"
  docker restart "%ARG%" >> "%LOGFILE%" 2>&1
) else (
  echo [%date% %time%] No service or container named %ARG% found. >> "%LOGFILE%"
)

endlocal
exit /b 0
