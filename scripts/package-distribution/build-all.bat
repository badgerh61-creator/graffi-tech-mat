@echo off
REM build-all.bat
REM Build everything: backend wheel/sdist + frontend production bundle

echo === Build ALL ===

call build-backend.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Backend build failed. Aborting.
    exit /b 1
)

call build-frontend.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Frontend build failed. Aborting.
    exit /b 2
)

echo All builds succeeded.
