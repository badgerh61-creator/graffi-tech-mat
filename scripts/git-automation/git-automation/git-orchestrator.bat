@echo off
title Graffi-Tech-Mat Git Orchestrator
setlocal enabledelayedexpansion

:: ================================
::  HEADER
:: ================================
echo ==============================================
echo        GRAFFI-TECH-MAT GIT ORCHESTRATOR
echo ==============================================
echo.
echo Choose a Git Automation Operation:
echo.
echo 1. Validate Clean Working Tree
echo 2. Protect Main/Production Branch
echo 3. Run Pre-Commit Lint
echo 4. Run Pre-Push Tests
echo 5. Auto Tag Version
echo 6. Branch Cleanup
echo 7. Git Undo Last Commit
echo 8. Repo Backup
echo 9. Sync Upstream
echo 10. Mirror Push
echo 11. Pretty Git Log
echo 12. Contributor Report
echo 13. Safe Stash + Operation
echo 14. Run Full Release Pipeline
echo 0. Exit
echo.

set /p choice=Select option: 

echo.
echo Running selected operation...
echo.

:: Root paths
set HOOKS_DIR=%~dp0hooks
set WORKFLOW_DIR=%~dp0workflows

:: ================================
::  FUNCTIONS
:: ================================

:validate_clean
call "%WORKFLOW_DIR%\validate-clean-working-tree.bat"
exit /b

:protect_branch
call "%WORKFLOW_DIR%\protect-main-branch.bat"
exit /b

:pre_commit_lint
call "%HOOKS_DIR%\pre-commit-lint.bat"
exit /b

:pre_push_tests
call "%HOOKS_DIR%\pre-push-tests.bat"
exit /b

:auto_tag
call "%WORKFLOW_DIR%\auto-tag.bat"
exit /b

:branch_cleanup
call "%WORKFLOW_DIR%\branch-cleanup.bat"
exit /b

:undo_last
call "%WORKFLOW_DIR%\git-undo-last.bat"
exit /b

:repo_backup
call "%WORKFLOW_DIR%\repo-backup.bat"
exit /b

:sync_upstream
call "%WORKFLOW_DIR%\sync-upstream.bat"
exit /b

:mirror_push
call "%WORKFLOW_DIR%\mirror-push.bat"
exit /b

:pretty_log
call "%WORKFLOW_DIR%\git-log-pretty.bat"
exit /b

:contrib_report
call "%WORKFLOW_DIR%\git-contrib-report.bat"
exit /b

:safe_stash
echo Enter the command you want to run during safe stash:
set /p cmd=Command: 
call "%WORKFLOW_DIR%\git-stash-safe.bat" %cmd%
exit /b

:full_release
echo Running FULL RELEASE PIPELINE...
call "%WORKFLOW_DIR%\validate-clean-working-tree.bat"
call "%WORKFLOW_DIR%\protect-main-branch.bat"
call "%HOOKS_DIR%\pre-commit-lint.bat"
call "%HOOKS_DIR%\pre-push-tests.bat"
call "%WORKFLOW_DIR%\auto-tag.bat"
call "%WORKFLOW_DIR%\release.bat"
echo.
echo ===== Release Pipeline Completed =====
exit /b

:: ================================
::  MENU EXECUTION
:: ================================

if "%choice%"=="1" goto validate_clean
if "%choice%"=="2" goto protect_branch
if "%choice%"=="3" goto pre_commit_lint
if "%choice%"=="4" goto pre_push_tests
if "%choice%"=="5" goto auto_tag
if "%choice%"=="6" goto branch_cleanup
if "%choice%"=="7" goto undo_last
if "%choice%"=="8" goto repo_backup
if "%choice%"=="9" goto sync_upstream
if "%choice%"=="10" goto mirror_push
if "%choice%"=="11" goto pretty_log
if "%choice%"=="12" goto contrib_report
if "%choice%"=="13" goto safe_stash
if "%choice%"=="14" goto full_release
if "%choice%"=="0" exit /b

echo Invalid option. Try again.
exit /b
