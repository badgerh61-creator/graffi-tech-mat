@echo off
REM release.bat <patch|minor|major> [remote] [publish]
set TYPE=%1
if "%TYPE%"=="" set TYPE=patch
set REMOTE=%2
if "%REMOTE%"=="" set REMOTE=origin

REM 1) Ensure working tree is clean
git diff --quiet --ignore-submodules HEAD
if %ERRORLEVEL% neq 0 (
  echo Working tree not clean. Commit or stash changes before releasing.
  exit /b 1
)

REM 2) Bump version
call "%~dp0version-bump.bat" %TYPE%

REM 3) Generate changelog
REM If you want to use repository-local changelog-gen.bat, ensure it exists; otherwise call the uploaded one
if exist "%~dp0changelog-gen.bat" (
  call "%~dp0changelog-gen.bat"
) else (
  call "C:\Windows\System32\cmd.exe" /c "file:///mnt/data/424c68a6-1500-42a5-ad3a-c9be71d4b7ba.bat"
)

REM 4) Commit changelog & VERSION
git add CHANGELOG.md VERSION package.json 2>nul
git commit -m "chore(release): bump version and update changelog" || echo "No changes to commit"

REM 5) Create annotated tag
for /f "tokens=*" %%v in ('type "%~dp0\..\VERSION"') do set NEWVER=%%v
git tag -a v%NEWVER% -m "Release v%NEWVER%"

REM 6) Push tag & branch
git push %REMOTE% HEAD
git push %REMOTE% v%NEWVER%

REM 7) (Optional) publish artifacts - e.g. run pipeline release
echo Release v%NEWVER% created and pushed.

REM 8) Optional: call CI pipeline trigger or artifact publisher here

exit /b 0
