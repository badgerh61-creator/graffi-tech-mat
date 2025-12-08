@echo off
title Auto Tag Script

set VERSION_FILE=package.json

for /f "tokens=2 delims=:," %%A in ('findstr /i "version" %VERSION_FILE%') do (
    set RAW_VERSION=%%A
)

set VERSION=%RAW_VERSION:"=%
set VERSION=%VERSION: =%

echo Creating git tag v%VERSION%...

git tag -a v%VERSION% -m "Release v%VERSION%"
git push origin v%VERSION%

echo Tag v%VERSION% created and pushed.
exit /b 0
