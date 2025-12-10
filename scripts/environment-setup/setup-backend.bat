@echo off
echo ==============================================
echo   GRAFFI-TECH-MAT BACKEND AUTO SETUP
echo ==============================================

cd backend

echo Removing old virtual environment (if present)...
rmdir /S /Q venv 2>nul

echo Creating new virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Backend setup complete!
pause
