@echo off
REM docker-clean.bat

echo WARNING: This will remove unused Docker items.
pause

docker system prune -af --volumes
echo Docker cleaned.
