@echo off
REM ====================================================================
REM ingest-images.bat
REM Usage: ingest-images.bat [source_folder]
REM - Scans source_folder for images (jpg, png, webp), validates, copies to assets/images,
REM   queues them to processing/images/ and optionally calls a processor (python/node).
REM ====================================================================

setlocal enabledelayedexpansion
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\images

set ASSETS_DIR=%cd%\assets\images
set PROCESS_DIR=%cd%\processing\images
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-images_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting image ingestion from "%SOURCE%" >> "%LOGFILE%"

if not exist "%SOURCE%" (
  echo Source folder "%SOURCE%" not found. >> "%LOGFILE%"
  echo ERROR: Source not found.
  exit /b 2
)

rem Allowed file extensions (case-insensitive)
for %%F in ("%SOURCE%\*.*") do (
  set FILE=%%~fF
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="jpg" (
    call :PROCESS_FILE "%%~fF"
  ) else if /I "!EXT!"=="jpeg" (
    call :PROCESS_FILE "%%~fF"
  ) else if /I "!EXT!"=="png" (
    call :PROCESS_FILE "%%~fF"
  ) else if /I "!EXT!"=="webp" (
    call :PROCESS_FILE "%%~fF"
  ) else (
    rem ignore other files
  )
)

echo [%date% %time%] Image ingestion finished. >> "%LOGFILE%"
exit /b 0

:PROCESS_FILE
set FILEPATH=%~1
set BASENAME=%~n1
set DEST=%ASSETS_DIR%\%BASENAME%%~x1
set PROC_DEST=%PROCESS_DIR%\%BASENAME%%~x1

echo [%date% %time%] Processing %FILEPATH% >> "%LOGFILE%"

rem Basic validation - ensure file size > 0
for %%S in ("%FILEPATH%") do set SIZE=%%~zS
if %SIZE%==0 (
  echo [%date% %time%] SKIP zero-size file: %FILEPATH% >> "%LOGFILE%"
  goto :EOF
)

rem Copy to assets (keep original) and move to processing for pipeline
copy /Y "%FILEPATH%" "%DEST%" >> "%LOGFILE%" 2>&1
move /Y "%FILEPATH%" "%PROC_DEST%" >> "%LOGFILE%" 2>&1

if exist "%CD%\scripts\processors\process_image.py" (
  echo [%date% %time%] Calling Python image processor for %PROC_DEST% >> "%LOGFILE%"
  python "%CD%\scripts\processors\process_image.py" "%PROC_DEST%" >> "%LOGFILE%" 2>&1 || echo [%date% %time%] Processor failed for %PROC_DEST% >> "%LOGFILE%"
) else (
  echo [%date% %time%] No image processor found; file queued at %PROC_DEST% >> "%LOGFILE%"
)
goto :EOF
