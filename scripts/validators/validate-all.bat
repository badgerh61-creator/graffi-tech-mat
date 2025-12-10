@echo off
REM =====================================================================
REM validate-all.bat
REM Master validator orchestrator for Graffi-Tech-Mat.
REM Runs ALL validation scripts and generates a summary report.
REM =====================================================================

setlocal enabledelayedexpansion

echo ==========================================================
echo   GRAFFI-TECH-MAT VALIDATOR ORCHESTRATOR
echo ==========================================================

set LOG_DIR=%cd%\logs\validators
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set TS=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TS=%TS: =0%
set LOGFILE=%LOG_DIR%\validation-report_%TS%.log

echo Writing detailed logs to: %LOGFILE%
echo ==========================================================>> "%LOGFILE%"

REM ------------------ FUNCTION TO RUN VALIDATOR -------------------------
:RUN
set SCRIPT=%1
set NAME=%2

echo Running: %NAME%
echo [%DATE% %TIME%] START %NAME% (%SCRIPT%) >> "%LOGFILE%"

call "%SCRIPT%" >nul 2>&1
set EXIT=%ERRORLEVEL%

if !EXIT! EQU 0 (
    echo   ✓ PASS  - %NAME%
    echo [%DATE% %TIME%] PASS %NAME% >> "%LOGFILE%"
) else (
    echo   ✗ FAIL  - %NAME%   (code !EXIT!)
    echo [%DATE% %TIME%] FAIL %NAME% (exit !EXIT!) >> "%LOGFILE%"
    set /a FAILURES+=1
)

echo ---------------------------------------------------------->> "%LOGFILE%"
goto :EOF


REM =====================================================================
REM Initialize counters
REM =====================================================================

set /a FAILURES=0

echo.
echo ===== 1) ENVIRONMENT VALIDATORS =====
call :RUN "validate-system-requirements.bat"  "System Requirements"
call :RUN "validate-os-compatibility.bat"      "OS Compatibility"
call :RUN "validate-env-variables.bat"         "Environment Variables"
call :RUN "validate-storage-space.bat"         "Storage Space"


echo.
echo ===== 2) BACKEND VALIDATORS =====
call :RUN "validate-backend-dependencies.bat"  "Backend Dependencies"
call :RUN "validate-backend-routes.bat"        "Backend Routes"
call :RUN "validate-backend-config.bat"        "Backend Config"
call :RUN "validate-backend-security.bat"      "Backend Security"


echo.
echo ===== 3) FRONTEND VALIDATORS =====
call :RUN "validate-react-components.bat"      "React Components"
call :RUN "validate-ui-theme.bat"              "UI Theme"
call :RUN "validate-frontend-dependencies.bat" "Frontend Dependencies"
call :RUN "validate-frontend-build-ready.bat"  "Frontend Build Ready"


echo.
echo ===== 4) DOCKER / DEVOPS VALIDATORS =====
call :RUN "validate-docker-installed.bat"      "Docker Installed"
call :RUN "validate-docker-running.bat"        "Docker Daemon Running"
call :RUN "validate-docker-compose.bat"        "Docker Compose Installed"
call :RUN "validate-container-health.bat"      "Container Health"


echo.
echo ===== 5) AI / MODEL VALIDATORS =====
call :RUN "validate-embeddings.bat"            "Embeddings Check"
call :RUN "validate-model-files.bat"           "AI Model Files"
call :RUN "validate-ai-engine-running.bat"     "AI Engine Running"
call :RUN "validate-ai-configurations.bat"     "AI Configurations"


echo.
echo ===== 6) API VALIDATORS =====
call :RUN "validate-api-endpoints.bat"         "API Endpoints"
call :RUN "validate-openapi-schema.bat"        "OpenAPI Schema"
call :RUN "validate-api-auth.bat"              "API Auth"
call :RUN "validate-webhooks.bat"              "Webhook Validation"


echo.
echo ==========================================================
echo                  VALIDATION SUMMARY
echo ==========================================================

if %FAILURES% EQU 0 (
    echo ALL VALIDATIONS PASSED ✓✓✓
    echo ALL VALIDATIONS PASSED ✓✓✓ >> "%LOGFILE%"
) else (
    echo %FAILURES% VALIDATOR(S) FAILED ✗
    echo %FAILURES% VALIDATOR(S) FAILED ✗ >> "%LOGFILE%"
)

echo Detailed report saved to:
echo   %LOGFILE%

echo ==========================================================
exit /b %FAILURES%
