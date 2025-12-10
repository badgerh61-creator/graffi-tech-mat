@echo off
REM test-reset.bat

echo Clearing pytest cache...
rmdir /s /q src\backend\.pytest_cache 2>nul

echo Clearing Jest/Vitest cache...
rmdir /s /q src\frontend\node_modules\.cache 2>nul

echo Test environment reset.
