@echo off
REM test-ci-gate.bat

call test-backend.bat
IF %ERRORLEVEL% NEQ 0 exit /b 1

call test-frontend.bat
IF %ERRORLEVEL% NEQ 0 exit /b 2

call test-lint.bat
IF %ERRORLEVEL% NEQ 0 exit /b 3

call test-security.bat
IF %ERRORLEVEL% NEQ 0 exit /b 4

echo CI Gate PASSED.
exit /b 0
