@echo off
set MSGFILE=%1
set /p MSG=<%MSGFILE%
echo %MSG% | findstr /R "^\(feat\|fix\|docs\|style\|refactor\|perf\|test\|chore\)(\([a-z0-9._-]\+\))\?: .*" >nul
if %ERRORLEVEL% neq 0 (
  echo Commit message does not follow Conventional Commits.
  exit /b 1
)
exit /b 0
