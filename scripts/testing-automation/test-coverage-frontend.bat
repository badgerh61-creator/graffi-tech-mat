@echo off
REM test-coverage-frontend.bat

pushd src\frontend
npm test -- --coverage
popd

echo Frontend coverage complete.
