@echo off
REM scaffold-root.bat
REM Creates the main folder structure and common root files

SETLOCAL ENABLEDELAYEDEXPANSION

:: Config - edit these to match your project
SET PROJECT_NAME=graffi-tech-mat
SET LICENSE=MIT
SET AUTHOR="Your Name <you@example.com>"
SET REPO_URL=https://example.com/your/repo.git

echo.
echo === Scaffolding root structure for %PROJECT_NAME% ===
echo.

:: Top-level folders
for %%d in (
    src
    src\backend
    src\frontend
    infra
    scripts
    docs
    tests
    assets
    ci
    tools
    tmp
    .github\workflows
) do (
    if not exist "%%d" (
        mkdir "%%d" && echo Created folder: %%d
    ) else (
        echo Exists: %%d
    )
)

:: Common root files
if not exist README.md (
    echo # %PROJECT_NAME% > README.md
    echo. >> README.md
    echo Project scaffolded on %DATE% >> README.md
    echo >> README.md
    echo ## Quick start >> README.md
    echo See scripts/scaffold-root.bat for structure. >> README.md
    echo Created README.md
) else (
    echo README.md exists
)

if not exist .gitignore (
    (
      echo node_modules/
      echo env/
      echo .venv/
      echo dist/
      echo build/
      echo *.log
      echo tmp/
    ) > .gitignore
    echo Created .gitignore
) else (
    echo .gitignore exists
)

if not exist LICENSE (
    (
      echo %LICENSE% License
      echo Copyright (c) %DATE% %AUTHOR%
    ) > LICENSE
    echo Created LICENSE placeholder (please replace with full text)
) else (
    echo LICENSE exists
)

:: Initialize git if not already
where git >nul 2>&1
if %ERRORLEVEL%==0 (
    if not exist .git (
        git init
        if defined REPO_URL (
            git remote add origin %REPO_URL% 2>nul
        )
        echo Git repo initialized
    ) else (
        echo Git repo already initialized
    )
) else (
    echo Git not found in PATH; skipping git init
)

echo.
echo Root scaffolding complete.
ENDLOCAL
