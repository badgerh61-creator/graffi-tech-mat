@echo off
REM repo-backup.bat - create a git bundle of the repo
set OUTDIR=%~dp0..\backups
set DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%
mkdir "%OUTDIR%" >nul 2>&1
git bundle create "%OUTDIR%\graffi-repo-%DATE%.bundle" --all
echo Bundle created at %OUTDIR%
exit /b 0
