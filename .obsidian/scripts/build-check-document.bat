@echo off
REM Windows batch script to build Check Document from Obsidian
cd /d "%~dp0..\.."
bash .ops/build_check_document.sh
pause
