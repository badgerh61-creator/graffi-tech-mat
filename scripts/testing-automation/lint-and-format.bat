@echo off
title Lint & Format
color 0F

echo ==========================================
echo       LINTING & FORMATTING CODE
echo ==========================================
echo.

cd backend
npm run lint
npm run format
cd ..

cd frontend
npm run lint
npm run format
cd ..

echo.
echo [SUCCESS] Code linted and formatted.
exit /b 0
