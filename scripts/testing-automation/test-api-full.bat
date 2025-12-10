@echo off
REM test-api-full.bat

SET TEST_FILE=tests\api\api-tests.http

echo === Running FULL API Tests ===

if not exist "%TEST_FILE%" (
    echo API test file not found: %TEST_FILE%
    exit /b 1
)

powershell -Command "Invoke-WebRequest -Uri 'http://localhost:5000/users' -UseBasicParsing"
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:5000/products' -UseBasicParsing"

echo Full API suite done.
