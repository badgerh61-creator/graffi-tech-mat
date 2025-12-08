@echo off
set VEC_DIR=ai\embeddings

if not exist "%VEC_DIR%" (
  echo Embeddings folder missing.
  exit /b 1
)

dir "%VEC_DIR%" | findstr ".vec .json" >nul
if %ERRORLEVEL% neq 0 (
  echo No embedding files detected.
  exit /b 2
)

echo Embeddings OK.
exit /b 0
