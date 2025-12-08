@echo off
set name=%1

if "%name%"=="" (
    echo Usage: scaffold-ai-pipeline.bat PipelineName
    exit /b
)

mkdir ai\pipelines\%name%
echo module.exports = { run: () => console.log('Pipeline %name% running') }; > ai\pipelines\%name%\index.js

echo AI pipeline "%name%" created.
pause
