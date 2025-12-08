@echo off
REM ====================================================================
REM ai-cache-clear.bat
REM Clears ML temporary cache, model artifacts, tensor dumps, etc.
REM ====================================================================

echo ==== CLEARING AI CACHE ====

if exist ai\\cache (
  rmdir /S /Q ai\\cache
  echo Deleted /ai/cache folder.
)

if exist ai\\temp (
  rmdir /S /Q ai\\temp
  echo Deleted /ai/temp folder.
)

echo AI cache cleared.
exit /b 0
