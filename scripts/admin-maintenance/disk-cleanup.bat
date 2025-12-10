@echo off
REM disk-cleanup.bat — frees disk space

echo Emptying Recycle Bin...
powershell "Clear-RecycleBin -Force"

echo Cleaning system temp...
rmdir /s /q C:\Windows\Temp 2>nul
mkdir C:\Windows\Temp

echo Cleaning user temp...
rmdir /s /q %TEMP% 2>nul
mkdir %TEMP%

echo Disk cleanup complete.
