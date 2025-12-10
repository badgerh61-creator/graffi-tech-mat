@echo off
setlocal

:: Rollback last migration. Adjust to your migration tooling.
echo Rolling back last DB migration...
if exist package.json (
    npm run migrate:rollback || (
        echo Rollback failed. Check your migration tool and adjust this script.
        pause
        exit /b 1
    )
) else (
    echo No package.json detected. Update this script to run your rollback command.
    pause
    exit /b 1
)

echo Rollback complete.
endlocal
pause
