@echo off
echo Running pre-push checks...
if exist package.json (
  where npm >nul 2>&1
  if %ERRORLEVEL%==0 (
    npm run test:ci || (echo Tests failed & exit /b 1)
  )
)
exit /b 0
