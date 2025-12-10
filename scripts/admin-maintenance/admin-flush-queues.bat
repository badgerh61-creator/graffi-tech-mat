@echo off
REM ====================================================================
REM admin-flush-queues.bat
REM Flushes local processing queues by moving failed items back to incoming or removing old items.
REM Usage: admin-flush-queues.bat [dry-run]
REM WARNING: destructive operations should be used with care.
REM ====================================================================

setlocal enabledelayedexpansion
set DRY=%~1
set PROCESS_ROOT=%~dp0..\..\processing
set INCOMING_ROOT=%~dp0..\..\incoming
set LOG_DIR=%~dp0..\..\logs\admin
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOGFILE=%LOG_DIR%\admin-flush-queues_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

echo [%date% %time%] Starting queue flush (dry=%DRY%) >> "%LOGFILE%"

for %%Q in (images videos 3d presets moodboards prompts) do (
  set QDIR=%PROCESS_ROOT%%%Q
  if exist "!QDIR!" (
    echo [%date% %time%] Checking queue: !QDIR! >> "%LOGFILE%"
    for /f "delims=" %%F in ('dir /B "!QDIR!\*.failed" 2^>nul') do (
      echo [%date% %time%] Found failed: %%F >> "%LOGFILE%"
      if /I "%DRY%"=="dry-run" (
        echo DRY-RUN: would move %%F back to incoming >> "%LOGFILE%"
      ) else (
        echo Moving %%F back to incoming >> "%LOGFILE%"
        move /Y "!QDIR!\%%F" "%INCOMING_ROOT%%%Q\" >> "%LOGFILE%" 2>&1 || (
          echo Failed to move %%F >> "%LOGFILE%"
        )
      )
    )
  ) else (
    echo [%date% %time%] Queue folder not found: !QDIR! >> "%LOGFILE%"
  )
)

echo [%date% %time%] Queue flush complete. >> "%LOGFILE%"
endlocal
exit /b 0
