@echo off
REM ====================================================================
REM ingest-3d-assets.bat
REM Usage: ingest-3d-assets.bat [source_folder]
REM - Ingests 3D assets (obj, fbx, glb, gltf), validates and queues for conversion.
REM ====================================================================

setlocal enabledelayedexpansion
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\3d

set ASSETS_DIR=%cd%\assets\3d
set PROCESS_DIR=%cd%\processing\3d
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-3d_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting 3D asset ingestion from "%SOURCE%" >> "%LOGFILE%"

for %%F in ("%SOURCE%\*.*") do (
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="obj" call :HANDLE "%%~fF"
  if /I "!EXT!"=="fbx" call :HANDLE "%%~fF"
  if /I "!EXT!"=="glb" call :HANDLE "%%~fF"
  if /I "!EXT!"=="gltf" call :HANDLE "%%~fF"
)

echo [%date% %time%] 3D ingestion finished. >> "%LOGFILE%"
exit /b 0

:HANDLE
set FILE=%~1
set NAME=%~n1
set PROC_DEST=%PROCESS_DIR%\%NAME%%~x1
copy /Y "%FILE%" "%ASSETS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
move /Y "%FILE%" "%PROC_DEST%" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Queued 3D asset %NAME% >> "%LOGFILE%"

REM Optional converter call (e.g., glb optimization)
if exist "%CD%\scripts\processors\convert_3d.bat" (
  call "%CD%\scripts\processors\convert_3d.bat" "%PROC_DEST%" >> "%LOGFILE%" 2>&1
)
goto :EOF
