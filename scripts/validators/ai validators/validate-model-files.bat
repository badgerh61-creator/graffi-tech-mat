@echo off
set MODEL_DIR=ai\models

if not exist "%MODEL_DIR%" (
  echo Missing models folder.
  exit /b 1
)

dir "%MODEL_DIR%" | findstr ".onnx .bin .pt .model" >nul
if %ERRORLEVEL% neq 0 (
  echo Model files missing.
  exit /b 2
)

echo Model files validated.
exit /b 0
