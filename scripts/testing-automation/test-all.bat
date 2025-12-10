@echo off
REM test-all.bat

echo === Running ALL Tests ===

call test-backend.bat
call test-frontend.bat
call test-lint.bat
call test-security.bat

echo ALL tests completed.
