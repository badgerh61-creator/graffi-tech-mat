@echo off
REM ====================================================================
REM embeddings-generate.bat
REM Generates embeddings for all assets (images, 3D, moodboards, etc.)
REM ====================================================================

echo ==== GENERATING EMBEDDINGS ====

if exist venv (
  call venv\Scripts\activate.bat
)

if not exist ai\embeddings\generate.py (
  echo Missing generate.py in ai\\embeddings\\
  exit /b 1
)

python ai\embeddings\generate.py --rebuild

if %ERRORLEVEL% neq 0 (
  echo Embeddings generation FAILED.
  exit /b 2
)

echo Embeddings successfully generated.
exit /b 0
