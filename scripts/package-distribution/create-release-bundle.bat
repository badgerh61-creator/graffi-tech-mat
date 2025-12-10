@echo off
REM create-release-bundle.bat
REM Creates a release tarball containing packaged backend, frontend, infra manifests.

SETLOCAL ENABLEDELAYEDEXPANSION

SET VERSION=1.0.0
SET OUT_DIR=releases
SET BUNDLE=%OUT_DIR%\graffi-release-%VERSION%.tar.gz

echo === Creating release bundle %BUNDLE% ===

mkdir "%OUT_DIR%" >nul 2>&1

call package-backend.bat
call package-frontend.bat

REM Create bundle (requires tar in PATH; on Windows 10+, tar is available)
tar -czf "%BUNDLE" releases\backend-%VERSION%.zip releases\frontend-%VERSION%.zip infra src\backend\migrations README.md LICENSE

IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create release bundle. Trying PowerShell fallback...
    powershell -Command "Compress-Archive -Path releases\* , infra\* , src\backend\migrations\* , README.md, LICENSE -DestinationPath '%OUT_DIR%\graffi-release-%VERSION%.zip'"
    IF %ERRORLEVEL% NEQ 0 (
        echo Fallback failed.
        exit /b 3
    ) ELSE (
        echo Created ZIP fallback release at %OUT_DIR%\graffi-release-%VERSION%.zip
        exit /b 0
    )
)

echo Release bundle created at %BUNDLE%
ENDLOCAL
