@echo off
REM cleanup-node-modules.bat

echo Searching for node_modules folders...
for /d /r %%i in (node_modules) do (
    echo Removing %%i
    rmdir /s /q "%%i"
)

echo node_modules cleanup complete.
