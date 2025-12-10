@echo off
REM watch-health.bat — restart Windows service if it dies

:LOOP
sc query graffi-backend | find "RUNNING" >nul

if %ERRORLEVEL% neq 0 (
    echo Backend service stopped — restarting...
    net start graffi-backend
)

timeout /t 10 >nul
goto LOOP
