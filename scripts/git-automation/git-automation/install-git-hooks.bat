@echo off
title Graffi-Tech-Mat Git Hooks Auto Installer
setlocal enabledelayedexpansion

echo ==================================================
echo      GRAFFI-TECH-MAT : GIT HOOKS AUTO INSTALLER
echo ==================================================
echo.

:: Detect project root (folder containing .git)
set ROOT=%~dp0..\..
set HOOKS_SOURCE=%~dp0hooks
set GIT_HOOKS_DIR=%ROOT%\.git\hooks

if not exist "%GIT_HOOKS_DIR%" (
    echo ERROR: .git folder not found.
    echo Make sure you run this inside a cloned repository.
    exit /b 1
)

echo Installing hooks into: %GIT_HOOKS_DIR%
echo.

for %%H in (
    pre-commit
    commit-msg
    pre-push
) do (
    if exist "%HOOKS_SOURCE%\%%H.bat" (
        echo Installing %%H hook...
        copy /y "%HOOKS_SOURCE%\%%H.bat" "%GIT_HOOKS_DIR%\%%H"
        echo @echo off > "%GIT_HOOKS_DIR%\%%H"
        echo call "%HOOKS_SOURCE%\%%H.bat" >> "%GIT_HOOKS_DIR%\%%H"
        echo exit /b 0 >> "%GIT_HOOKS_DIR%\%%H"
    ) else (
        echo Skipping %%H.bat (not found)
    )
)

echo.
echo Hooks installed successfully!
echo.

exit /b 0
