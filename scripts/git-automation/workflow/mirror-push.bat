@echo off
REM mirror-push.bat <mirror-remote-name> [branch]
set MIRROR=%1
if "%MIRROR%"=="" (
  echo Usage: mirror-push.bat <mirror-remote-name> [branch]
  exit /b 2
)
set BRANCH=%2
if "%BRANCH%"=="" set BRANCH=--all

echo Pushing to mirror %MIRROR% ...
git push %MIRROR% %BRANCH%
exit /b %ERRORLEVEL%
