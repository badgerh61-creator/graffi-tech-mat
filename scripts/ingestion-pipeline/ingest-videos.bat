@echo off
REM ====================================================================
REM ingest-videos.bat
REM Usage: ingest-videos.bat [source_folder]
REM - Handles mp4, mov, avi. Moves to assets/videos and queues for encoding/transcoding.
REM ====================================================================

setlocal enabledelayedexpansion
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\videos

set ASSETS_DIR=%cd%\assets\videos
set PROCESS_DIR=%cd%\processing\videos
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-videos_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting video ingestion from "%SOURCE%" >> "%LOGFILE%"

if not exist "%SOURCE%" (
  echo Source folder "%SOURCE%" not found. >> "%LOGFILE%"
  echo ERROR: Source not found.
  exit /b 2
)

for %%F in ("%SOURCE%\*.*") do (
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="mp4" (
    call :HANDLE "%%~fF"
  ) else if /I "!EXT!"=="mov" (
    call :HANDLE "%%~fF"
  ) else if /I "!EXT!"=="avi" (
    call :HANDLE "%%~fF"
  )
)

echo [%date% %time%] Video ingestion finished. >> "%LOGFILE%"
exit /b 0

:HANDLE
set FILEPATH=%~1
set BASENAME=%~n1
set PROC_DEST=%PROCESS_DIR%\%BASENAME%%~x1
set ASSET_DEST=%ASSETS_DIR%\%BASENAME%%~x1

echo [%date% %time%] Queuing video %FILEPATH% >> "%LOGFILE%"

copy /Y "%FILEPATH%" "%ASSET_DEST%" >> "%LOGFILE%" 2>&1
move /Y "%FILEPATH%" "%PROC_DEST%" >> "%LOGFILE%" 2>&1

rem If ffmpeg-based transcoder exists, call it
if exist "%CD%\scripts\processors\transcode_video.bat" (
  echo [%date% %time%] Calling transcode tool for %PROC_DEST% >> "%LOGFILE%"
  call "%CD%\scripts\processors\transcode_video.bat" "%PROC_DEST%" >> "%LOGFILE%" 2>&1 || echo [%date% %time%] Transcode failed for %PROC_DEST% >> "%LOGFILE%"
) else (
  echo [%date% %time%] No transcode script found; queued at %PROC_DEST% >> "%LOGFILE%"
)
goto :EOF
