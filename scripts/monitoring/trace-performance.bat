@echo off
REM ============================================================
REM trace-performance.bat
REM Simple API performance benchmark using curl.
REM ============================================================

set URL=http://localhost:8000/health

echo === Performance Trace ===
echo Target: %URL%
echo.

for /L %%X in (1,1,10) do (
    echo Request %%X:
    powershell -NoProfile -Command "(Measure-Command { curl.exe -s %URL% > $null }).TotalMilliseconds"
)
