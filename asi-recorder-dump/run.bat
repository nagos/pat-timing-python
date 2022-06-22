@echo off
@setlocal enableextensions
@cd /d "%~dp0"
set /p IP="Device IP: " %=%
putty -ssh root@%IP% -m cmd.txt
pscp.exe root@%IP%:*ts .
pause

