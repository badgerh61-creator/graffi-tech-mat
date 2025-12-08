@echo off
REM ====================================================================
REM ml-inference-test.bat
REM Runs a simple inference test to ensure models load properly.
REM ====================================================================

echo ==== ML INFERENCE TEST ====

if exist venv (
  call venv\Scripts\activate.bat
)

if not exist ai\inference\test_inference.py (
  echo ERROR: Inference test file not found at ai\inference\test_inference.py
  exit /b 1
)

python ai\inference\test_inference.py

if %ERRORLEVEL% neq 0 (
  echo Inference test FAILED.
  exit /b 2
)

echo Inference test PASSED.
exit /b 0
