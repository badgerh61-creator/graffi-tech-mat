@echo off
REM ====================================================================
REM ai-benchmark.bat
REM Benchmarks ML performance: throughput, latency, CPU/GPU load.
REM ====================================================================

echo ==== AI BENCHMARK START ====

if exist venv (
  call venv\Scripts\activate.bat
)

if not exist ai\benchmark\benchmark.py (
  echo benchmark.py missing — expected at ai\benchmark\benchmark.py
  exit /b 1
)

python ai\benchmark\benchmark.py

if %ERRORLEVEL% neq 0 (
  echo Benchmark failed.
  exit /b 2
)

echo ==== BENCHMARK COMPLETE ====
exit /b 0
