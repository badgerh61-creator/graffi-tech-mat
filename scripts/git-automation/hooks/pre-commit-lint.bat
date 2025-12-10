@echo off
title Pre-Commit Lint Check

echo Running ESLint...
call npx eslint . --ext .js,.jsx,.ts,.tsx
if %errorlevel% neq 0 (
    echo ESLint failed. Fix issues before committing.
    exit /b 1
)

echo Running Prettier check...
call npx prettier --check .
if %errorlevel% neq 0 (
    echo Prettier formatting issues detected.
    echo Run: npx prettier --write .
    exit /b 1
)

echo Pre-commit lint check passed.
exit /b 0
