@echo off
REM test-frontend.bat

SETLOCAL ENABLEDELAYEDEXPANSION

SET FRONTEND_DIR=src\frontend

echo === Frontend Tests ===

pushd %FRONTEND_DIR%
npm test
popd

echo Frontend tests complete.
ENDLOCAL
