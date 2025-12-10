@echo off
title Safe Git Stash

echo Stashing uncommitted changes...
git stash push -m "auto-stash" --include-untracked

if %errorlevel% neq 0 (
    echo Failed to stash changes.
    exit /b 1
)

echo Running the requested operation...
%*

echo Restoring stashed changes...
git stash pop

echo Operation completed with restored changes.
exit /b 0
