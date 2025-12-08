@echo off
REM ====================================================================
REM ingest-presets.bat
REM Usage: ingest-presets.bat [source_folder]
REM - Ingests presets (zip, json, presets) and registers them in DB or index.
REM ====================================================================

setlocal
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\presets

set ASSETS_DIR=%cd%\assets\presets
set PROCESS_DIR=%cd%\processing\presets
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-presets_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting presets ingestion from "%SOURCE%" >> "%LOGFILE%"

for %%F in ("%SOURCE%\*.*") do (
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="zip" call :PROC "%%~fF"
  if /I "!EXT!"=="json" call :PROC "%%~fF"
  if /I "!EXT!"=="preset" call :PROC "%%~fF"
)

echo [%date% %time%] Presets ingestion finished. >> "%LOGFILE%"
exit /b 0

:PROC
set FILE=%~1
set NAME=%~n1
copy /Y "%FILE%" "%ASSETS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
move /Y "%FILE%" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Preset registered: %NAME% >> "%LOGFILE%"

REM Optionally call importer
if exist "%CD%\scripts\processors\import_preset.py" (
  python "%CD%\scripts\processors\import_preset.py" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
)
goto :EOF
