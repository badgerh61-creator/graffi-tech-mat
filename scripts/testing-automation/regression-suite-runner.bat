@echo off
title Regression Test Suite
color 0D

echo ==========================================
echo       FULL REGRESSION TEST SUITE
echo ==========================================
echo.

call automated-unit-tests.bat
IF %ERRORLEVEL% NEQ 0 exit /b 1

call automated-integration-tests.bat
IF %ERRORLEVEL% NEQ 0 exit /b 1

call run-e2e-tests.bat
IF %ERRORLEVEL% NEQ 0 exit /b 1

echo.
echo [SUCCESS] ALL regression tests passed!
exit /b 0
