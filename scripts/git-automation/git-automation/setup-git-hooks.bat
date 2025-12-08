@echo off
REM setup-git-hooks.bat - set git hooks path to automation/git/git-hooks

IF NOT EXIST .git (
  echo This does not appear to be a git repo root. Run from repo root.
  exit /b 1
)

REM Ensure hooks dir exists
if not exist automation\git\git-hooks (
  echo No git-hooks directory found at automation\git\git-hooks
  exit /b 1
)

git config core.hooksPath automation/git/git-hooks
echo Git hooks path set to automation/git/git-hooks
exit /b 0
