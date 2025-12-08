@echo off
REM ====================================================================
REM embeddings-refresh.bat
REM Rebuilds embeddings only for modified or new assets.
REM ====================================================================

echo ==== REFRESHING EMBEDDINGS ====

if exist venv (
  call venv\Scripts\activate.bat
)

if not exist ai\embeddings\refresh.py (
  echo Missing refresh.py in ai\\embeddings\\
  exit /b 1
)

python ai\embeddings\refresh.py

if %ERRORLEVEL% neq 0 (
  echo Embeddings refresh failed.
  exit /b 2
)

echo Embeddings refreshed successfully.
exit /b 0
