@echo off
REM ====================================================================
REM validate-ai-pipelines.bat
REM Validates all AI/ML pipelines end-to-end.
REM ====================================================================

echo ==== VALIDATING AI PIPELINES ====

if exist venv (
  call venv\Scripts\activate.bat
)

set VALIDATION_SCRIPTS=ai\\validation\\validate_training.py ai\\validation\\validate_inference.py ai\\validation\\validate_embeddings.py

for %%S in (%VALIDATION_SCRIPTS%) do (
  if not exist %%S (
    echo Missing validation script %%S
    exit /b 1
  )

  python %%S
  if %ERRORLEVEL% neq 0 (
    echo Validation FAILED on %%S
    exit /b 2
  )
)

echo All AI pipelines validated successfully.
exit /b 0
