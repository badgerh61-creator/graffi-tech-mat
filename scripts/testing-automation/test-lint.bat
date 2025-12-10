@echo off
REM test-lint.bat

echo === Linting Code ===

where flake8 >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Running Python lint...
    flake8 src\backend
) else (
    echo flake8 not installed.
)

pushd src\frontend
where eslint >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Running JS lint...
    npx eslint src
) else (
    echo eslint not installed.
)
popd

echo Linting complete.
