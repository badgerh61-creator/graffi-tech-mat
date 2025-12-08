@echo off
REM cleanup-temp.bat — wipe temporary folders

set TEMP1=%TEMP%
set TEMP2=C:\Windows\Temp

echo Cleaning user temp...
rmdir /s /q "%TEMP1%" 2>nul
mkdir "%TEMP1%"

echo Cleaning system temp...
rmdir /s /q "%TEMP2%" 2>nul
mkdir "%TEMP2%"

echo Temp cleanup complete.
