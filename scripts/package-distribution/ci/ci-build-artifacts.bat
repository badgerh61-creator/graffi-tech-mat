@echo off
REM ci-build-artifacts.bat

echo Building backend wheel/packages...
REM add python build commands

echo Building frontend production build...
pushd src\frontend
npm run build
popd

echo Artifacts ready.
