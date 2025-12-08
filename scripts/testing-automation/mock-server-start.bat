@echo off
title Starting Mock Server
color 0E
echo ==========================================
echo          STARTING MOCK SERVER
echo ==========================================
echo.

cd mock-server

npm install --silent
node server.js

cd ..
