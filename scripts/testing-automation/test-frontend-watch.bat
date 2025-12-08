@echo off
REM test-frontend-watch.bat

pushd src\frontend
npm test -- --watch
popd
