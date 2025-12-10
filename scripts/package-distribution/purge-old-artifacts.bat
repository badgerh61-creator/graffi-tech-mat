@echo off
REM purge-old-artifacts.bat

set ART_DIR=artifacts
set DAYS=30

mkdir "%ART_DIR%" >nul 2>&1

echo Removing artifacts older than %DAYS% days...
forfiles /p %ART_DIR% /s /m *.* /d -%DAYS% /c "cmd /c del @path"

echo Artifact purge complete.
