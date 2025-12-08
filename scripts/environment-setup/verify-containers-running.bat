@echo off
rem ====================================================================
rem verify-containers-running.bat
rem Confirms required containers (by name) are running; prints status.
rem Edit REQUIRED_CONTAINERS to match your docker-compose service names.
rem ====================================================================

setlocal
set REQUIRED_CONTAINERS=graffi_db graffi_backend graffi_frontend

echo ==== Checking required containers ====

for %%C in (%REQUIRED_CONTAINERS%) do (
  docker ps --filter "name=%%C" --format "table {{.Names}}\t{{.Status}}" | findstr /R /C:"%%C" >nul
  if %ERRORLEVEL%==0 (
    echo Container %%C: RUNNING
  ) else (
    echo Container %%C: NOT RUNNING
  )
)

echo ==== Done ====
endlocal
