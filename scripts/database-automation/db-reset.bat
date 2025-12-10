@echo off
setlocal

:: Full reset: drop, create, migrate, seed
set db=%1
if "%db%"=="" set db=postgres

call db-drop.bat %db%
if %errorlevel% neq 0 echo Warning: drop may have failed.

call db-create.bat %db%
if %errorlevel% neq 0 (
    echo Failed to create DB. Aborting.
    pause
    exit /b 1
)

call db-migrate.bat
if %errorlevel% neq 0 (
    echo Migrations failed. Aborting.
    pause
    exit /b 1
)

call db-seed.bat
echo Database reset complete.
endlocal
pause
