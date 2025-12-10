@echo off
REM pre-commit.bat - simple pre-commit checks for Windows Git
echo Running pre-commit checks...
git diff --exit-code --quiet
if %ERRORLEVEL% neq 0 (
  echo You have unstaged changes. Please stage or stash them.
  exit /b 1
)
if exist package.json (
  where npm >nul 2>&1
  if %ERRORLEVEL%==0 (
    npm run -s lint || (echo Lint failed & exit /b 1)
  )
)
exit /b 0


