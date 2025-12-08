@echo off
title Pretty Git Log

git log --graph --decorate --pretty=format:"%%C(yellow)%%h%%Creset - %%C(cyan)%%an%%Creset - %%Cgreen%%cr%%Creset : %%s"
exit /b 0
