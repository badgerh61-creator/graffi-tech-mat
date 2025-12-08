@echo off
REM pipeline-build.bat - build docker images for services defined in repo
SETLOCAL

echo Building Docker images...

REM List of services to build - edit names to match your repo
set SERVICES=backend frontend worker

for %%S in (%SERVICES%) do (
  if exist "%%S\Dockerfile" (
    echo Building image: graffi/%%S:latest
    docker build -t graffi/%%S:latest ./%%S
    if %ERRORLEVEL% neq 0 (
      echo Build failed for %%S
      exit /b 1
    )
  ) else (
    echo No Dockerfile for %%S - skipping
  )
)

echo Docker images built.
ENDLOCAL
