@echo off
REM setup-git-hooks.bat - installs git hooks from .githooks directory
SETLOCAL

IF NOT EXIST .git (
  echo This is not a git repository. Run from repository root.
  exit /b 1
)

if not exist .githooks (
  echo No .githooks directory found. Creating sample pre-commit...
  mkdir .githooks
  echo @echo off> .githooks\pre-commit
  echo call ..\automation\devops\devops-check.bat >> .githooks\pre-commit
)

git config core.hooksPath .githooks
echo git hooks path set to .githooks
ENDLOCAL
