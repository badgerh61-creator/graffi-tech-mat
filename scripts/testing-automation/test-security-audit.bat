@echo off
title Security Audit
color 09

echo ==========================================
echo           SECURITY AUDIT
echo ==========================================
echo.

cd backend
npm audit --json > audit-backend.json
cd ..

cd frontend
npm audit --json > audit-frontend.json
cd ..

echo Audit reports generated:
echo backend/audit-backend.json
echo frontend/audit-frontend.json

echo.
echo [INFO] Review audit files for vulnerabilities.
exit /b 0
