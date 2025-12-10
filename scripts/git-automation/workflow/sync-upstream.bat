@echo off
title Sync Upstream Repo

echo Fetching upstream...
git fetch upstream

echo Rebasing current branch on upstream/main...
git rebase upstream/main

echo Sync completed.
exit /b 0
