@echo off
title Validate Clean Working Tree

echo Checking git status...

git diff-index --quiet HEAD --
if %errorlevel% neq 0 (
    echo Uncommitted changes detected.
    echo Commit or stash before continuing.
    exit /b 1
)

git diff --cached --quiet
if %errorlevel% neq 0 (
    echo Staged but uncommitted changes detected.
    exit /b 1
)

echo Working tree is clean.
exit /b 0
