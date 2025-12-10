@echo off
REM ================================================================
REM validate-system-requirements.bat
REM Checks CPU, RAM, disk space, OS version, and architecture.
REM ================================================================

echo == Validating System Requirements ==

systeminfo | find "OS Name" 
systeminfo | find "OS Version"

wmic cpu get Name
wmic computersystem get TotalPhysicalMemory

echo Checking disk space...
wmic logicaldisk get size,freespace,caption

echo Checking 64-bit architecture...
wmic os get osarchitecture

echo System requirement validation completed.
exit /b 0
