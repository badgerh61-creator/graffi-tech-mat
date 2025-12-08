@echo off
REM branch-cleanup.bat - delete merged local branches (except main/master)
set BASE=%1
if "%BASE%"=="" set BASE=main

echo Fetching remote...
git fetch --prune

echo Deleting local branches merged into %BASE%...
for /f "tokens=*" %%b in ('git branch --merged %BASE% ^| findstr /v /R \"(^\*|%BASE%)\"') do (
  set BR=%%b
  set BR=!BR: =!
  echo Deleting local branch !BR!
  git branch -d !BR!
)

echo Optionally delete remote branches merged into %BASE%? (y/N)
set /p RESP=
if /I "%RESP%"=="y" (
  for /f "tokens=*" %%r in ('git branch -r --merged origin/%BASE% ^| findstr /v origin/%BASE%') do (
    set REM=%%r
    set REM=!REM: =!
    REM remove origin/ prefix
    set REM=!REM:origin/=!
    echo Deleting remote branch !REM!
    git push origin --delete !REM!
  )
)

exit /b 0
