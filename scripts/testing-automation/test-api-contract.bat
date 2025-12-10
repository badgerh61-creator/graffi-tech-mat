@echo off
title API Contract Validation
color 0A

echo ==========================================
echo       API CONTRACT VALIDATION
echo ==========================================
echo.

REM Requires openapi-validator package
npx @redocly/cli lint api/openapi.yaml || (
    echo [ERROR] API Contract Validation Failed.
    exit /b 1
)

echo.
echo [SUCCESS] API Contract is valid.
exit /b 0
