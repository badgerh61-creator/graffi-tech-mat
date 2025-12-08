@echo off
:: =====================================================================
:: validate-permissions.bat
:: Ensures critical project folders do not have Everyone/FULL permissions.
:: =====================================================================

set TARGET_DIR=%cd%

echo === VALIDATING PERMISSIONS FOR: %TARGET_DIR% ===

icacls "%TARGET_DIR%" | findstr /I "Everyone:F"
if %ERRORLEVEL%==0 (
    echo WARNING: 'Everyone' has FULL control in this directory — NOT SECURE.
) else (
    echo Permissions look secure.
)

exit /b 0
