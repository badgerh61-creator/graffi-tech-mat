@echo off
REM pipeline-release.bat - tag, push docker images, push git tag, uplod artifacts
SETLOCAL

if "%~1"=="" (
  echo Usage: pipeline-release.bat <version>
  exit /b 2
)
set VERSION=%~1

echo Creating git tag v%VERSION%
git tag -a v%VERSION% -m "Release v%VERSION%"
git push origin v%VERSION%

echo Pushing docker images with tag %VERSION%
for %%S in (backend frontend worker) do (
  docker tag graffi/%%S:latest graffi/%%S:%VERSION%
  docker push graffi/%%S:%VERSION%
)

echo Running changelog generator...
call "%~dp0changelog-gen.bat"

echo Move artifacts to release folder...
if not exist "%~dp0..\releases" mkdir "%~dp0..\releases"
xcopy /E /I /Y "%~dp0..\automation\artifacts" "%~dp0..\releases\%VERSION%" >nul

echo Release %VERSION% completed.
ENDLOCAL
