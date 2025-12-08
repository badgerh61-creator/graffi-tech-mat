@echo off
REM ====================================================================
REM prepare-ai-dataset.bat
REM Prepares datasets: validates files, builds structure, converts formats.
REM ====================================================================

echo ==== PREPARING DATASET ====

if not exist ai\\dataset (
  mkdir ai\\dataset
  echo Created dataset directory.
)

if exist venv (
  call venv\Scripts\activate.bat
)

if not exist ai\dataset\prepare.py (
  echo Missing dataset prepare script at ai\\dataset\\prepare.py
  exit /b 1
)

python ai\dataset\prepare.py

if %ERRORLEVEL% neq 0 (
  echo Dataset preparation FAILED.
  exit /b 2
)

echo Dataset prepared successfully.
exit /b 0
