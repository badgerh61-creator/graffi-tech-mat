@echo off
title Protect Main Branch

git rev-parse --abbrev-ref HEAD > current-branch.txt
set /p BRANCH=<current-branch.txt

if /i "%BRANCH%"=="main" (
    echo ERROR: Cannot push directly to main.
    echo Please create a feature branch.
    exit /b 1
)

if /i "%BRANCH%"=="production" (
    echo ERROR: Cannot push directly to production.
    exit /b 1
)

echo Branch %BRANCH% is allowed for push.
exit /b 0
