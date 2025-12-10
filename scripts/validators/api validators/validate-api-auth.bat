@echo off
set API=http://localhost:3000

curl -H "Authorization: Bearer invalid_token" %API%/protected >nul 2>&1
if %ERRORLEVEL%==0 (
  echo WARNING: API accepted invalid token!
  exit /b 1
)

echo Auth validation OK.
exit /b 0
