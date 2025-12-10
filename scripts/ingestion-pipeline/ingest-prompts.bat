@echo off
REM ====================================================================
REM ingest-prompts.bat
REM Usage: ingest-prompts.bat [source_file_or_folder]
REM - Ingests text prompts (txt, csv, json) and loads into prompts store.
REM ====================================================================

setlocal
set SOURCE=%~1
if "%SOURCE%"=="" set SOURCE=%cd%\incoming\prompts

set PROCESS_DIR=%cd%\processing\prompts
set LOG_DIR=%cd%\logs\ingest
set LOGFILE=%LOG_DIR%\ingest-prompts_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%PROCESS_DIR%" mkdir "%PROCESS_DIR%"

echo [%date% %time%] Starting prompt ingestion from "%SOURCE%" >> "%LOGFILE%"

if exist "%SOURCE%" (
  if exist "%SOURCE%\*" (
    for %%F in ("%SOURCE%\*.*") do call :PROC "%%~fF"
  ) else (
    call :PROC "%SOURCE%"
  )
) else (
  echo Source %SOURCE% not found >> "%LOGFILE%"
  exit /b 2
)

echo [%date% %time%] Prompt ingestion finished. >> "%LOGFILE%"
exit /b 0

:PROC
set FILE=%~1
set NAME=%~n1
echo [%date% %time%] Ingesting %FILE% >> "%LOGFILE%"
copy /Y "%FILE%" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
if exist "%CD%\scripts\processors\import_prompts.py" (
  python "%CD%\scripts\processors\import_prompts.py" "%PROCESS_DIR%\%NAME%%~x1" >> "%LOGFILE%" 2>&1
)
goto :EOF
