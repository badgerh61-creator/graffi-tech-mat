@echo off
REM ci-build-test.bat

echo === CI Pipeline Simulation ===

echo Running backend tests...
call scripts\testing\run-backend-tests.bat

echo Building frontend...
pushd src\frontend
npm install
npm run build
popd

echo Running linter (if installed)...
REM placeholder for eslint/flake8

echo CI simulation complete.
