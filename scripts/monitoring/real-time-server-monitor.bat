@echo off
REM ============================================================
REM real-time-server-monitor.bat
REM Live displays system CPU, RAM, network usage every 5 seconds.
REM ============================================================

:loop
cls
echo === REAL-TIME SERVER MONITOR ===
echo.

echo --- CPU ---
wmic cpu get loadpercentage
echo.

echo --- MEMORY ---
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value
echo.

echo --- TOP 10 PROCESSES (by memory) ---
wmic process get Name,WorkingSetSize | sort /r /+2 | more
echo.

echo --- NETWORK CONNECTIONS ---
netstat -an | find "ESTABLISHED"
echo.

echo Refreshing in 5 seconds...
timeout /t 5 >nul
goto loop
