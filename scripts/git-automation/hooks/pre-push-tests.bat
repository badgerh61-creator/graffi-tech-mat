@echo off
title Pre-Push Test Runner

echo Running unit tests...
call npm run test:unit
if %errorlevel% neq 0 (
    echo Unit tests failed. Push blocked.
    exit /b 1
)

echo Running integration tests...
call npm run test:integration
if %errorlevel% neq 0 (
    echo Integration tests failed. Push blocked.
    exit /b 1
)

echo All tests passed. Push allowed.
exit /b 0
