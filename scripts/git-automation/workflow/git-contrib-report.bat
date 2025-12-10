@echo off
title Git Contributor Report

echo Counting commits per contributor...
git shortlog -sn

echo Generating detailed stats...
git shortlog -sne

exit /b 0
