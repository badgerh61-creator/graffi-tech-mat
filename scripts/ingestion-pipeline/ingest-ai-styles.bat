@echo off
REM ====================================================================
REM ingest-ai-styles.bat
REM Usage: ingest-ai-styles.bat [source_folder]
REM - Ingests AI style files (json, yaml, .style) into assets/styles, registers them.
REM ====================================================================

setlocal
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\styles

set ASSETS_DIR=%cd%\assets\styles
set PROCESS_DIR=%cd%\processing\styles
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-styles_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting style ingestion from "%SOURCE%" >> "%LOGFILE%"

for %%F in ("%SOURCE%\*.*") do (
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="json" call :PROC "%%~fF"
  if /I "!EXT!"=="yaml" call :PROC "%%~fF"
  if /I "!EXT!"=="yml" call :PROC "%%~fF"
  if /I "!EXT!"=="style" call :PROC "%%~fF"
)

echo [%date% %time%] Style ingestion finished. >> "%LOGFILE%"
exit /b 0

:PROC
set FILE=%~1
set NAME=%~n1
copy /Y "%FILE%" "%ASSETS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
move /Y "%FILE%" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Registered style %NAME% >> "%LOGFILE%"

REM Optional: Call registration script
if exist "%CD%\scripts\processors\register_style.py" (
  python "%CD%\scripts\processors\register_style.py" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
)
goto :EOF
