@echo off
REM git-undo-last.bat - reset last commit, keep changes
git log -1 --pretty=format:"%h %s" > "%TEMP%\lastcommit.txt"
type "%TEMP%\lastcommit.txt"
echo Are you sure you want to undo the last commit? (y/N)
set /p RESP=
if /I "%RESP%"=="y" (
  git reset --soft HEAD~1
  echo Last commit undone (soft). Changes remain staged.
) else (
  echo Aborted.
)
exit /b 0
