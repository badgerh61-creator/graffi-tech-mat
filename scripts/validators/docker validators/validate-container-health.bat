@echo off
set SERVICES=backend frontend database ai_engine

for %%S in (%SERVICES%) do (
  docker ps --filter "name=%%S" --filter "health=healthy" | find "healthy" >nul
  if %ERRORLEVEL% neq 0 (
    echo Container %%S not healthy.
    set ERR=1
  ) else (
    echo Container %%S healthy.
  )
)

if "%ERR%"=="1" exit /b 2

echo All containers healthy.
exit /b 0
