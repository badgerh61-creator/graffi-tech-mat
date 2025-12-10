@echo off
REM ====================================================================
REM ingest-moodboards.bat
REM Usage: ingest-moodboards.bat [source_folder]
REM - Ingests moodboard archives/images and extracts metadata, thumbnails.
REM ====================================================================

setlocal
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\moodboards

set ASSETS_DIR=%cd%\assets\moodboards
set PROCESS_DIR=%cd%\processing\moodboards
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-moodboards_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting moodboard ingestion from "%SOURCE%" >> "%LOGFILE%"

for %%F in ("%SOURCE%\*.*") do (
  set EXT=%%~xF
  set EXT=!EXT:~1!
  if /I "!EXT!"=="zip" call :UNPACK "%%~fF"
  if /I "!EXT!"=="jpg" call :PROCIMG "%%~fF"
  if /I "!EXT!"=="png" call :PROCIMG "%%~fF"
)

echo [%date% %time%] Moodboard ingestion finished. >> "%LOGFILE%"
exit /b 0

:UNPACK
set FILE=%~1
set NAME=%~n1
set TMPDIR=%PROCESS_DIR%\%NAME%
mkdir "%TMPDIR%" 2>nul
echo [%date% %time%] Extracting %FILE% to %TMPDIR% >> "%LOGFILE%"
powershell -NoProfile -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [IO.Compression.ZipFile]::ExtractToDirectory('%FILE%','%TMPDIR%')" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Extraction complete for %NAME% >> "%LOGFILE%"
REM Optionally call a metadata extractor
if exist "%CD%\scripts\processors\moodboard_extract.py" (
  python "%CD%\scripts\processors\moodboard_extract.py" "%TMPDIR%" >> "%LOGFILE%" 2>&1
)
goto :EOF

:PROCIMG
set FILE=%~1
set NAME=%~n1
set DEST=%ASSETS_DIR%\%NAME%%~x1
set PROC_DEST=%PROCESS_DIR%\%NAME%%~x1
copy /Y "%FILE%" "%DEST%" >> "%LOGFILE%" 2>&1
move /Y "%FILE%" "%PROC_DEST%" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Moodboard image queued: %NAME% >> "%LOGFILE%"
goto :EOF
