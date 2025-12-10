@echo off
findstr "AI_MODEL_PATH" .env >nul
if %ERRORLEVEL% neq 0 (
  echo AI model path missing in .env
  exit /b 1
)

findstr "EMBEDDING_PROVIDER" .env >nul
if %ERRORLEVEL% neq 0 (
  echo Missing embedding provider config.
  exit /b 1
)

echo AI config validated.
exit /b 0
