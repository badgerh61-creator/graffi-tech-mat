@echo off
REM test-backend-watch.bat

SET BACKEND_DIR=src\backend

pushd %BACKEND_DIR%
pytest --maxfail=1 --disable-warnings -q --looponfail
popd
