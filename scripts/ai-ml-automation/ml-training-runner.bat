@echo off
title Graffi-Tech-Mat - ML Training Runner

echo ================================
echo  STARTING ML TRAINING SESSION
echo ================================

REM Activate training environment
call venv\Scripts\activate

echo Running training script...
python ai/train.py --config configs/train.yaml

if %errorlevel% neq 0 (
    echo Training FAILED!
    exit /b 1
)

echo Training completed successfully.
