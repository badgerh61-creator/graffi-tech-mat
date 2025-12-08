@echo off
REM changelog-gen.bat
REM Generate CHANGELOG.md from git log between last tag and HEAD

SETLOCAL ENABLEDELAYEDEXPANSION

SET OUT=CHANGELOG.md

where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo git not found.
    exit /b 1
)

echo ## Changelog > %OUT%
echo >> %OUT%

REM Get last tag
for /f "usebackq delims=" %%t in (`git describe --tags --abbrev=0 2^>nul`) do set LASTTAG=%%t

if "%LASTTAG%"=="" (
    echo No tags found — listing recent commits >> %OUT%
    git log --pretty=format:"- %s (%an)" -n 50 >> %OUT%
) else (
    echo Changes since %LASTTAG% >> %OUT%
    echo >> %OUT%
    git log %LASTTAG%..HEAD --pretty=format:"- %s (%an)" >> %OUT%
)

echo Changelog written to %OUT%
ENDLOCAL
