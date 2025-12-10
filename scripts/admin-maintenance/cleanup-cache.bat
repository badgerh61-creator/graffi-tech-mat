@echo off
REM cleanup-cache.bat — clear browser & package manager cache

echo Cleaning NPM cache...
npm cache clean --force

echo Cleaning Yarn cache...
yarn cache clean

echo Cleaning browser cache (Chrome)...
for /d %%x in ("%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Cache*") do (
    rmdir /s /q "%%x"
)

echo Cache cleanup complete.
